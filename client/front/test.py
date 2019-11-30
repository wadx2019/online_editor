import os,sys,CodeWidget
import PyQt5.Qsci
from PyQt5.QtWidgets import QApplication,QWidget,QHBoxLayout,QMenuBar,QMenu,QAction,QMainWindow,QFileDialog,QTabWidget
from PyQt5.QtGui import QDesktopServices
from PyQt5.QtCore import QUrl


class MainWindow(QMainWindow):

    def __init__(self,parent=None):
        super(MainWindow,self).__init__(parent)
        self.setWindowTitle("代码编辑器")
        self.setMinimumSize(600,800)
        self.tab=QTabWidget()
        self.tab.setTabsClosable(True)
        self.tab.tabCloseRequested.connect(self.tab.removeTab)
        self.files=[]
        self.editors=[]
        self.addNewTab()
        self.setCentralWidget(self.tab)
        self.menuBar=self.menuBar()
        self.init_MenuBar()
    def addNewTab(self):
        editor = CodeWidget.CodeWidget()
        self.editors.append(editor)
        self.tab.addTab(editor, "未命名")
        self.files.append("-0-")
        return editor
    def init_MenuBar(self):#初始化菜单
        self.fileMenu = self.menuBar.addMenu("文件 (&F)")
        self.editMenu = self.menuBar.addMenu("编辑 (&E)")
        self.toolMenu = self.menuBar.addMenu("工具 (&T)")
        self.helpMenu = self.menuBar.addMenu("帮助 (&H)")
        self.init_Action()

    def init_Action(self):
        #文件菜单
        openFile=QAction("打开",self)
        self.fileMenu.addAction(openFile)
        openFile.triggered.connect(self.openFile)
        newFile = QAction('新建', self)
        newFile.setShortcut('Ctrl+N')
        newFile.triggered.connect(self.addNewTab)
        self.fileMenu.addAction(newFile)
        saveFile = QAction('保存', self)
        saveFile.setShortcut('Ctrl+S')
        saveFile.triggered.connect(self.saveFile)
        self.fileMenu.addAction(saveFile)
        exitWin=QAction("退出",self)
        self.fileMenu.addAction(exitWin)
        exitWin.triggered.connect(self.exitWindow)
        #编辑菜单
        copy = QAction("复制",self)
        copy.setShortcut("Ctrl+C")
        self.editMenu.addAction(copy)
        cut =QAction("剪切",self)
        cut.setShortcut("Ctrl+X")
        self.editMenu.addAction(cut)
        paste=QAction("粘贴",self)
        paste.setShortcut("Ctrl+V")
        self.editMenu.addAction(paste)
        #工具菜单
        option=QAction("选项",self)
        self.toolMenu.addAction(option)
        language=QMenu("语言",self)
        self.toolMenu.addMenu(language)

        bash=QAction("Bash",self)
        bash.triggered.connect(self.chgBashLexer)
        cpp=QAction("C++",self)
        cpp.triggered.connect(self.chgCppLexer)
        py=QAction("Python",self)
        py.triggered.connect(self.chgPyLexer)
        java=QAction("Java",self)
        java.triggered.connect(self.chgJavaLexer)
        language.addActions([bash,cpp,py,java])

        #帮助菜单
        help=QAction("使用教程",self)
        self.helpMenu.addAction(help)
        knowUs=QAction("了解我们",self)
        self.helpMenu.addAction(knowUs)
        knowUs.triggered.connect(self.openUrl)

    def chgCppLexer(self):
        self.editors[self.tab.currentIndex()].set_Lexer(1)

    def chgBashLexer(self):
        self.editors[self.tab.currentIndex()].set_Lexer(0)

    def chgPyLexer(self):
        self.editors[self.tab.currentIndex()].set_Lexer(2)

    def chgJavaLexer(self):
        self.editors[self.tab.currentIndex()].set_Lexer(3)
    def openUrl(self):
        QDesktopServices.openUrl(QUrl("https://github.com/SheepHuan/online_editor"))
    # def chgLexer(self,type=1):
    #     self.editors[self.tab.currentIndex()].set_Lexer(type)
    def saveFile(self):
        filePath=self.files[self.tab.currentIndex()]
        if filePath=="-0-":#表示未命名文件
            filePath = QFileDialog.getSaveFileName(self, '保存文件')
            self.files[self.tab.currentIndex()]=filePath[0]
            self.tab.setTabText(self.tab.currentIndex(),filePath[0].split("/")[-1])
            with open(filePath[0], 'w') as f:
                my_text = self.editors[self.tab.currentIndex()].text()
                f.write(my_text)
        else:
            with open(filePath, 'w') as f:
                my_text = self.editors[self.tab.currentIndex()].text()
                f.write(my_text)
    def openFile(self):
        fileUrl = QFileDialog.getOpenFileName(self)
        try:
            if fileUrl:
                filePath = fileUrl[0]
                self.files.append(filePath)
                with open(filePath,"r") as f:
                    lines=f.readlines()
                text=""
                for line in lines:
                    text+=line
                print(text)
                self.editors[self.tab.currentIndex()].setText(text)
        except Exception as e:
            print(e)
    def exitWindow(self):
        self.close()

if __name__=="__main__":
    app = QApplication(sys.argv)
    win = MainWindow()
    win.show()
    sys.exit(app.exec_())