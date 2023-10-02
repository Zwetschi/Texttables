from Texttables_2 import LineParser
import tkinter
import time

p = print


def print(*args):
    p(*args, end="")


def example_parser_1():
    header = ["Header1", "Header2.0\nHeader2.1", "Header3"]
    data = [
        ["Franz1", 563, "Nothing"],
        ["Johannes", "44", 55],
        ["Volker", 2.7, "idk"],
    ]
    parser = LineParser()
    parser.set_cell_aligns("rrc")
    parser.set_cell_widths([15, 20, 23])
    parser.add_row(header)
    print(parser.get_border_top_bottom("utf_8_top_1"))
    print(parser.get_row())
    print(parser.get_border_top_bottom("utf_8_parting_1"))
    for row in data:
        parser.add_row(row)
        print(parser.get_row())

    print(parser.get_border_top_bottom("utf_8_bottom_1"))


def example_parser_2():
    header = ["Example2", "Header2.0\nHeader2.1", "Header3"]
    data = [
        ["Franz1", 563, "Nothing"],
        ["Johannes", "44", 55],
        ["Volker", 2.7, "idk"],
    ]
    parser = LineParser()
    parser.set_cell_aligns("rrc")
    parser.set_cell_widths([15, 20, 23])
    parser.add_row(header)
    parser.set_line_align_indent(5)
    print(parser.get_border_top_bottom("utf_8_top_1"))
    print(parser.get_row())
    print(parser.get_border_top_bottom("utf_8_parting_1"))
    for row in data:
        parser.add_row(row)
        print(parser.get_row())

    print(parser.get_border_top_bottom("utf_8_bottom_1"))


def example_parser_3():
    header = ["Header1", "Header2.0\nHeader2.1", "Header3"]
    data = [
        ["Franz1", 563, "Nothing", "Joke"],
        ["Johannes", "44", 55, "Rope"],
        ["Volker", 2.7, "idk", "Ok"],
    ]
    parser_header = LineParser()
    parser_header.set_cell_aligns("rrc")
    parser_header.set_cols_distance_from_left([15, 30, 70])
    parser_header.set_cell_text_to_border("  ", "  ")
    for cell in header:
        parser_header.add_cell(cell)

    print(parser_header.get_border_top_bottom("000"))
    print(parser_header.get_row())

    parser_data = LineParser()
    parser_data.set_cell_aligns("clcr")
    parser_data.set_cols_distance_from_left([15, 30, 50, 70])
    parser_data.set_border_chars_top_bottom("162", "╞═╪═╪═╤═╡")

    print(parser_data.get_border_top_bottom("162"))
    for row in data:
        for cell in row:
            parser_data.add_cell(cell)
        print(parser_data.get_row())

        parser_data.clear_data_advanced()
    print(parser_data.get_border_top_bottom("111"))


example_parser_2()


class Example:
    class Data:
        def __init__(self, text, color) -> None:
            self.a = text
            self.b = color

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
        p1 = LineParser("clrr", [20, 30, 10, 30])
        data = [
            self.Data(1, "blue"),
            self.Data("ghgh", "red"),
            self.Data("ztzt", "blue"),
            self.Data(87, "red"),
        ]
        for cell in data:
            p1.add_cell(cell.a, my_color=cell.b)
        result = p1.get_row()
        for part in result:
            try:
                color = part.kwargs["my_color"]
            except KeyError:
                color = "black"
            self.textwidget.insert("end", part, color)
            # if part.get_token() == "frame":
            #     self.textwidget.insert("end", part, "blue")
            # else:
            # try:

            # except AttributeError:
            #     self.textwidget.insert("end", part, "green")


# Example()
