from ly.pitch import transpose
from ly.pitch.transpose import ModalTransposer
import re
from PyQt5.QtWidgets import QFileDialog
import subprocess
from abjad import LilyPondFile
from abjad.parsers import parse


class Sheet():
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

    def openFile(self, parent):
        # Get filename from user
        filename, _ = QFileDialog.getOpenFileName(parent, "Open Sheet Music", "", "Lilypond Files (*.ly)")
        if not filename:
            return

        # Load LilyPond file
        with open(filename, 'r') as f:
            lilypond_text = f.read()

        # Parse LilyPond file - tohle je divný
        # lilypond_file = LilyPondFile() #definuje datovej typ
        # lilypond_file = parse.parse(lilypond_text)
        #parse.show(lilypond_file)
        #self.musicEdit.

        parent.musicEdit.setPlainText(lilypond_text)
        # Set widget values
        #self.musicEdit.setPlainText(lilypond_text.items()[0].to_lilypond())