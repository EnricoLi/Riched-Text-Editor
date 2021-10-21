from Texteditor import Ui_Text_Editor_Rich
from PyQt5 import QtWidgets, QtGui, QtCore
from PyQt5.QtWidgets import QFileDialog, QMessageBox, QFontDialog, QColorDialog
from PyQt5.QtPrintSupport import QPrinter, QPrintDialog, QPrintPreviewDialog
from PyQt5.QtCore import QFileInfo, Qt
from PyQt5.QtGui import QFont


class EditorWindow(QtWidgets.QMainWindow, Ui_Text_Editor_Rich):
    def __init__(self):
        super().__init__()
        self.setupUi(self)

        self.actionNew.triggered.connect(self.fileNew)
        self.actionOpen.triggered.connect(self.openFile)
        self.actionSave.triggered.connect(self.fileSave)
        self.actionPrint.triggered.connect(self.printFile)
        self.actionPrint_Preview.triggered.connect(self.printPreview)
        self.actionExport_PDF.triggered.connect(self.exportPdf)
        self.actionExit.triggered.connect(self.close)
        self.actionCopy.triggered.connect(self.copy)
        self.actionPaste.triggered.connect(self.paste)
        self.actionCut.triggered.connect(self.cut)
        self.actionUndo.triggered.connect(self.textEdit.undo)
        self.actionRedo.triggered.connect(self.textEdit.redo)
        self.actionFont.triggered.connect(self.fontDialog)
        self.actionColor.triggered.connect(self.colorDialog)
        self.actionBold.triggered.connect(self.textBold)
        self.actionItalic.triggered.connect(self.textItalic)
        self.actionUnderline.triggered.connect(self.textUnderline)
        self.actionLeft.triggered.connect(self.alignLeft)
        self.actionCenter.triggered.connect(self.alignCenter)
        self.actionRight.triggered.connect(self.alignRight)
        self.actionJustify.triggered.connect(self.justify)
        self.actionText_Highlight.triggered.connect(self.change_color)

        self.show()

    def fileNew(self):
        self.textEdit.clear()

    def openFile(self):
        filename = QtWidgets.QFileDialog.getOpenFileName(self, "Open File", "C:\\")
        print(filename)

        if filename[0]:
            fileopen = open(filename[0], 'r')

            with fileopen:
                data = fileopen.read()
                self.textEdit.setText(data)
    
    def fileSave(self):
        filename = QtWidgets.QFileDialog.getSaveFileName(self, "Save File")

        if filename[0]:
            filesave = open(filename[0], "w")

            with filesave:
                text = self.textEdit.toPlainText()
                filesave.write(text)

                QMessageBox.about(self, "Save File", "File Saved Successfully")
    
    def printFile(self):
        printer = QPrinter(QPrinter.HighResolution)
        dialog = QPrintDialog(printer, self)

        if dialog.exec_() == QPrintDialog.Accepted:
            self.textEdit.print_(printer)

    def printPreview(self):
        printer = QPrinter(QPrinter.HighResolution)
        previewDialog = QPrintPreviewDialog(printer, self)
        previewDialog.paintRequested.connect(self.printView)
        previewDialog.exec_()
    
    def printView(self, printer):
        self.textEdit.print_(printer)
    
    def exportPdf(self):
        fn, _ = QFileDialog.getSaveFileName(self, "Export PDF", None, 
        "PDF files (* .pdf) ;; All Files")
        if fn != "":
            if QFileInfo(fn).suffix() == "" :fn += '.pdf'
            printer = QPrinter(QPrinter.HighResolution)
            printer.setOutputFormat(QPrinter.PdfFormat)
            printer.setOutputFileName(fn)
            self.textEdit.document().print_(printer)
    
    def copy(self):
        cursor = self.textEdit.textCursor()
        textSelected = cursor.selectedText()
        self.copiedText = textSelected
    
    def paste(self):
        try:
            self.textEdit.append(self.copiedText)
        except AttributeError:
            pass
    
    def cut(self):
        cursor = self.textEdit.textCursor()
        textSelected = cursor.selectedText()
        self.copiedText = textSelected
        self.textEdit.cut()

    def fontDialog(self):
        font, ok = QFontDialog.getFont ()

        if ok:
            self.textEdit.setFont(font)

    def colorDialog(self):
        color = QColorDialog.getColor()
        self.textEdit.setTextColor(color)
    
    def textBold(self):
        font = QFont()
        font.setBold(True)
        self.textEdit.setFont(font)

    def textItalic(self):
        font = QFont()
        font.setItalic(True)
        self.textEdit.setFont(font)

    def textUnderline(self):
        font = QFont()
        font.setUnderline(True)
        self.textEdit.setFont(font)

    def alignLeft(self):
        self.textEdit.setAlignment(Qt.AlignLeft)
    
    def alignCenter(self):
        self.textEdit.setAlignment(Qt.AlignCenter)

    def alignRight(self):
        self.textEdit.setAlignment(Qt.AlignRight)

    def justify(self):
        self.textEdit.setAlignment(Qt.AlignJustify)

    def change_color(self):
        cursor = self.textEdit.textCursor()
        
        if cursor.hasSelection():
            fmt = QtGui.QTextCharFormat()
            fmt.setBackground(QtCore.Qt.yellow)
            cursor.setCharFormat(fmt)
