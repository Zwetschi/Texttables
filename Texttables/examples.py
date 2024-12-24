from Texttable import (
    LineParser,
    TextTableInTime,
    InputCell,
    TextTableFast,
)
import tkinter
import time
from colorama import Fore, Back, Style
import colorama

colorama.init(autoreset=True)


def example_parser_1():
    header = [
        InputCell("Example", Fore.RED),
        "Header2.0\nHeader2.1\nhghg\njhuz\njzhgg\nhghk",
        "Header3",
    ]
    data = [
        ["Franz1", 563, "Nothing"],
        ["Johannes", "44", 55],
        ["Volker", 2.7, "idk"],
    ]
    parser = LineParser()
    parser.set_cell_aligns("crc")
    parser.set_cell_widths([15, 20, 23])
    parser.set_cell_valigns("mtb")
    parser.set_row(header)
    print(parser.get_border_top_bottom("utf_8_top_1"), end="")
    print(parser.get_row(), end="")
    print(parser.get_border_top_bottom("utf_8_parting_1"), end="")
    for row in data:
        parser.set_row(row)
        print(parser.get_row(), end="")

    print(parser.get_border_top_bottom("utf_8_bottom_1"))


def example_parser_2():
    header = ["Header1", "Header2.0\nHeader2.1", "Header3"]
    data = [
        ["Franz1", 563, "Nothing", "Joke"],
        ["Johannes", "44", 55, "Rope"],
        ["Volker", 2.7, "idk", "Ok"],
    ]
    parser_header = LineParser()
    parser_header.set_cell_aligns("rrc")
    parser_header.set_cell_valigns("mmm")
    parser_header.set_cols_distance_from_left([15, 30, 70])
    parser_header.set_cell_text_to_border("  ", "  ")
    parser_header.set_line_indent(5)
    parser_header.set_row(header)

    print(parser_header.get_border_top_bottom("000"), end="")
    print(parser_header.get_row(), end="")

    parser_data = LineParser()
    parser_data.set_cell_aligns("clcr")
    parser_data.set_cell_valigns("mmmm")
    parser_data.set_cols_distance_from_left([15, 30, 50, 70])
    parser_data.set_border_chars_top_bottom("162", "╞═╪═╪═╤═╡")
    parser_data.set_line_indent(5)

    print(parser_data.get_border_top_bottom("162"), end="")
    for row in data:
        parser_data.set_row(row)
        print(parser_data.get_row(), end="")

        parser_data.clear_raw_data()
    print(parser_data.get_border_top_bottom("111"), end="")


def example_parser_3():
    p1 = LineParser()
    p2 = LineParser(end_of_line=False)
    p3 = LineParser()
    p1.set_cols_distance_from_left([15, 30, 65])
    p2.set_cols_distance_from_left([15])
    p3.set_cols_distance_from_left([15, 33, 50])
    p2.set_border_chars_top_bottom("top1", ["+", "-", "+", "+"])
    p3.set_border_chars_top_bottom("top2", ["", "-", "+", "+"])
    p3.set_border_chars_left_right("side1", ["", "|", "|"])
    p1.set_cell_aligns("ccc")
    p2.set_cell_aligns("c")
    p3.set_cell_aligns("lrc")
    p1.set_cell_valigns("ttt")
    p2.set_cell_valigns("t")
    p3.set_cell_valigns("ttt")

    p1.set_row(["parser1", "parser1\nparser1", "parser1\np1"])
    print(p1.get_border_top_bottom("666"), end="")
    print(p1.get_row(), end="")

    p2.set_row(["parser2\nrow\nheader\nparser2\n"])
    x1 = (
        [p2.get_border_top_bottom_chunks("top1")]
        + [line for line in p2.get_line_by_line_chunks("111")]
        + [p2.get_border_top_bottom_chunks("top1")]
    )
    p3.set_row(["parser3\ndata11", "parser3\ndata12", "parser3\ndata13"])
    lines2_1 = [p3.get_border_top_bottom_chunks("top2")] + [
        line for line in p3.get_line_by_line_chunks()
    ]
    p3.set_row(["parser3\ndata21", "parser3\ndata22", "parser3\ndata23"])
    lines2_2 = (
        [p3.get_border_top_bottom_chunks()]
        + [line for line in p3.get_line_by_line_chunks()]
        + [p3.get_border_top_bottom_chunks("top2")]
    )
    for a, b in zip(x1, lines2_1 + lines2_2):
        for chunk in a + b:
            print(chunk, end="")


