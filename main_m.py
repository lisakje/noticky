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
    
    def transpose_up(self):
        with open("new_file.ly", "r") as f:
            code = f.read
            #transponitko = ModalTransposer(7, 0)
            tonina = ModalTransposer.getKeyIndex(f)
            transpose(tonina)
        
        with open("new_file.ly", "r") as f:
            f.write(code)
            #self.pitch = transpose.transpose_pitch(self.pitch, "1")

    def transpose_down(self):
        self.pitch = transpose.transpose_pitch(self.pitch, "-1")


    def add_becko_to_file(self):
        with open("new_file.ly", "r") as f:
            code = f.read()
        
        # Get current text in music editor
        current_text = self.musicEdit.toPlainText()

        # Add znaminko to music editor
        new_text = current_text.rstrip() + "{ \\flat }" + " "

        # Set new text in music editor
        self.musicEdit.setPlainText(new_text)

    def add_krizek_to_file(self):
        # Get current text in music editor
        current_text = self.musicEdit.toPlainText()

        # Add znaminko to music editor
        new_text = current_text.rstrip() + "{ \sharp }" + " "

        # Set new text in music editor
        self.musicEdit.setPlainText(new_text)
    

    def bpm_changed(slider_val, self):
        bpm = slider_val
        with open("new_file.ly", "r+") as file:
            data = file.read()
            file.seek(0)
            file.truncate()
            parameter = f"\\override Score.MetronomeMark #'stencil = ##f \\override Score.MetronomeMark #'break-visibility = ##(#f #f #f) \\tempo {bpm}"
            data = re.sub(r'\\override Score\.MetronomeMark #\'stencil = ##f \\override Score\.MetronomeMark #\'break-visibility = ##\(#f #f #f\) \\tempo \d+', parameter, data)
            file.write(data)
     

    def clef_changed(self):
        if self.alto_button.isChecked():
            clef = 'alto'
        elif self.bass_button.isChecked():
            clef = 'bass'
        else:
            clef = 'treble'
        
        with open("new_file.ly", "r") as f:
            code = f.read()
        
         # Replace the clef in the LilyPond code
        code = re.sub(r'\\clef\s+\w+', f'\\clef {clef}', code)

        # Write the modified LilyPond code to a new file
        with open("new_file.ly", "w") as f:
            f.write(code)


    def add_note_to_file(self, note):
        with open("new_file.ly", "r") as f:
            code = f.read()
        # Get current text in music editor

        # Add note to music editor - v pohodě, protože value tý noty potom dostane v argumetu
        new_text = code + note + " "

        # Set new text in music editor
        with open("new_file.ly", "w") as f:
            f.write(new_text)

    def create_new_file(self):
        # Get filename from user
        filename, _ = QFileDialog.getSaveFileName(self, "Save Sheet Music", "", "Lilypond Files (*.ly)")
        if not filename:
            return

        #text = self.fileTitle.text()
        #self.musicEdit.setDocumentTitle(text)

        with open("new_file.ly", "w") as f:
            f.write("\\version \"2.18.2\"\n\n")
            #f.write(f"\\clef {self.clef}\n")
            f.write("\\header {\n")
            f.write("\ttitle = \"Untitled\"\n")
            f.write("}\n\n")
            f.write("\\score {\n")
            f.write("\t\\new Staff { }\n")
            f.write("\t\\layout { }\n")
            f.write("}\n")
            #self.pitch = Pitch("c'")

    def saveFile(self):
        #oficiálně funguje
        current_text = self.musicEdit.toPlainText()
        filename, _ = QFileDialog.getSaveFileName(self, "Save Sheet Music", "", "Lilypond Files (*.ly)")
        if not filename:
            return    
        #když existuje stejný jméno, tak to zakřičí  

        with open(filename, 'w') as f:
            f.write(current_text)

    def refresh_sheet(self):
        #tohle musí jít udělat líp než jenom paste saveFile - probrat s Borkem
        #oficiálně funguje
        current_text = self.musicEdit.toPlainText()
        filename, _ = QFileDialog.getSaveFileName(self, "Save Sheet Music", "", "Lilypond Files (*.ly)")
        if not filename:
            return    
        #když existuje stejný jméno, tak to zakřičí  

        with open(filename, 'w') as f:
            f.write(current_text)
        
        pdf_file = subprocess.check_output([f"{filename} --pdf"])

        self.graphicsView.addItem(pdf_file)

    def openFile(self):
        # Get filename from user
        filename, _ = QFileDialog.getOpenFileName(self, "Open Sheet Music", "", "Lilypond Files (*.ly)")
        if not filename:
            return

        # Load LilyPond file
        with open(filename, 'r') as f:
            lilypond_text = f.read()

        # Parse LilyPond file - tohle je divný
        lilypond_file = LilyPondFile() #definuje datovej typ
        lilypond_file = parse.parse(lilypond_text)
        #parse.show(lilypond_file)
        #self.musicEdit.

        self.graphicsView.addItem(lilypond_file)
        # Set widget values
        #self.musicEdit.setPlainText(lilypond_text.items()[0].to_lilypond())

if __name__ == '__main__':
    app = QApplication(sys.argv)
    editor = SheetMusicEditor()
    editor.show()
    sys.exit(app.exec())