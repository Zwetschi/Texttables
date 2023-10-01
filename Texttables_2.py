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
    left: int
    right: int
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


class CharsetTuple(NamedTuple):
    """chars for the horizontal lines

    draw is the information if the line is created

    Args:
        NamedTuple (_type_): _description_
    """

    charset: list
    draw: bool


class Charset:
    def __init__(self) -> None:
        self.frame_top: CharsetTuple = None
        self.frame_border: CharsetTuple = None
        self.frame_bottom: CharsetTuple = None
        self.frame_special: CharsetTuple = None

    def ready(self):
        for key, value in self.__dict__.items():
            if value is None:
                raise AttributeError(f"please set a {key} in the charset")

    def get_attributes(self):
        return self.__dict__.items()

    def get_att_by_name(self, name) -> CharsetTuple:
        return self.__getattribute__(name)

    def set(self, frame_name, data: CharsetTuple):
        if frame_name not in self.__dict__.keys():
            raise KeyError(f"{frame_name} must be in {self.__dict__.keys()}")
        self.__setattr__(frame_name, data)


class Charsets:
    def __init__(self) -> None:
        self.standart_1 = Charset()
        # horizontal frames
        self.standart_1.frame_top = CharsetTuple(["┌", "─", "┬", "┐"], True)
        self.standart_1.frame_border = CharsetTuple(["│", "│", "│"], True)
        self.standart_1.frame_bottom = CharsetTuple(["└", "─", "┴", "┘"], True)
        self.standart_1.frame_special = CharsetTuple(["╞", "═", "╪", "╡"], True)
        self.standart_2 = Charset()
        self.standart_2.frame_top = CharsetTuple(["├", "─", "┼", "┤"], True)
        self.standart_2.frame_border = CharsetTuple(["│", "│", "│"], True)
        self.standart_2.frame_bottom = CharsetTuple(["└", "─", "┴", "┘"], True)
        self.standart_2.frame_special = CharsetTuple(["╞", "═", "╪", "╡"], True)
        self.unicode = Charset()
        self.unicode.frame_top = CharsetTuple(["+", "-", "+", "+"], True)
        self.unicode.frame_border = CharsetTuple(["|", "|", "|"], True)
        self.unicode.frame_bottom = CharsetTuple(["+", "-", "+", "+"], True)
        self.unicode.frame_special = CharsetTuple(["+", "_", "+", "+"], True)

    def get_charset(self, charset_name: str) -> Charset:
        """try to return a instance of Charset by name"""
        if charset_name not in self.__dict__.keys():
            raise KeyError(f"{charset_name} is not in {self.__dict__.keys()}")
        return self.__getattribute__(charset_name)

    def set(self, charset_name: str, frame: str, chars, draw):
        if charset_name not in self.__dict__.keys():
            self.__setattr__(charset_name, Charset())
        # if chars is None:
        # # look if chars was set  # TODO
        # actual_chars = self.get_charset(charset_name).get_att_by_name(frame).charset
        # if actual_chars is None

        self.get_charset(charset_name).set(frame, CharsetTuple(chars, draw))

    def check_charset(self, charset_name: str):
        """check if there are set all attributes in a charset

        if there is any charset (top bottom special or boarder) no set by user
        copie the standart to active charset

        Args:
            name (str): name of the charset
        """
        for key, value in self.get_charset(charset_name).get_attributes():
            if value is None:
                # if nothing is chosen, set to standart
                self.set(charset_name, key, self.standart_1.get_att_by_name(key))


