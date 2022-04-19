from tkinter import *
from tkinter import *
from tkinter.filedialog import *
from tkinter.messagebox import *
from tkinter.font import Font
from tkinter.scrolledtext import *
from tkinter import *
from tkinter.simpledialog import *
from tkinter.filedialog import *
from tkinter.messagebox import *
from tkinter import *
from tkinter.colorchooser import askcolor
from tkinter.font import Font, families
from tkinter.scrolledtext import *
import time
import sys


class Edit():
    def popup(self, event):
        self.rightClick.post(event.x_root, event.y_root)

    def copy(self, *args):
        sel = self.text.selection_get()
        self.clipboard = sel

    def cut(self, *args):
        sel = self.text.selection_get()
        self.clipboard = sel
        self.text.delete(SEL_FIRST, SEL_LAST)

    def paste(self, *args):
        self.text.insert(INSERT, self.clipboard)

    def selectAll(self, *args):
        self.text.tag_add(SEL, "1.0", END)
        self.text.mark_set(0.0, END)
        self.text.see(INSERT)

    def undo(self, *args):
        self.text.edit_undo()

    def redo(self, *args):
        self.text.edit_redo()

    def find(self, *args):
        self.text.tag_remove('found', '1.0', END)
        target = askstring('Find', 'Search String:')

        if target:
            idx = '1.0'
            while 1:
                idx = self.text.search(target, idx, nocase=1, stopindex=END)
                if not idx:
                    break
                lastidx = '%s+%dc' % (idx, len(target))
                self.text.tag_add('found', idx, lastidx)
                idx = lastidx
            self.text.tag_config(
                'found', foreground='white', background='blue')

    def __init__(self, text, root):
        self.clipboard = None
        self.text = text
        self.rightClick = Menu(root, tearoff=0)


class File():
    def newFile(self):
        self.filename = "Untitled"
        self.text.delete(0.0, END)

    def saveFile(self):
        try:
            t = self.text.get(0.0, END)
            f = open(self.filename, 'w')
            f.write(t)
            f.close()
        except:
            self.saveAs()

    def saveAs(self):
        f = asksaveasfile(mode='w', defaultextension='.txt')
        t = self.text.get(0.0, END)
        try:
            f.write(t.rstrip())
        except:
            showerror(title="Oops!", message="Unable to save file...")

    def openFile(self):
        f = askopenfile(mode='r')
        self.filename = f.name
        t = f.read()
        self.text.delete(0.0, END)
        self.text.insert(0.0, t)

    def quit(self):
        entry = askyesno(
            title="Quit", message="Are you sure you want to quit?")
        if entry == True:
            self.root.destroy()

    def __init__(self, text, root):
        self.filename = None
        self.text = text
        self.root = root


class Format():
    def __init__(self, text):
        self.text = text

    def changeBg(self):
        (triple, hexstr) = askcolor()
        if hexstr:
            self.text.config(bg=hexstr)

    def changeFg(self):
        (triple, hexstr) = askcolor()
        if hexstr:
            self.text.config(fg=hexstr)

    def bold(self, *args):  # Works only if text is selected
        try:
            current_tags = self.text.tag_names("sel.first")
            if "bold" in current_tags:
                self.text.tag_remove("bold", "sel.first", "sel.last")
            else:
                self.text.tag_add("bold", "sel.first", "sel.last")
                bold_font = Font(self.text, self.text.cget("font"))
                bold_font.configure(weight="bold")
                self.text.tag_configure("bold", font=bold_font)
        except:
            pass

    def italic(self, *args):  # Works only if text is selected
        try:
            current_tags = self.text.tag_names("sel.first")
            if "italic" in current_tags:
                self.text.tag_remove("italic", "sel.first", "sel.last")
            else:
                self.text.tag_add("italic", "sel.first", "sel.last")
                italic_font = Font(self.text, self.text.cget("font"))
                italic_font.configure(slant="italic")
                self.text.tag_configure("italic", font=italic_font)
        except:
            pass

    def underline(self, *args):  # Works only if text is selected
        try:
            current_tags = self.text.tag_names("sel.first")
            if "underline" in current_tags:
                self.text.tag_remove("underline", "sel.first", "sel.last")
            else:
                self.text.tag_add("underline", "sel.first", "sel.last")
                underline_font = Font(self.text, self.text.cget("font"))
                underline_font.configure(underline=1)
                self.text.tag_configure("underline", font=underline_font)
        except:
            pass

    def overstrike(self, *args):  # Works only if text is selected
        try:
            current_tags = self.text.tag_names("sel.first")
            if "overstrike" in current_tags:
                self.text.tag_remove("overstrike", "sel.first", "sel.last")
            else:
                self.text.tag_add("overstrike", "sel.first", "sel.last")
                overstrike_font = Font(self.text, self.text.cget("font"))
                overstrike_font.configure(overstrike=1)
                self.text.tag_configure("overstrike", font=overstrike_font)
        except:
            pass

    def addDate(self):
        full_date = time.localtime()
        day = str(full_date.tm_mday)
        month = str(full_date.tm_mon)
        year = str(full_date.tm_year)
        date = day + '/' + month + '/' + year
        self.text.insert(INSERT, date, "a")


