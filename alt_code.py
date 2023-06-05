import sys
sys.path.append('/home/lida/Downloads/lilypond-2.24.1/python')
from PyQt5 import uic
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QTextEdit, QPushButton, QFileDialog, QVBoxLayout
#from lilypond import LilyPondFile, LilyPondFormat
from ly import *

class SheetMusicEditor(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()
        uic.loadUi("klikatko.ui", self)
        self.show()

    def initUI(self):
        # Create widgets
        self.titleLabel = QLabel("Title:", self)
        self.titleEdit = QTextEdit(self)
        self.musicLabel = QLabel("Sheet Music:", self)
        self.musicEdit = QTextEdit(self)
        self.saveButton = QPushButton("Save", self)
        self.saveButton.clicked.connect(self.saveFile)
        self.openButton = QPushButton("Open", self)
        self.openButton.clicked.connect(self.openFile)

        # Set widget properties
        self.musicEdit.setAcceptRichText(False)

        # Create layout
        layout = QVBoxLayout()
        layout.addWidget(self.titleLabel)
        layout.addWidget(self.titleEdit)
        layout.addWidget(self.musicLabel)
        layout.addWidget(self.musicEdit)
        layout.addWidget(self.saveButton)
        layout.addWidget(self.openButton)

        # Set window properties
        self.setLayout(layout)
        self.setWindowTitle("Sheet Music Editor")
        self.setGeometry(100, 100, 400, 400)

    def saveFile(self):
        # Get filename from user
        filename, _ = QFileDialog.getSaveFileName(self, "Save Sheet Music", "", "Lilypond Files (*.ly)")
        if not filename:
            return

        # Create LilyPond file
        lilypond_file = LilyPondFile()
        lilypond_file.header_title = self.titleEdit.toPlainText()
        lilypond_file.add_item(self.musicEdit.toPlainText())

        # Save LilyPond file
        lilypond_format = LilyPondFormat()
        with open(filename, 'w') as f:
            f.write(lilypond_format(lilypond_file))

    def openFile(self):
        # Get filename from user
        filename, _ = QFileDialog.getOpenFileName(self, "Open Sheet Music", "", "Lilypond Files (*.ly)")
        if not filename:
            return

        # Load LilyPond file
        with open(filename, 'r') as f:
            lilypond_text = f.read()

        # Parse LilyPond file
        lilypond_file = LilyPondFile()
        lilypond_file.parse(lilypond_text)

        # Set widget values
        self.titleEdit.setPlainText(lilypond_file.header_title)
        self.musicEdit.setPlainText(lilypond_file.items()[0].to_lilypond())

if __name__ == '__main__':
    app = QApplication(sys.argv)
    editor = SheetMusicEditor()
    editor.show()
    sys.exit(app.exec_())