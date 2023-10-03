from Texttables_2 import LineParser, TextTables
import tkinter
import time
from colorama import Fore, Back, Style
import colorama

colorama.init(autoreset=True)
p = print


def print(*args):
    p(*args, end="")


class Example:
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

        tkinter.Button(self.root, text="CreateTexttale", command=self.table).grid()
        self.root.mainloop()

    def table(self):
        data = [
            (1, "blue"),
            ("ghgh", "red"),
            ("ztzt", "blue"),
            (87, "red"),
        ]
        p1 = LineParser()
        p1.set_cell_aligns("clrr")
        p1.set_cell_widths([20, 20, 10, 30])
        p1.set_row(data)
        result = p1.get_row_adwanced()
        for part in result:
            try:
                color = part.args
            except KeyError:
                color = "black"
            self.textwidget.insert("end", part, color)
            # if part.get_token() == "frame":
            #     self.textwidget.insert("end", part, "blue")
            # else:
            # try:

            # except AttributeError:
            #     self.textwidget.insert("end", part, "green")


def example_parser_1():
    header = ["Example2", "Header2.0\nHeader2.1", "Header3"]
    data = [
        ["Franz1", 563, "Nothing"],
        ["Johannes", "44", 55],
        ["Volker", 2.7, "idk"],
    ]
    parser = LineParser()
    parser.set_cell_aligns("rrc")
    parser.set_cell_widths([15, 20, 23])
    parser.set_row(header)
    print(parser.get_border_top_bottom("utf_8_top_1"))
    print(parser.get_row())
    print(parser.get_border_top_bottom("utf_8_parting_1"))
    for row in data:
        parser.set_row(row)
        print(parser.get_row())

    print(parser.get_border_top_bottom("utf_8_bottom_1"))


def example_parser_2():
    header = [("Header1", "blue"), "Header2.0\nHeader2.1", "Header3"]
    data = [
        ["Franz1", 563, "Nothing", "Joke"],
        ["Johannes", "44", 55, "Rope"],
        ["Volker", 2.7, "idk", "Ok"],
    ]
    parser_header = LineParser()
    parser_header.set_cell_aligns("rrc")
    parser_header.set_cols_distance_from_left([15, 30, 70])
    parser_header.set_cell_text_to_border("  ", "  ")
    parser_header.set_line_align_indent(5)
    parser_header.set_row(header)

    print(parser_header.get_border_top_bottom("000"))
    print(parser_header.get_row())

    parser_data = LineParser()
    parser_data.set_cell_aligns("clcr")
    parser_data.set_cols_distance_from_left([15, 30, 50, 70])
    parser_data.set_border_chars_top_bottom("162", "╞═╪═╪═╤═╡")
    parser_data.set_line_align_indent(5)

    print(parser_data.get_border_top_bottom("162"))
    for row in data:
        parser_data.set_row(row)
        print(parser_data.get_row())

        parser_data.clear_data()
    print(parser_data.get_border_top_bottom("111"))


def example_table_1():
    header = [
        ("Header1", "blue"),
        "Header2.0\nHeader2.1",
        ("Header3", "red"),
        "header4",
    ]
    data = [
        ["Franz1", 563, "Nothing", ("Joke", "green")],
        ["Johannes", "44", 55, "Rope"],
        ["Volker", 2.7, "idk", ("Ok", "green")],
    ]
    texttable = TextTables()
    texttable.set_cell_width([20, 20, 20, 20])
    texttable.set_cell_align("crlr")
    texttable.add_row_header(header)
    for row in data:
        texttable.add_row_data(row)
    table = texttable.get_complete()
    for chunk in table:
        print(chunk)


# example_parser_1()
example_table_1()
# Example()
