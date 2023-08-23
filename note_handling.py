import sys
#from ly.pitch import transpose
#from ly.pitch.transpose import ModalTransposer
import re
from PyQt5.QtWidgets import QFileDialog, QGraphicsScene, QGraphicsView, QGraphicsPixmapItem
from PyQt5.QtGui import QImage, QPixmap
import subprocess
import pathlib


class Sheet():
    def __init__(self, sheet_music_editor):
        self.sme = sheet_music_editor
        self.filename = None

    def transpose_up(self):
        current_text = self.sme.musicEdit.toPlainText()
    
        list_of_toniny = ["c  ", "cis", "d  ", "dis", "e  ", "f  ", "fis", "g  ", "gis", "a  ", "ais", "h  "]    
        k = False
        for i in list_of_toniny:
            if k:
                current_text[31:33] = i
                k=False
                break
            if current_text[31:33] == i:
                k = True
        if k:
            current_text[31:33] = i
        current_text[29] = list_of_toniny[i] #puvodni tonina (vzdy c)

        self.sme.musicEdit.setPlainText(current_text)

        """with open(self.filename, "r") as f:
            code = f.read
            tonina = ModalTransposer.getKeyIndex(code)
            # operuje s kvintovým kruhem - bacha!
            new_text = transpose(code, 1)
            #self.pitch = transpose.transpose_pitch(self.pitch, "1")
            
            self.sme.musicEdit.setPlainText(new_text)"""

    def transpose_down(self):
        pass
        #self.pitch = transpose.transpose(self.pitch, "-1")


    def add_becko_to_file(self):
        # pridava becko, ale až na konec textu - to je v pohode lol
        with open(self.filename, "r") as f:
            code = f.read()
        
        current_text = self.sme.musicEdit.toPlainText()

        # Add znaminko to music editor
        new_text = current_text[:(-2)] + " " + "es" + current_text[(-2):]

        # Set new text in music editor
        self.sme.musicEdit.setPlainText(new_text)


    def add_krizek_to_file(self):
        current_text = self.sme.musicEdit.toPlainText()

        new_text = current_text[:(-2)] + " " + "is" + current_text[(-2):]

        self.sme.musicEdit.setPlainText(new_text)
        

    def clef_changed(self):
        current_text = self.sme.musicEdit.toPlainText()

        if self.sme.alto_button.isChecked():
            new_text = current_text.replace("bass", "alto")
            new_text = current_text.replace("treble", "alto")
        elif self.sme.bass_button.isChecked():
            new_text = current_text.replace("treble", "bass")
            new_text = current_text.replace("alto", "bass")
        else:
            new_text = current_text.replace("alto", "treble")
            new_text = current_text.replace("bass", "treble")

        self.sme.musicEdit.setPlainText(new_text)


    def add_note_to_file(self, note):
        #oficiálně funguje
        current_text = self.sme.musicEdit.toPlainText()

        # Add note to music editor - v pohodě, protože value tý noty potom dostane v argumetu
        new_text = current_text[:(-4)] + " " + note + current_text[(-4):]

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
            f.write("\\transpose c c {\n")
            f.write("\t\\relative {\n")
            f.write("\t\key c \major\n")
            f.write("\t\clef treble \n")
            f.write("\t }\n")
            f.write("}\n")

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
        # nějak funguje??? (magicky)
        self.saveFile()
        
        pp = pathlib.PurePath(self.filename)
        print(pp.parents[0])
        
        name_of_file = pathlib.PurePath(self.filename)

        subprocess.run([f"lilypond", "--png", name_of_file], capture_output=False)
        p = pathlib.Path(self.filename)
        png_img = str(p.with_suffix(".png"))
        
        image = QImage(png_img)
        item = QGraphicsPixmapItem(
            QPixmap.fromImage(image))
        scene = QGraphicsScene()
        scene.addItem(item)
        
        self.sme.graphicsView.setScene(scene)


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