class RowParser:
    def __init__(self) -> None:
        self._charsets = Charsets()
        self._row: list[CellWrapper] = []
        self.__line_stack_sizes = []
        self._result_row: list[OutputPart] = []
        self.set_distance_in_cell()
        self.set_charset_active("standart_1")

    def set_cell_width(self, cells_width: list[int]):
        """cols widht\n
        ├────────20──────────┼─────────20────────┼──────────20─────────┤\n"""
        try:
            if len(cells_width) != len(self._cells_allign):
                raise IndexError(
                    f"Amount off cells widths ({self._cells_allign}) and cells allign ({cells_width}) is not the same"
                )
        except AttributeError:
            pass
        for width in cells_width:
            if not isinstance(width, int):
                raise ValueError(f"{width} in {cells_width} is not an integer!")
        self._cells_width = cells_width

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
        try:
            if len(self._cells_width) != len(cells_allign):
                raise IndexError(
                    f"Amount off cells widths ({self._cells_width}) and cells allign ({cells_allign}) is not the same"
                )
        except AttributeError:
            pass

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

    def get_special_horizontal_line(self) -> list[OutputPart]:
        chars = self._charsets.get_charset(self._active_charset).frame_special
        if chars.draw:
            return self.__parse_horizontal_line_without_text(chars.charset)
        else:
            return []

    def clear_row(self):
        self._row = []
        self.__line_stack_sizes = []

    def add_row(self, row: list[str]):
        for cell in row:
            self.add_cell(cell)

    def get_row(self, row: list[str] = None) -> list[OutputPart]:
        """if row is None the row is parsed with added data
        if row is a list with string, these strings are parsed

        (dount forget do call clear_row when finished)

        Args:
            row (list[str], optional): _description_. Defaults to None.

        Returns:
            list[OutputPart]: _description_
        """
        if row is not None:
            self.add_row(row)
        return self._result_row

    def add_cell(self, cell_text: str, **kwargs):
        """add a cell to row (dount forget do call clear_row when finished)

        kwargs is to set outher attributes like color
        this attributes is on kwargs["your_attrubure"] on the output objects
        (not every output wrapper has this attribut!)
        """
        cell_wrapper = CellWrapper(cell_text, **kwargs)
        self.__line_stack_sizes.append(cell_wrapper.get_line_amount())
        self._row.append(cell_wrapper)

    def run(self):
        self._parse_row()
        self.clear_row()

    def set_frame_vertical_line_top(
        self, draw: bool = True, charset: str = None, chars: list[str] = None
    ):
        self._set_frame_vertical_line(draw, charset, chars, "top")

    def set_frame_border(self, charset: str = None, chars: list[str] = None):
        self._set_frame_vertical_line(True, charset, chars, "border")

    def set_frame_vertical_line_bottom(
        self, draw: bool = True, charset: str = None, chars: list[str] = None
    ):
        self._set_frame_vertical_line(draw, charset, chars, "bottom")

    def set_frame_vertical_line_special(
        self, charset: str = None, chars: list[str] = None
    ):
        self._set_frame_vertical_line(True, charset, chars, "special")

    def set_charset_active(self, charset: str = None):
        """set a charset active

        Args:
            charset (str, optional): the charset whitch shoul be active. Defaults to "standart".

        Raises:
            ValueError: _description_
        """
        self._charsets.check_charset(charset)
        self._active_charset = charset

    def set_distance_in_cell(self, left=1, right=1):
        """set the distance to the frame on the text in echt cell"""
        if left < 0 and right < 0:
            raise ValueError(
                f"the distance must be bigger then 0! (left: {left}, right:{right}"
            )
        self._cell_distance_text = CellTextDistance(left, right, left + right)

    def set_cols_distance_from_left(self, distances: list[int]):
        """
        ├──────────────────20┼─────────────────40┼───────────────────60┤\n
        """
        self._cells_width = []
        reminder = 0
        for distance in distances:
            self._cells_width.append(distance - reminder)
            reminder = distance

    def _set_frame_vertical_line(
        self, draw: bool, charset: str, chars: list[str], frame: str
    ):
        knew_modes = ("top", "bottom", "border", "special")
        prefix = "frame_"
        if frame not in knew_modes:
            raise Exception(f"mode not in {knew_modes}")
        if frame == "border":
            self.__check_chars_len(chars, 3, "border")
        else:
            self.__check_chars_len(chars, 4, "line")
        if charset is None:
            charset = self._active_charset

        self._charsets.set(charset, prefix + frame, chars, draw)
        self.set_charset_active(charset)

    def _max_cell_amount(self) -> int:
        # return len(self._cells_allign)
        return len(self._cells_width)

    def _get_vertical_line_top(self) -> list[OutputPart]:
        chars = self._charsets.get_charset(self._active_charset).frame_top
        if chars.draw:
            return self.__parse_horizontal_line_without_text(chars.charset)
        return []

    def _get_vertical_line_bottom(self) -> list[OutputPart]:
        chars = self._charsets.get_charset(self._active_charset).frame_bottom
        if chars.draw:
            return self.__parse_horizontal_line_without_text(chars.charset)
        return []

    def _get_vertical_line_special(self) -> list[OutputPart]:
        chars = self._charsets.get_charset(self._active_charset).frame_special
        if chars.draw:
            return self.__parse_horizontal_line_without_text(chars.charset)
        return []

    def _get_max_line_stack_size(self) -> int:
        return max(self.__line_stack_sizes)

    # -----------------------------------------------------------------------------------------------------
    # Parser
    # -----------------------------------------------------------------------------------------------------
    def _parse_row(self):
        """create the complete row

        Args:
            border_chars (list[str]): the chars used for the boarder in the table

        Returns:
            list[OutputPart]: the parsed line with spaces, boarders, text and **kwargs
        """
        # │               fgtZZZZff           │                ggg │                      hhh             │
        # left distance space text distance middle        ....       middle distance space text distance right
        self._result_row = []
        self.__check_row_for_data()
        self.__check_row_ready()
        self.__parse_step_1_fill_up()
        self._result_row += self._get_vertical_line_top()
        # for evry line in the cells iterarte over all cells and try to get the line
        for line_counter in range(max(self.__line_stack_sizes)):
            self._result_row += self.__parse_line_with_text(line_counter)
        self._result_row += self._get_vertical_line_bottom()

    def __parse_text_inside_line(self, line_text: str, widh: int, allign) -> str:
        spaces_left = self._cell_distance_text.left * " "
        spaces_right = self._cell_distance_text.left * " "
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

    def __parse_line_with_text(self, line_counter: int) -> list[OutputPart]:
        """parse one line of the table

        (one row can have more then one line)

        Args:
            border_chars (list[str]): the chars used for the boarder in the table
            line_counter (int): the position of the line in a List on a CellWrapper class

        Returns:
            list[OutputPart]: the parsed line with spaces, boarders, text and **kwargs
        """
        border_chars = self._charsets.get_charset(
            self._active_charset
        ).frame_border.charset
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

    def __parse_horizontal_line_without_text(
        self, chars: list[str]
    ) -> list[OutputPart]:
        """┌────────────────────┬────────────────────┬────────────────────┐
        left   between     middle   between     middle   between    right"""
        chars = chars.copy()
        result_line = []
        if len(chars) == 4:
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

    def __check_chars_len(self, chars, check_len, variant):
        """only check if the chars input make sense

        variant: 'line' or 'text' (dount save)"""

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
            if variant == "line"
            else sensible_lengt_text_line
        )
        if chars is None:
            return
        if len(chars) != check_len and len(chars) != func(len(self._cells_width)):
            raise TypeError(
                f"The legth of of boarder chars must be {check_len} by standart\n"
                + f"wrong chars: {chars}\n"
                + "in a special case there can be chosen a boarder char for every single cell\n"
                + f"the table is set to a len of {len(self._cells_width)} cells so there have to be {func(len(self._cells_width))} boarder chars"
            )

    def __check_row_for_data(self):
        """if there are no data in the table to parse, create dummy data"""
        if len(self._row) == 0:
            for _ in self._cells_allign:
                self.add_cell("")

    def __check_row_ready(self):
        """check if the len of data and the amount of cells is the same

        Raises:
            IndexError: _description_
        """
        if len(self._row) < self._max_cell_amount():
            return False
        elif len(self._row) == self._max_cell_amount():
            return True
        else:
            data = [x.get_line() for x in self._row]
            raise IndexError(
                f"the lenth of rows: {len(self._row)} - {data} - is not the same as \n"
                + f"the lenght of amount of cells {len(self._cells_width)} - {self._cells_width} -\n"
                + " if you want to start a new row you may call clear_row"
            )

    # -------------------------------------------------------------------------------------------
    def __repr__(self) -> str:
        return "".join([str(x) for x in self._result_row])


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

    def __parse_header_lines(self):
        # TODO brauch auch nen wrapper
        return "\n".join(self._main_header)

    def _parse_table(self):
        result_table = []

    def __repr__(self) -> str:
        return "TODO"
