import sys
from ly.pitch import transpose
from ly.pitch.transpose import ModalTransposer
import re
from PyQt5.QtWidgets import QFileDialog
import subprocess
import fitz
#from abjad import LilyPondFile
#from abjad.parsers import parse


class Sheet():
    def __init__(self, sheet_music_editor):
        self.sme = sheet_music_editor
        self.filename = None

    def transpose_up(self):
            with open(self.filename, "r") as f:
                code = f.read
                #transponitko = ModalTransposer(7, 0)
                tonina = ModalTransposer.getKeyIndex(f)
                transpose(tonina)
            
            with open(self.filename, "r") as f:
                f.write(code)
                #self.pitch = transpose.transpose_pitch(self.pitch, "1")

    def transpose_down(self):
        self.pitch = transpose.transpose_pitch(self.pitch, "-1")


    def add_becko_to_file(self):
        # pridava becko, ale až na konec textu
        with open(self.filename, "r") as f:
            code = f.read()
        
        current_text = self.sme.musicEdit.toPlainText()

        # Add znaminko to music editor
        new_text = current_text.rstrip() + "es" + " "

        # Set new text in music editor
        self.sme.musicEdit.setPlainText(new_text)

    def add_krizek_to_file(self):
        # Get current text in music editor
        current_text = self.sme.musicEdit.toPlainText()

        # Add znaminko to music editor
        new_text = current_text.rstrip() + "is" + " "

        # Set new text in music editor
        self.sme.musicEdit.setPlainText(new_text)


    def bpm_changed(slider_val, self):
        bpm = slider_val
        with open(self.filename, "r+") as file:
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
        
        with open(self.filename, "r") as f:
            code = f.read()
        
            # Replace the clef in the LilyPond code
        code = re.sub(r'\\clef\s+\w+', f'\\clef {clef}', code)

        # Write the modified LilyPond code to a new file
        with open(self.filename, "w") as f:
            f.write(code)


    def add_note_to_file(self, note):
        current_text = self.sme.musicEdit.toPlainText()

        # Add note to music editor - v pohodě, protože value tý noty potom dostane v argumetu
        new_text = current_text.rstrip() + " " + note

        self.sme.musicEdit.setPlainText(new_text)


    def title_changed(self):
        #tady to prijme ten vstup
        new_title = self.titleName.textChanged(self)

        with open(self.filename, "r") as f:
            code = f.read()

            clear_code = code.rstrip()
            
            position = clear_code.rfind("title = ") #nevim jestli takhle outputuje?
            new_text = clear_code[:position] + new_title + clear_code[position + 1:]
        
        with open(self.filename, "w") as f:
            f.write(new_text)

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

    def saveFile(self):
            #oficiálně funguje na nový i existující věci
            current_text = self.sme.musicEdit.toPlainText()

            if self.filename is None:
                self.filename, _ = QFileDialog.getSaveFileName(self.sme, "Save Sheet Music", "", "Lilypond Files (*.ly)")
                #TO-DO když existuje stejný jméno, tak to zakřičí
            if not self.filename:
                return    

            with open(self.filename, 'w') as f:
                f.write(current_text)

    def refresh_sheet(self):
        #snad napsané skoro funkčně, zeptat se požára
        self.saveFile()
        
        subprocess.run(["cd ~/noticky/aut"])
        subprocess.run([f"lilypond {self.filename}"])
        #TODO s borkem přepsat tak, aby filename bylo actually jenom filename (edit: nejsem si tak jistá, že to actually vadí)

        doc = fitz.open(self.filename)
        png_page_list = []
        for i, page in enumerate(doc):
            pix = page.get_pixmap()  # render page to an image
            for i in doc:
                another_page = pix.save(f"{self.filename}_page_{i}.png")
                png_page_list.append(another_page)

        self.sme.graphicsView.addItem(png_page_list)

    def openFile(self):
        #tohle oficiálně funguje - pdfko ale nezobrazí - to je všechno podle plánu
        # Get filename from user
        self.filename, _ = QFileDialog.getOpenFileName(self.sme, "Open Sheet Music", "", "Lilypond Files (*.ly)")
        if not self.filename:
            return

        # Load LilyPond file
        with open(self.filename, 'r') as f:
            lilypond_text = f.read()

        self.sme.musicEdit.setPlainText(lilypond_text)

    def closeEvent(self):
        sys.exit(0)