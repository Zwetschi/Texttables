from typing import NamedTuple


class CellWrapper:
    """
    ┌──────────────────────┬────────────────────────┐
    │          CellWrapper │        CellWrapper     │
    │                      │                        │
    └──────────────────────┴────────────────────────┘
    """

    def __init__(self, text: str, **kwargs) -> None:
        self._cell_text: list[str] = []
        self.kwargs = kwargs
        self.__set_cell_text(text)

    def fill_up_lines(self, fill_empty_lines: int):
        for empty_line in range(fill_empty_lines):
            self._cell_text.append("")

    def get_line_amount(self):
        return len(self._cell_text)

    def get_line(self, position: int = None):
        if position is None:
            return self._cell_text
        return self._cell_text[position]

    def __set_cell_text(self, text: str):
        text = self.__check_cell_input(text)
        for line in text.split("\n"):
            self._cell_text.append(line)

    def __check_cell_input(self, cell_text) -> str:
        if not isinstance(cell_text, (str, float, int)):
            raise TypeError(
                "The input must be str, float or int.\n"
                + f"the input is: {cell_text}"
                + "if you want to input an objekt you can use **kwargs in add_cell"
            )
        elif isinstance(cell_text, (float, int)):
            return str(cell_text)
        return cell_text


class CellTextDistance(NamedTuple):
    left: str
    right: str
    sum: int


class OutputPart:
    TOKENS = ["frame", "text", "end_of_line", "end_of_row"]

    def __init__(self, part: str, token: str, **kwargs) -> None:
        self.__part = part
        self.__set_token(token)
        self.kwargs = kwargs

    def get_part(self):
        return self.__part

    def __set_token(self, token):
        if token not in self.TOKENS:
            raise KeyError(f"token must be in {self.TOKENS}")
        self.__token = token

    def get_token(self) -> str:
        """_summary_

        Returns:
            str: "frame", "text", "end_of_line", "end_of_row"
        """
        return self.__token

    def __repr__(self) -> str:
        return self.__part


