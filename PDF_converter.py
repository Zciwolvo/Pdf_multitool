#author Igor Gawlowicz
#version=0.8

from PIL import Image
from PIL import UnidentifiedImageError
from tkinter import Tk
import tkinter as tk
from tkinter.messagebox import showinfo
from tkinter import filedialog
from tkinter import Label
from PyPDF2 import PdfFileMerger
from PyPDF2 import PdfFileWriter
from PyPDF2 import PdfFileReader
from PyPDF2.utils import PdfReadError
import os
from fpdf import FPDF


class Application(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.master = master
        self.pack()
        self.create_widgets()



#===============================================MENU===================================================================================================================



    def create_widgets(self):
        convert_to_pdf_button = tk.Button(root, text="Konwertuj pliki", command=self.pdf_converter)
        convert_to_pdf_button.pack(fill='x')

        split_compress_pdf_button = tk.Button(root, text="Kompresuj pliki pdf", command=self.pdf_compressor)
        split_compress_pdf_button.pack(fill='x')

        split_pdf_button = tk.Button(root, text="Rozdziel pliki pdf", command=self.pdf_splitter)
        split_pdf_button.pack(fill='x')

        merge_pdf_button = tk.Button(root, text="Złącz pliki pdf", command=self.pdf_merger)
        merge_pdf_button.pack(fill='x')

        button_bonus = tk.Button(root, text="Info", command=self.info)
        button_bonus.pack(fill='x')

        exit_button = tk.Button(root, text="Wyjdź", command=self.master.destroy)
        exit_button.pack(fill='x')


        self.author = Label(text = "©Igor Gawłowicz")
        self.author.pack(side="bottom")

        self.author_contact = Label(text = "igor.gawlowicz@gmail.com")
        self.author_contact.pack(side="bottom")





#===============================================FUNKCJE===============================================================================================================================

# ===============================================CONVERTER==========================================================================================
    def pdf_converter(self):
        Tk().withdraw()
        while True:
            try:
                loaded_image = (filedialog.askopenfilenames(parent=root, title='Wybierz plik'))
                imagelist = root.tk.splitlist(loaded_image)
                name = imagelist[0]
                final_name = name[::-1].replace("/", "_fdp/", 1)
                final_name = final_name[::-1]
                split_string = final_name.split(".", -1)
                final_name = split_string[0]
                pdf = FPDF()
                for imageFile in imagelist:
                    cover = Image.open(imageFile)
                    width, height = cover.size
                    width, height = float(width * 0.264583), float(height * 0.264583)
                    pdf_size = {'P': {'w': 210, 'h': 297}, 'L': {'w': 297, 'h': 210}}
                    orientation = 'P' if width < height else 'L'
                    width = width if width < pdf_size[orientation]['w'] else pdf_size[orientation]['w']
                    height = height if height < pdf_size[orientation]['h'] else pdf_size[orientation]['h']
                    pdf.add_page(orientation=orientation)
                    pdf.image(imageFile, 0, 0, width, height)
                pdf.output(final_name+".pdf", "F")
                showinfo("Komunikat", "Sukces")
                break
            except UnidentifiedImageError:
                showinfo("Komunikat", "Format pliku nie obsługiwany")
                break

# ===============================================COMPRESSOR==========================================================================================
    def pdf_compressor(self):
        showinfo("Komunikat", "Opcja chwilowo niedostępna")

# ===============================================MERGER==========================================================================================

    def pdf_merger(self):
        while True:
            try:
                input = (filedialog.askopenfilenames(parent=root, title='Wybierz plik'))
                files = root.tk.splitlist(input)
                save_file_name = input[0]
                "".join(save_file_name)
                final_name = save_file_name[::-1].replace("/", "_weN/", 1)
                final_name = final_name[::-1]

                merger = PdfFileMerger()
                for pdf in files:
                    merger.append(pdf)

                merger.write(final_name)
                merger.close()
                showinfo("Komunikat", "Sukces")
                break
            except PdfReadError:
                showinfo("Komunikat", "Nie wybrano pliku pdf")
                break

# ===============================================SPLITTER==========================================================================================
    def pdf_splitter(self):
        while True:
            try:
                input = (filedialog.askopenfilenames(parent=root, title='Wybierz plik'))
                file = input[0]
                split_op = file[::-1].split("/", 1)
                file_name = split_op[0].split(".", 1)
                final_path = split_op[1]
                final_path = final_path[::-1]
                file_name = file_name[1]
                file_name = file_name[::-1]
                final_path = final_path + "/Dokumenty/"
                if not os.path.exists(final_path):
                    os.mkdir(final_path)
                inputpdf = PdfFileReader(open(file, "rb"))
                for i in range(inputpdf.numPages):
                    output = PdfFileWriter()
                    output.addPage(inputpdf.getPage(i))
                    with open(final_path+ file_name +"_document-page%s.pdf" % i, "wb") as outputStream:
                        output.write(outputStream)
                showinfo("Komunikat", "Sukces")
                break
            except PdfReadError:
                showinfo("Komunikat", "Nie wybrano pliku pdf")
                break

# ===============================================INFO==========================================================================================
    def info(self):
        window = tk.Toplevel()
        text = "-pdf multitool v0.7-\n \n -Konwersja do pliku pdf-\n obsługa podstawowych formatów systemu windows\n \n -Kompresja plików pdf- \n funkcja chwilowo wyłączona \n \n -Rozdzielanie plików pdf- \n Po wybraniu pliku pdf w jego lokalizacji\n utworzy się nowy folder o nazwie 'dokumenty'\n w którym będą znajdować się wszystkie\n strony wybranego dokumentu\n \n -Złącz pliki pdf-\n Po wybraniu plików w ich lokalizacji\npojawi się nowy plik zawierający wszystkie\nwybrane wcześniej dokumenty"
        label = tk.Label(window, text=text)
        label.pack(fill='x', padx=100, pady=100)

        button_close = tk.Button(window, text="Zamknij", command=window.destroy)
        button_close.pack(fill='x')


#===============================================OKNO==================================================================================================================
root = tk.Tk()
root.geometry("200x200")
root.wm_title("Pdf Multitool")
app = Application(master=root)
app.mainloop()