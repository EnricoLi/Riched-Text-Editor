import sys
from PyQt5.QtWidgets import QApplication
from EditorWindow import EditorWindow


app = QApplication(sys.argv)
textEditor = EditorWindow()
sys.exit(app.exec())