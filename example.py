import Texttables
import tkinter


def example_1():
    t1 = Texttables.Texttables(side_mode=False)
    t1.add.header("hehey")
    t1.set.cols_width([20, 20, 20])
    t1.set.align_cols(["r"] * 3)
    t1.set.align_header(["r"] * 3)
    t1.add.header_column(["one\none", "second\nsecond", ""])
    t1.set.v_line_special(5)
    for i in range(10):
        t1.add.row(["fgtZZZZff", "ggg", "hhh"])
    t1.end()
    t1.add.header("heheyfrt")
    t1.set.cols_width([10, 15, 5] * 2)
    t1.set.align_cols(["r"] * 3 * 2)
    t1.set.align_header(["r"] * 3 * 2)
    t1.set.v_line_normal(False)
    t1.add.header_column(["one\none", "second\nsecond", ""] * 2)
    for i in range(14):
        t1.add.row(["fgZZff", "ggg", "hhh"] * 2)
    t1.end()
    print(t1.get_str())


def example_2():
    root = tkinter.Tk()
    textwidget = tkinter.Text(root)
    textwidget.pack()
    textwidget.tag_config("black", foreground="black")
    textwidget.tag_config("red", foreground="red")

    class Example2:
        def __init__(self, text, color) -> None:
            self.text = text
            self.color = color

    def table_2():
        t2 = Texttables.Texttables(side_mode=False)
        t2.add.header("hehey")
        t2.set.cols_width([20, 20, 20])
        t2.set.align_cols(["r"] * 3)
        t2.set.align_header(["r"] * 3)
        t2.add.header_column(["one\none", "second\nsecond", ""])
        t2.set.v_line_special(5)
        for i in range(10):
            t2.add.row([Example2("fgtZZZ\nZff", "red"), "ggg", "hhh"])
        t2.end()
        result = t2.get_obj()
        for obj in result:
            try:
                textwidget.insert("end", obj.text, obj.input.color)
            except AttributeError:
                textwidget.insert("end", obj.text, "green")

    tkinter.Button(root, text="CreateTexttale", command=table_2).pack()
    root.mainloop()


class Example:
    class Example2:
        def __init__(self, text, color) -> None:
            self.text = text
            self.color = color

    def __init__(self) -> None:
        self.root = tkinter.Tk()
        scollbar = tkinter.Scrollbar(self.root, orient="horizontal")
        self.textwidget = tkinter.Text(
            self.root, xscrollcommand=scollbar.set, wrap="none"
        )
        self.textwidget.config(width=200, height=40)
        scollbar.config(command=self.textwidget.xview)
        self.textwidget.grid(sticky="nswe")
        scollbar.grid(sticky="nesw")
        self.textwidget.tag_config("black", foreground="black")
        self.textwidget.tag_config("blue", foreground="blue")
        self.textwidget.tag_config("red", foreground="red")

        tkinter.Button(self.root, text="CreateTexttale", command=self.table_3).grid()
        self.root.mainloop()

    def table_3(self):
        t2 = Texttables.Texttables(side_mode=True)
        t2.add.header("hehey")
        t2.set.cols_width([20, 20, 20])
        t2.set.align_cols(["r"] * 3)
        t2.set.align_header(["r"] * 3)
        t2.add.header_column(["one\none", "second\nsecond", ""])
        t2.set.v_line_special(5)
        for i in range(10):
            t2.add.row([self.Example2("fgtZZZZff", "red"), "ggg", "hhh"])
        t2.end()
        t2.add.header("hehey")
        t2.set.cols_width([20, 20, 20])
        t2.set.align_cols(["r"] * 3)
        t2.set.align_header(["r"] * 3)
        t2.add.header_column(["one\none", "second\nsecond", ""])
        t2.set.v_line_special(5)
        for i in range(10):
            t2.add.row([self.Example2("fgtZZZZff", "red"), "ggg", "hhh"])
        t2.end()
        result = t2.get_obj()
        for obj in result:
            if obj.token == "frame":
                self.textwidget.insert("end", obj.text, "blue")
            else:
                try:
                    self.textwidget.insert("end", obj.text, obj.input.color)
                except AttributeError:
                    self.textwidget.insert("end", obj.text, "green")


def example_4():
    t4 = Texttables.Texttables(side_mode=False)
    t4.add.header("heheyfrt")
    t4.set.cols_width([10, 15, 5] * 2)
    t4.set.align_cols(["r"] * 3 * 2)
    t4.set.align_header(["r"] * 3 * 2)
    t4.set.v_line_normal(False)
    t4.add.header_column(["one\none", "second", ""] * 2)
    for i in range(5):
        t4.add.row(["fgZZff", "ggg", "hhh"] * 2)
    t4.end()
    print(t4.get_str())


Example()
