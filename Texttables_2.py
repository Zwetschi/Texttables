from typing import NamedTuple


class _CellTextDistance(NamedTuple):
    left: str
    right: str
    sum: int


class _BorderChars:
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
        if name is None or chars is None:
            return
        self.__last_top_bottom_key = name
        self._border_chars_top_bottom[name] = chars

    def get_boarder_top_bottom(self, name: str) -> list[str]:
        if name is None:
            return self._border_chars_top_bottom[self.__last_top_bottom_key]
        if name not in self._border_chars_top_bottom.keys():
            raise Exception(
                f"'{name}' dount exist! boarder options:\n"
                + str(list((self._border_chars_top_bottom.keys())))
                + "\n"
                + f"To use a your own chars, set boarder chars first by calling '{self.set_boarder_top_bottom.__name__}'"
            )
        return self._border_chars_top_bottom[name]

    def set_boarder_left_right(self, name: str, chars: list[str]):
        if name is None or chars is None:
            return
        self.__last_left_right_key = name
        self._border_chars_left_right[name] = chars

    def get_boarder_left_right(self, name: str):
        if name is None:
            return self._border_chars_left_right[self.__last_left_right_key]
        if name not in self._border_chars_left_right.keys():
            raise KeyError(
                f"{name} is not in {self._border_chars_left_right.keys()}\n"
                + f"set boarder chars first by caling '{self.set_boarder_left_right.__name__}''"
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


class OutputChunk:
    TOKENS = [
        "frame",
        "text",
        "end_of_line",
        "cell_align_right",
        "cell_align_left",
        "indent",
        "white_space",
    ]

    def __init__(self, chunk: str, token: str, *args) -> None:
        self.__chunk = chunk
        self.__set_token(token)
        self.args = args

    def get_chunk(self):
        return self.__chunk

    def get_token(self) -> str:
        """_summary_

        Returns:
            str: "frame", "text", "end_of_line", "end_of_row"
        """
        return self.__token

    def __set_token(self, token):
        if token not in self.TOKENS:
            raise KeyError(f"token must be in {self.TOKENS}")
        self.__token = token

    def __repr__(self) -> str:
        return self.__chunk


class InputCell:
    """
    Check and modiefie the input
    ┌──────────────────────┬────────────────────────┐
    │          CellWrapper │        CellWrapper     │
    │                      │                        │
    └──────────────────────┴────────────────────────┘
    """

    def __init__(self, text: str, *args, **kwargs) -> None:
        self.args = args
        self.kwargs = kwargs
        self.cell_text = []  # modiefied with valign
        self._cell_text_input = []  # originial input
        self.__set_cell_text(text)

    def get_line(self, position: int = None):
        if position is None:
            return self.cell_text
        return self.cell_text[position]

    def get_line_amount(self):
        return len(self._cell_text_input)

    def __set_cell_text(self, text: str):
        text = self.__check_cell_input(text)
        self._cell_text_input: list[str] = text.split("\n")

    def __check_cell_input(self, cell_text) -> str:
        if not isinstance(cell_text, (str, float, int)):
            raise TypeError(
                "The input must be str, float or int.\n"
                + f"the input is: {cell_text}"
                + "if you want to input an objekt you can use *args in add_cell"
            )
        elif isinstance(cell_text, (float, int)):
            return str(cell_text)
        return cell_text


class LineParser:
    def __init__(self, rise_parsing_errors=False, end_of_line=True) -> None:
        self._charsets = _BorderChars()
        self._input_row: list[InputCell] = []
        self.__lines_in_cells = []  # how many lines are in every single cell
        self._set_rise_parsing_errors(rise_parsing_errors)
        self._set_end_of_line(end_of_line)
        self.set_cell_text_to_border()
        self.set_line_indent()
        self.set_line_outdent()
        self._cells_align = []
        self._cells_valign = []
        self._cells_width = []

    def set_cell_aligns(self, cells_align: list[str]):
        """set cell align

        set a align for evry single cell
        'c': center
        'r': right
        'l'. left

        Args:
            cells_align (list[str]): example: ['c', 'r', 'l'] for a table with 3 colls

        Raises:
            IndexError: _description_
            TypeError: _description_
            ValueError: _description_
        """

        if isinstance(cells_align, str):
            cells_align = list(cells_align)
        if not isinstance(cells_align, list):
            raise TypeError(
                f"align must be a list or string - align input: {cells_align}"
            )
        for value in cells_align:
            if value not in ("r", "l", "c"):
                raise ValueError(
                    f"all aligns must be 'r', 'l' or 'c' - align input: {value} - {cells_align}"
                )
        self._cells_align = cells_align

    def set_cell_valign(self, cells_valign: list[str]):
        if isinstance(cells_valign, str):
            cells_valign = list(cells_valign)
        if not isinstance(cells_valign, list):
            raise TypeError(
                f"vertical align must be a list or string - vertical align input: {cells_valign}"
            )
        for value in cells_valign:
            if value not in ("t", "m", "b"):
                raise ValueError(
                    f"all aligns must be 't', 'm' or 'b' - vertical align input: {value} - {cells_valign}"
                )
        self._cells_valign = cells_valign

    def set_cell_widths(self, cells_width: list[int]):
        """cols widht\n
        ├────────20──────────┼─────────20────────┼──────────20─────────┤\n"""
        for width in cells_width:
            if not isinstance(width, int):
                raise ValueError(f"{width} in {cells_width} is not an integer!")
            if width <= 0:
                raise ValueError(
                    f"a cell cant be 0 or smaler ({width} in {cells_width}"
                )
        self._cells_width = cells_width

    def set_line_indent(self, align: int = 0):
        """Set an align before the line to get more distance from left"""
        self._left_line_indent: str = align * " "

    def set_line_outdent(self, align: int = 0):
        """Set an align before the line to get more distance from left"""
        self._left_line_outdent: str = align * " "

    def set_cols_distance_from_left(self, distances: list[int]):
        """
        ├──────────────────20┼─────────────────40┼───────────────────60┤\n
        """
        # that is so complicated because
        # when a table with 3 cells, and a table with 5 cells
        # and the right distacne from booath tables is 100
        # in the table with 3 cells are missing 2 chars because of the vertical boarders
        dist = distances.copy()
        dist.insert(0, 0)
        breite_real = [
            ((dist[i + 1] - dist[i])) - (self._cell_distance_text.sum + 1) // 2
            for i in range(len(dist) - 1)
        ]
        self.set_cell_widths(breite_real)

    def set_border_chars_left_right(self, name: str, chars: list[str]):
        """─ │ ┌ ┐ └ ┘ ├ ┤ ┬ ┴ ┼ ═ ║ ╒ ╓ ╔ ╕ ╖ ╗ ╘ ╙ ╚ ╛ ╜ ╝ ╞ ╟ ╠ ╡ ╢ ╣ ╤ ╥ ╦ ╧ ╨ ╩ ╪ ╫ ╬
        ─ ━ │ ┃ ┄ ┅ ┆ ┇ ┈ ┉  ┊┋ ┌ ┍ ┎ ┏ ┐ ┑ ┒ ┓ └ ┕ ┖ ┗ ┘ ┙ ┚ ┛ ├ ┝ ┞ ┟ ┠ ┡ ┢ ┣ ┤ ┥ ┦ ┧
        ┨ ┩ ┪ ┫ ┬ ┭ ┮ ┯ ┰ ┱ ┲ ┳ ┴ ┵ ┶ ┷ ┸ ┹ ┺ ┻ ┼ ┽ ┾ ┿ ╀ ╁ ╂ ╃ ╄ ╅ ╆ ╇ ╈ ╉ ╊ ╋ ╌ ╍╎ ╏ ═
        ║ ╒ ╓ ╔ ╕ ╖ ╗ ╘ ╙╚ ╛ ╜ ╝ ╞ ╟ ╠ ╡ ╢ ╣ ╤ ╥ ╦ ╧ ╨ ╩ ╪ ╫ ╬ ╭ ╮ ╯╰ ╴ ╵ ╶ ╷ ╸"""
        chars = self.__check_border_chars(name, chars, check_len=3)
        if chars:
            self._charsets.set_boarder_left_right(name, chars)

    def set_border_chars_top_bottom(self, name: str, chars: list[str]):
        """─ │ ┌ ┐ └ ┘ ├ ┤ ┬ ┴ ┼ ═ ║ ╒ ╓ ╔ ╕ ╖ ╗ ╘ ╙ ╚ ╛ ╜ ╝ ╞ ╟ ╠ ╡ ╢ ╣ ╤ ╥ ╦ ╧ ╨ ╩ ╪ ╫ ╬
        ─ ━ │ ┃ ┄ ┅ ┆ ┇ ┈ ┉  ┊┋ ┌ ┍ ┎ ┏ ┐ ┑ ┒ ┓ └ ┕ ┖ ┗ ┘ ┙ ┚ ┛ ├ ┝ ┞ ┟ ┠ ┡ ┢ ┣ ┤ ┥ ┦ ┧
        ┨ ┩ ┪ ┫ ┬ ┭ ┮ ┯ ┰ ┱ ┲ ┳ ┴ ┵ ┶ ┷ ┸ ┹ ┺ ┻ ┼ ┽ ┾ ┿ ╀ ╁ ╂ ╃ ╄ ╅ ╆ ╇ ╈ ╉ ╊ ╋ ╌ ╍╎ ╏ ═
        ║ ╒ ╓ ╔ ╕ ╖ ╗ ╘ ╙╚ ╛ ╜ ╝ ╞ ╟ ╠ ╡ ╢ ╣ ╤ ╥ ╦ ╧ ╨ ╩ ╪ ╫ ╬ ╭ ╮ ╯╰ ╴ ╵ ╶ ╷ ╸"""
        chars = self.__check_border_chars(name, chars, check_len=4)
        if chars:
            self._charsets.set_boarder_top_bottom(name, chars)

    def set_cell_text_to_border(self, left: str = " ", right: str = " "):
        """set the distance to the frame on the text in echt cell\n
        left = Y = " " \n
        right = X = " " \n
        ┌────────────────────┐\n
        │Y               oneX│\n
        │Y               oneX│\n
        └────────────────────┘\n
        """
        if not isinstance(left, str) or not isinstance(left, str):
            raise ValueError(f"left and right must be string!")

        self._cell_distance_text = _CellTextDistance(
            left, right, len(left) + len(right)
        )

    def _set_rise_parsing_errors(self, x: bool):
        """hide parsing error to get a table with to smal cells instead an error

        ugly is better then nothing

        Args:
            x (bool): _description_

        Raises:
            Exception: _description_
        """
        if not isinstance(x, bool):
            raise Exception(f"Must be bool")
        self._rise_parsing_errors = x

    def _set_end_of_line(self, x: bool):
        """newline at the end of line

        Args:
            x (bool): _description_

        Raises:
            Exception: _description_
        """
        if not isinstance(x, bool):
            raise Exception(f"Must be bool")
        self._end_of_line = x

    def _add_cell(self, input_cell: str | InputCell, *args, **kwargs):
        """add a cell to row (dount forget do call clear_row when finished)

        kwargs is to set outher attributes like color
        this attributes is on kwargs["your_attrubure"] on the output objects
        (not every output wrapper has this attribut!)
        """
        if isinstance(input_cell, InputCell):
            self.__lines_in_cells.append(input_cell.get_line_amount())
            self._input_row.append(input_cell)
        elif isinstance(input_cell, (str, int, float)):
            cell_wrapper = InputCell(input_cell, *args, **kwargs)
            self.__lines_in_cells.append(cell_wrapper.get_line_amount())
            self._input_row.append(cell_wrapper)
        else:
            raise Exception(
                f"Input must me string or {InputCell}, input is {input_cell}"
            )

    def set_row(self, row: list[str] | list[InputCell]):
        """add a new row and delete the old data"""
        self.clear_raw_data()
        for cell in row:
            self._add_cell(cell)

    def get_border_top_bottom_advanced(
        self, boarder_chars_name: str = None
    ) -> list[OutputChunk]:
        """_summary_

        Args:
            boarder_chars_name (str, optional): strg+f _standart_border_chars_top_bottom or try any string
            Defaults to None. If None always the last name is used which was set

        Returns:
            list[OutputPart]: of a horizontal line. For example ┌──────┬───────┐newline
        """
        return self.__parse_line_without_text(boarder_chars_name)

    def get_border_top_bottom(self, boarder_chars_name: str = None) -> str:
        """

        Args:
            boarder_chars_name (str, optional): strg+f _standart_border_chars_top_bottom or try any string
            Defaults to None.

            if None always the last name is used which was set

        Returns:
            str: only the string of a horizontal line. For example ┌──────┬───────┐newline
        """
        return "".join(
            [str(part) for part in self.__parse_line_without_text(boarder_chars_name)]
        )

    def get_line_by_line_advanced(
        self, boarder_chars_name: str = None
    ) -> list[OutputChunk]:
        # implementet to have the option parse tables on left in future
        self.__check_amount_of_cells()
        self.__parse_step_1_fill_up()
        # for evry line in the cells iterarte over all cells and try to get the line
        for line_counter in range(max(self.__lines_in_cells)):
            yield self.__parse_line_with_text(line_counter, boarder_chars_name)

    def get_row_adwanced(self, boarder_chars_name: str = None) -> list[OutputChunk]:
        """_summary_

        Args:
            boarder_chars_name (str, optional): try any string.
            Defaults to None. If None always the last name is used which was set

        Returns:
            list[OutputPart]: _description_
        """
        result = []
        for line in self.get_line_by_line_advanced(boarder_chars_name):
            result += line
        return result

    def get_row(self, boarder_chars_name: str = None) -> str:
        """_summary_

        Args:
            boarder_chars_name (str, optional): border_1.
            Defaults to None. If None always the last name is used which was set

        Returns:
            str: example:
        """

        return "".join(
            [str(part) for part in self.get_row_adwanced(boarder_chars_name)]
        )

    def clear_raw_data(self):
        """delete the last raw input data (not parsed data)"""
        self._input_row = []
        self.__lines_in_cells = []

    # -----------------------------------------------------------------------------------------------------
    # Parser
    # -----------------------------------------------------------------------------------------------------

    def __parse_text_inside_cell(
        self, line_text: str, widh: int, align, _actual_cell: InputCell
    ) -> list[OutputChunk]:
        result = [OutputChunk(self._cell_distance_text.left, "cell_align_left")]
        spaces_align = widh - len(line_text) - self._cell_distance_text.sum
        if align in ("r", "right"):
            result.append(
                OutputChunk(spaces_align * " " + line_text, "text", *_actual_cell.args)
            )
        elif align in ("l", "left"):
            result.append(
                OutputChunk(line_text + spaces_align * " ", "text", *_actual_cell.args)
            )
        elif align in ("c", "center"):
            center_left = (spaces_align + 1) // 2 * " "
            center_right = spaces_align // 2 * " "
            result.append(
                OutputChunk(
                    center_left + line_text + center_right,
                    "text",
                    *_actual_cell.args,
                )
            )
        else:
            if self._rise_parsing_errors:
                raise Exception("never happen")
        result.append(OutputChunk(self._cell_distance_text.right, "cell_align_right"))
        return result

    def __parse_line_with_text(
        self, line_counter: int, boarder_chars_name: str = None
    ) -> list[OutputChunk]:
        """parse one line of the table

        (one row can have more then one line)

        Args:
            border_chars (list[str]): the chars used for the boarder in the table
            line_counter (int): the position of the line in a List on a CellWrapper class

        Returns:
            list[OutputPart]: the parsed line with spaces, boarders, text and *args
        """
        # │               fgtZZZZff           │                ggg │                      hhh             │
        # left distance space text distance middle        ....       middle distance space text distance right
        border_chars = self._charsets.get_boarder_left_right(boarder_chars_name)
        if len(self._cells_width) == 0:
            raise Exception("pls set cell with before parsing rows!")
        if len(border_chars) == 3:
            left, middle, right = border_chars
            border_chars = [left] + [middle] * (len(self._cells_width) - 1) + [right]

        result_line: list[OutputChunk] = [
            OutputChunk(self._left_line_indent, "indent"),
            OutputChunk(border_chars[0], "frame"),
        ]

        for _actual_cell, width, align, border_char in zip(
            self._input_row, self._cells_width, self._cells_align, border_chars[1:]
        ):
            cell_text_line = _actual_cell.get_line(line_counter)
            self.__check_text_and_cell_width(cell_text_line, width)
            result_line += self.__parse_text_inside_cell(
                cell_text_line, width, align, _actual_cell
            )

            result_line.append(OutputChunk(border_char, "frame"))
        result_line.append(OutputChunk(self._left_line_outdent, "white_space"))
        if self._end_of_line:
            result_line.append(OutputChunk("\n", "end_of_line"))
        return result_line

    def __parse_step_1_fill_up(self):
        """add a emty field to the row in line in wich its necesary

        (fill up)"""

        for actual_cell, valign in zip(self._input_row, self._cells_valign):
            actual_cell.cell_text = actual_cell._cell_text_input.copy()
            diff = max(self.__lines_in_cells) - actual_cell.get_line_amount()
            if valign == "t":
                for i in range(diff):
                    actual_cell.cell_text.append("")
            elif valign == "b":
                for i in range(diff):
                    actual_cell.cell_text.insert(0, "")
            elif valign == "m":
                center_top = diff // 2
                center_bottom = (diff + 1) // 2
                for k in range(center_bottom):
                    actual_cell.cell_text.append("")
                for j in range(center_top):
                    actual_cell.cell_text.insert(0, "")
            else:
                raise Exception

    def __parse_line_without_text(self, boarder_chars_name: str) -> list[OutputChunk]:
        """┌────────────────────┬────────────────────┬────────────────────┐
        left   between     middle   between     middle   between    right"""

        chars = self._charsets.get_boarder_top_bottom(boarder_chars_name).copy()
        if len(self._cells_width) == 0:
            raise Exception("pls set cell with before parsing rows!")
        if len(chars) == 4:
            # create one char for every place in line
            left, between, middle, right = chars
            chars = (
                [left]
                + [between, middle] * (len(self._cells_width) - 1)
                + [between]
                + [right]
            )

        result_line = [
            OutputChunk(self._left_line_indent, "indent"),
            OutputChunk(chars[0], "frame"),
        ]
        chars = chars[1:]
        for position, cell_width in zip(range(0, len(chars), 2), self._cells_width):
            result_line.append(
                OutputChunk(chars[position] * cell_width + chars[position + 1], "frame")
            )
        result_line.append(OutputChunk(self._left_line_outdent, "white_space"))
        if self._end_of_line:
            result_line.append(OutputChunk("\n", "end_of_line"))
        return result_line

    # -----------------------------------------------------------------------------------------------------
    # Checks
    # -----------------------------------------------------------------------------------------------------
    def __check_text_and_cell_width(self, line_text, width):
        if len(line_text) > width - self._cell_distance_text.sum:
            error_message = f"'{line_text}' is larger then cell width {width} - {self._cell_distance_text.sum} (cell distanes from left and right)\n minimum cell width is: {len(line_text)+ self._cell_distance_text.sum}"
            if self._rise_parsing_errors:
                raise ValueError(error_message)
            print(f"WARNING: {error_message}")

    def __check_border_chars(
        self, name: str, chars: list[str], check_len: int
    ) -> list[str]:
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
        if name is None and chars is None:
            return False
        if isinstance(chars, str):
            chars = list(chars)
        if len(self._cells_width) == 0:
            raise AttributeError(
                "Before set the border chars, set the cell widhts by calling "
                + f"'{self.set_cell_widths.__name__}' or '{self.set_border_chars_left_right.__name__}'"
            )
        if len(chars) != check_len and len(chars) != func(len(self._cells_width)):
            raise TypeError(
                f"The legth of of boarder chars must be {check_len} by standart\n"
                + f"Wrong chars: {chars}\n"
                + "In a special case there can be chosen a boarder char for every single place in cell.\n"
                + f"The table len is {len(self._cells_width)} cells, so there have to be {func(len(self._cells_width))} boarder chars, but there are {len(chars)}"
            )
        return chars

    def __check_amount_of_cells(self):
        """check if the len of data and the amount of cells is the same

        Raises:
            IndexError: _description_
        """
        if len(self._input_row) == 0:
            raise Exception("There is no row to parse")
        if not (
            len(self._input_row)
            == len(self._cells_width)
            == len(self._cells_align)
            == len(self._cells_valign)
        ):
            raise IndexError(
                "The lenght of data cells, cell width and cell align ist not the same!\n"
                + f"data: (len {len(self._input_row)}) {[x.get_line() for x in self._input_row]}\n"
                + f"cells width: (len {len(self._cells_width)}) {self._cells_width}\n"
                + f"cells align: (len {len(self._cells_align)}) {self._cells_align}\n"
                + f"cells valign: (len {len(self._cells_valign)}) {self._cells_valign}\n"
            )


class TextTable_Styles:
    def __init__(self) -> None:
        # 1. a partling line between rows
        # 2  only parting between header and table
        # ... ===== ===== =======
        # ... A     B     A and B
        # ... ===== ===== =======
        # ... False False False
        # ... True  False False
        # ... False True  False
        # ... True  True  True
        # ... ===== ===== =======

        # foo    bar    baz
        # ====== ====== ======
        # data 1 data 2 data 3
        # data 4 data 5 data 6

        # +########+########+########+
        # |header 1|header 2|header 3|
        # +========+========+========+
        # |data 1  |  data 2| data 3 |
        # +--------+--------+--------+
        # |data 4  |  data 5| data 6 |
        # +________+________+________+

        #         '|header 1  |  header 2| header 3 |\n'
        # ...     '+==========+==========+==========+\n'
        # ...     '|data 1    |    data 2|  data 3  |\n'
        # ...     '+----------+----------+----------+\n'
        # ...     '|data 4    |    data 5|  data 6  |\n'
        # ...     '+__________+__________+__________+\n'
        pass


class TextTable_Fast:
    def __init__(self) -> None:
        pass

    # first row i iterpreted as header, (bool)
    # add the complete table (with header) in ine list
    # and get back the string. only string
    # u can use fixe styles ()
    # auto align center, auto cell widt max (iterate over the table on setting)


class TextTable:
    def __init__(self) -> None:
        self._main_header = []
        self._parser_header = LineParser()
        self._parser_data = LineParser()
        self._actual_return = []
        self.__row_counter = 0
        self.__header_rows = []
        self.__data_rows = []
        self._special_horizontal_borders = []

    def add_header_lines(self, header_lines: list[str]):
        """add the lines of the header (not cells)"""
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
        self._parser_header.set_cell_widths(cells_width)
        self._parser_data.set_cell_widths(cells_width)

    def set_cols_distance_from_left(self, distances: list[int]):
        self._parser_header.set_cols_distance_from_left(distances)
        self._parser_data.set_cols_distance_from_left(distances)

    def set_cell_valign(self, cells_valign: list[str]):
        self._parser_header.set_cell_valign(cells_valign)
        self._parser_data.set_cell_valign(cells_valign)

    def set_cell_align_header(self, cells_align: list[str]):
        self._parser_header.set_cell_aligns(cells_align)

    def set_cell_align_data(self, cells_align: list[str]):
        self._parser_data.set_cell_aligns(cells_align)

    def set_special_horizontal_border(self, borders: int | list[int]):
        self._special_horizontal_borders = borders

    def add_row_header(self, row: list[str]):
        self._parser_header.set_row(row)
        self.__header_rows.append(row)

    def add_row_data(self, row: list[str]):
        self._parser_data.set_row(row)
        self.__data_rows.append(row)

    def get_row_header(self):
        # fmt:off
        result= self._parser_header.get_border_top_bottom_advanced("utf_8_top_1")
        result += self._parser_header.get_row_adwanced("utf_8_border_1")
        result += self._parser_header.get_border_top_bottom_advanced("utf_8_parting_1")
        # fmt:on
        return result

    def get_row_data(self):
        # fmt:off
        result =self._get_special_horizontal_line("utf_8_parting_2")
        result += self._parser_data.get_row_adwanced("utf_8_border_1")
        self.__row_counter +=1
        # fmt:on
        return result

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
                return self._parser_data.get_border_top_bottom_advanced(name)
        elif isinstance(self._special_horizontal_borders, list):
            if self.__row_counter in self._special_horizontal_borders:
                return self._parser_data.get_border_top_bottom_advanced(name)
        return []

    def get_table_end(self):
        return self._parser_data.get_border_top_bottom_advanced("utf_8_bottom_1")

    def get_complete(self) -> list[OutputChunk]:
        result = []
        for header_row in self.__header_rows:
            self._parser_header.set_row(header_row)
            result += self.get_row_header()
        for data_row in self.__data_rows:
            self._parser_data.set_row(data_row)
            result += self.get_row_data()
        result += self.get_table_end()
        return result

    def clear_table(self):
        self.__data_rows = []
        self.__header_rows = []

    def _create_table_header(self):
        pass


class Texttables:
    def __init__(self) -> None:
        super().__init__()
        self._texttable = list[TextTable] = []

    def add_row_header(self, row, table: int = 0):
        pass

    def get_complete(self) -> list[OutputChunk]:
        result = []
        for header_row in self.__header_rows:
            self._parser_header.set_row(header_row)
            result += self.get_row_header()
        for data_row in self.__data_rows:
            self._parser_data.set_row(data_row)
            result += self.get_row_data()
        result += self.get_table_end()
        return result
