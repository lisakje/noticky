from PyQt5.QtWidgets import QFileDialog
import subprocess
from abjad import LilyPondFile
from abjad.parsers import parse


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