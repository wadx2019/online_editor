import PyQt5.Qsci as Qsci
import PyQt5.QtGui as QtGui
from PyQt5.QtCore import Qt

class CodeWidget(Qsci.QsciScintilla):

    def __init__(self):
        super().__init__()
        self.setEolMode(self.SC_EOL_LF)    # 以\n换行
        self.setWrapMode(self.WrapWord)    # 自动换行。self.WrapWord是父类QsciScintilla的
        self.setAutoCompletionSource(self.AcsAll)  # 自动补全。对于所有Ascii字符
        self.setAutoCompletionCaseSensitivity(False)  # 自动补全大小写敏感
        self.setAutoCompletionThreshold(3)  # 输入多少个字符才弹出补全提示
        self.setFolding(True)  # 代码可折叠
        self.setFont(QtGui.QFont('Consolas', 12))  # 设置默认字体
        self.setCaretLineVisible(True) #突出显示当前行
        self.setMarginType(1, self.NumberMargin)    # 0~4。第0个左边栏显示行号
        self.setMarginLineNumbers(0, True)  # 我也不知道
        self.setTabWidth(4) #\t=4
        # self.setMarginsBackgroundColor(QtGui.QColor(120, 220, 180))  # 边栏背景颜色
        # self.setMarginWidth(0, 30)  # 边栏宽度
        self.setAutoIndent(True)  # 换行后自动缩进
        self.setUtf8(True)  # 支持中文字符
        # 开启自动缩进
        # editor->setAutoIndent(true);
        # // 设置缩进的显示方式
        # editor->setIndentationGuides(QsciScintilla::SC_IV_LOOKBOTH);
        # // 显示选中的行号
        # editor->setCaretLineVisible(true);
        # // 显示选中行号的背景色
        self.setCaretLineBackgroundColor(Qt.lightGray)
        # // 左侧行号显示的背景色
        # self.setMarginsBackgroundColor(Qt::gray);
        # // 设置括号匹配
        # self.setBraceMatching(Qsci.SloppyBraceMatch)

        self.set_Lexer()

    def set_Lexer(self,type=2):  #设置解释器
        dic={
            0:Qsci.QsciLexerBash(),
            1:Qsci.QsciLexerCPP(),
            2:Qsci.QsciLexerPython(),
            3:Qsci.QsciLexerJava(),

        }
        textLexer=dic[type]
        # textLexer->setColor(QColor(Qt:: yellow), QsciLexerCPP::CommentLine); // 设置自带的注释行为绿色
        self.setLexer(textLexer)


