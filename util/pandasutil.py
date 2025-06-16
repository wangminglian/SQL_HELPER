import pandas as pd
from PySide6.QtCore import Qt, QAbstractTableModel
from typing import List, Any, Optional, Dict, Tuple, Set, Union
import logging
import re
from PySide6.QtGui import QColor
import networkx as nx

# 配置日志输出格式
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(filename)s - %(funcName)s - %(message)s'
)


class PandasModel(QAbstractTableModel):
    """用于将 Pandas DataFrame 显示到 QTableView 的模型类。
    
    提供基本的表格显示功能，支持行列计数和数据显示。
    """
    def __init__(self, data: pd.DataFrame):
        """初始化 PandasModel 实例。
        
        Args:
            data: 要显示的 Pandas DataFrame 数据
        """
        super().__init__()
        self._data = data

    def rowCount(self, parent=None):
        """返回表格的行数。"""
        return len(self._data)

    def columnCount(self, parent=None):
        """返回表格的列数。"""
        return len(self._data.columns)

    def data(self, index, role=Qt.DisplayRole):
        """返回指定索引和角色的单元格数据。"""
        if role == Qt.DisplayRole:
            value = self._data.iloc[index.row(), index.column()]
            return str(value)
        return None

    def headerData(self, section, orientation, role=Qt.DisplayRole):
        """返回表头数据。"""
        if role == Qt.DisplayRole:
            if orientation == Qt.Horizontal:
                return str(self._data.columns[section])
            if orientation == Qt.Vertical:
                return str(self._data.index[section])
        return None