class BorderCharsSets:
    CHARS_UNICODE_1 = "─ │ ┌ ┐ └ ┘ ├ ┤ ┬ ┴ ┼ ═ ║ ╒ ╓ ╔ ╕ ╖ ╗ ╘ ╙ ╚ ╛ ╜ ╝ ╞ ╟ ╠ ╡ ╢ ╣ ╤ ╥ ╦ ╧ ╨ ╩ ╪ ╫ ╬"
    CHARS_UNICODE_2 = "─ ━ │ ┃ ┄ ┅ ┆ ┇ ┈ ┉  ┊┋ ┌ ┍ ┎ ┏ ┐ ┑ ┒ ┓ └ ┕ ┖ ┗ ┘ ┙ ┚ ┛ ├ ┝ ┞ ┟ ┠ ┡ ┢ ┣ ┤ ┥ ┦ ┧"
    CHARS_UNICODE_3 = "┨ ┩ ┪ ┫ ┬ ┭ ┮ ┯ ┰ ┱ ┲ ┳ ┴ ┵ ┶ ┷ ┸ ┹ ┺ ┻ ┼ ┽ ┾ ┿ ╀ ╁ ╂ ╃ ╄ ╅ ╆ ╇ ╈ ╉ ╊ ╋ ╌ ╍╎ ╏ ═"
    CHARS_UNICODE_4 = (
        "║ ╒ ╓ ╔ ╕ ╖ ╗ ╘ ╙╚ ╛ ╜ ╝ ╞ ╟ ╠ ╡ ╢ ╣ ╤ ╥ ╦ ╧ ╨ ╩ ╪ ╫ ╬ ╭ ╮ ╯╰ ╴ ╵ ╶ ╷ ╸ "
    )

    def __init__(self) -> None:
        # standarts are splitet in char familys
        # sometimes there aar encoding problems
        self.__last_top_bottom_key: str = "utf_8_top_1"
        self.__last_left_right_key: str = "utf_8_border_1"
        self._border_chars_left_right = {}
        self._border_chars_top_bottom = {}

        self._standart_border_chars_top_bottom = {
            "utf_8_top_1": ["┌", "─", "┬", "┐"],
            "utf_8_bottom_1": ["└", "─", "┴", "┘"],
            "utf_8_parting_1": ["╞", "═", "╪", "╡"],
            "utf_8_parting_2": ["├", "─", "┼", "┤"],
            "utf_8_parting_3": ["├", " ", "┼", "┤"],
            "utf_8_parting_4": ["│", " ", "│", "│"],
            "ascii_top_1": ["+", "-", "+", "+"],
            "ascii_bottom_1": ["+", "_", "+", "+"],
            "ascii_bottom_2": ["+", "=", "+", "+"],
        }

        self._standart_border_chars_left_right = {
            "utf_8_border_1": ["│", "│", "│"],
            "ascii_border_1": ["|", "|", "|"],
            "empty_border": [" ", " ", " "],
        }
        self._init_alternative_keys()

    def set_boarder_top_bottom(self, name: str, chars: list[str]):
        self.__last_top_bottom_key = name
        self._border_chars_top_bottom[name] = chars

    def get_boarder_top_bottom(self, name: str):
        if name is None:
            return self._border_chars_top_bottom[self.__last_top_bottom_key]
        if name not in self._border_chars_top_bottom.keys():
            raise KeyError(
                f"{name} is not in {self._border_chars_top_bottom.keys()}\n"
                + f"set boarder chars first by calling '{self.set_boarder_top_bottom.__name__}'"
            )
        return self._border_chars_top_bottom[name]

    def set_boarder_left_right(self, name: str, chars: list[str]):
        self.__last_left_right_key = name
        self._border_chars_left_right[name] = chars

    def get_boarder_left_right(self, name: str):
        if name is None:
            return self._border_chars_left_right[self.__last_left_right_key]
        if name not in self._border_chars_left_right.keys():
            raise KeyError(
                f"{name} is not in {self._border_chars_left_right.keys()}\n"
                + f"set boarder chars first by calling '{self.set_boarder_left_right.__name__}''"
            )

        return self._border_chars_left_right[name]

    def _init_alternative_keys(self):
        for i, (key, value) in enumerate(
            self._standart_border_chars_top_bottom.items()
        ):
            alternative_key = str(i) * 3  # something like 000 or 111 ....
            self._border_chars_top_bottom[alternative_key] = value
            self._border_chars_top_bottom[key] = value
        for i, (key, value) in enumerate(
            self._standart_border_chars_left_right.items()
        ):
            alternative_key = str(i) * 3
            self._border_chars_left_right[alternative_key] = value
            self._border_chars_left_right[key] = value


