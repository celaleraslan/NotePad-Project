from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtPrintSupport import *
import sys, os

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.editor = QPlainTextEdit()  #We create notepads so that we can write on it.
        self.setCentralWidget(self.editor)

        font = QFontDatabase.systemFont(QFontDatabase.FixedFont)   #We do it to set the font
        font.setPointSize(12)
        self.editor.setFont(font)

        self.path = None

        status = QStatusBar()    #at the bottom where the explanations appear
        self.setStatusBar(status)

        toolbar = QToolBar()    #Created place to add shortcuts to our tabs and buttons
        toolbar.setIconSize(QSize(14,14))   #We use it to adjust the size of the added shortcuts buttons.
        self.addToolBar(toolbar)

        menu_bar = QMenuBar()
        menu_bar = self.menuBar()

        file_menu = menu_bar.addMenu("File")
        add_menu = menu_bar.addMenu("Add")

        open_file = QAction(QIcon(os.path.join("open_file.png")), "Open File", self)  #to create an icon to open the file. The png file must be in the folder where the project is located.
        open_file.setStatusTip("Allows You to Open Another Text File On Your NotePad.")  #Shows explanation in statusbar
        open_file.setShortcut("Ctrl+O")
        toolbar.addAction(open_file)  #Adds to toolbar
        file_menu.addAction(open_file)   #Adds to file_menu

        save = QAction(QIcon(os.path.join("save.png")),"Save", self)
        save.setStatusTip("Allows you to save the file you created in txt format.")
        save.setShortcut("Ctrl+S")
        toolbar.addAction(save)
        file_menu.addAction(save)

        save_as = QAction(QIcon(os.path.join("save_as.png")),"Save as", self)
        save_as.setStatusTip("It allows you to save the file we have created wherever we want.")
        toolbar.addAction(save_as)
        file_menu.addAction(save_as)

        print_ = QAction(QIcon(os.path.join("print.png")), "Print", self)
        print_.setStatusTip("It allows you to print the file we created.")
        print_.setShortcut("Ctrl+P")
        toolbar.addAction(print_)
        file_menu.addAction(print_)

        undo = QAction(QIcon(os.path.join("undo.png")), "Undo", self)
        undo.setStatusTip("Allows you to undo the last change you made.")
        undo.setShortcut("Ctrl+Z")
        toolbar.addAction(undo)
        add_menu.addAction(undo)

        redo = QAction(QIcon(os.path.join("redo.png")), "Redo", self)
        redo.setStatusTip("It allows to restore the last change you made.")
        redo.setShortcut("Ctrl+Y")
        toolbar.addAction(redo)
        add_menu.addAction(redo)

        cut = QAction(QIcon(os.path.join("cut.png")), "Cut", self)
        cut.setStatusTip("Allows you to cut the items you select.")
        cut.setShortcut("Ctrl+X")
        toolbar.addAction(cut)
        add_menu.addAction(cut)

        copy = QAction(QIcon(os.path.join("copy.png")), "Copy", self)
        copy.setStatusTip("Allows you to copy the items you have selected.")
        copy.setShortcut("Ctrl+C")
        toolbar.addAction(copy)
        add_menu.addAction(copy)

        paste = QAction(QIcon(os.path.join("paste.png")), "Paste", self)
        paste.setStatusTip("Allows you to paste the item you copied.")
        paste.setShortcut("Ctrl+V")
        toolbar.addAction(paste)
        add_menu.addAction(paste)

        select_all = QAction(QIcon(os.path.join("select_all.png")), "Select all", self)
        select_all.setStatusTip("Selects everything written in the file.")
        select_all.setShortcut("Ctrl+A")
        toolbar.addAction(select_all)
        add_menu.addAction(select_all)

        open_file.triggered.connect(self.open_file_def)
        save.triggered.connect(self.save_def)
        save_as.triggered.connect(self.save_as_def)
        print_.triggered.connect(self.print_def)
        undo.triggered.connect(self.editor.undo)  #There is no need to create functions for them because they are included in the editor.
        redo.triggered.connect(self.editor.redo)
        cut.triggered.connect(self.editor.cut)
        copy.triggered.connect(self.editor.copy)
        paste.triggered.connect(self.editor.paste)
        select_all.triggered.connect(self.editor.selectAll)


        self.update_title()
        self.setGeometry(100,100,500,500)
        self.show()

    def update_title(self):
        self.setWindowTitle("{} - NotePad".format(os.path.basename(self.path) if self.path else "Untitled"))  #We do this to write Untitled

    def error_message(self, message):   #If an error is encountered it returns the error to the user.
        error = QMessageBox()
        error.setText(mesaj)
        error.setIcon(QMessageBox.Critical)
        error.show()

    def open_file_def(self):
        path, _ = QFileDialog.getOpenFileName(self, "Open File", "", "Text Files (*.txt)")

        if path:
            try:
                with open(path, "r") as file:
                    text = file.read()
            except Exception as e:
                self.error_message(e)
            else:
                self.editor.setPlainText(text)
                self.path = path
                self.basligi_guncelle()

    def save_def(self):
        if self.path == None:
            return self.save_as_def()
        text = self.editor.toPlainText()

        try:
            with open(self.path, "w") as file:
                file.write(text)
        except Exception as e:
            self.error_message(e)

    def save_as_def(self):
        path, _= QFileDialog.getSaveFileName(self, "Save As", "", "Text Files(*.txt)")  #we do this to save with filename
        if not path:
            return
        text = self.editor.toPlainText()  #All texts in our editor will be defined to the variable named text.

        try:
            with open(path, "w") as file:
                file.write(text)   #We wrote to the file
        except Exception as e:
            self.error_message(e)
        else:
            self.path = path
            self.update_title()


    def print_def(self):
        message = QPrintDialog()  #It will connect to the print screen on your computer
        if message.exec_():  #if the user pressed the print key
            self.editor.print_(message.printer())


if __name__ == '__main__':    #This means that if the file to be run has the same name as the main file, run the program
    app = QApplication(sys.argv)
    app.setApplicationName("NotePad")

    window = MainWindow()

    app.exec()
