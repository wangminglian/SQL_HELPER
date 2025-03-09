from PySide6.QtWidgets import (QWidget, QApplication, QPushButton, QLineEdit, 
                             QComboBox, QRadioButton, QTableView, QTextEdit, QLabel, QFileDialog, QMessageBox,
                             QStyledItemDelegate, QListWidget, QListWidgetItem, QHBoxLayout, QVBoxLayout, QDialog)
from clinet.TBSQL_UI import Ui_TBSQL_UI
import sys
import json
from util.pandasutil import  EditableTableManager
from PySide6.QtWidgets import QAbstractItemView  # 确保导入了这个类
from PySide6.QtCore import Qt, QPoint, QTimer  # 添加 Qt 和 QPoint
import logging
from PySide6.QtWidgets import QInputDialog
from PySide6.QtGui import QKeySequence, QFocusEvent, QCursor
import re


# 设置loging 打印到控制台
logging.basicConfig(level=logging.INFO,format='%(asctime)s - %(levelname)s -%(filename)s- %(funcName)s - %(message)s')




INNT_DATA = {
    "表格列表": {}
    ,"函数列表":{}
    ,"模板列表":{}
    ,"运行记录":{}
}

ININT_TB_DATA ={
    "表格字段": []
    ,"表格数据": []
}

INNT_FUNC_DATA ={
    "函数描述": "函数描述"
    ,"函数参数": []
    ,"函数类型": "函数类型"
    ,"函数数据": "函数数据"
    ,"函数范围": "函数范围"
}

INNT_MB_DATA ={
    "模板描述": "模板描述"
    ,"模板数据": "模板数据"
    ,"模板范围": "模板范围"
}

INNT_RUN_DATA ={
    "运行记录时间": ""
    ,"运行记录语句": ""
}