class RowParser:
    def __init__(self) -> None:
        self._charsets = BorderCharsSets()
        self._row: list[CellWrapper] = []
        self.__line_stack_sizes = []
        self.set_cell_text_to_border()

    def set_cell_allign(self, cells_allign: list[str]):
        """set cell allign

        set a allign for evry single cell
        'c': center
        'r': right
        'l'. left

        Args:
            cells_allign (list[str]): example: ['c', 'r', 'l'] for a table with 3 colls

        Raises:
            IndexError: _description_
            TypeError: _description_
            ValueError: _description_
        """

        if isinstance(cells_allign, str):
            cells_allign = list(cells_allign)
        if not isinstance(cells_allign, list):
            raise TypeError(
                f"allign must be a list or string - allign input: {cells_allign}"
            )

        for value in cells_allign:
            if value not in ("r", "l", "c"):
                raise ValueError(
                    f"all alligns must be 'r', 'l' or 'c' - allign input: {value} - {cells_allign}"
                )
        self._cells_allign = cells_allign

    def set_cell_width(self, cells_width: list[int]):
        """cols widht\n
        ├────────20──────────┼─────────20────────┼──────────20─────────┤\n"""
        # try:
        #     if len(cells_width) != len(self._cells_allign):
        #         raise IndexError(
        #             f"Amount off cells widths ({self._cells_allign}) and cells allign ({cells_width}) is not the same"
        #         )
        # except AttributeError:
        #     pass
        for width in cells_width:
            if not isinstance(width, int):
                raise ValueError(f"{width} in {cells_width} is not an integer!")
            if width <= 0:
                raise ValueError(
                    f"a cell cant be 0 or smaler ({width} in {cells_width}"
                )
        self._cells_width = cells_width

    def set_cols_distance_from_left(self, distances: list[int]):
        """
        ├──────────────────20┼─────────────────40┼───────────────────60┤\n
        """
        # that is so complicated because
        # when a table with 3 cells, and a table with 5 cells
        # and the right distacne from booath tables is 100
        # in the table with 3 cells are missing 2 chars because of the vertical boarders
        distances.insert(0, 0)
        breite_real = [
            ((distances[i + 1] - distances[i]))
            - (self._cell_distance_text.sum + 1) // 2
            for i in range(len(distances) - 1)
        ]
        self.set_cell_width(breite_real)

    def set_border_chars_left_right(self, name: str, chars: list[str]):
        """─ │ ┌ ┐ └ ┘ ├ ┤ ┬ ┴ ┼ ═ ║ ╒ ╓ ╔ ╕ ╖ ╗ ╘ ╙ ╚ ╛ ╜ ╝ ╞ ╟ ╠ ╡ ╢ ╣ ╤ ╥ ╦ ╧ ╨ ╩ ╪ ╫ ╬
        ─ ━ │ ┃ ┄ ┅ ┆ ┇ ┈ ┉  ┊┋ ┌ ┍ ┎ ┏ ┐ ┑ ┒ ┓ └ ┕ ┖ ┗ ┘ ┙ ┚ ┛ ├ ┝ ┞ ┟ ┠ ┡ ┢ ┣ ┤ ┥ ┦ ┧
        ┨ ┩ ┪ ┫ ┬ ┭ ┮ ┯ ┰ ┱ ┲ ┳ ┴ ┵ ┶ ┷ ┸ ┹ ┺ ┻ ┼ ┽ ┾ ┿ ╀ ╁ ╂ ╃ ╄ ╅ ╆ ╇ ╈ ╉ ╊ ╋ ╌ ╍╎ ╏ ═
        ║ ╒ ╓ ╔ ╕ ╖ ╗ ╘ ╙╚ ╛ ╜ ╝ ╞ ╟ ╠ ╡ ╢ ╣ ╤ ╥ ╦ ╧ ╨ ╩ ╪ ╫ ╬ ╭ ╮ ╯╰ ╴ ╵ ╶ ╷ ╸"""
        chars = self.__check_border_chars(chars, check_len=3)
        self._charsets.set_boarder_left_right(name, chars)

    def set_border_chars_horizontal(self, name, chars: list[str]):
        """─ │ ┌ ┐ └ ┘ ├ ┤ ┬ ┴ ┼ ═ ║ ╒ ╓ ╔ ╕ ╖ ╗ ╘ ╙ ╚ ╛ ╜ ╝ ╞ ╟ ╠ ╡ ╢ ╣ ╤ ╥ ╦ ╧ ╨ ╩ ╪ ╫ ╬
        ─ ━ │ ┃ ┄ ┅ ┆ ┇ ┈ ┉  ┊┋ ┌ ┍ ┎ ┏ ┐ ┑ ┒ ┓ └ ┕ ┖ ┗ ┘ ┙ ┚ ┛ ├ ┝ ┞ ┟ ┠ ┡ ┢ ┣ ┤ ┥ ┦ ┧
        ┨ ┩ ┪ ┫ ┬ ┭ ┮ ┯ ┰ ┱ ┲ ┳ ┴ ┵ ┶ ┷ ┸ ┹ ┺ ┻ ┼ ┽ ┾ ┿ ╀ ╁ ╂ ╃ ╄ ╅ ╆ ╇ ╈ ╉ ╊ ╋ ╌ ╍╎ ╏ ═
        ║ ╒ ╓ ╔ ╕ ╖ ╗ ╘ ╙╚ ╛ ╜ ╝ ╞ ╟ ╠ ╡ ╢ ╣ ╤ ╥ ╦ ╧ ╨ ╩ ╪ ╫ ╬ ╭ ╮ ╯╰ ╴ ╵ ╶ ╷ ╸"""
        chars = self.__check_border_chars(chars, check_len=4)
        self._charsets.set_boarder_top_bottom(name, chars)

    def set_cell_text_to_border(self, left: str = " ", right: str = " "):
        """set the distance to the frame on the text in echt cell
        left = Y = " "
        right = X = " "
        ┌────────────────────┐
        │Y               oneX│
        │Y               oneX│
        └────────────────────┘
        """
        if not isinstance(left, str) or not isinstance(left, str):
            raise ValueError(f"left and right must be string!")

        self._cell_distance_text = CellTextDistance(left, right, len(left) + len(right))

    def add_cell(self, cell_text: str, **kwargs):
        """add a cell to row (dount forget do call clear_row when finished)

        kwargs is to set outher attributes like color
        this attributes is on kwargs["your_attrubure"] on the output objects
        (not every output wrapper has this attribut!)
        """
        cell_wrapper = CellWrapper(cell_text, **kwargs)
        self.__line_stack_sizes.append(cell_wrapper.get_line_amount())
        self._row.append(cell_wrapper)

    def get_horizontal_border(self, boarder_chars_name: str = None) -> list[OutputPart]:
        """_summary_

        Args:
            boarder_chars_name (str, optional): top_1, bottom_1, parting_1, parting_2.
            Defaults to None. If None always the last name is used which was set

        Returns:
            list[OutputPart]: of a horizontal line. For example ┌──────┬───────┐newline
        """
        return self.__parse_line_without_text(boarder_chars_name)

    def get_border_horizontal_string(self, boarder_chars_name: str = None) -> str:
        """

        Args:
            boarder_chars_name (str, optional): top_1, bottom_1, parting_1, parting_2.
            Defaults to None.

            if None always the last name is used which was set

        Returns:
            str: only the string of a horizontal line. For example ┌──────┬───────┐newline
        """
        return "".join(
            [str(part) for part in self.__parse_line_without_text(boarder_chars_name)]
        )

    def get_row(self, boarder_chars_name: str = None) -> list[OutputPart]:
        """_summary_

        Args:
            boarder_chars_name (str, optional): border_1.
            Defaults to None. If None always the last name is used which was set

        Returns:
            list[OutputPart]: _description_
        """
        return self._parse_row_with_text(boarder_chars_name)

    def get_row_string(self, boarder_chars_name: str = None) -> str:
        """_summary_

        Args:
            boarder_chars_name (str, optional): border_1.
            Defaults to None. If None always the last name is used which was set

        Returns:
            str: example:
        """
        return "".join(
            [str(part) for part in self._parse_row_with_text(boarder_chars_name)]
        )

    def clear_data(self):
        self._row = []
        self.__line_stack_sizes = []

    def _max_cell_amount(self) -> int:
        # return len(self._cells_allign)
        return len(self._cells_width)

    def _get_max_line_stack_size(self) -> int:
        return max(self.__line_stack_sizes)

    # -----------------------------------------------------------------------------------------------------
    # Parser
    # -----------------------------------------------------------------------------------------------------
    def _parse_row_with_text(self, boarder_chars_name: str = None) -> list[OutputPart]:
        result_row = []
        self.__check_row_for_data()
        self.__check_amount_of_cells()
        self.__parse_step_1_fill_up()
        # for evry line in the cells iterarte over all cells and try to get the line
        for line_counter in range(max(self.__line_stack_sizes)):
            result_row += self.__parse_line_with_text(line_counter, boarder_chars_name)
        return result_row

    def __parse_text_inside_line(self, line_text: str, widh: int, allign) -> str:
        spaces_left = self._cell_distance_text.left
        spaces_right = self._cell_distance_text.right
        spaces_allign = widh - len(line_text) - self._cell_distance_text.sum
        if allign in ("r", "right"):
            return spaces_left + spaces_allign * " " + line_text + spaces_right
        elif allign in ("l", "left"):
            return spaces_left + line_text + spaces_allign * " " + spaces_right
        elif allign in ("c", "center"):
            center_left = (spaces_allign + 1) // 2 * " "
            center_right = spaces_allign // 2 * " "
            return spaces_left + center_left + line_text + center_right + spaces_right
        else:
            raise Exception("never happen")

    def __parse_line_with_text(
        self, line_counter: int, boarder_chars_name: str = None
    ) -> list[OutputPart]:
        """parse one line of the table

        (one row can have more then one line)

        Args:
            border_chars (list[str]): the chars used for the boarder in the table
            line_counter (int): the position of the line in a List on a CellWrapper class

        Returns:
            list[OutputPart]: the parsed line with spaces, boarders, text and **kwargs
        """
        # │               fgtZZZZff           │                ggg │                      hhh             │
        # left distance space text distance middle        ....       middle distance space text distance right
        border_chars = self._charsets.get_boarder_left_right(boarder_chars_name)
        if len(border_chars) == 3:
            left, middle, right = border_chars
            border_chars = [left] + [middle] * (len(self._cells_width) - 1) + [right]

        result_line: list[OutputPart] = [OutputPart(border_chars[0], "frame")]

        for _actual_cell, width, allign, border_char in zip(
            self._row, self._cells_width, self._cells_allign, border_chars[1:]
        ):
            line_text_line = _actual_cell.get_line(line_counter)
            self.__check_text_and_cell_width(line_text_line, width)
            alligned_text = self.__parse_text_inside_line(line_text_line, width, allign)

            result_line.append(
                OutputPart(alligned_text, token="text", **_actual_cell.kwargs)
            )
            result_line.append(OutputPart(border_char, "frame"))
        result_line.append(OutputPart("\n", "end_of_line"))
        return result_line

    def __parse_step_1_fill_up(self):
        """add a emty field to the row in line in wich its necesary

        (fill up)"""

        for _actual_cell in self._row:
            if _actual_cell.get_line_amount() != self._get_max_line_stack_size():
                _actual_cell.fill_up_lines(
                    self._get_max_line_stack_size() - _actual_cell.get_line_amount()
                )

    def __parse_line_without_text(self, boarder_chars_name: str) -> list[OutputPart]:
        """┌────────────────────┬────────────────────┬────────────────────┐
        left   between     middle   between     middle   between    right"""

        chars = self._charsets.get_boarder_top_bottom(boarder_chars_name).copy()
        result_line = []
        if len(chars) == 4:
            # create one char for every place in line
            left, between, middle, right = chars
            chars = (
                [left]
                + [between, middle] * (len(self._cells_width) - 1)
                + [between]
                + [right]
            )

        result_line.append(OutputPart(chars[0], "frame"))
        chars = chars[1:]
        for position, cell_width in zip(range(0, len(chars), 2), self._cells_width):
            result_line.append(
                OutputPart(chars[position] * cell_width + chars[position + 1], "frame")
            )
        result_line.append(OutputPart("\n", "end_of_line"))
        return result_line

    # -----------------------------------------------------------------------------------------------------
    # Checks
    # -----------------------------------------------------------------------------------------------------
    def __check_text_and_cell_width(self, line_text, width):
        if len(line_text) > width - self._cell_distance_text.sum:
            raise ValueError(
                f"'{line_text}' is larger then cell width {width} - {self._cell_distance_text.sum} (cell distanes from lfet and right)\n"
                + f"minimum cell width is: {len(line_text)+ self._cell_distance_text.sum}"
            )

    def __check_border_chars(self, chars: list[str], check_len: int) -> list[str]:
        """only check if the chars input make sense"""

        def sensible_lengt_hoizontal_line(amount_of_cells):
            """┌────────────────────┬────────────────────┬────────────────────┐
            1           2        3         4          5       6             7 and so on
            """
            if amount_of_cells == 1:
                return 3
            return amount_of_cells * 2 + 1

        def sensible_lengt_text_line(amount_of_cells):
            """
            │      c1 │         c2      │   c3  │     c4 │      c5         │  c6   │
            1         2                 3       4         5                6       7

            """
            return amount_of_cells + 1

        func = (
            sensible_lengt_hoizontal_line
            if check_len == 4
            else sensible_lengt_text_line
        )
        if chars is None:
            raise TypeError("Boarder chars cant be None!")
        if isinstance(chars, str):
            chars = list(chars)
        try:
            if len(chars) != check_len and len(chars) != func(len(self._cells_width)):
                raise TypeError(
                    f"The legth of of boarder chars must be {check_len} by standart\n"
                    + f"Wrong chars: {chars}\n"
                    + "In a special case there can be chosen a boarder char for every single place in cell.\n"
                    + f"The table len is {len(self._cells_width)} cells, so there have to be {func(len(self._cells_width))} boarder chars, but there are {len(chars)}"
                )
        except AttributeError:
            # cells widht is not set
            raise AttributeError(
                "Before set the border chars, set the cell widhts by calling "
                + f"'{self.set_cell_width.__name__}' or '{self.set_border_chars_left_right.__name__}'"
            )
        return chars

    def __check_row_for_data(self):
        """if there are no data in the table to parse, create dummy data"""
        if len(self._row) == 0:
            for _ in self._cells_allign:
                self.add_cell("")

    def __check_amount_of_cells(self):
        """check if the len of data and the amount of cells is the same

        Raises:
            IndexError: _description_
        """

        if not (len(self._row) == len(self._cells_width) == len(self._cells_allign)):
            raise IndexError(
                "The lenght of data cells, cell width and cell allign ist not the same!\n"
                + f"data: (len {len(self._row)}) {[x.get_line() for x in self._row]}\n"
                + f"cells width: (len {len(self._cells_width)}) {self._cells_width}\n"
                + f"cells allign: (len {len(self._cells_allign)}) {self._cells_allign}\n"
            )

    # -------------------------------------------------------------------------------------------
    # def __repr__(self) -> str:
    #     # TODO
    #     return "".join([str(x) for x in self._result_row])


