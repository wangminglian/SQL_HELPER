# UI美化需求文档

## 功能描述
对主界面进行美化，提升用户体验，保持原有布局不变。

## 实现方案
### 1. 界面美化
- **背景色**: 采用淡青色 (#e0f7fa) 作为主背景色，营造清新的视觉效果
- **按钮样式**: 
  - 默认状态：蓝色背景 (#0288d1)，白色文字
  - 悬停状态：白色背景，蓝色边框，提供交互反馈
  - 统一的内边距和字体大小，保持一致性
- **文本组件**: 
  - 标签文字：深灰色 (#333)，字体大小14px
  - 输入框和下拉框：白色背景，浅灰色边框
  - 文本编辑器：白色背景，浅灰色边框

### 2. 技术实现
- 使用 QStyleSheet 进行样式设置
- 在 setupUi() 方法中添加样式代码
- 保持原有组件布局和功能不变

## 实现效果
- 界面更加美观，色彩搭配和谐
- 按钮具有良好的交互反馈
- 整体风格统一，提升专业感

## 文件修改
- `clinet/main_ui.py`: 添加 CSS 样式设置代码

## 注释说明
```python
# 添加美化样式 - 为主窗口设置CSS样式
MainWindow.setStyleSheet("""
    QWidget {
        background-color: #e0f7fa;  # 设置整体背景色为淡青色
        color: #333;                # 设置文字颜色为深灰色
    }
    QPushButton {
        background-color: #0288d1;  # 按钮背景色为蓝色
        color: white;               # 按钮文字为白色
        border: none;               # 去除边框
        padding: 5px 10px;          # 设置内边距
        text-align: center;         # 文字居中
        font-size: 16px;            # 字体大小
        margin: 4px 2px;            # 外边距
    }
    QPushButton:hover {
        background-color: white;    # 悬停时背景变白
        color: black;               # 悬停时文字变黑
        border: 2px solid #0288d1;  # 悬停时添加蓝色边框
    }
    QLabel {
        font-size: 14px;            # 标签字体大小
        color: #333;                # 标签文字颜色
    }
    QLineEdit, QComboBox {
        background-color: white;    # 输入框背景色
        color: #333;                # 输入框文字颜色
        border: 1px solid #ccc;     # 输入框边框
        padding: 5px;               # 输入框内边距
    }
    QTextEdit, QTextBrowser {
        background-color: white;    # 文本编辑器背景色
        color: #333;                # 文本编辑器文字颜色
        border: 1px solid #ccc;     # 文本编辑器边框
    }
""")
``` 