# 创建新增列对话框类
class AddColumnDialog(QInputDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        
        # 设置对话框样式表，使用与主界面相匹配的蓝色主题
        dialog_style = """
            QInputDialog {
                background-color: #e0f7fa;
                color: #333;
                font-family: Arial;
                font-size: 14px;
            }
            
            QInputDialog QLineEdit {
                background-color: white;
                color: #01579B;
                border: 1px solid #ccc;
                padding: 5px;
                border-radius: 3px;
            }
            
            QInputDialog QPushButton {
                background-color: #0288d1;
                color: white;
                border: none;
                padding: 5px 10px;
                text-align: center;
                font-size: 16px;
                margin: 4px 2px;
                border-radius: 5px;
            }
            
            QInputDialog QPushButton:hover {
                background-color: white;
                color: black;
                border: 2px solid #0288d1;
            }
            
            QInputDialog QLabel {
                font-size: 14px;
                color: #01579B;
            }
        """
        
        self.setStyleSheet(dialog_style)
        self.setWindowTitle("新增列")
        self.setLabelText("请输入列名:")
        self.setInputMode(QInputDialog.TextInput)
        
        # 设置按钮文本为中文
        self.setOkButtonText("确定")
        self.setCancelButtonText("退出")

    def get_column_name(self):
        """获取用户输入的列名"""
        if self.exec() == QInputDialog.Accepted:
            return self.textValue()
        return None


class ColumnSelector(QListWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowFlags(Qt.Popup | Qt.FramelessWindowHint | Qt.NoDropShadowWindowHint)
        self.setFocusPolicy(Qt.NoFocus)  # 改为 NoFocus，不再捕获焦点
        self.setMaximumHeight(200)
        self.setAttribute(Qt.WA_ShowWithoutActivating)  # 不激活窗口
        self.setMouseTracking(True)
        
        # 设置样式
        self.setStyleSheet("""
            QListWidget {
                border: 1px solid #0288d1;
                background-color: white;
                border-radius: 3px;
            }
            QListWidget::item {
                padding: 5px;
                color: #01579B;
            }
            QListWidget::item:selected {
                background-color: #e0f7fa;
                color: #01579B;
            }
            QListWidget::item:hover {
                background-color: #b3e5fc;
            }
        """)
        
        self.itemClicked.connect(self.on_item_clicked)
        self.visible_items_count = 0

    def filter_items(self, text):
        """根据输入文本过滤列表项"""
        self.visible_items_count = 0
        for i in range(self.count()):
            item = self.item(i)
            if text.lower() in item.text().lower():
                item.setHidden(False)
                self.visible_items_count += 1
            else:
                item.setHidden(True)
                
        # 如果没有可见项，自动隐藏选择框
        if self.visible_items_count == 0:
            self.hide()
        else:
            self.show()
            # 选中第一个可见项
            for i in range(self.count()):
                if not self.item(i).isHidden():
                    self.setCurrentRow(i)
                    break

    def leaveEvent(self, event):
        """处理鼠标离开事件"""
        # 延迟一小段时间后检查鼠标位置
        QTimer.singleShot(100, self.check_mouse_position)
        super().leaveEvent(event)

    def check_mouse_position(self):
        """检查鼠标位置决定是否隐藏选择框"""
        if not self.rect().contains(self.mapFromGlobal(QCursor.pos())):
            self.hide()

    def mousePressEvent(self, event):
        """处理鼠标点击事件"""
        super().mousePressEvent(event)
        # 获取点击的项
        item = self.itemAt(event.position().toPoint())
        if item:
            self.on_item_clicked(item)

    def showEvent(self, event):
        """处理显示事件"""
        super().showEvent(event)
        # 确保选择框在显示时获得焦点
        self.setFocus()

    def hideEvent(self, event):
        """处理隐藏事件"""
        super().hideEvent(event)
        # 如果有父窗口的搜索框，将焦点返回给它
        if hasattr(self, 'parent_widget'):
            self.parent_widget.setFocus()

    def on_item_clicked(self, item):
        if hasattr(self, 'parent_widget'):
            # 获取当前搜索框的文本
            current_text = self.parent_widget.text()
            # 找到最后一个@的位置
            last_at = current_text.rfind('@')
            if last_at != -1:
                # 保留@符号，并添加选中的列名
                new_text = current_text[:last_at] + '@' + item.text()
                self.parent_widget.setText(new_text)
        self.hide()

    def keyPressEvent(self, event):
        """处理键盘事件"""
        if event.key() in (Qt.Key_Return, Qt.Key_Enter):
            # 获取当前选中的项
            current_item = self.currentItem()
            if current_item and not current_item.isHidden():
                self.on_item_clicked(current_item)
            event.accept()
        else:
            super().keyPressEvent(event)


class FormulaInputDialog(QDialog):
    def __init__(self, parent=None, functions=None):
        super().__init__(parent, Qt.Popup | Qt.FramelessWindowHint)
        self.parent = parent
        self.functions = functions or []
        self.selected_function = None
        
        # 设置布局
        layout = QVBoxLayout(self)
        layout.setContentsMargins(5, 5, 5, 5)
        layout.setSpacing(0)
        
        # 创建输入框
        self.input_field = QLineEdit(self)
        self.input_field.setPlaceholderText("输入函数名进行搜索...")
        self.input_field.textChanged.connect(self.filter_functions)
        layout.addWidget(self.input_field)
        
        # 创建函数列表
        self.function_list = QListWidget(self)
        self.function_list.setMaximumHeight(200)
        self.function_list.itemClicked.connect(self.on_function_selected)
        layout.addWidget(self.function_list)
        
        # 添加函数到列表
        for func in self.functions:
            self.function_list.addItem(func)
            
        # 设置样式
        self.setStyleSheet("""
            QDialog {
                background-color: white;
                border: 1px solid #0288d1;
                border-radius: 3px;
            }
            QLineEdit {
                padding: 5px;
                border: 1px solid #b3e5fc;
                border-radius: 3px;
                margin-bottom: 5px;
            }
            QListWidget {
                border: none;
                background-color: white;
            }
            QListWidget::item {
                padding: 5px;
                color: #01579B;
            }
            QListWidget::item:selected {
                background-color: #e0f7fa;
                color: #01579B;
            }
            QListWidget::item:hover {
                background-color: #b3e5fc;
            }
        """)
        
        # 设置焦点
        self.input_field.setFocus()
        
    def filter_functions(self, text):
        """根据输入文本过滤函数列表"""
        for i in range(self.function_list.count()):
            item = self.function_list.item(i)
            if text.lower() in item.text().lower():
                item.setHidden(False)
            else:
                item.setHidden(True)
                
        # 选中第一个可见项
        for i in range(self.function_list.count()):
            if not self.function_list.item(i).isHidden():
                self.function_list.setCurrentRow(i)
                break
                
    def on_function_selected(self, item):
        """处理函数选择事件"""
        self.selected_function = item.text()
        self.accept()
        
    def keyPressEvent(self, event):
        """处理键盘事件"""
        if event.key() in (Qt.Key_Return, Qt.Key_Enter):
            # 获取当前选中的项
            current_item = self.function_list.currentItem()
            if current_item and not current_item.isHidden():
                self.on_function_selected(current_item)
            event.accept()
        elif event.key() == Qt.Key_Escape:
            self.reject()
        else:
            super().keyPressEvent(event)


class TBSQLWindow(QWidget):
    def __init__(self,filename=None):
        super().__init__()
        # 创建UI对象
        self.ui = Ui_TBSQL_UI()
        # 设置UI
        self.ui.setupUi(self)
        # 创建 TableManager 实例
        self.table_manager = EditableTableManager()
        
        # 注册自定义函数
        self._register_custom_functions()
        
        # 初始化界面
        self.init_ui()
        
        # 如果指定文件名，则读取文件，初始化数据
        if filename:
            self.load_json(filename)
        
    def _register_custom_functions(self):
        """注册自定义函数"""
        # 计算年龄函数
        def calculate_age(date_str):
            """计算年龄函数，支持表名.列名格式
            
            参数可以是:
            1. 直接值: calculate_age("2000-01-01")
            2. 当前表列名: calculate_age(入职日期)
            3. 其他表列名: calculate_age(员工信息表.入职日期)
            """
            try:
                if not date_str or date_str.startswith("#REF"):
                    return "#REF!"
                
                # 这里只是示例，实际应该计算真实年龄
                # 可以使用datetime计算年龄差
                return f"{date_str}:@@@公式计算"
            except Exception as e:
                return f"#ERROR: {str(e)}"
                
        # 注册函数
        self.table_manager.register_function('calculate_age', calculate_age)
        
        # 可以继续注册更多自定义函数
        def sum_range(start_cell, end_cell):
            """计算单元格范围求和
            
            参数可以是:
            1. 单元格引用: sum_range(A1, B5)
            2. 列名引用: sum_range(工资, 奖金)
            3. 表名.列名引用: sum_range(工资表.基本工资, 工资表.绩效)
            """
            try:
                # 这里只是示例，实际应该计算真实的和
                return f"求和({start_cell},{end_cell})"
            except Exception as e:
                return f"#ERROR: {str(e)}"
            
        def average_range(start_cell, end_cell):
            """计算单元格范围平均值
            
            参数可以是:
            1. 单元格引用: average_range(A1, B5)
            2. 列名引用: average_range(工资, 奖金)
            3. 表名.列名引用: average_range(工资表.基本工资, 工资表.绩效)
            """
            try:
                # 这里只是示例，实际应该计算真实的平均值
                return f"平均值({start_cell},{end_cell})"
            except Exception as e:
                return f"#ERROR: {str(e)}"
            
        # 注册更多函数
        self.table_manager.register_function('sum_range', sum_range)
        self.table_manager.register_function('average_range', average_range)

    def init_ui(self):
        # ====== 按钮组件 ======
        # 导入文档按钮
        self.pb_input_excel: QPushButton = self.ui.pb_input_excel
        # 保存数据按钮
        self.pb_save: QPushButton = self.ui.pb_save
        # 新建表格按钮
        self.pb_add_tab: QPushButton = self.ui.pb_add_tab
        # 创建函数按钮
        self.pb_create_func: QPushButton = self.ui.pb_create_func
        # 删除表格按钮
        self.pb_del_excel: QPushButton = self.ui.pb_del_excel
        # 删除函数按钮
        self.pb_del_func: QPushButton = self.ui.pb_del_func
        # 数据导入按钮
        self.pb_tab1_data_in: QPushButton = self.ui.pb_tab1_data_in
        # 新增列按钮
        self.pb_tab1_add_col: QPushButton = self.ui.pb_tab1_add_col
        # 删除列按钮
        self.pb_tab1_del_col: QPushButton = self.ui.pb_tab1_del_col
        # 新增行按钮
        self.pb_tab1_add_row: QPushButton = self.ui.pb_tab1_add_row
        # 删除行按钮
        self.pb_tab1_del_row: QPushButton = self.ui.pb_tab1_del_row
        # 存为模板按钮
        self.pb_save_mb: QPushButton = self.ui.pb_save_mb
        # 历史记录按钮
        self.pb_history: QPushButton = self.ui.pb_history
        # 生成按钮
        self.pb_run: QPushButton = self.ui.pb_run

        # ====== 输入框组件 ======
        # 表格搜索输入框
        self.li_tb_search: QLineEdit = self.ui.li_tb_search
        # 字段筛选输入框
        self.li_tab1_search: QLineEdit = self.ui.li_tab1_search
        # 命令输入框
        self.li_com: QLineEdit = self.ui.li_com
        # 表格名称输入框
        self.li_tb: QLineEdit = self.ui.li_tb
        # 列名输入框
        self.li_col: QLineEdit = self.ui.li_col
        # 变量搜索输入框
        self.li_search_arg: QLineEdit = self.ui.li_search_arg
        # 模板搜索输入框
        self.li_mb_search: QLineEdit = self.ui.li_mb_search

        # ====== 下拉框组件 ======
        # 表格选择下拉框
        self.com_table: QComboBox = self.ui.com_table

        # ====== 单选按钮 ======
        # 是否置顶单选框
        self.ra_zhiding: QRadioButton = self.ui.ra_zhiding

        # ====== 表格组件 ======
        # 主数据表格
        self.tb_data: QTableView = self.ui.tb_data
        # 参数列表表格
        self.tb_arg_list: QTableView = self.ui.tb_arg_list

        # ====== 文本框组件 ======
        # 所有命令文本框
        self.tx_all_com: QTextEdit = self.ui.tx_all_com
        # 输出文本框
        self.tx_out: QTextEdit = self.ui.tx_out

        # ====== 初始化数据 ======
        self.data_dict = INNT_DATA
        
        # ====== 绑定事件 ======
        self.pb_input_excel.clicked.connect(self.import_json)
        # 绑定下拉框选择事件
        self.com_table.currentTextChanged.connect(self.on_table_changed)
        
        # 设置表格编辑触发方式
        self.tb_data.setEditTriggers(QTableView.DoubleClicked | 
                                   QTableView.EditKeyPressed | 
                                   QTableView.AnyKeyPressed)
        
        # 允许多选
        self.tb_data.setSelectionMode(QTableView.ExtendedSelection)
        # 设置表格调整模式
        self.tb_data.horizontalHeader().setStretchLastSection(True)
        self.tb_data.horizontalHeader().setSectionsMovable(True)
        
        # 启用表格单元格的自定义颜色显示
        self.tb_data.setAlternatingRowColors(False)  # 禁用交替行颜色，以便更好地显示公式单元格颜色
        
        # 设置表格双击事件
        self.tb_data.doubleClicked.connect(self.on_tb_data_double_clicked)
        # 新增列按钮
        self.pb_tab1_add_col.clicked.connect(self.add_column)
        # 绑定新增行按钮事件
        self.pb_tab1_add_row.clicked.connect(self.add_row)
        # 绑定删除行按钮事件
        self.pb_tab1_del_row.clicked.connect(self.delete_row)
        # 绑定删除列按钮事件
        self.pb_tab1_del_col.clicked.connect(self.delete_column)
        # 绑定表格搜索按钮事件
        self.li_tb_search.textChanged.connect(self.search_table)
        # 绑定数据搜索按钮事件
        self.li_tab1_search.textChanged.connect(self.search_data_by_rule)
        # 绑定命令输入框事件
        self.li_com.textChanged.connect(self.handle_command_input)
        # 绑定执行按钮事件
        self.pb_run.clicked.connect(self.execute_command)
        
        # 记录上一个search_rule 
        self.last_search_rule = ""
        # 记录上一个command_input
        self.last_command_input = ""

        # 添加公式单元格图例标签
        self.formula_legend = QLabel(self)
        self.formula_legend.setText("绿色文字表示公式单元格")
        self.formula_legend.setStyleSheet("""
            background-color: rgb(230, 245, 255); 
            color: rgb(0, 128, 0);
            padding: 3px;
            border-radius: 3px;
            font-size: 12px;
            border: 1px solid rgb(200, 225, 255);
        """)
        self.formula_legend.setFixedHeight(20)
        self.formula_legend.setAlignment(Qt.AlignCenter)
        
        # 将图例放在表格上方
        legend_container = QWidget(self)
        legend_layout = QHBoxLayout(legend_container)
        legend_layout.setContentsMargins(0, 0, 0, 0)
        legend_layout.addStretch()
        legend_layout.addWidget(self.formula_legend)
        
        # 将图例容器添加到表格上方
        # 在水平布局3（包含表格的布局）前插入图例
        self.ui.verticalLayout_3.insertWidget(3, legend_container)

        # 初始化上一次输入的表格名
        self.last_table_input = ""
        
        # 连接表格名称输入框的文本变化信号
        self.li_tb.textChanged.connect(self.handle_table_input)

    # 实现li_tb功能，
    # 当用户在li_tb中输入@时，像li_com一样弹出选择器，选择器中包含所有表格名称
    # 选择器支持键盘上下键切换，回车选择
    

    # 处理命令输入框的输入
    def handle_command_input(self):
        """处理命令输入框的输入，提供智能提示功能"""
        try:
            # 获取当前输入的文本
            command_input = self.li_com.text().strip()
            
            # 如果输入比上一次短，说明是删除操作，隐藏选择器
            if len(command_input) < len(self.last_command_input):
                if hasattr(self, 'formula_selector'):
                    self.formula_selector.hide()
                if hasattr(self, 'table_selector'):
                    self.table_selector.hide()
                if hasattr(self, 'column_selector_for_command'):
                    self.column_selector_for_command.hide()
                self.last_command_input = command_input
                return
            
            # 更新上一次输入
            self.last_command_input = command_input
            
            # 检查是否输入了等号，弹出公式选择器
            if '=' in command_input and command_input.endswith('='):
                self.show_formula_selector()
                return
                
            # 检查是否输入了@符号，弹出表名选择器
            if '@' in command_input:
                last_at_pos = command_input.rfind('@')
                after_at = command_input[last_at_pos + 1:].strip()
                
                # 如果@后面有空格或其他分隔符，则不显示选择框
                if '=' in after_at or ' ' in after_at or ',' in after_at or '.' in after_at:
                    if hasattr(self, 'table_selector'):
                        self.table_selector.hide()
                else:
                    self.show_table_selector(after_at, self.li_com)
                return
                
            # 检查是否输入了点号，弹出列名选择器
            if '.' in command_input:
                last_dot_pos = command_input.rfind('.')
                # 获取点号前的表名
                dot_context = command_input[:last_dot_pos]
                table_name = None
                
                # 尝试从@符号后提取表名
                if '@' in dot_context:
                    at_pos = dot_context.rfind('@')
                    potential_table = dot_context[at_pos + 1:].strip()
                    # 检查表名是否存在
                    if potential_table in self.data_dict.get("表格列表", {}):
                        table_name = potential_table
                
                # 如果找到了表名，显示该表的列名选择器
                if table_name:
                    after_dot = command_input[last_dot_pos + 1:].strip()
                    # 如果点号后面有空格或其他分隔符，则不显示选择框
                    if '=' in after_dot or ' ' in after_dot or ',' in after_dot:
                        if hasattr(self, 'column_selector_for_command'):
                            self.column_selector_for_command.hide()
                    else:
                        self.show_column_selector_for_command(table_name, after_dot)
                return
                
            # 如果没有特殊字符，隐藏所有选择器
            if hasattr(self, 'formula_selector'):
                self.formula_selector.hide()
            if hasattr(self, 'table_selector'):
                self.table_selector.hide()
            if hasattr(self, 'column_selector_for_command'):
                self.column_selector_for_command.hide()
                
        except Exception as e:
            logging.error(f"处理命令输入时出错: {str(e)}")
    
    def show_formula_selector(self):
        """显示公式选择器"""
        try:
            # 获取已注册的函数列表
            functions = list(self.table_manager._custom_functions.keys())
            
            # 创建并显示公式输入对话框
            formula_dialog = FormulaInputDialog(self, functions)
            
            # 设置位置和大小
            pos = self.li_com.mapToGlobal(QPoint(0, self.li_com.height()))
            formula_dialog.move(pos)
            formula_dialog.setFixedWidth(self.li_com.width())
            
            # 显示对话框并等待结果
            if formula_dialog.exec() == QDialog.Accepted and formula_dialog.selected_function:
                # 用户选择了函数
                current_text = self.li_com.text()
                # 保留等号，并添加选中的函数名加括号
                new_text = current_text + formula_dialog.selected_function + "("
                self.li_com.setText(new_text)
                # 将光标移动到括号内
                self.li_com.setCursorPosition(len(new_text))
            
        except Exception as e:
            logging.error(f"显示公式选择器时出错: {str(e)}")
    
    def show_table_selector(self, filter_text="", parent_widget=None):
        """显示表名选择器
        
        Args:
            filter_text: 过滤文本
            parent_widget: 父组件，默认为 li_com
        """
        try:
            # 如果没有指定父组件，默认使用 li_com
            if parent_widget is None:
                parent_widget = self.li_com
            
            # 确保表名选择器已创建
            if not hasattr(self, 'table_selector'):
                self.table_selector = ColumnSelector(self)
            
            # 设置父组件
            self.table_selector.parent_widget = parent_widget
            
            # 获取所有表名
            tables = list(self.data_dict.get("表格列表", {}).keys())
            
            # 清空并重新添加表名
            self.table_selector.clear()
            for table in tables:
                self.table_selector.addItem(table)
            
            # 设置位置和大小
            pos = parent_widget.mapToGlobal(QPoint(0, parent_widget.height()))
            self.table_selector.move(pos)
            self.table_selector.setFixedWidth(parent_widget.width())
            
            # 根据输入过滤列表项
            self.table_selector.filter_items(filter_text)
            
            # 设置选择器的点击事件处理
            def on_table_selected(item):
                current_text = parent_widget.text()
                # 找到最后一个@符号的位置
                last_at_pos = current_text.rfind('@')
                # 替换@后面的内容为选中的表名
                new_text = current_text[:last_at_pos + 1] + item.text()
                
                # 如果父组件是 li_com，则在表名后添加点号
                if parent_widget == self.li_com:
                    new_text += "."
                
                parent_widget.setText(new_text)
                # 将光标移动到末尾
                parent_widget.setCursorPosition(len(new_text))
                self.table_selector.hide()
                
                # 如果父组件是 li_com，自动触发列名选择器
                if parent_widget == self.li_com:
                    self.show_column_selector_for_command(item.text(), "")
            
            # 绑定选择事件
            self.table_selector.on_item_clicked = on_table_selected
            
            # 显示选择器
            self.table_selector.show()
            
        except Exception as e:
            logging.error(f"显示表名选择器时出错: {str(e)}")
    
    def show_column_selector_for_command(self, table_name, filter_text=""):
        """显示列名选择器（用于命令输入）"""
        try:
            # 确保列名选择器已创建
            if not hasattr(self, 'column_selector_for_command'):
                self.column_selector_for_command = ColumnSelector(self)
                self.column_selector_for_command.parent_widget = self.li_com
            
            # 获取指定表的列名
            if table_name in self.data_dict.get("表格列表", {}):
                columns = self.data_dict["表格列表"][table_name]["表格字段"]
                
                # 清空并重新添加列名
                self.column_selector_for_command.clear()
                for col in columns:
                    self.column_selector_for_command.addItem(col)
                
                # 设置位置和大小
                pos = self.li_com.mapToGlobal(QPoint(0, self.li_com.height()))
                self.column_selector_for_command.move(pos)
                self.column_selector_for_command.setFixedWidth(self.li_com.width())
                
                # 根据输入过滤列表项
                self.column_selector_for_command.filter_items(filter_text)
                
                # 设置选择器的点击事件处理
                def on_column_selected(item):
                    current_text = self.li_com.text()
                    # 找到最后一个点号的位置
                    last_dot_pos = current_text.rfind('.')
                    # 替换点号后面的内容为选中的列名
                    new_text = current_text[:last_dot_pos + 1] + item.text()
                    self.li_com.setText(new_text)
                    # 将光标移动到末尾
                    self.li_com.setCursorPosition(len(new_text))
                    self.column_selector_for_command.hide()
                
                # 绑定选择事件
                self.column_selector_for_command.on_item_clicked = on_column_selected
            
        except Exception as e:
            logging.error(f"显示列名选择器时出错: {str(e)}")

    # 弹出选择器，选择文本（用于表格搜索）
    def show_column_selector(self, search_rule):
        """弹出选择器，选择文本（用于表格搜索）"""
        # 如果search_rule 比 last_search_rule 长度短，说明是删除，则不显示选择框
        if len(search_rule) < len(self.last_search_rule):
            if hasattr(self, 'column_selector'):
                self.column_selector.hide()
            return
            
        # 检查是否刚输入了@符号
        if '@' in search_rule:
            last_at_pos = search_rule.rfind('@')
            after_at = search_rule[last_at_pos + 1:].strip()
            logging.info(f"after_at: {after_at}")
            
            # 如果@后面有空格或其他分隔符，则不显示选择框
            if '=' in after_at or ' ' in after_at or ',' in after_at:
                if hasattr(self, 'column_selector'):
                    self.column_selector.hide()
            else:
                current_table = self.com_table.currentText()
                if current_table:
                    # 确保列名选择器已创建
                    if not hasattr(self, 'column_selector'):
                        self.column_selector = ColumnSelector(self)
                        self.column_selector.parent_widget = self.li_tab1_search
                    
                    # 获取当前表格的列名
                    columns = self.data_dict["表格列表"][current_table]["表格字段"]
                    
                    # 清空并重新添加列名
                    self.column_selector.clear()
                    for col in columns:
                        self.column_selector.addItem(col)
                    
                    # 设置位置和大小
                    pos = self.li_tab1_search.mapToGlobal(QPoint(0, self.li_tab1_search.height()))
                    self.column_selector.move(pos)
                    self.column_selector.setFixedWidth(self.li_tab1_search.width())
                    
                    # 根据输入过滤列表项（这会自动处理显示/隐藏）
                    self.column_selector.filter_items(after_at)
                    
                    # 如果没有@后的文本，不进行搜索
                    if not after_at:
                        return
        else:
            # 如果没有@符号，确保选择框是隐藏的
            if hasattr(self, 'column_selector'):
                self.column_selector.hide()

    # 表格中数据搜索
    def search_data_by_rule(self):
        """根据规则搜索表格数据"""
        try:
            # 获取搜索规则
            search_rule = self.li_tab1_search.text().strip()
            
            # 弹出选择器，选择文本
            self.show_column_selector(search_rule)

            # 记录上一个search_rule
            self.last_search_rule = search_rule

            # 调用 table_manager 的 search_by_rule 方法进行搜索
            filtered_model = self.table_manager.search_by_rule(search_rule)
            
            if filtered_model:
                # 设置过滤后的数据模型
                self.tb_data.setModel(filtered_model)
                # 记录日志
                logging.info(f"过滤后的数据行数: {filtered_model.rowCount()}")
            else:
                # 如果搜索失败，显示错误消息
                self.on_table_changed(self.com_table.currentText())
                
        except Exception as e:
            logging.error(f"搜索数据时出错: {str(e)}")
            QMessageBox.critical(self, "错误", f"搜索失败: {str(e)}")
            # 发生错误时恢复显示所有数据
            self.on_table_changed(self.com_table.currentText())

    # 实现表格搜索功能
    def search_table(self):
        """实现表格搜索功能"""
        try:
            # 获取搜索框中的文本
            search_text = self.li_tb_search.text().strip().lower()
            
            # 清空下拉框
            self.com_table.clear()
            
            # 从data_dict中获取所有表格名称
            all_tables = self.data_dict.get("表格列表", {}).keys()
            
            # 根据搜索文本过滤表格名称
            filtered_tables = [table for table in all_tables 
                             if search_text in table.lower()]
            
            # 将过滤后的表格名称添加到下拉框
            self.com_table.addItems(filtered_tables)
            
        except Exception as e:
            logging.error(f"搜索表格时出错: {str(e)}")
            QMessageBox.critical(self, "错误", f"搜索表格失败: {str(e)}")
    

    # 绑定键盘事件
    def keyPressEvent(self, event):
        """处理键盘事件"""
        # 处理Ctrl+C复制表格内容
        if event.key() == Qt.Key_C and event.modifiers() == Qt.ControlModifier:
            # 检查焦点是否在表格上
            if self.tb_data.hasFocus():
                self.copy_selected_cells()
                event.accept()
                return
        
        # 处理表格选择器的键盘事件
        if hasattr(self, 'table_selector') and self.table_selector.isVisible():
            if event.key() == Qt.Key_Up:
                # 向上选择
                current_row = self.table_selector.currentRow()
                if current_row > 0:
                    # 找到上一个可见项
                    for i in range(current_row - 1, -1, -1):
                        if not self.table_selector.item(i).isHidden():
                            self.table_selector.setCurrentRow(i)
                            break
                event.accept()
                return
            elif event.key() == Qt.Key_Down:
                # 向下选择
                current_row = self.table_selector.currentRow()
                if current_row < self.table_selector.count() - 1:
                    # 找到下一个可见项
                    for i in range(current_row + 1, self.table_selector.count()):
                        if not self.table_selector.item(i).isHidden():
                            self.table_selector.setCurrentRow(i)
                            break
                event.accept()
                return
            elif event.key() == Qt.Key_Return or event.key() == Qt.Key_Enter:
                # 确认选择
                current_item = self.table_selector.currentItem()
                if current_item and not current_item.isHidden():
                    self.table_selector.on_item_clicked(current_item)
                event.accept()
                return
            elif event.key() == Qt.Key_Escape:
                # 关闭选择器
                self.table_selector.hide()
                event.accept()
                return
                
        if hasattr(self, 'column_selector') and self.column_selector.isVisible():
            if event.key() == Qt.Key_Up:
                # 向上选择
                current_row = self.column_selector.currentRow()
                if current_row > 0:
                    # 找到上一个可见项
                    for i in range(current_row - 1, -1, -1):
                        if not self.column_selector.item(i).isHidden():
                            self.column_selector.setCurrentRow(i)
                            break
                event.accept()
                return
            elif event.key() == Qt.Key_Down:
                # 向下选择
                current_row = self.column_selector.currentRow()
                if current_row < self.column_selector.count() - 1:
                    # 找到下一个可见项
                    for i in range(current_row + 1, self.column_selector.count()):
                        if not self.column_selector.item(i).isHidden():
                            self.column_selector.setCurrentRow(i)
                            break
                event.accept()
                return
            elif event.key() == Qt.Key_Return or event.key() == Qt.Key_Enter:
                # 确认选择
                current_item = self.column_selector.currentItem()
                if current_item and not current_item.isHidden():
                    self.column_selector.on_item_clicked(current_item)
                event.accept()
                return
            elif event.key() == Qt.Key_Escape:
                # 关闭选择器
                self.column_selector.hide()
                event.accept()
                return
        
        # 其他键盘事件交给默认处理
        super().keyPressEvent(event)
        
    def copy_selected_cells(self):
        """复制表格中选中的单元格内容"""
        try:
            # 获取选择模型
            selection = self.tb_data.selectionModel()
            if not selection.hasSelection():
                return
                
            # 获取选中的索引
            selected_indexes = selection.selectedIndexes()
            if not selected_indexes:
                return
                
            # 按行列排序索引
            rows = sorted(set(index.row() for index in selected_indexes))
            columns = sorted(set(index.column() for index in selected_indexes))
            
            # 创建二维数组存储数据
            data = []
            for row in rows:
                row_data = []
                for column in columns:
                    # 查找当前行列的索引
                    for index in selected_indexes:
                        if index.row() == row and index.column() == column:
                            # 获取单元格数据
                            cell_data = self.tb_data.model().data(index, Qt.DisplayRole)
                            row_data.append(str(cell_data) if cell_data is not None else "")
                            break
                    else:
                        # 如果没有找到对应的单元格，添加空字符串
                        row_data.append("")
                data.append(row_data)
            
            # 将数据转换为制表符分隔的文本
            text = "\n".join("\t".join(cell for cell in row) for row in data)
            
            # 复制到剪贴板
            clipboard = QApplication.clipboard()
            clipboard.setText(text)
            
            # 显示状态栏提示信息，不弹窗打扰用户
            logging.info(f"已复制 {len(rows)}行 {len(columns)}列 数据到剪贴板")
            # 如果有状态栏，可以显示提示信息
            # self.statusBar().showMessage(f"已复制 {len(rows)}行 {len(columns)}列 数据到剪贴板", 3000)
            
        except Exception as e:
            logging.error(f"复制单元格失败: {str(e)}")
            QMessageBox.warning(self, "复制失败", f"复制单元格失败: {str(e)}")

    # 删除列
    def delete_column(self):
        """删除选中的列"""
        try:
            # 检查是否选择了表格
            current_table = self.com_table.currentText()
            if not current_table:
                QMessageBox.warning(self, "警告", "请先选择一个表格!")
                return

            # 确保 table_manager 已初始化
            if not hasattr(self, 'table_manager') or self.table_manager is None:
                logging.error("table_manager 未初始化")
                QMessageBox.critical(self, "错误", "表格管理器未初始化!")
                return

            # 获取选中的列索引
            selected_columns = self.tb_data.selectionModel().selectedColumns()
            if not selected_columns:
                QMessageBox.warning(self, "警告", "请先选择要删除的列!")
                return

            # 确认是否删除
            reply = QMessageBox.question(self, "确认", "确定要删除选中的列吗?",
                                       QMessageBox.Yes | QMessageBox.No)
            if reply == QMessageBox.No:
                return

            # 获取要删除的列索引并排序(从大到小,避免删除时索引变化)
            columns_to_delete = sorted([index.column() for index in selected_columns], reverse=True)

            # 删除选中的列
            for column in columns_to_delete:
                success = self.table_manager.delete_column_by_index(column)
                if not success:
                    QMessageBox.warning(self, "错误", f"删除第 {column + 1} 列失败!")
                    return

            # 更新表格显示
            self.on_table_changed(current_table)

        except Exception as e:
            logging.error(f"删除列时出错: {str(e)}")
            QMessageBox.critical(self, "错误", f"删除列失败: {str(e)}")
    

    # 删除行
    def delete_row(self):
        """删除选中的行"""
        try:
            # 检查是否选择了表格
            current_table = self.com_table.currentText()
            if not current_table:
                QMessageBox.warning(self, "警告", "请先选择一个表格!")
                return

            # 确保 table_manager 已初始化
            if not hasattr(self, 'table_manager') or self.table_manager is None:
                logging.error("table_manager 未初始化")
                QMessageBox.critical(self, "错误", "表格管理器未初始化!")
                return

            # 获取选中的行索引
            selected_rows = self.tb_data.selectionModel().selectedRows()
            if not selected_rows:
                QMessageBox.warning(self, "警告", "请先选择要删除的行!")
                return

            # 确认是否删除
            reply = QMessageBox.question(self, "确认", "确定要删除选中的行吗?",
                                       QMessageBox.Yes | QMessageBox.No)
            if reply == QMessageBox.No:
                return

            # 获取要删除的行索引并排序(从大到小,避免删除时索引变化)
            rows_to_delete = sorted([index.row() for index in selected_rows], reverse=True)

            # 删除选中的行
            for row in rows_to_delete:
                success = self.table_manager.delete_row(row)
                if not success:
                    QMessageBox.warning(self, "错误", f"删除第 {row + 1} 行失败!")
                    return

            # 更新表格显示
            self.on_table_changed(current_table)

        except Exception as e:
            logging.error(f"删除行时出错: {str(e)}")
            QMessageBox.critical(self, "错误", f"删除行失败: {str(e)}")

    
    # 新增行
    def add_row(self):
        """新增行"""
        try:
            # 检查是否选择了表格
            current_table = self.com_table.currentText()
            if not current_table:
                QMessageBox.warning(self, "警告", "请先选择一个表格!")
                return
                
            # 确保 table_manager 已初始化
            if not hasattr(self, 'table_manager') or self.table_manager is None:
                logging.error("table_manager 未初始化")
                QMessageBox.critical(self, "错误", "表格管理器未初始化!")
                return
                
            # 获取当前表格的列数,创建空行
            col_count = len(self.data_dict["表格列表"][current_table]["表格字段"])
            empty_row = ["" for _ in range(col_count)]
            
            try:
                # 添加新行到数据模型
                success = self.table_manager.add_row(empty_row)
                if success:
                    # 更新表格显示
                    self.on_table_changed(current_table)
                    # QMessageBox.information(self, "成功", "已添加新行")
                else:
                    QMessageBox.warning(self, "错误", "添加行失败!")
            except Exception as e:
                logging.error(f"添加行到数据模型时出错: {str(e)}")
                QMessageBox.critical(self, "错误", f"添加行失败: {str(e)}")
                
        except Exception as e:
            logging.error(f"新增行时出错: {str(e)}")
            QMessageBox.critical(self, "错误", f"新增行失败: {str(e)}")
            


    # 新增列
    def add_column(self):
        """新增列"""
        try:
            # 首先检查是否有选中的表格
            current_table = self.com_table.currentText()
            if not current_table:
                QMessageBox.warning(self, "警告", "请先选择一个表格!")
                return
                
            # 创建并显示新增列对话框
            dialog = AddColumnDialog(self)
            column_name = dialog.get_column_name()
            
            # 添加日志以便调试
            logging.info(f"输入的列名: {column_name}")
            
            if not column_name:
                logging.info("用户取消输入或未输入列名")
                return
                
            # 检查列名是否已存在
            existing_columns = self.data_dict["表格列表"][current_table]["表格字段"]
            if column_name in existing_columns:
                QMessageBox.warning(self, "警告", f"列名 '{column_name}' 已存在!")
                return
                
            # 确保 table_manager 已初始化
            if not hasattr(self, 'table_manager') or self.table_manager is None:
                logging.error("table_manager 未初始化")
                QMessageBox.critical(self, "错误", "表格管理器未初始化!")
                return
                
            # 添加新列到数据模型
            try:
                success = self.table_manager.add_column(column_name)
                if success:
                    # 更新数据字典中的表格字段
                    self.data_dict["表格列表"][current_table]["表格字段"]
                    # 更新表格显示
                    self.on_table_changed(current_table)
                    # QMessageBox.information(self, "成功", f"已添加列: {column_name}")
                else:
                    QMessageBox.warning(self, "错误", "添加列失败!")
            except Exception as e:
                logging.error(f"添加列到数据模型时出错: {str(e)}")
                QMessageBox.critical(self, "错误", f"添加列失败: {str(e)}")
                
        except Exception as e:
            logging.error(f"添加列失败: {str(e)}")
            QMessageBox.critical(self, "错误", f"添加列失败: {str(e)}")


    def on_tb_data_double_clicked(self, index):
        """处理表格双击事件"""
        # 设置当前单元格为编辑状态
        self.table_manager.set_editing_cell(index)
        
        # 获取当前单元格的编辑器
        editor = self.tb_data.edit(index)
        if editor:
            # 确保编辑器获得焦点
            editor.setFocus()
            
            # 连接编辑完成信号
            editor.editingFinished.connect(lambda: self._on_cell_editing_finished(index))
            
    def _on_cell_editing_finished(self, index):
        """处理单元格编辑完成事件"""
        # 清除编辑状态
        self.table_manager.clear_editing_cell()
        
    def init_data(self):
        """初始化数据到各组件"""
        # 清空当前下拉框选项
        self.com_table.clear()
        
        # 从data_dict中获取表格列表
        tables = self.data_dict.get("表格列表", {})
        
        # 遍历表格列表,将表格名称添加到下拉框
        for table_name in tables.keys():
            self.com_table.addItem(table_name)
            
        # 获取第一个表格数据并显示
        if tables:
            # 获取第一个表格名称
            first_table = list(tables.keys())[0]
            table_data = tables[first_table]
            
            # 设置表格数据
            model = self.table_manager.set_data(
                data=table_data["表格数据"],
                columns=table_data["表格字段"],
                table_name=first_table
            )
            self.tb_data.setModel(model)

    def on_table_changed(self, table_name):
        """表格切换事件"""
        try:
            # 获取选中的表格名称
            table_name = self.com_table.currentText()
            
            # 获取表格数据
            table_data = self.data_dict["表格列表"][table_name]
            
            # 设置表格数据
            model = self.table_manager.set_data(
                data=table_data["表格数据"],
                columns=table_data["表格字段"],
                table_name=table_name
            )
            self.tb_data.setModel(model)
            
        except Exception as e:
            logging.error(f"表格切换失败: {str(e)}")
    
    
    def load_json(self,file_path):
        try:
            if file_path:
                # 读取JSON文件
                with open(file_path, 'r', encoding='utf-8') as f:
                    self.data_dict = json.load(f)
                # 初始化数据到组件
                self.init_data()                
        except Exception as e:
            QMessageBox.critical(self, "错误", f"导入失败: {str(e)}")
            
    # 在导入JSON后调用初始化
    def import_json(self):
        """导入JSON文件"""
        logging.info("导入JSON文件")
        try:
            # 打开文件选择对话框
            file_path, _ = QFileDialog.getOpenFileName(
                    self,
                    "选择JSON文件", 
                    "",
                    "JSON Files (*.json)"
                )                
            self.load_json(file_path)
        except Exception as e:
            QMessageBox.critical(self, "错误", f"导入失败: {str(e)}")

    # 执行命令输入框中的命令
    def execute_command(self):
        """执行命令输入框中的命令"""
        try:
            # 获取命令文本
            command = self.li_com.text().strip()
            if not command:
                QMessageBox.warning(self, "警告", "请输入命令!")
                return
                
            # 记录命令到输出框
            self.tx_all_com.append(f">> {command}")
            
            # 解析命令
            if command.startswith('='):
                # 公式计算
                try:
                    # 去掉等号
                    formula = command[1:]
                    
                    # 替换@表名.列名引用
                    table_col_pattern = r'@([^.]+)\.([^,\s\)]+)'
                    
                    def replace_table_col_ref(match):
                        table_name = match.group(1)
                        col_name = match.group(2)
                        
                        # 检查表名和列名是否存在
                        if table_name in self.data_dict.get("表格列表", {}) and \
                           col_name in self.data_dict["表格列表"][table_name]["表格字段"]:
                            return f"{table_name}.{col_name}"
                        else:
                            return f"#REF!{table_name}.{col_name}"
                    
                    formula = re.sub(table_col_pattern, replace_table_col_ref, formula)
                    
                    # 提取函数名和参数
                    match = re.match(r'(\w+)\((.*)\)', formula)
                    if match:
                        func_name = match.group(1)
                        args_str = match.group(2)
                        
                        if func_name in self.table_manager._custom_functions:
                            # 解析参数
                            args = [arg.strip() for arg in args_str.split(',')]
                            
                            # 执行函数
                            result = self.table_manager._custom_functions[func_name](*args)
                            
                            # 显示结果
                            self.tx_all_com.append(f"结果: {result}")
                        else:
                            self.tx_all_com.append(f"错误: 未知函数 '{func_name}'")
                    else:
                        self.tx_all_com.append(f"错误: 无效的公式格式")
                        
                except Exception as e:
                    self.tx_all_com.append(f"错误: {str(e)}")
            else:
                # 其他命令处理
                self.tx_all_com.append(f"未实现的命令类型")
                
            # 清空命令输入框
            self.li_com.clear()
            
        except Exception as e:
            logging.error(f"执行命令时出错: {str(e)}")
            self.tx_all_com.append(f"执行错误: {str(e)}")

    def handle_table_input(self):
        """处理表格名称输入框的输入"""
        try:
            # 获取当前输入的文本
            table_name = self.li_tb.text()
            
            # 检查是否输入了@符号
            if '@' in table_name:
                # 如果输入了新的@符号，清空之前的所有内容，只保留新的@
                current_cursor_pos = self.li_tb.cursorPosition()
                # 检查光标前一个字符是否为@
                if current_cursor_pos > 0 and table_name[current_cursor_pos-1] == '@':
                    # 清空输入框，只保留@符号
                    self.li_tb.setText('@')
                    self.li_tb.setCursorPosition(1)  # 将光标移动到@后面
                    # 更新上一次输入
                    self.last_table_input = '@'
                    # 显示表格选择器
                    self.show_table_selector("", self.li_tb)
                    return
                
                # 处理其他情况下的@符号
                last_at_pos = table_name.rfind('@')
                after_at = table_name[last_at_pos + 1:].strip()
                
                # 如果@后面有空格或其他分隔符，则不显示选择框
                if '=' in after_at or ' ' in after_at or ',' in after_at or '.' in after_at:
                    if hasattr(self, 'table_selector'):
                        self.table_selector.hide()
                else:
                    self.show_table_selector(after_at, self.li_tb)
                    
                # 确保输入框中只有一个@表名引用
                if table_name.count('@') > 1:
                    # 保留最后一个@及其后面的内容
                    new_text = '@' + after_at
                    self.li_tb.setText(new_text)
                    # 将光标放在文本末尾
                    self.li_tb.setCursorPosition(len(new_text))
                    # 更新上一次输入
                    self.last_table_input = new_text
                return
            
            # 如果输入比上一次短，说明是删除操作，隐藏选择器
            if len(table_name) < len(self.last_table_input):
                if hasattr(self, 'table_selector'):
                    self.table_selector.hide()
                self.last_table_input = table_name
                return
            
            # 更新上一次输入
            self.last_table_input = table_name
                
            # 检查是否输入了点号，弹出列名选择器
            if '.' in table_name:
                last_dot_pos = table_name.rfind('.')
                # 获取点号前的表名
                dot_context = table_name[:last_dot_pos]
                table_name = None
                
                # 尝试从@符号后提取表名
                if '@' in dot_context:
                    at_pos = dot_context.rfind('@')
                    potential_table = dot_context[at_pos + 1:].strip()
                    # 检查表名是否存在
                    if potential_table in self.data_dict.get("表格列表", {}):
                        table_name = potential_table
                
                # 如果找到了表名，显示该表的列名选择器
                if table_name:
                    after_dot = table_name[last_dot_pos + 1:].strip()
                    # 如果点号后面有空格或其他分隔符，则不显示选择框
                    if '=' in after_dot or ' ' in after_dot or ',' in after_dot:
                        if hasattr(self, 'column_selector_for_command'):
                            self.column_selector_for_command.hide()
                    else:
                        self.show_column_selector_for_command(table_name, after_dot)
                return
                
            # 如果没有特殊字符，隐藏所有选择器
            if hasattr(self, 'table_selector'):
                self.table_selector.hide()
            if hasattr(self, 'column_selector_for_command'):
                self.column_selector_for_command.hide()
                
        except Exception as e:
            logging.error(f"处理表格名称输入时出错: {str(e)}")


def main():
    app = QApplication(sys.argv)
    window = TBSQLWindow(filename="./data/yangben.json")
    window.show()
    sys.exit(app.exec())

if __name__ == "__main__":
    main()
