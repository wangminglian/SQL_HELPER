from PySide6.QtWidgets import QPushButton, QRadioButton, QTabWidget, QLineEdit, QTableView, QTextEdit

        # 导入Excel文件的按钮
        self.pb_input_excel: QPushButton = self.ui.pb_input_excel
        # 保存数据的按钮
        self.pb_save: QPushButton = self.ui.pb_save
        # 添加新Tab的按钮
        self.pb_add_tab: QPushButton = self.ui.pb_add_tab
        # 创建函数的按钮
        self.pb_create_func: QPushButton = self.ui.pb_create_func
        # 删除函数的按钮
        self.pb_del_func: QPushButton = self.ui.pb_del_func
        # 是否置顶的单选按钮
        self.ra_zhiding: QRadioButton = self.ui.ra_zhiding
        # Tab控件
        self.tab_table: QTabWidget = self.ui.tab_table
        # Tab1中的搜索输入框
        self.li_tab1_search: QLineEdit = self.ui.li_tab1_search
        # Tab1中的数据导入按钮
        self.pb_tab1_data_in: QPushButton = self.ui.pb_tab1_data_in
        # Tab1中添加列的按钮
        self.pb_tab1_add_col: QPushButton = self.ui.pb_tab1_add_col
        # Tab1中添加行的按钮
        self.pb_tab1_add_row: QPushButton = self.ui.pb_tab1_add_row
        # Tab1中删除列的按钮
        self.pb_tab1_del_col: QPushButton = self.ui.pb_tab1_del_col
        # Tab1中删除行的按钮
        self.pb_tab1_del_row: QPushButton = self.ui.pb_tab1_del_row
        # Tab1中的数据表格
        self.tb_tab1_data: QTableView = self.ui.tb_tab1_data
        # Tab1中的命令输入框
        self.li_tab1_com: QLineEdit = self.ui.li_tab1_com
        # Tab1中的表名输入框
        self.li_tab1_tb: QLineEdit = self.ui.li_tab1_tb
        # Tab1中的列名输入框
        self.li_tab1_col: QLineEdit = self.ui.li_tab1_col
        # Tab1中执行命令的按钮
        self.pb_tab1_run: QPushButton = self.ui.pb_tab1_run
        # 显示所有命令的文本编辑框
        self.tx_all_com: QTextEdit = self.ui.tx_all_com
        # 搜索参数的输入框
        self.li_search_arg: QLineEdit = self.ui.li_search_arg
        # 参数列表的表格
        self.tb_arg_list: QTableView = self.ui.tb_arg_list
        # 模板搜索的输入框
        self.li_mb_search: QLineEdit = self.ui.li_mb_search
        # 保存为模板的按钮
        self.pb_save_mb: QPushButton = self.ui.pb_save_mb
        # 查看历史记录的按钮
        self.pb_history: QPushButton = self.ui.pb_history
        # 生成的按钮
        self.pb_run: QPushButton = self.ui.pb_run
        # 输出文本编辑框
        self.tx_out: QTextEdit = self.ui.tx_out 