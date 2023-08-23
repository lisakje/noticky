import sys
import os
sys.path.append('/home/lida/Downloads/lilypond-2.24.1/python')
from PyQt5.QtWidgets import *
from PyQt5.QtCore import Qt, QThread, pyqtSignal
from PyQt5.QtGui import QPixmap
from PyQt5 import uic
from ly import *
import ly.document
import ly.music

from note_handling import Sheet

class ojojError(QWidget):
    def __init__(self):
        QWidget.__init__(self)
        uic.loadUi(os.path.normpath(os.path.join(__file__, "..", "ojoj.ui")), self)

class SheetMusicEditor(QDialog):
    def __init__(self):
        sheet = Sheet(sheet_music_editor=self)
        super(SheetMusicEditor, self).__init__()
        uic.loadUi(os.path.normpath(os.path.join(__file__, "..", "main_ui.ui")), self)

        self.show()

        self.pushButton.clicked.connect(sheet.transpose_up)
        self.pushButton_2.clicked.connect(sheet.transpose_down)
        self.krizek_button.clicked.connect(sheet.add_krizek_to_file)
        self.becko_button.clicked.connect(sheet.add_becko_to_file)
        self.treble_button.setChecked(True)
        self.treble_button.toggled.connect(sheet.clef_changed)
        self.alto_button.toggled.connect(sheet.clef_changed)
        self.bass_button.toggled.connect(sheet.clef_changed)

        self.save_button.clicked.connect(sheet.saveFile)
        self.openFile_button.clicked.connect(sheet.openFile)
        self.new_file_button.clicked.connect(sheet.create_new_file)
        self.refresh_button.clicked.connect(sheet.refresh_sheet)

        self.c_button.clicked.connect(lambda: sheet.add_note_to_file("c'"))
        self.d_button.clicked.connect(lambda: sheet.add_note_to_file("d'"))
        self.e_button.clicked.connect(lambda: sheet.add_note_to_file("e'"))
        self.f_button.clicked.connect(lambda: sheet.add_note_to_file("f'"))
        self.g_button.clicked.connect(lambda: sheet.add_note_to_file("g'"))
        self.a_button.clicked.connect(lambda: sheet.add_note_to_file("a'"))
        self.b_button.clicked.connect(lambda: sheet.add_note_to_file("b'"))

        #self.actionClose.triggered.connect(exit)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    editor = SheetMusicEditor()
    editor.show()
    sys.exit(app.exec())