class TextTables:
    def __init__(self) -> None:
        self._main_header = []
        self._row_headers: list[OutputPart] = []
        self._row_data: list[OutputPart] = []
        # self._header_allign = []
        # self._cols_allign = []
        self._parser_header = RowParser()
        self._parser_table = RowParser()

    def add_header_lines(self, header_lines: list[str]):
        if not isinstance(header_lines, (list, str)):
            raise Exception("must be str or list of string")
        if isinstance(header_lines, str):
            self._main_header.append(header_lines)
        elif isinstance(header_lines, list):
            for header_line in header_lines:
                if not isinstance(header_line, str):
                    raise Exception("header must be string")
                self._main_header.append(header_line)

    def set_cell_width(self, cells_width: list[int]):
        self._parser_header.set_cell_width(cells_width)
        self._parser_table.set_cell_width(cells_width)

    def set_cell_allign(self, cells_allign: list[str]):
        self._parser_header.set_cell_width(cells_allign)
        self._parser_table.set_cell_width(cells_allign)

    def add_header_cell(self, cell, **kwargs):
        self._parser_header.add_cell(cell, **kwargs)

    def add_table_cell(self, cell, **kwargs):
        self._parser_table.add_cell(cell, **kwargs)

    def end_header_row(self):
        self._row_headers = self._parser_header.get_row()

    def end_table_row(self):
        self._row_data += self._parser_table.get_row()

    def get(self):
        pass

    def __repr__(self) -> str:
        return "TODO"
