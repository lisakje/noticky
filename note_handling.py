from ly.pitch import transpose
from ly.pitch.transpose import ModalTransposer
import re
from PyQt5.QtWidgets import QFileDialog
import subprocess
#from abjad import LilyPondFile
#from abjad.parsers import parse


class Sheet():
    def __init__(self, sheet_music_editor):
        self.sme = sheet_music_editor
        self.filename = None

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
        current_text = self.sme.musicEdit.toPlainText()

        # Add znaminko to music editor
        new_text = current_text.rstrip() + "{ \\flat }" + " "

        # Set new text in music editor
        self.sme.musicEdit.setPlainText(new_text)

    def add_krizek_to_file(self):
        # Get current text in music editor
        current_text = self.sme.musicEdit.toPlainText()

        # Add znaminko to music editor
        new_text = current_text.rstrip() + "{ \sharp }" + " "

        # Set new text in music editor
        self.sme.musicEdit.setPlainText(new_text)


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

    def saveFile(self):
        #oficiálně funguje
        current_text = self.sme.musicEdit.toPlainText()

        if self.filename is None:
            self.filename, _ = QFileDialog.getSaveFileName(self.sme, "Save Sheet Music", "", "Lilypond Files (*.ly)")
        else:
            pass
            #když existuje stejný jméno, tak to zakřičí  
        if not self.filename:
            return    

        with open(self.filename, 'w') as f:
            f.write(current_text)

    def create_new_file(self):
        # oficiálně funguje
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

        with open("new_file.ly", 'r') as f:
            lilypond_text = f.read()

        self.sme.musicEdit.setPlainText(lilypond_text)

    def refresh_sheet(self):
        self.saveFile()
        # protože filename existuje, tak to prostě nic nedělá
        
        png_file = subprocess.check_output([f"{self.filename} --png"])

        # myslím, že jí chybí dání té instrukce "teď tu věc pojmenuj takhle (v našem připadě "nazev.ly" --> "nazev.png")"

        self.sme.graphicsView.addItem(png_file)

    def openFile(self):
        #tohle oficiálně funguje - pdfko ale nezobrazí - to je všechno podle plánu
        # Get filename from user
        self.filename, _ = QFileDialog.getOpenFileName(self.sme, "Open Sheet Music", "", "Lilypond Files (*.ly)")
        if not self.filename:
            return

        # Load LilyPond file
        with open(self.filename, 'r') as f:
            lilypond_text = f.read()
        
        #lilypond_file = LilyPondFile()
        #lilypond_file = parse.parse(lilypond_text)
        #parse.show(lilypond_file)

        self.sme.musicEdit.setPlainText(lilypond_text)
        # Set widget values
        #self.sme.musicEdit.setPlainText(lilypond_text.items()[0].to_lilypond())