class Help():
    def about(root):
        showinfo(title="About", message="Created by OMAR TOUIL\nGItHub:omar-195")


def mainEdit(root, text, menubar):
    objEdit = Edit(text, root)
    editmenu = Menu(menubar, tearoff=0)
    editmenu.add_command(
        label="Copy", command=objEdit.copy, accelerator="Ctrl+C")
    editmenu.add_command(label="Cut", command=objEdit.cut,
                         accelerator="Ctrl+X")
    editmenu.add_command(
        label="Paste", command=objEdit.paste, accelerator="Ctrl+V")
    editmenu.add_command(
        label="Undo", command=objEdit.undo, accelerator="Ctrl+Z")
    editmenu.add_command(
        label="Redo", command=objEdit.redo, accelerator="Ctrl+Y")
    editmenu.add_command(
        label="Find", command=objEdit.find, accelerator="Ctrl+F")
    editmenu.add_separator()
    editmenu.add_command(label="Select All",
                         command=objEdit.selectAll, accelerator="Ctrl+A")
    menubar.add_cascade(label="Edit", menu=editmenu)

    root.bind_all("<Control-z>", objEdit.undo)
    root.bind_all("<Control-y>", objEdit.redo)
    root.bind_all("<Control-f>", objEdit.find)
    root.bind_all("Control-a", objEdit.selectAll)
    objEdit.rightClick.add_command(label="Copy", command=objEdit.copy)
    objEdit.rightClick.add_command(label="Cut", command=objEdit.cut)
    objEdit.rightClick.add_command(label="Paste", command=objEdit.paste)
    objEdit.rightClick.add_separator()
    objEdit.rightClick.add_command(
        label="Select All", command=objEdit.selectAll)
    objEdit.rightClick.bind("<Control-q>", objEdit.selectAll)
    text.bind("<Button-3>", objEdit.popup)
    root.config(menu=menubar)


def mainFileMenu(root, text, menubar):
    filemenu = Menu(menubar, tearoff=0)
    objFile = File(text, root)
    filemenu.add_command(label="New", command=objFile.newFile)
    filemenu.add_command(label="Open", command=objFile.openFile)
    filemenu.add_command(label="Save", command=objFile.saveFile)
    filemenu.add_command(label="Save As...", command=objFile.saveAs)
    filemenu.add_separator()
    filemenu.add_command(label="Quit", command=objFile.quit)
    menubar.add_cascade(label="File", menu=filemenu)
    root.config(menu=menubar)


def mainFormat(root, text, menubar):
    objFormat = Format(text)

    fontoptions = families(root)
    font = Font(family="Arial", size=10)
    text.configure(font=font)

    formatMenu = Menu(menubar, tearoff=0)

    fsubmenu = Menu(formatMenu, tearoff=0)
    ssubmenu = Menu(formatMenu, tearoff=0)

    for option in fontoptions:
        fsubmenu.add_command(
            label=option, command=lambda option=option: font.configure(family=option))
    for value in range(1, 31):
        ssubmenu.add_command(
            label=str(value), command=lambda value=value: font.configure(size=value))

    formatMenu.add_command(label="Change Background",
                           command=objFormat.changeBg)
    formatMenu.add_command(label="Change Font Color",
                           command=objFormat.changeFg)
    formatMenu.add_cascade(label="Font", underline=0, menu=fsubmenu)
    formatMenu.add_cascade(label="Size", underline=0, menu=ssubmenu)
    formatMenu.add_command(
        label="Bold", command=objFormat.bold, accelerator="Ctrl+B")
    formatMenu.add_command(
        label="Italic", command=objFormat.italic, accelerator="Ctrl+I")
    formatMenu.add_command(
        label="Underline", command=objFormat.underline, accelerator="Ctrl+U")
    formatMenu.add_command(
        label="Overstrike", command=objFormat.overstrike, accelerator="Ctrl+T")
    formatMenu.add_command(label="Add Date", command=objFormat.addDate)
    menubar.add_cascade(label="Format", menu=formatMenu)

    root.bind_all("<Control-b>", objFormat.bold)
    root.bind_all("<Control-i>", objFormat.italic)
    root.bind_all("<Control-u>", objFormat.underline)
    root.bind_all("<Control-T>", objFormat.overstrike)

    root.grid_columnconfigure(0, weight=1)
    root.resizable(True, True)

    root.config(menu=menubar)


def mainHelp(root, text, menubar):

    help = Help()

    helpMenu = Menu(menubar, tearoff=0)
    helpMenu.add_command(label="About", command=help.about)
    menubar.add_cascade(label="Help", menu=helpMenu)

    root.config(menu=menubar)


class MainFile(Tk):
    def __init__(self):
        super().__init__()
        self.title("Text Editor")
        self.geometry("300x250+300+300")
        self.minsize(width=400, height=400)
        self.text = ScrolledText(self, state='normal', height=400,
                                 width=400, wrap='word', pady=2, padx=3, undo=True)
        self.text.pack(fill=Y, expand=1)
        self.text.focus_set()
        self.menubar = Menu(self)
        mainFileMenu(self, self.text, self.menubar)
        mainEdit(self, self.text, self.menubar)
        mainFormat(self, self.text, self.menubar)
        mainHelp(self, self.text, self.menubar)


if __name__ == '__main__':
    MainFile().mainloop()
