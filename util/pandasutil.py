import pandas as pd
from PySide6.QtCore import Qt, QAbstractTableModel
from typing import List, Any, Optional, Dict, Tuple, Set
import logging
import re
from PySide6.QtGui import QColor
import networkx as nx

# 设置loging 打印到控制台
logging.basicConfig(level=logging.INFO,format='%(asctime)s - %(levelname)s -%(filename)s- %(funcName)s - %(message)s')


class PandasModel(QAbstractTableModel):
    """用于将Pandas DataFrame显示到QTableView的模型类"""
    def __init__(self, data: pd.DataFrame):
        super().__init__()
        self._data = data

    def rowCount(self, parent=None):
        return len(self._data)

    def columnCount(self, parent=None):
        return len(self._data.columns)

    def data(self, index, role=Qt.DisplayRole):
        if role == Qt.DisplayRole:
            value = self._data.iloc[index.row(), index.column()]
            return str(value)
        return None

    def headerData(self, section, orientation, role=Qt.DisplayRole):
        if role == Qt.DisplayRole:
            if orientation == Qt.Horizontal:
                return str(self._data.columns[section])
            if orientation == Qt.Vertical:
                return str(self._data.index[section])
        return None

class EditableTableManager(QAbstractTableModel):
    """可编辑的表格数据管理模型，继承自QAbstractTableModel
    用于管理和操作二维表格数据，支持增删改查等功能
    """
    def __init__(self):
        """初始化表格管理器
        创建空的数据列表和列名列表
        """
        super().__init__()
        self._data = []  # 存储实际值
        self._formulas = []  # 存储公式
        self._columns = []
        self._custom_functions = {}  # 存储自定义函数
        self._editing_cell = None  # 存储当前正在编辑的单元格
        self._table_name = ""  # 当前表名
        self._all_tables = {}  # 存储所有表格数据 {表名: {列名: [值]}}
        
        # 创建依赖图
        self._dependency_graph = nx.DiGraph()  # 存储单元格之间的依赖关系
        self._cell_dependencies = {}  # 存储每个单元格的依赖关系 {(row, col): [(依赖的行, 依赖的列), ...]}
        self._reverse_dependencies = {}  # 存储反向依赖关系 {(row, col): [(依赖此单元格的行, 依赖此单元格的列), ...]}

    def register_function(self, name: str, func: callable):
        """注册自定义函数"""
        self._custom_functions[name] = func
        
    def set_data(self, data: List[dict], columns: List[str], table_name: str = ""):
        """设置表格数据和列名"""
        try:
            self._columns = columns
            self._data = []
            self._formulas = []
            self._table_name = table_name
            
            # 处理数据和公式
            for row in data:
                try:
                    # 确保行数据格式正确
                    row_values = row.get("值", [])
                    if not isinstance(row_values, list):
                        row_values = []
                    
                    # 确保公式数据格式正确
                    row_formulas = row.get("公式", [])
                    if not isinstance(row_formulas, list):
                        row_formulas = []
                    
                    # 填充数据长度
                    while len(row_values) < len(columns):
                        row_values.append("")
                    
                    # 填充公式长度
                    while len(row_formulas) < len(columns):
                        row_formulas.append(None)
                    
                    self._data.append(row_values)
                    self._formulas.append(row_formulas)
                except Exception as e:
                    logging.error(f"处理行数据错误: {str(e)}")
                    # 添加空行
                    self._data.append([""] * len(columns))
                    self._formulas.append([None] * len(columns))
            
            # 更新所有表格数据字典
            if table_name:
                try:
                    # 构建列数据字典
                    table_data = {}
                    for col_idx, col_name in enumerate(columns):
                        column_values = []
                        for row in self._data:
                            if col_idx < len(row):
                                column_values.append(row[col_idx])
                            else:
                                column_values.append("")
                        table_data[col_name] = column_values
                    self._all_tables[table_name] = table_data
                except Exception as e:
                    logging.error(f"更新表格数据字典错误: {str(e)}")
            
            # 更新依赖图
            try:
                self._update_dependency_graph()
            except Exception as e:
                logging.error(f"更新依赖图错误: {str(e)}")
            
            self.layoutChanged.emit()
            return self
        except Exception as e:
            logging.error(f"设置表格数据错误: {str(e)}")
            # 确保至少有一些有效的数据
            self._columns = columns if columns else []
            self._data = []
            self._formulas = []
            self.layoutChanged.emit()
            return self

    def _evaluate_formula(self, formula: str, row: int, col: int) -> Any:
        """计算公式结果"""
        try:
            # 如果不是公式，直接返回None
            formula = formula.replace('@', '')
            if not formula or not formula.startswith("="):
                return None
                
            # 去掉等号
            formula = formula[1:]
            
            # 解析单元格引用 (例如: A1, B2 等)
            def replace_cell_ref(match):
                cell_ref = match.group(0)
                col_name = ''.join(filter(str.isalpha, cell_ref))
                
                # 检查是否包含数字（行号）
                if any(c.isdigit() for c in cell_ref):
                    row_num = int(''.join(filter(str.isdigit, cell_ref))) - 1
                else:
                    # 如果只有列字母，使用当前行
                    row_num = row
                    
                col_num = sum((ord(c) - ord('A') + 1) * (26 ** i) 
                            for i, c in enumerate(reversed(col_name))) - 1
                return str(self._get_cell_value(row_num, col_num))
                
            # 替换所有单元格引用，包括只有列字母的引用
            formula = re.sub(r'[A-Z]+[0-9]*', replace_cell_ref, formula)
            
            # 提取函数名和参数
            match = re.match(r'(\w+)\((.*)\)', formula)
            if match:
                func_name = match.group(1)
                args_str = match.group(2)
                
                if func_name in self._custom_functions:
                    # 解析参数
                    args = []
                    for arg in [a.strip() for a in args_str.split(',')]:
                        # 检查是否包含表名.列名格式
                        table_col_match = re.match(r'([^.]+)\.([^.]+)', arg)
                        if table_col_match:
                            # 表名.列名格式
                            table_name = table_col_match.group(1)
                            col_name = table_col_match.group(2)
                            
                            # 从其他表获取数据
                            if table_name in self._all_tables and col_name in self._all_tables[table_name]:
                                # 获取对应行的值
                                if row < len(self._all_tables[table_name][col_name]):
                                    args.append(self._all_tables[table_name][col_name][row])
                                else:
                                    args.append("")
                            else:
                                args.append(f"#REF!{table_name}.{col_name}")
                        else:
                            # 仅列名格式，从当前表获取
                            if arg in self._columns:
                                col_idx = self._columns.index(arg)
                                args.append(self._get_cell_value(row, col_idx))
                            else:
                                # 直接传递参数值
                                args.append(arg)
                    
                    # 执行函数
                    return self._custom_functions[func_name](*args)
                
            return eval(formula, {"__builtins__": {}}, self._custom_functions)
            
        except Exception as e:
            logging.error(f"公式计算错误: {str(e)}")
            return f"#ERROR: {str(e)}"
            
    def _get_cell_value(self, row: int, col: int) -> Any:
        """获取单元格的实际值"""
        if row < 0 or row >= len(self._data) or col < 0 or col >= len(self._columns):
            return "#REF!"
            
        # 如果有公式，计算公式结果
        formula = self._formulas[row][col]
        if formula:
            return self._evaluate_formula(formula, row, col)
            
        # 否则返回实际值
        return self._data[row][col]
        
    def set_editing_cell(self, index):
        """设置当前正在编辑的单元格"""
        self._editing_cell = (index.row(), index.column()) if index.isValid() else None
        if index.isValid():
            self.dataChanged.emit(index, index)
            
    def clear_editing_cell(self):
        """清除当前正在编辑的单元格"""
        if self._editing_cell:
            old_index = self.index(self._editing_cell[0], self._editing_cell[1])
            self._editing_cell = None
            self.dataChanged.emit(old_index, old_index)
        
    def data(self, index, role=Qt.DisplayRole):
        """获取单元格显示数据"""
        if not index.isValid():
            return None
            
        row, col = index.row(), index.column()
        
        # 检查是否是公式单元格
        has_formula = self._formulas[row][col] is not None
        
        if role == Qt.DisplayRole:
            # 如果是正在编辑的单元格，显示公式
            if self._editing_cell == (row, col):
                formula = self._formulas[row][col]
                if formula:
                    return formula
                    
            # 否则显示计算结果
            value = self._get_cell_value(row, col)
            return str(value) if value is not None else ""
            
        elif role == Qt.EditRole:
            # 编辑时返回公式（如果有）
            formula = self._formulas[row][col]
            if formula:
                return formula
            return str(self._data[row][col]) if self._data[row][col] is not None else ""
            
        elif role == Qt.BackgroundRole and has_formula:
            # 公式单元格背景色为浅蓝色
            return QColor(230, 245, 255)  # 浅蓝色背景
            
        elif role == Qt.ForegroundRole and has_formula:
            # 公式单元格文字颜色为绿色
            return QColor(0, 128, 0)  # 绿色文字
            
        elif role == Qt.ToolTipRole and has_formula:
            # 添加工具提示显示公式内容
            formula = self._formulas[row][col]
            return f"公式: {formula}"
            
        return None
        
    def setData(self, index, value, role=Qt.EditRole):
        """设置单元格数据"""
        if not index.isValid():
            return False
            
        row, col = index.row(), index.column()
        
        try:
            # 检查行列边界
            if row < 0 or row >= len(self._data) or col < 0 or col >= len(self._columns):
                return False
                
            # 确保数据行长度足够
            while len(self._data[row]) <= col:
                self._data[row].append("")
                
            # 确保公式行长度足够
            while len(self._formulas[row]) <= col:
                self._formulas[row].append(None)
                
            old_value = self._data[row][col]
            old_formula = self._formulas[row][col]
            
            # 检查值是否为公式
            if isinstance(value, str) and value.startswith('='):
                try:
                    # 尝试计算公式是否有效
                    self._formulas[row][col] = value
                    self._data[row][col] = None
                    test_result = self._evaluate_formula(value, row, col)
                    if isinstance(test_result, str) and test_result.startswith('#ERROR'):
                        # 如果计算出错，保留公式但显示错误
                        pass
                except Exception as e:
                    logging.error(f"公式计算错误: {str(e)}")
            else:
                # 普通值
                self._formulas[row][col] = None
                self._data[row][col] = value
                
            # 更新表格数据字典
            if self._table_name and col < len(self._columns):
                col_name = self._columns[col]
                if col_name in self._all_tables.get(self._table_name, {}):
                    # 确保行数足够
                    while len(self._all_tables[self._table_name][col_name]) <= row:
                        self._all_tables[self._table_name][col_name].append("")
                    
                    # 更新列数据
                    if self._formulas[row][col]:
                        # 如果是公式，使用计算结果
                        result = self._evaluate_formula(self._formulas[row][col], row, col)
                        self._all_tables[self._table_name][col_name][row] = result
                    else:
                        # 否则使用实际值
                        self._all_tables[self._table_name][col_name][row] = self._data[row][col]
                        
            # 如果单元格内容有变化，更新依赖图
            if old_value != self._data[row][col] or old_formula != self._formulas[row][col]:
                # 分析新的依赖关系
                try:
                    # 更新整个依赖图（更加健壮但可能较慢）
                    self._update_dependency_graph()
                    
                    # 更新依赖此单元格的所有单元格
                    self._update_dependent_cells(row, col)
                except Exception as e:
                    logging.error(f"更新依赖单元格时发生错误: {str(e)}")
            
            # 发送数据更改信号
            self.dataChanged.emit(index, index)
            return True
            
        except Exception as e:
            logging.error(f"设置单元格数据错误: {str(e)}")
            return False

    def rowCount(self, parent=None):
        """获取行数
        Returns:
            int: 表格的总行数
        """
        return len(self._data)

    def columnCount(self, parent=None):
        """获取列数
        Returns:
            int: 表格的总列数
        """
        return len(self._columns)

    def headerData(self, section, orientation, role=Qt.DisplayRole):
        """获取表头数据
        Args:
            section: int，行号或列号
            orientation: Qt.Orientation，方向（水平/垂直）
            role: Qt.ItemDataRole，数据角色
        Returns:
            str: 表头显示的文本
        """
        if role == Qt.DisplayRole:
            if orientation == Qt.Horizontal:
                return str(self._columns[section])
        return None

    def flags(self, index):
        """设置单元格的标志
        Returns:
            Qt.ItemFlags: 单元格的标志（可编辑、可选择、可用）
        """
        return Qt.ItemIsEditable | Qt.ItemIsEnabled | Qt.ItemIsSelectable

    def add_row(self, row_data: List[Any]) -> bool:
        """添加新行
        Args:
            row_data: List[Any]，新行的数据列表
        Returns:
            bool: 添加是否成功
        """
        try:
            self._data.append(row_data)
            self.layoutChanged.emit()
            return True
        except Exception:
            return False


    def add_column(self, column_name: str, default_value: Any = "") -> bool:
        """添加新列
        Args:
            column_name: str，新列的列名
            default_value: Any，新列的默认值
        Returns:
            bool: 添加是否成功
        """
        try:
            self._columns.append(column_name)
            for row in self._data:
                row.append(default_value)
            self.layoutChanged.emit()
            return True
        except Exception:
            return False

    def delete_row(self, row_index: int) -> bool:
        """删除指定行
        Args:
            row_index: int，要删除的行索引
        Returns:
            bool: 删除是否成功
        """
        try:
            self._data.pop(row_index)
            self.layoutChanged.emit()
            return True
        except Exception as e:
            logging.error(f"删除行失败: {e}")
            return False

    def delete_column_by_index(self, column_index: int) -> bool:
        """删除指定列号的列
        Args:
            column_index: int，要删除的列索引
        Returns:
            bool: 删除是否成功
        """
        try:
            self._columns.pop(column_index)
            for row in self._data:
                row.pop(column_index)
            self.layoutChanged.emit()
            return True
        except Exception as e:
            logging.error(f"删除列失败: {e}")
            return False
    def delete_column(self, column_name: str) -> bool:
        """删除指定列
        Args:
            column_name: str，要删除的列名
        Returns:
            bool: 删除是否成功
        """
        try:
            self._columns.remove(column_name)
            for row in self._data:
                row.pop(self._columns.index(column_name))
            self.layoutChanged.emit()
            return True
        except Exception:
            return False
    
    def update_cell_by_index(self, row: int, column: int, value: Any) -> bool:
        """更新指定单元格的值
        Args:
            row: int，行索引
            column: int，列索引 
            value: Any，新的值
        Returns:
            bool: 更新是否成功
        """
        try:
            self._data[row][column] = value
            self.dataChanged.emit(self.index(row, column), 
                                self.index(row, column))
            return True
        except Exception as e:
            logging.error(f"更新单元格失败: {e}")
            return False

    def update_cell(self, row: int, column: str, value: Any) -> bool:
        """更新指定单元格的值
        Args:
            row: int，行索引
            column: str，列名
            value: Any，新的值
        Returns:
            bool: 更新是否成功
        """
        try:
            self._data[row][self._columns.index(column)] = value
            self.dataChanged.emit(self.index(row, self._columns.index(column)), 
                                self.index(row, self._columns.index(column)))
            return True
        except Exception as e:
            logging.error(f"更新单元格失败: {e}")
            return False

    # 这个功能需要支持复杂的搜索规则，包括与(&)、或(|)、非(^)操作，以及列名引用(@)。以下是实现代码：
    # 搜索规则应该类似于" @姓名 =张& @工号 =11| @姓名 =李"
    # @列名 其中列名是 pandas中的列名， 后面可以支持 = > < != 等操作
    def search_by_rule(self, rule: str = "|") -> Optional[QAbstractTableModel]:
        """根据复杂规则搜索数据
        Args:
            rule: str，搜索规则，如"@姓名=张三&@工号=001"
        Returns:
            Optional[QAbstractTableModel]: 搜索结果数据模型，失败返回None
        """
        try:
            # 如果规则为空,返回所有数据
            if not rule.strip():
                return self
            
            # 记录原始数据
            filtered_data = self._data.copy()
            filtered_formulas = self._formulas.copy() if hasattr(self, '_formulas') else [None] * len(filtered_data)
            
            # 分割搜索条件（按&和|分割）
            conditions = []
            operators = []
            
            # 首先按|分割
            or_parts = rule.split('|')
            for or_part in or_parts:
                # 再按&分割
                and_parts = or_part.split('&')
                and_conditions = []
                
                for condition in and_parts:
                    condition = condition.strip()
                    if not condition:
                        continue
                        
                    # 解析单个条件（格式：@列名=值）
                    if not condition.startswith('@'):
                        continue
                        
                    parts = condition[1:].split('=')  # 去掉@后分割
                    if len(parts) != 2:
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
            
            # 处理每组OR条件
            for or_conditions in conditions:
                matching_rows = []
                matching_formulas = []
                
                # 遍历所有行
                for i, row in enumerate(filtered_data):
                    # 检查是否满足所有AND条件
                    matches_all = True
                    for col_name, search_value in or_conditions:
                        col_idx = self._columns.index(col_name)
                        cell_value = str(row[col_idx]).strip()
                        if search_value.lower() not in cell_value.lower():
                            matches_all = False
                            break
                    
                    if matches_all:
                        matching_rows.append(row)
                        # 如果有公式数据，也添加对应的公式
                        if hasattr(self, '_formulas') and i < len(self._formulas):
                            matching_formulas.append(self._formulas[i])
                        else:
                            matching_formulas.append([None] * len(row))
                
                # 将匹配的行添加到结果中
                result_data.extend(matching_rows)
                result_formulas.extend(matching_formulas)
            
            # 去重（同时保持数据和公式的对应关系）
            unique_results = []
            unique_formulas = []
            seen = set()
            
            for i, row in enumerate(result_data):
                row_tuple = tuple(row)
                if row_tuple not in seen:
                    seen.add(row_tuple)
                    unique_results.append(row)
                    if i < len(result_formulas):
                        unique_formulas.append(result_formulas[i])
            
            # 如果没有找到匹配的数据
            if not unique_results:
                logging.info("未找到匹配的数据")
                # 返回空数据但保持原有结构
                new_model = EditableTableManager()
                new_model._columns = self._columns.copy()
                new_model._data = []
                new_model._formulas = []
                new_model._custom_functions = self._custom_functions
                return new_model
                
            # 创建新的EditableTableManager并返回
            new_model = EditableTableManager()
            new_model._columns = self._columns.copy()
            new_model._data = unique_results
            new_model._formulas = unique_formulas
            new_model._custom_functions = self._custom_functions
            return new_model
            
        except Exception as e:
            logging.error(f"搜索规则解析失败: {str(e)}")
            return None




    def filter_data(self, column: str, value: Any) -> Optional[QAbstractTableModel]:
        """按列值筛选数据
        Args:
            column: str，要筛选的列名
            value: Any，筛选的值
        Returns:
            Optional[QAbstractTableModel]: 筛选后的数据模型，失败返回None
        """
        try:
            filtered_data = [row for row in self._data if str(row[self._columns.index(column)]).lower().find(str(value).lower()) != -1]
            return PandasModel(pd.DataFrame(filtered_data, columns=self._columns))
        except Exception:
            return None

    def search_global(self, keyword: str) -> Optional[QAbstractTableModel]:
        """全局搜索数据
        Args:
            keyword: str，搜索关键词
        Returns:
            Optional[QAbstractTableModel]: 搜索结果数据模型，失败返回None
        """
        try:
            filtered_data = [row for row in self._data if any(str(item).lower().find(keyword.lower()) != -1 for item in row)]
            return PandasModel(pd.DataFrame(filtered_data, columns=self._columns))
        except Exception:
            return None

    def reset_filter(self) -> QAbstractTableModel:
        """重置筛选，返回原始数据
        Returns:
            QAbstractTableModel: 当前数据模型实例
        """
        return self

    def get_data(self) -> List[List[Any]]:
        """获取当前表格的所有数据
        Returns:
            List[List[Any]]: 二维列表形式的表格数据
        """
        return self._data

    def _parse_formula_dependencies(self, formula: str, row: int, col: int) -> List[Tuple[int, int]]:
        """分析公式依赖的单元格，返回依赖的单元格列表[(row, col), ...]"""
        if not formula or not isinstance(formula, str) or not formula.startswith("="):
            return []
            
        dependencies = []
        
        # 去掉等号
        formula = formula[1:]
        
        # 检查是否是 函数名(@表名.列名) 格式
        func_table_col_pattern = r'(\w+)\(\@(\w+)\.(\w+)\)'
        func_table_col_matches = re.finditer(func_table_col_pattern, formula)
        
        for match in func_table_col_matches:
            table_name = match.group(2)
            col_name = match.group(3)
            
            # 记录整列依赖
            if table_name == self._table_name and col_name in self._columns:
                col_idx = self._columns.index(col_name)
                # 记录依赖此列的所有单元格
                for r in range(len(self._data)):
                    dependencies.append((r, col_idx))
        
        # 解析单元格引用 (例如: A1, B2 等)
        cell_ref_pattern = r'[A-Z]+[0-9]+'
        cell_refs = re.findall(cell_ref_pattern, formula)
        
        for cell_ref in cell_refs:
            col_name = ''.join(filter(str.isalpha, cell_ref))
            row_num = int(''.join(filter(str.isdigit, cell_ref))) - 1
            
            col_idx = 0
            for i, c in enumerate(reversed(col_name)):
                col_idx += (ord(c) - ord('A') + 1) * (26 ** i)
            col_idx -= 1
            
            dependencies.append((row_num, col_idx))
        
        return dependencies
        
    def _update_dependency_graph(self):
        """更新整个依赖图"""
        # 清空现有图
        self._dependency_graph.clear()
        self._cell_dependencies.clear()
        self._reverse_dependencies.clear()
        
        # 遍历所有单元格，构建依赖关系
        for row in range(len(self._formulas)):
            for col in range(len(self._formulas[row])):
                formula = self._formulas[row][col]
                if formula:
                    # 分析公式依赖
                    dependencies = self._parse_formula_dependencies(formula, row, col)
                    
                    # 记录依赖关系
                    self._cell_dependencies[(row, col)] = dependencies
                    
                    # 构建依赖图
                    for dep_row, dep_col in dependencies:
                        # 添加节点和边
                        self._dependency_graph.add_edge((dep_row, dep_col), (row, col))
                        
                        # 记录反向依赖
                        if (dep_row, dep_col) not in self._reverse_dependencies:
                            self._reverse_dependencies[(dep_row, dep_col)] = []
                        self._reverse_dependencies[(dep_row, dep_col)].append((row, col))
    
    def _update_dependent_cells(self, row: int, col: int):
        """更新依赖于指定单元格的所有单元格"""
        # 使用拓扑排序获取更新顺序
        if (row, col) in self._reverse_dependencies:
            visited = set()
            to_visit = [(row, col)]
            
            # 按依赖顺序更新单元格
            while to_visit:
                curr_row, curr_col = to_visit.pop(0)
                if (curr_row, curr_col) in visited:
                    continue
                    
                visited.add((curr_row, curr_col))
                
                # 查找所有依赖此单元格的单元格
                if (curr_row, curr_col) in self._reverse_dependencies:
                    for dep_row, dep_col in self._reverse_dependencies[(curr_row, curr_col)]:
                        # 更新单元格值
                        formula = self._formulas[dep_row][dep_col]
                        if formula:
                            try:
                                # 重新计算公式
                                result = self._evaluate_formula(formula, dep_row, dep_col)
                                self._data[dep_row][dep_col] = result
                                
                                # 添加到访问队列
                                to_visit.append((dep_row, dep_col))
                            except Exception as e:
                                logging.error(f"更新依赖单元格时发生错误: {str(e)}")
            
            # 发出数据变化信号
            self.dataChanged.emit(
                self.index(0, 0), 
                self.index(len(self._data) - 1, len(self._columns) - 1)
            )

