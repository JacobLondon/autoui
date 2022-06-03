from ctypes import alignment
from tkinter import *
from tkinter.ttk import *

class MenuMediator:
    def __init__(self, title: str, save_callable, open_callable, coord_callable):
        self.do_save = save_callable
        self.do_open = open_callable
        self.do_coord = coord_callable

        # UI #

        self.root = Tk()
        self.root.title(title)
        self.root.config(bg='#31364A')

        # https://stackoverflow.com/questions/32289175/list-of-all-tkinter-events
        # https://www.tcl.tk/man/tcl/TkCmd/keysyms.html
        self.root.bind_all('<Control-Alt_L>', lambda a: self.do_coord(self))
        self.root.bind_all('<Control-s>', lambda a: self.do_save(self))
        self.root.bind_all('<Control-o>', lambda a: self.do_open(self))

        # text box for line input
        self.entry_url = Entry(self.root, width=70)
        self.entry_url.grid(column=0, row=0, sticky=W, pady=5, padx=5)

        self.button_open = Button(self.root, text="Open", command=lambda: self.do_open(self))
        self.button_open.grid(column=1, row=0, sticky=W+E, pady=5, padx=5, columnspan=1)

        self.button_save = Button(self.root, text="Save", command=lambda: self.do_save(self))
        self.button_save.grid(column=2, row=0, sticky=W+E, pady=5, padx=5, columnspan=1)

        # label with x,y
        self.label_coords = Label(
            self.root, text="x, y", width=10
        )
        self.label_coords.grid(column=0, row=1, sticky=E, pady=5, padx=5, columnspan=1)

        self.label_usage = Label(
            self.root, text="Press Ctrl+Alt to save coords"
        )
        self.label_usage.grid(column=1, row=1, sticky=W, pady=5, padx=5, columnspan=2)

        # big text area with scrollbar
        self.text_box = Text(self.root, height=40, width=75)
        self.text_box.grid(column=0, row=2, sticky=W+E, pady=5, padx=5, columnspan=3)
        self.text_box_scrollbar_sb = Scrollbar(self.root)
        self.text_box_scrollbar_sb.grid(column=4, row=2, sticky=N+S+W, pady=5, padx=5, columnspan=3)
        self.text_box.config(yscrollcommand=self.text_box_scrollbar_sb.set)
        self.text_box_scrollbar_sb.config(command=self.text_box.yview)

    def start(self):
        self.root.mainloop()

    def set_coords(self, text):
        self.label_coords['text'] = text
    
    def get_coords(self):
        return self.label_coords.cget('text')

    def append_text(self, text):
        self.text_box.insert(END, text + "\n")

    def get_text(self):
        return self.text_box.get('1.0', 'end')

    def delete_text(self):
        self.text_box.delete('1.0', 'end')

    def get_url(self):
        return self.entry_url.get()

def _do_save(mediator):
    print('save')
    mediator.set_coords("1, 2")

def _do_open(mediator):
    print('open')

def _do_coords(mediator):
    print("Control-Alt detected")
    mediator.append_text('ok there')

def _main(argv):
    m = MenuMediator("test", _do_save, _do_open, _do_coords)
    m.start()
    return 0

if __name__ == '__main__':
    import sys
    exit(_main(sys.argv))