class EditableTableManager(QAbstractTableModel):
    """大宽表数据管理模型，统一管理所有表格数据。
    
    使用单一大宽表存储所有表格数据，支持增删改查、公式计算等功能。
    列名格式为"@表格名.字段名"，每行数据具有唯一ID。
    """
    def __init__(self):
        """初始化表格管理器。"""
        super().__init__()
        # 大宽表数据结构
        self._wide_df = pd.DataFrame()  # 存储所有表格数据的大宽表
        self._wide_formulas = pd.DataFrame()  # 存储所有公式的大宽表
        
        # 表格和列映射关系
        self._column_mapping = {}  # 表格与列名的映射 {表名: [内部列名列表]}
        self._display_mapping = {}  # 显示名称与内部名的映射 {显示名: 内部列名}
        self._internal_mapping = {}  # 内部列名与显示名称的映射 {内部列名: 显示名}
        
        # 当前显示状态
        self._table_name = ""  # 当前显示的表格名称
        self._columns = []  # 当前显示的列名列表（显示名）
        self._current_display_columns = []  # 当前显示的内部列名列表
        self._next_row_id = 1  # 下一个可用的行ID
        self._editing_cell = None  # 当前正在编辑的单元格
        
        # 为了兼容性保留的旧数据结构
        self._data = []  # 当前视图中的数据 (二维数组)
        self._formulas = []  # 当前视图中的公式 (二维数组)
        
        # 自定义函数
        self._custom_functions = {}  # 存储自定义函数 {函数名: 函数对象}
        
        # 依赖图
        self._dependency_graph = nx.DiGraph()  # 存储单元格之间的依赖关系
        self._cell_dependencies = {}  # 单元格依赖关系 {(row_id, col): [(依赖的行id, 依赖的列), ...]}
        self._reverse_dependencies = {}  # 反向依赖关系 {(row_id, col): [(依赖此单元格的行id, 依赖的列), ...]}

    def register_function(self, name: str, func: callable) -> None:
        """注册自定义函数，可在公式中使用。
        
        Args:
            name: 函数名称
            func: 函数对象
        """
        logging.info(f"注册自定义函数: {name}")
        self._custom_functions[name] = func
        
    def load_all_tables(self, tables_list: Dict[str, Dict]) -> 'EditableTableManager':
        """一次性加载所有表格信息，构建统一大宽表。
        
        Args:
            tables_list: 表格数据字典，格式为：
                {
                    "表格名1": {
                        "表格字段": [...],
                        "表格数据": [...]
                    },
                    "表格名2": {...}
                }
        
        Returns:
            self: 返回自身实例，支持链式调用
        """
        try:
            # 数据检查
            if not tables_list:
                logging.error("加载表格错误: 传入的表格列表为空")
                return self
                
            table_names = list(tables_list.keys())
            logging.info(f"开始加载表格列表, 共 {len(table_names)} 个表格: {table_names}")
            
            # 清空现有数据和映射
            self._column_mapping = {}
            self._display_mapping = {}
            self._internal_mapping = {}
            self._next_row_id = 1
            
            # 收集所有表格数据
            all_table_data = []  # 存储所有表格的DataFrame
            all_formula_data = []  # 存储所有表格的公式DataFrame
            max_rows = 0  # 跟踪最大行数，用于后面填充
            
            # 处理每个表格
            for table_name, table_info in tables_list.items():
                columns = table_info.get("表格字段", [])
                data = table_info.get("表格数据", [])
                
                # 记录表格信息
                row_count = len(data)
                col_count = len(columns)
                logging.info(f"处理表格 '{table_name}': 列数={col_count}, 行数={row_count}")
                
                # 数据完整性检查
                if not columns:
                    logging.warning(f"表格 '{table_name}' 缺少列定义，跳过处理")
                    continue
                    
                # 更新最大行数
                max_rows = max(max_rows, row_count)
                
                # 创建表格数据和公式的DataFrame
                table_df = pd.DataFrame(index=range(row_count))
                formula_df = pd.DataFrame(index=range(row_count))
                
                # 创建列映射
                internal_columns = []  # 内部列名列表
                
                # 处理每一列
                for col_idx, col_name in enumerate(columns):
                    # 创建内部列名: @表格名.列名
                    internal_col_name = f"@{table_name}.{col_name}"
                    internal_columns.append(internal_col_name)
                    
                    # 创建显示名与内部名的映射
                    self._display_mapping[col_name] = internal_col_name
                    self._internal_mapping[internal_col_name] = col_name
                    
                    # 收集列数据和公式
                    col_values = []
                    col_formulas = []
                    
                    # 处理每一行
                    for row_idx, row in enumerate(data):
                        if row_idx < row_count:
                            row_values = row.get("值", [])
                            row_formulas = row.get("公式", [])
                            
                            # 获取值
                            value = "" if col_idx >= len(row_values) else row_values[col_idx]
                            col_values.append(value)
                            
                            # 获取公式
                            formula = None if not row_formulas or col_idx >= len(row_formulas) else row_formulas[col_idx]
                            col_formulas.append(formula)
                    
                    # 添加到DataFrame
                    table_df[internal_col_name] = col_values
                    formula_df[internal_col_name] = col_formulas
                
                # 保存列映射
                self._column_mapping[table_name] = internal_columns
                
                # 添加到数据集合
                all_table_data.append(table_df)
                all_formula_data.append(formula_df)
            
            # 合并所有表格数据到大宽表
            if all_table_data:
                # 创建行ID列
                row_ids = list(range(1, max_rows + 1))
                id_df = pd.DataFrame({'row_id': row_ids}, index=range(max_rows))
                
                # 合并数据表
                dfs_to_concat = [id_df] + all_table_data
                self._wide_df = pd.concat(dfs_to_concat, axis=1)
                self._wide_df.set_index('row_id', inplace=True)
                
                # 合并公式表
                formula_dfs = [pd.DataFrame({'row_id': row_ids}, index=range(max_rows))] + all_formula_data
                self._wide_formulas = pd.concat(formula_dfs, axis=1)
                self._wide_formulas.set_index('row_id', inplace=True)
                
                # 设置下一个可用行ID
                self._next_row_id = max_rows + 1
                
                logging.info(f"大宽表构建完成: 行数={max_rows}, 列数={len(self._wide_df.columns)}")
            else:
                logging.warning("未能构建大宽表: 没有有效的表格数据")
            
            # 更新依赖图
            self._update_dependency_graph()
            
            return self
        except Exception as e:
            logging.error(f"加载所有表格错误: {str(e)}", exc_info=True)
            return self

    def get_table_model(self, table_name: str) -> 'EditableTableManager':
        """获取指定表格的显示模型。
        
        筛选大宽表中对应表格的列，准备显示数据。
        
        Args:
            table_name: 表格名称
            
        Returns:
            self: 返回自身实例用于显示
        """
        logging.info(f"获取表格模型: 表名='{table_name}'")
        
        # 验证表格是否存在
        if table_name not in self._column_mapping:
            logging.error(f"获取表格模型错误: 未找到表格 '{table_name}'")
            return self
            
        # 更新当前表格名称
        self._table_name = table_name
        
        # 获取内部列名列表（@表格名.列名格式）
        internal_columns = self._column_mapping[table_name]
        if not internal_columns:
            logging.warning(f"表格 '{table_name}' 没有列")
            self._columns = []
            self._current_display_columns = []
            self._data = []  # 清空兼容数据
            self._formulas = []  # 清空兼容数据
            self._update_column_indexes()
            return self
            
        # 获取显示列名（不含表格前缀）
        display_columns = []
        for internal_col in internal_columns:
            display_name = self._internal_mapping.get(internal_col, internal_col)
            display_columns.append(display_name)
        
        # 更新当前显示的列
        self._columns = display_columns
        self._current_display_columns = internal_columns
        
        # 从大宽表提取数据到兼容数据结构
        self._extract_data_from_wide_table()
        
        # 通知视图结构已变更
        self._update_column_indexes()
        
        # 记录信息
        row_count = len(self._data)
        col_count = len(display_columns)
        logging.info(f"表格 '{table_name}' 准备完成: 行数={row_count}, 列数={col_count}")
        
        return self
        
    def _extract_data_from_wide_table(self):
        """从大宽表中提取当前表格的数据到兼容数据结构。"""
        # 清空旧数据
        self._data = []
        self._formulas = []
        
        # 如果大宽表为空，返回
        if self._wide_df.empty:
            return
            
        # 提取选定表格的数据
        for _, row_id in enumerate(self._wide_df.index):
            # 创建新行数据和公式
            row_values = []
            row_formulas = []
            
            # 为每一列获取值和公式
            for internal_col in self._current_display_columns:
                # 获取值
                if internal_col in self._wide_df.columns:
                    value = self._wide_df.at[row_id, internal_col]
                    row_values.append(value if pd.notna(value) else "")
                else:
                    row_values.append("")
                
                # 获取公式
                if internal_col in self._wide_formulas.columns:
                    formula = self._wide_formulas.at[row_id, internal_col]
                    row_formulas.append(formula if formula else None)
                else:
                    row_formulas.append(None)
            
            # 添加到兼容数据结构
            self._data.append(row_values)
            self._formulas.append(row_formulas)
        
    def _update_column_indexes(self):
        """更新列索引，通知QT界面数据结构变化。"""
        self.beginResetModel()
        self.endResetModel()
        
    def rowCount(self, parent=None):
        """返回表格的行数。"""
        return len(self._data)
        
    def columnCount(self, parent=None):
        """返回表格的列数。"""
        return len(self._columns)
        
    def data(self, index, role=Qt.DisplayRole):
        """返回指定索引和角色的单元格数据。"""
        if not index.isValid():
            return None
            
        row, col = index.row(), index.column()
        
        # 检查行列是否超出范围
        if row < 0 or row >= len(self._data) or col < 0 or col >= len(self._columns):
            return None
            
        # 检查是否是公式单元格
        has_formula = self._formulas[row][col] is not None
        
        if role == Qt.DisplayRole:
            # 显示单元格值
            value = self._data[row][col]
            return str(value) if value is not None else ""
            
        elif role == Qt.EditRole:
            # 编辑时返回公式（如果有）
            formula = self._formulas[row][col]
            if formula:
                return formula
            return str(self._data[row][col]) if self._data[row][col] is not None else ""
            
        return None
        
    def headerData(self, section, orientation, role=Qt.DisplayRole):
        """返回表头数据。"""
        if role != Qt.DisplayRole:
            return None
            
        if orientation == Qt.Horizontal and 0 <= section < len(self._columns):
            return self._columns[section]
            
        return None
        
    def flags(self, index):
        """设置单元格的标志。"""
        if not index.isValid():
            return Qt.NoItemFlags
            
        return Qt.ItemIsEditable | Qt.ItemIsEnabled | Qt.ItemIsSelectable
        
    def update_cell(self, table_name: str, row_id: int, col_name: str, value: Any, formula: Any = None) -> bool:
        """更新单元格的值和公式。
        
        Args:
            table_name: 表格名称
            row_id: 行ID
            col_name: 列名
            value: 单元格值
            formula: 公式，默认为None
            
        Returns:
            是否更新成功
        """
        try:
            # 构建内部列名
            internal_col_name = f"@{table_name}.{col_name}"
            
            # 检查列是否存在
            if internal_col_name not in self._wide_df.columns:
                logging.error(f"更新单元格错误: 列 '{internal_col_name}' 不存在")
                return False
                
            # 检查行ID是否存在
            if row_id not in self._wide_df.index:
                logging.error(f"更新单元格错误: 行ID {row_id} 不存在")
                return False
            
            # 更新单元格值
            old_value = self._wide_df.at[row_id, internal_col_name]
            self._wide_df.at[row_id, internal_col_name] = value
            logging.info(f"更新单元格值: 表={table_name}, 行ID={row_id}, 列={col_name}, 旧值={old_value}, 新值={value}")
            
            # 更新公式
            if formula is not None and internal_col_name in self._wide_formulas.columns:
                old_formula = self._wide_formulas.at[row_id, internal_col_name]
                self._wide_formulas.at[row_id, internal_col_name] = formula
                logging.info(f"更新单元格公式: 表={table_name}, 行ID={row_id}, 列={col_name}, 旧公式={old_formula}, 新公式={formula}")
                
            # 如果当前正在显示此表格，同步更新兼容数据结构
            if self._table_name == table_name:
                self._extract_data_from_wide_table()
                
                # 通知视图数据变化
                self._update_column_indexes()
            
            return True
        except Exception as e:
            logging.error(f"更新单元格错误: {str(e)}", exc_info=True)
            return False
            
    def add_row(self, table_name: str, values: List[Any] = None, formulas: List[Any] = None) -> int:
        """向表格添加新行。
        
        Args:
            table_name: 表格名称
            values: 行数据列表，可选
            formulas: 公式列表，可选
            
        Returns:
            新行的ID，失败返回-1
        """
        try:
            # 验证表格是否存在
            if table_name not in self._column_mapping:
                logging.error(f"添加行错误: 表格 '{table_name}' 不存在")
                return -1
                
            # 获取表格的内部列名列表
            internal_columns = self._column_mapping[table_name]
            if not internal_columns:
                logging.error(f"添加行错误: 表格 '{table_name}' 没有列")
                return -1
            
            # 创建新行ID
            new_row_id = self._next_row_id
            self._next_row_id += 1
            
            # 准备新行数据
            new_row_data = {}
            new_row_formulas = {}
            
            # 填充数据
            for i, col_name in enumerate(internal_columns):
                if values and i < len(values):
                    new_row_data[col_name] = values[i]
                else:
                    new_row_data[col_name] = ""
                    
                if formulas and i < len(formulas):
                    new_row_formulas[col_name] = formulas[i]
                else:
                    new_row_formulas[col_name] = None
            
            # 添加到大宽表
            self._wide_df.loc[new_row_id] = pd.Series(new_row_data)
            self._wide_formulas.loc[new_row_id] = pd.Series(new_row_formulas)
            
            logging.info(f"已添加新行: 表={table_name}, 行ID={new_row_id}, 列数={len(internal_columns)}")
            
            # 如果当前正在显示此表格，更新兼容数据结构
            if self._table_name == table_name:
                self._extract_data_from_wide_table()
                
                # 通知视图数据变化
                self._update_column_indexes()
            
            return new_row_id
        except Exception as e:
            logging.error(f"添加行错误: {str(e)}", exc_info=True)
            return -1
    
    def delete_row(self, table_name: str, row_id: int) -> bool:
        """从表格中删除指定行。
        
        Args:
            table_name: 表格名称
            row_id: 行ID
            
        Returns:
            是否删除成功
        """
        try:
            # 检查表格是否存在
            if table_name not in self._column_mapping:
                logging.error(f"删除行错误: 表格 '{table_name}' 不存在")
                return False
                
            # 检查行ID是否存在
            if row_id not in self._wide_df.index:
                logging.error(f"删除行错误: 行ID {row_id} 不存在")
                return False
                
            # 从大宽表中删除行
            self._wide_df = self._wide_df.drop(row_id)
            self._wide_formulas = self._wide_formulas.drop(row_id)
            
            logging.info(f"已删除行: 表={table_name}, 行ID={row_id}")
            
            # 如果当前正在显示此表格，更新兼容数据结构
            if self._table_name == table_name:
                self._extract_data_from_wide_table()
                
                # 通知视图数据变化
                self._update_column_indexes()
            
            return True
        except Exception as e:
            logging.error(f"删除行错误: {str(e)}", exc_info=True)
            return False
            
    def add_column(self, table_name: str, column_name: str, default_value: Any = "") -> bool:
        """向表格添加新列。
        
        Args:
            table_name: 表格名称
            column_name: 列名
            default_value: 默认值，可选
            
        Returns:
            是否添加成功
        """
        try:
            # 验证表格是否存在
            if table_name not in self._column_mapping:
                logging.error(f"添加列错误: 表格 '{table_name}' 不存在")
                return False
                
            # 构建内部列名
            internal_col_name = f"@{table_name}.{column_name}"
            
            # 检查列名是否已存在
            if internal_col_name in self._wide_df.columns:
                logging.error(f"添加列错误: 列 '{internal_col_name}' 已存在")
                return False
                
            # 向大宽表添加列
            self._wide_df[internal_col_name] = default_value
            self._wide_formulas[internal_col_name] = None
            
            # 更新列映射
            if table_name in self._column_mapping:
                self._column_mapping[table_name].append(internal_col_name)
            else:
                self._column_mapping[table_name] = [internal_col_name]
                
            # 更新显示映射
            self._display_mapping[column_name] = internal_col_name
            self._internal_mapping[internal_col_name] = column_name
            
            logging.info(f"已添加新列: 表={table_name}, 列={column_name}")
            
            # 如果当前正在显示此表格，更新兼容数据结构
            if self._table_name == table_name:
                self._extract_data_from_wide_table()
                
                # 通知视图数据变化
                self._update_column_indexes()
            
            return True
        except Exception as e:
            logging.error(f"添加列错误: {str(e)}", exc_info=True)
            return False
            
    def delete_column(self, table_name: str, column_name: str) -> bool:
        """从表格中删除指定列。
        
        Args:
            table_name: 表格名称
            column_name: 列名
            
        Returns:
            是否删除成功
        """
        try:
            # 检查表格是否存在
            if table_name not in self._column_mapping:
                logging.error(f"删除列错误: 表格 '{table_name}' 不存在")
                return False
                
            # 构建内部列名
            internal_col_name = f"@{table_name}.{column_name}"
            
            # 检查列是否存在
            if internal_col_name not in self._wide_df.columns:
                logging.error(f"删除列错误: 列 '{internal_col_name}' 不存在")
                return False
                
            # 从大宽表中删除列
            self._wide_df = self._wide_df.drop(columns=[internal_col_name])
            self._wide_formulas = self._wide_formulas.drop(columns=[internal_col_name])
            
            # 更新列映射
            if internal_col_name in self._column_mapping[table_name]:
                self._column_mapping[table_name].remove(internal_col_name)
                
            # 更新显示映射
            if column_name in self._display_mapping:
                del self._display_mapping[column_name]
            if internal_col_name in self._internal_mapping:
                del self._internal_mapping[internal_col_name]
                
            logging.info(f"已删除列: 表={table_name}, 列={column_name}")
            
            # 如果当前正在显示此表格，更新兼容数据结构
            if self._table_name == table_name:
                self._extract_data_from_wide_table()
                
                # 通知视图数据变化
                self._update_column_indexes()
            
            return True
        except Exception as e:
            logging.error(f"删除列错误: {str(e)}", exc_info=True)
            return False
            
    def set_editing_cell(self, index):
        """设置当前正在编辑的单元格。"""
        if not index.isValid():
            self._editing_cell = None
            return
            
        row, col = index.row(), index.column()
        if row < 0 or row >= len(self._data) or col < 0 or col >= len(self._columns):
            self._editing_cell = None
            return
            
        self._editing_cell = (row, col)
        self.dataChanged.emit(index, index)
            
    def clear_editing_cell(self):
        """清除当前正在编辑的单元格。"""
        if self._editing_cell:
            row, col = self._editing_cell
            old_index = self.index(row, col)
            self._editing_cell = None
            self.dataChanged.emit(old_index, old_index)
            
    def _update_dependency_graph(self):
        """更新依赖图。"""
        # 简化版实现，实际应根据大宽表中的公式构建依赖关系
        pass
        
    def search_by_rule(self, rule: str = "|") -> Optional[QAbstractTableModel]:
        """根据复杂规则搜索数据。
        
        支持复杂的搜索条件，包括与(&)、或(|)操作，以及列名引用(@)。
        搜索规则示例："@姓名=张三&@工号=001|@部门=技术部"
        
        Args:
            rule: str，搜索规则
            
        Returns:
            Optional[QAbstractTableModel]: 搜索结果数据模型，失败返回None
        """
        try:
            logging.info(f"开始按规则搜索数据: 规则='{rule}'")
            
            # 如果规则为空，返回所有数据
            if not rule or not rule.strip():
                logging.info("搜索规则为空，返回原始数据")
                return self
            
            # 记录原始数据
            filtered_data = self._data.copy()
            filtered_formulas = self._formulas.copy() if hasattr(self, '_formulas') else [None] * len(filtered_data)
            
            # 分割搜索条件（按&和|分割）
            conditions = []
            
            # 首先按|分割（或操作）
            or_parts = rule.split('|')
            for or_part in or_parts:
                # 再按&分割（与操作）
                and_parts = or_part.split('&')
                and_conditions = []
                
                for condition in and_parts:
                    condition = condition.strip()
                    if not condition:
                        continue
                        
                    # 解析单个条件（格式：@列名=值）
                    if not condition.startswith('@'):
                        logging.warning(f"跳过非法条件格式: {condition}")
                        continue
                        
                    parts = condition[1:].split('=')  # 去掉@后分割
                    if len(parts) != 2:
                        logging.warning(f"跳过无法解析的条件: {condition}")
                        continue
                        
                    col_name = parts[0].strip()
                    search_value = parts[1].strip()
                    
                    # 检查列名是否存在
                    if col_name not in self._columns:
                        logging.warning(f"列名不存在: {col_name}")
                        continue
                        
                    and_conditions.append((col_name, search_value))
                
                if and_conditions:
                    conditions.append(and_conditions)
            
            # 应用搜索条件
            result_data = []
            result_formulas = []
            row_mapping = {}  # 筛选后的行索引 -> 原始行索引的映射
            
            # 处理每组OR条件
            for or_conditions in conditions:
                matching_rows = []
                matching_formulas = []
                matching_indices = []  # 存储匹配的原始行索引
                
                # 遍历所有行
                for i, row in enumerate(filtered_data):
                    # 检查是否满足所有AND条件
                    matches_all = True
                    for col_name, search_value in or_conditions:
                        col_idx = self._columns.index(col_name)
                        if col_idx < len(row):
                            cell_value = str(row[col_idx]).strip()
                            if search_value.lower() not in cell_value.lower():
                                matches_all = False
                                break
                        else:
                            matches_all = False
                            break
                    
                    if matches_all:
                        matching_rows.append(row)
                        matching_indices.append(i)  # 保存原始行索引
                        # 如果有公式数据，也添加对应的公式
                        if i < len(filtered_formulas):
                            matching_formulas.append(filtered_formulas[i])
                        else:
                            matching_formulas.append([None] * len(row))
                
                # 将匹配的行添加到结果中
                for idx, row in enumerate(matching_rows):
                    result_data.append(row)
                    if idx < len(matching_formulas):
                        result_formulas.append(matching_formulas[idx])
                    
                    # 记录筛选后行索引与原始行索引的映射
                    row_mapping[len(result_data) - 1] = matching_indices[idx]
            
            # 去重（同时保持数据和公式的对应关系）
            unique_results = []
            unique_formulas = []
            unique_row_mapping = {}
            seen = set()
            
            for i, row in enumerate(result_data):
                row_tuple = tuple(row)
                if row_tuple not in seen:
                    seen.add(row_tuple)
                    unique_results.append(row)
                    unique_row_mapping[len(unique_results) - 1] = row_mapping[i]
                    if i < len(result_formulas):
                        unique_formulas.append(result_formulas[i])
            
            # 如果没有找到匹配的数据
            if not unique_results:
                logging.info("未找到匹配的数据")
                # 返回空数据但保持原有结构
                new_model = EditableTableManager()
                new_model._table_name = self._table_name
                new_model._columns = self._columns.copy()
                new_model._current_display_columns = self._current_display_columns.copy()
                new_model._data = []
                new_model._formulas = []
                
                # 继承原模型的其他属性
                new_model._wide_df = self._wide_df
                new_model._wide_formulas = self._wide_formulas
                new_model._column_mapping = self._column_mapping
                new_model._display_mapping = self._display_mapping
                new_model._internal_mapping = self._internal_mapping
                new_model._custom_functions = self._custom_functions
                
                logging.info("返回空搜索结果模型")
                return new_model
                
            # 创建新的模型并返回
            new_model = EditableTableManager()
            
            # 继承数据和结构
            new_model._table_name = self._table_name
            new_model._columns = self._columns.copy()
            new_model._current_display_columns = self._current_display_columns.copy()
            new_model._data = unique_results
            new_model._formulas = unique_formulas
            
            # 继承原模型的其他属性
            new_model._wide_df = self._wide_df
            new_model._wide_formulas = self._wide_formulas
            new_model._column_mapping = self._column_mapping
            new_model._display_mapping = self._display_mapping
            new_model._internal_mapping = self._internal_mapping
            new_model._custom_functions = self._custom_functions
            
            # 添加行映射信息
            new_model._row_mapping = unique_row_mapping
            
            logging.info(f"搜索完成，找到 {len(unique_results)} 条匹配记录")
            return new_model
            
        except Exception as e:
            logging.error(f"搜索规则解析失败: {str(e)}", exc_info=True)
            return None
            
    def filter_data(self, column: str, value: Any) -> Optional[QAbstractTableModel]:
        """按列值筛选数据。
        
        Args:
            column: str，要筛选的列名
            value: Any，筛选的值
            
        Returns:
            Optional[QAbstractTableModel]: 筛选后的数据模型，失败返回None
        """
        try:
            logging.info(f"按列值筛选数据: 列='{column}', 值='{value}'")
            
            # 检查列名是否存在
            if column not in self._columns:
                logging.error(f"筛选错误: 列名 '{column}' 不存在")
                return None
                
            col_idx = self._columns.index(column)
            
            # 筛选数据
            filtered_data = []
            filtered_formulas = []
            
            for i, row in enumerate(self._data):
                if col_idx < len(row) and str(row[col_idx]).lower().find(str(value).lower()) != -1:
                    filtered_data.append(row)
                    if i < len(self._formulas):
                        filtered_formulas.append(self._formulas[i])
            
            # 创建新模型
            filtered_model = EditableTableManager()
            filtered_model._table_name = self._table_name
            filtered_model._columns = self._columns.copy()
            filtered_model._current_display_columns = self._current_display_columns.copy()
            filtered_model._data = filtered_data
            filtered_model._formulas = filtered_formulas
            
            # 继承原模型的其他属性
            filtered_model._wide_df = self._wide_df
            filtered_model._wide_formulas = self._wide_formulas
            filtered_model._column_mapping = self._column_mapping
            filtered_model._display_mapping = self._display_mapping
            filtered_model._internal_mapping = self._internal_mapping
            filtered_model._custom_functions = self._custom_functions
            
            logging.info(f"筛选完成，找到 {len(filtered_data)} 条匹配记录")
            return filtered_model
            
        except Exception as e:
            logging.error(f"按列值筛选数据错误: {str(e)}", exc_info=True)
            return None
            
    def search_global(self, keyword: str) -> Optional[QAbstractTableModel]:
        """全局搜索数据。
        
        在所有列中搜索包含关键词的行。
        
        Args:
            keyword: str，搜索关键词
            
        Returns:
            Optional[QAbstractTableModel]: 搜索结果数据模型，失败返回None
        """
        try:
            logging.info(f"全局搜索数据: 关键词='{keyword}'")
            
            if not keyword:
                logging.info("搜索关键词为空，返回原始数据")
                return self
                
            # 筛选数据
            filtered_data = []
            filtered_formulas = []
            
            for i, row in enumerate(self._data):
                if any(str(item).lower().find(keyword.lower()) != -1 for item in row):
                    filtered_data.append(row)
                    if i < len(self._formulas):
                        filtered_formulas.append(self._formulas[i])
            
            # 创建新模型
            filtered_model = EditableTableManager()
            filtered_model._table_name = self._table_name
            filtered_model._columns = self._columns.copy()
            filtered_model._current_display_columns = self._current_display_columns.copy()
            filtered_model._data = filtered_data
            filtered_model._formulas = filtered_formulas
            
            # 继承原模型的其他属性
            filtered_model._wide_df = self._wide_df
            filtered_model._wide_formulas = self._wide_formulas
            filtered_model._column_mapping = self._column_mapping
            filtered_model._display_mapping = self._display_mapping
            filtered_model._internal_mapping = self._internal_mapping
            filtered_model._custom_functions = self._custom_functions
            
            logging.info(f"全局搜索完成，找到 {len(filtered_data)} 条匹配记录")
            return filtered_model
            
        except Exception as e:
            logging.error(f"全局搜索数据错误: {str(e)}", exc_info=True)
            return None
            
    def reset_filter(self) -> QAbstractTableModel:
        """重置筛选，返回原始数据。
        
        Returns:
            QAbstractTableModel: 当前数据模型实例
        """
        logging.info("重置筛选，返回原始数据")
        return self
        
    def get_data(self) -> List[List[Any]]:
        """获取当前表格的所有数据。
        
        Returns:
            List[List[Any]]: 二维列表形式的表格数据
        """
        logging.info(f"获取当前表格数据: 行数={len(self._data)}, 列数={len(self._columns) if self._columns else 0}")
        return self._data
        
    # ---------------- 向后兼容的方法 ----------------
    
    def add_column_to_wide_table(self, table_name: str, column_name: str, default_value: Any = "") -> bool:
        """向大宽表添加一列（向后兼容方法）。
        
        Args:
            table_name: 表格名称
            column_name: 列名
            default_value: 默认值，可选
            
        Returns:
            是否添加成功
        """
        logging.info(f"调用兼容方法 add_column_to_wide_table: 表={table_name}, 列={column_name}")
        return self.add_column(table_name, column_name, default_value)
        
    def delete_column_from_wide_table(self, table_name: str, column_name: str) -> bool:
        """从大宽表中删除一列（向后兼容方法）。
        
        Args:
            table_name: 表格名称
            column_name: 列名
            
        Returns:
            是否删除成功
        """
        logging.info(f"调用兼容方法 delete_column_from_wide_table: 表={table_name}, 列={column_name}")
        return self.delete_column(table_name, column_name)
        
    def add_row_to_wide_table(self, table_name: str, values: List[Any] = None, formulas: List[Any] = None) -> int:
        """向大宽表添加一行（向后兼容方法）。
        
        Args:
            table_name: 表格名称
            values: 行数据列表，可选
            formulas: 公式列表，可选
            
        Returns:
            新行的ID，失败返回-1
        """
        logging.info(f"调用兼容方法 add_row_to_wide_table: 表={table_name}")
        return self.add_row(table_name, values, formulas)
        
    def delete_row_from_wide_table(self, table_name: str, row_id: int) -> bool:
        """从大宽表中删除一行（向后兼容方法）。
        
        Args:
            table_name: 表格名称
            row_id: 行ID
            
        Returns:
            是否删除成功
        """
        logging.info(f"调用兼容方法 delete_row_from_wide_table: 表={table_name}, 行ID={row_id}")
        return self.delete_row(table_name, row_id)
        
    def update_wide_table_data(self, table_name: str, row_id: int, col_name: str, value: Any, formula: Any = None) -> bool:
        """更新大宽表中的数据（向后兼容方法）。
        
        Args:
            table_name: 表格名称
            row_id: 行ID
            col_name: 列名
            value: 新值
            formula: 公式
            
        Returns:
            是否更新成功
        """
        logging.info(f"调用兼容方法 update_wide_table_data: 表={table_name}, 行ID={row_id}, 列={col_name}")
        return self.update_cell(table_name, row_id, col_name, value, formula)

