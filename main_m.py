import sys
import os
sys.path.append('/home/lida/Downloads/lilypond-2.24.1/python')
from PyQt5.QtWidgets import *
from PyQt5.QtCore import Qt, QThread, pyqtSignal
from PyQt5.QtGui import QPixmap
from PyQt5 import uic
import keyboard
from ly import *
import ly.document
import ly.music
#import ly.cli.command
#import ly.cli.main
from ly.pitch import transpose
from ly.pitch.transpose import ModalTransposer
from abjad import LilyPondFile, Note
from abjad.parsers import parse
from abjad.pitch import NamedPitch
import re
import subprocess

from note_handling import *
from file_handling import *

class SheetMusicEditor(QDialog):
    class KeyboardListener(QThread):
        note_added = pyqtSignal(str)

        def __init__(self, parent=None):
            super().__init__(parent=parent)
            self.key_to_note = {
                "c": NamedPitch("c'"),
                "d": NamedPitch("d'"),
                "e": NamedPitch("e'"),
                "f": NamedPitch("f'"),
                "g": NamedPitch("g'"),
                "a": NamedPitch("a'"),
                "b": NamedPitch("b'"),
            }

    def run(self):
        while True:
            key = keyboard.read_event().name
            if key in self.key_to_note:
                note = Note.from_pitch(self.key_to_note[key])
                self.note_added.emit(note.to_lilypond() + "")

    def __init__(self):
        super(SheetMusicEditor, self).__init__()
        #uic.loadUi("qtdesigner_zkouska.ui", self)
        uic.loadUi(os.path.normpath(os.path.join(__file__, "..", "qtdesigner_zkouska.ui")), self)

        self.keyboard_listener = self.KeyboardListener()
        self.keyboard_listener.note_added.connect(self.add_note_to_file)
        self.keyboard_listener.start()

        self.show()
        
        self.pushButton.clicked.connect(self.transpose_up)
        self.pushButton_2.clicked.connect(self.transpose_down)
        self.krizek_button.clicked.connect(self.add_krizek_to_file)
        self.becko_button.clicked.connect(self.add_becko_to_file)
        self.treble_button.setChecked(True)
        self.treble_button.toggled.connect(self.clef_changed)
        self.alto_button.toggled.connect(self.clef_changed)
        self.bass_button.toggled.connect(self.clef_changed)

        #self.pushButton_3.clicked.connect(self.make_big)
        #self.pushButton_4.clicked.connect(self.make_small)
        self.save_button.clicked.connect(self.saveFile)
        self.openFile_button.clicked.connect(self.openFile)
        self.new_file_button.clicked.connect(self.create_new_file)
        self.refresh_button.clicked.connect(self.refresh_sheet)

        self.c_button.clicked.connect(lambda: self.add_note_to_file("c'"))
        self.d_button.clicked.connect(lambda: self.add_note_to_file("d'"))
        self.e_button.clicked.connect(lambda: self.add_note_to_file("e'"))
        self.f_button.clicked.connect(lambda: self.add_note_to_file("f'"))
        self.g_button.clicked.connect(lambda: self.add_note_to_file("g'"))
        self.a_button.clicked.connect(lambda: self.add_note_to_file("a'"))
        self.b_button.clicked.connect(lambda: self.add_note_to_file("b'"))

        self.bpm_slider = QSlider(Qt.Horizontal)
        self.bpm_slider.setMinimum(1)
        self.bpm_slider.setMaximum(10000)
        self.bpm_slider.setSingleStep(5)
        self.bpm_slider.setValue(120)
        self.bpm_slider.setTickInterval(30)
        self.bpm_slider.setTickPosition(QSlider.TicksBelow)
        self.bpm_slider.valueChanged.connect(self.bpm_changed)
        #self.horizontalLayout_2.addWidget(self.bpm_slider)

        #self.actionClose.triggered.connect(exit)
    

if __name__ == '__main__':
    app = QApplication(sys.argv)
    editor = SheetMusicEditor()
    editor.show()
    sys.exit(app.exec())