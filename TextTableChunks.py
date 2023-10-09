from Texttable import LineParser, OutputChunk
from typing import Iterator


class TextTableChunks:
    def __init__(self, endline=True) -> None:
        # parser for header line
        self._parser_table_main_header = LineParser(end_of_line=endline)
        self._parser_table_main_header.set_border_chars_left_right(
            "header", [" ", " ", " "]
        )
        self._parser_table_main_header.set_cell_aligns("l")
        self._parser_table_main_header.set_cell_valigns("t")
        self._parser_header_row = LineParser(end_of_line=endline)
        self._parser_data = LineParser(end_of_line=endline)

        self._parsed_table: list[list[OutputChunk]] = []
        self._actual_parsed_lines: list[list[OutputChunk]] = []
        # to check if special horizontal line is needed
        self.__row_counter = 0
        self._special_horizontal_borders = []

        self._styles = {
            "grid_utf_8": {
                "top": "utf_8_top_1",
                "header": "utf_8_parting_1",
                "data": "utf_8_parting_2",
                "end": "utf_8_bottom_1",
                # "special": "utf_8_bottom_1",
                "border": "utf_8_border_1",
            },
            "grid_ascii": {
                "top": "ascii_parting_1",
                "header": "ascii_parting_2",
                "data": "ascii_parting_1",
                "end": "ascii_parting_1",
                # "special": "utf_8_bottom_1",
                "border": "ascii_border_1",
            },
            "github": {
                "header": "ascii_parting_4",
                "border": "ascii_border_1",
            },
            "simple": {
                "header": "ascii_parting_5",
                "border": "ascii_border_3",
            },
            "presto": {
                "header": "ascii_parting_6",
                "border": "ascii_border_2",
            },
            "psql": {
                "top": "ascii_parting_1",
                "header": "ascii_parting_7",
                "end": "ascii_parting_1",
                # "special": "utf_8_bottom_1",
                "border": "ascii_border_1",
            },
            "orgtbl": {
                "header": "ascii_parting_7",
                "border": "ascii_border_1",
            },
            "rst": {
                "top": "ascii_parting_8",
                "header": "ascii_parting_8",
                "end": "ascii_parting_8",
                # "special": "utf_8_bottom_1",
                "border": "ascii_border_4",
            },
            "outline": {
                "top": "ascii_parting_1",
                "header": "ascii_parting_2",
                "end": "ascii_parting_1",
                # "special": "utf_8_bottom_1",
                "border": "ascii_border_1",
            },
        }
        self.set_table_style("grid_utf_8")

    def set_table_style(self, style: str = "show"):
        if style not in self._styles.keys():
            raise KeyError(f"'{style}' not in {self._styles.keys()}")
        self._style = style

    # ------------ table creators  ---------------
    def _create_header_lines(self) -> Iterator[list[OutputChunk]]:
        # fmt:off
        for line in self._header_lines:
            self._parser_table_main_header.set_row([line])
            for line in self._parser_table_main_header.get_line_by_line_chunks("header"):
                yield line
        # fmt:on

    def _create_row_header(self) -> Iterator[list[OutputChunk]]:
        """create the row header depending on style

        Yields:
            Iterator[list[OutputChunk]]: _description_
        """
        # fmt:off
        if "top" in self._styles[self._style].keys():
            yield self._parser_header_row.get_border_top_bottom_chunks(self._styles[self._style]["top"])
        for line in self._parser_header_row.get_line_by_line_chunks(self._styles[self._style]["border"]):
            yield line
        if "header" in self._styles[self._style].keys():
            yield self._parser_header_row.get_border_top_bottom_chunks(self._styles[self._style]["header"])
        # fmt:on

    def _create_row_data(self) -> Iterator[list[OutputChunk]]:
        # fmt:off
        if "data" in self._styles[self._style].keys():
            yield self._get_special_horizontal_line(self._styles[self._style]["data"])
        for line in self._parser_data.get_line_by_line_chunks(self._styles[self._style]["border"]):
            yield line
        if "special" in self._styles[self._style].keys():
            yield self._get_special_horizontal_line()
        self.__row_counter +=1
        # fmt:on

    def _create_table_end(self) -> Iterator[list[OutputChunk]]:
        if "end" in self._styles[self._style].keys():
            return self._parser_data.get_border_top_bottom_chunks(
                self._styles[self._style]["end"]
            )

    def end_table(self):
        self._end_table = True

    def add_header(self, lines: list[str]):
        self._header_lines = lines

    def set_cols_distance_from_left(self, distances: list[int]):
        self._parser_header_row.set_cols_distance_from_left(distances)
        self._parser_data.set_cols_distance_from_left(distances)
        self._parser_table_main_header.set_cols_distance_from_left([distances[-1]])

    def set_cell_valign(self, cells_valign: list[str]):
        self._parser_header_row.set_cell_valigns(cells_valign)
        self._parser_data.set_cell_valigns(cells_valign)

    def set_cell_align_header(self, cells_align: list[str]):
        self._parser_header_row.set_cell_aligns(cells_align)

    def set_cell_align_data(self, cells_align: list[str]):
        self._parser_data.set_cell_aligns(cells_align)

    def set_special_horizontal_border(self, borders: int | list[int]):
        self._special_horizontal_borders = borders

    def add_row_header(self, row: list[str]):
        self._actual_parsed_lines = []
        self._parser_header_row.set_row(row)
        for line in self._create_row_header():
            self._parsed_table.append(line)
            self._actual_parsed_lines.append(line)

    def add_row_data(self, row: list[str]):
        self._actual_parsed_lines = []
        self._parser_data.set_row(row)
        for line in self._create_row_data():
            self._parsed_table.append(line)
            self._actual_parsed_lines.append(line)

    def _get_special_horizontal_line(self, name: str) -> list[OutputChunk]:
        """create a special vertical line after rows

        check if the special line is needed"""
        if self._special_horizontal_borders is None or self.__row_counter is None:
            return []
        if isinstance(self._special_horizontal_borders, int):
            if (
                self.__row_counter % self._special_horizontal_borders == 0
                and self.__row_counter != 0
            ):
                return self._parser_data.get_border_top_bottom_chunks(name)
        elif isinstance(self._special_horizontal_borders, list):
            if self.__row_counter in self._special_horizontal_borders:
                return self._parser_data.get_border_top_bottom_chunks(name)
        return []

    def get_actual_parsed_lines(self, end=False) -> list[list[OutputChunk]]:
        if end:
            return self._actual_parsed_lines.append(self._create_table_end())
        return self._actual_parsed_lines

    def test(self):
        # for line in self._actual_parsed_lines:
        #     for chunk in line:
        #         print(chunk, end="")
        print("complett:")
        for line in self._parsed_table:
            for chunk in line:
                print(chunk, end="")

    def get_complete_table(self) -> list[OutputChunk]:
        return


data = [
    ["Hallo\nFranz1", 563, "Nothing"],
    ["Johannes", "44", 55],
    ["Volker", 2.7, "idk"],
]
d = TextTableChunks()
d.set_cell_align_data("rrr")
d.set_cell_align_header("lll")
d.set_cell_valign("ttt")
d.set_cols_distance_from_left([20, 40, 60])
d.set_table_style("grid_utf_8")
d.add_row_header(["eins", "zwei", "dreu"])
for row in data:
    d.add_row_data(row)
d.end_table()

d.test()
