from Texttables_2 import LineParser
from typing import NamedTuple
import tkinter

p = print


def print(*args):
    p(*args, end="")


header = ["Header1", "Header2.0\nHeader2.1", "Header3"]
data = [
    ["Franz1", 563, "Nothing", "Joke"],
    ["Johannes", "44", 55, "Rope"],
    ["Volker", 2.7, "idk", "Ok"],
]


parser_header = LineParser()
parser_header.set_cell_align("rrc")
parser_header.set_cols_distance_from_left([15, 30, 70])


for cell in header:
    parser_header.add_cell(cell)

print(parser_header.get_border_top_bottom_string("000"))
print(parser_header.get_row_string())
# print(parser_header.get_border_horizontal_string("222"))

parser_data = LineParser()
parser_data.set_cell_align("clcr")
parser_data.set_cols_distance_from_left([15, 30, 50, 70])
parser_data.set_border_chars_top_bottom("162", "╞═╪═╪═╤═╡")

print(parser_data.get_border_top_bottom_string())
for row in data:
    for cell in row:
        parser_data.add_cell(cell)
    print(parser_data.get_row_string())

    parser_data.clear_data()
print(parser_data.get_border_top_bottom_string("111"))
# parser_header.set_frame_vertical_line_bottom(True


# parser_header.set_border_chars_top_bottom("ggg", "+-++")

# parser_header.add_row(data[0])
# parser_header.run()
# print(parser_header)
# print(parser_header)
# print(parser_header)
# print(parser_header)


# parser_header.add_row(header)
# table += parser_header.get_row()
# print(table)

# parser_data = RowParser()
# parser_data.set_cell_allign("clrc")
# parser_data.set_cols_distance_from_left([15, 30, 50, 70])
# parser_data.set_charset_active("standart_2")
# parser_data.set_frame_vertical_line_top(False)

# for row in data:
#     parser_data.add_row(row)
#     table += parser_data.get_row()


# t = TextTables()
# t.set

# p1 = RowParser()
# p1.set_cell_allign("clrc")
# p1.set_cell_width([20, 30, 10, 4])
# p1.add_row(data)
# print(p1)

# _enco = "utf-8"
# with open("chars.txt", "w", encoding=_enco) as f:
#     f.write(str(p1))

# print()
# p1.set_cols_distance_from_left([20, 50, 60, 90])
# p2 = Parser([10, 20, 20, 25], ["c", "l", "r", "r"])
# p1.set_frame_vertical_line_top(True, "my_own", chars=["┌", "─", "┬", "┐"])
# p1.set_frame_border("my_own", chars="│ixi│")
# p1.set_frame_vertical_line_special("my_own")
# p1.set_frame_vertical_line_bottom(True, "my_own")
# p1.set_charset_active("my_own")
# p2.set_frame_vertical_line_top(False)
# p2.set_frame_vertical_line_bottom(True)
# p.add_cell("aaa")
# p.add_cell("bb")
# p.add_cell("cccc")
# p.add_cell("ght")


# for part in p2.get_row(["gt", "ght", "ght", "ght"]):
#     print(part.get_part(), end="")


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