def example_parser_4():
    header = ["Header1", "Header2.0\nHeader2.1", "Header3"]
    data = [
        ["Franz1", 563, "Nothing"],
        ["Johannes", 55, "Rope"],
        ["Volker", 2.7, "Ok"],
    ]
    parser_left = LineParser(end_of_line=False)
    parser_right = LineParser()
    parser_left.set_cell_aligns("rrr")
    parser_left.set_cell_valigns("ttt")
    parser_left.set_cols_distance_from_left([20, 40, 60])


def example_texttable_1():
    header = [
        InputCell("Header1\n756h", Fore.BLUE),
        "Header2.0\nHeader2.1",
        InputCell("Header3", Fore.RED),
        "header4",
    ]
    data = [
        ["Franz1", 563, "Nothing", InputCell("Joke", Fore.RED)],
        ["Johannes", "44", 55, "Rope"],
        ["Volker", 2.7, "idk", InputCell("Ok", Fore.GREEN)],
        ["Franz1", 563, "Nothing", InputCell("Joke", Fore.BLUE)],
        ["Johannes", "44", 55, "Rope"],
        [InputCell("Volker", Fore.MAGENTA), 2.7, "idk", "servus"],
        ["Franz1", 563, "Nothing", InputCell("Joke")],
        ["Johannes", "44", 55, "Rope"],
        ["Volker", 2.7, "idk", InputCell("Ok", Fore.YELLOW)],
    ]
    texttable = TextTableInTime()
    texttable.add_header(
        [
            "Hi, this is the table header. \nAnd this is the second table header line",
            InputCell("Add a third red header line", Fore.RED),
        ],
    )
    texttable.set_cols_distance_from_left([19, 35, 49, 60])
    texttable.set_cell_align_header("cclr")
    texttable.set_cell_align_data("clrc")
    texttable.set_cell_valign("bbbb")
    texttable.set_special_horizontal_border([3, 4, 7])
    texttable.add_row_header(header)
    for chunk in texttable.get_header_lines():
        try:
            color = chunk.args[0]
        except IndexError:
            color = Fore.BLACK
        print(color + str(chunk), end="")

    for chunk in texttable.get_row_header():
        try:
            color = chunk.args[0]
        except IndexError:
            color = Fore.BLACK
        print(color + str(chunk), end="")

    for row in data:
        time.sleep(0.5)  # simulat any code running behind
        texttable.add_row_data(row)
        for chunk in texttable.get_row_data():
            try:
                color = chunk.args[0]
            except IndexError:
                color = Fore.BLACK
            print(color + str(chunk), end="")
    for chunk in texttable.get_table_end():
        try:
            color = chunk.args[0]
        except IndexError:
            color = Fore.BLACK
        print(color + str(chunk), end="")


def texttable_fast_1():
    header = ["Example", "Header2.0", "Header3"]
    data = [
        ["Hallo\nFranz1", 563, "Nothing"],
        ["Johannes", "44", 55],
        ["Volker", 2.7, "idk"],
    ]
    t = TextTableFast()
    t.add_row_header(header)
    for row in data:
        t.add_row_data(row)
    for predef_style in [
        "grid_utf_8",
        "grid_ascii",
        "github",
        "simple",
        "presto",
        "psql",
        "orgtbl",
        "rst",
        "outline",
    ]:
        table_string = t.get_table(predef_style)
        print(table_string)


def texttable_fast_2():
    header = ["Example", "Header2.0", "Header3"]
    data = [
        ["Hallo\nFranz1", 563, "Nothing"],
        ["Johannes", "44", 55],
        ["Volker", 2.7, "idk"],
    ]
    t = TextTableFast()
    t.add_row_header(header)
    for row in data:
        t.add_row_data(row)
    table_string = t.get_table("utf8_std")
    print(table_string)


# example_parser_1()
# example_parser_2()
# example_parser_3()
# example_texttable_1()
# texttable_fast_1()
texttable_fast_2()
