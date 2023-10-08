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

        self._parsed_header_cell: list[list[OutputChunk]] = []
        self._parsed_header_lines: list[list[OutputChunk]] = []
        self._actual_parsed_header_lines: list[list[OutputChunk]] = []
        self._parsed_data_lines: list[list[OutputChunk]] = []
        self._actual_parsed_data_lines: list[list[OutputChunk]] = []
        # to check if special horizontal line is needed
        self.__row_counter = 0
        self._special_horizontal_borders = []
        self.set_table_style("grid_utf_8")

        self._styles = {
            "grid_utf_8": {
                "top": "utf_8_top_1",
                "header": "utf_8_parting_1",
                "data": "utf_8_parting_2",
                "end": "utf_8_bottom_1",
                "special": "utf_8_bottom_1",
                "border": "utf_8_border_1",
            },
            # "grid_ascii": self._style_grid_ascii,
            # "github": self._style_github_ascii,
            # "simple": self._style_simple_ascii,
            # "presto": self._style_presto_ascii,
            # "psql": self._style_psql_ascii,
            # "psql": self._style_psql_ascii,
            # "orgtbl": self._style_orgtbl_ascii,
            # "rst": self._style_rst_ascii,
            # "outline": self._style_outline_ascii,
        }

    def set_table_style(self, style: str = "show"):
        if style not in self._styles.keys():
            raise KeyError(f"'{style}' not in {self._styles.keys()}")
        self._style = style

    # ------------ table creators  ---------------
    def _create_1(self, top, header, data, end, border) -> list[list[OutputChunk]]:
        result: list[list[OutputChunk]] = []
        result.append(self._parser.get_border_top_bottom_chunks(top))
        for header_row in self._parsed_header_lines:
            self._parser.set_row(header_row)
            for line in self._parser.get_line_by_line_chunks(border):
                result.append(line)
            result.append(self._parser.get_border_top_bottom_chunks(header))
        for data_row in self._parsed_data_lines[:-1]:
            self._parser.set_row(data_row)
            for line in self._parser.get_line_by_line_chunks(border):
                result.append(line)
            result.append(self._parser.get_border_top_bottom_chunks(data))
        self._parser.set_row(self._parsed_data_lines[-1])
        for line in self._parser.get_line_by_line_chunks(border):
            result.append(line)
        result.append(self._parser.get_border_top_bottom_chunks(end))
        return result

    def _create_2(self, top, header, end, border) -> list[list[OutputChunk]]:
        result: list[list[OutputChunk]] = []
        result.append(self._parser.get_border_top_bottom_chunks(top))
        for header_row in self._parsed_header_lines:
            self._parser.set_row(header_row)
            for line in self._parser.get_line_by_line_chunks(border):
                result.append(line)
            result.append(self._parser.get_border_top_bottom_chunks(header))
        for data_row in self._parsed_data_lines:
            self._parser.set_row(data_row)
            for line in self._parser.get_line_by_line_chunks(border):
                result.append(line)
        result.append(self._parser.get_border_top_bottom_chunks(end))
        return result

    def _create_3(self, header, border) -> list[list[OutputChunk]]:
        result: list[list[OutputChunk]] = []
        for header_row in self._parsed_header_lines:
            self._parser.set_row(header_row)
            for line in self._parser.get_line_by_line_chunks(border):
                result.append(line)
            result.append(self._parser.get_border_top_bottom_chunks(header))
        for data_row in self._parsed_data_lines:
            self._parser.set_row(data_row)
            for line in self._parser.get_line_by_line_chunks(border):
                result.append(line)
        return result

    # ------------ styles ---------------
    # das geht so nicht mehr
    def _style_grid_utf_8(self) -> list[list[OutputChunk]]:
        return self._create_1(
            "utf_8_top_1",
            "utf_8_parting_1",
            "utf_8_parting_2",
            "utf_8_bottom_1",
            "utf_8_border_1",
        )

    def _style_grid_ascii(self) -> list[list[OutputChunk]]:
        return self._create_1(
            "ascii_parting_1",
            "ascii_parting_2",
            "ascii_parting_1",
            "ascii_parting_1",
            "ascii_border_1",
        )

    def _style_github_ascii(self) -> list[list[OutputChunk]]:
        return self._create_3("ascii_parting_4", "ascii_border_1")

    def _style_simple_ascii(self) -> list[list[OutputChunk]]:
        return self._create_3("ascii_parting_5", "ascii_border_3")

    def _style_presto_ascii(self) -> list[list[OutputChunk]]:
        return self._create_3("ascii_parting_6", "ascii_border_2")

    def _style_psql_ascii(self) -> list[list[OutputChunk]]:
        return self._create_2(
            "ascii_parting_1",
            "ascii_parting_7",
            "ascii_parting_1",
            "ascii_border_1",
        )

    def _style_orgtbl_ascii(self) -> list[list[OutputChunk]]:
        return self._create_3("ascii_parting_7", "ascii_border_1")

    def _style_rst_ascii(self) -> list[list[OutputChunk]]:
        return self._create_2(
            "ascii_parting_8",
            "ascii_parting_8",
            "ascii_parting_8",
            "ascii_border_4",
        )

    def _style_outline_ascii(self) -> list[list[OutputChunk]]:
        return self._create_2(
            "ascii_parting_1",
            "ascii_parting_2",
            "ascii_parting_1",
            "ascii_border_1",
        )

    def end_table(self):
        pass  # marker for end of table

    ###################################################################################################
    ### override ###
    def _create_header_lines_1(self) -> Iterator[list[OutputChunk]]:
        # fmt:off
        for line in self._header_lines:
            self._parser_table_main_header.set_row([line])
            for line in self._parser_table_main_header.get_line_by_line_chunks("header"):
                yield line
        # fmt:on

    ### override ###
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

    ### override ###
    def _create_row_data(self) -> Iterator[list[OutputChunk]]:
        # fmt:off
        yield self._get_special_horizontal_line("utf_8_parting_2")
        yield self._parser_data.get_row_chunks("utf_8_border_1")
        self.__row_counter +=1
        # fmt:on

    ### override ###
    def _create_table_end(self) -> Iterator[list[OutputChunk]]:
        yield self._parser_data.get_border_top_bottom_chunks("utf_8_bottom_1")

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
        self._actual_parsed_header_lines = []
        self._parser_header_row.set_row(row)
        for line in self._create_row_header():
            self._parsed_header_lines.append(line)
            self._actual_parsed_header_lines.append(line)

    def add_row_data(self, row: list[str]):
        self._actual_parsed_data_lines = []
        self._parser_data.set_row(row)
        for line in self._create_row_data():
            self._parsed_data_lines.append(line)
            self._actual_parsed_data_lines = []

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

    def get_complete_table(self) -> list[OutputChunk]:
        return
