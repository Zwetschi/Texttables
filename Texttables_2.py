from typing import NamedTuple


class LineCellWrapper:
    """
    ┌──────────────────────┬────────────────────────┐
    │      LineCellWrapper │        LineCellWrapper │
    │      LineCellWrapper │                        │
    └──────────────────────┴────────────────────────┘
    """

    # final input class
    # line_text is the attibite which is parsed
    # kwargs carry outher information like color (for evry line in cell, its copied from cell to each line)
    def __init__(self, line_text: str, **kwargs) -> None:
        self.line_text = line_text
        self.kwargs = kwargs


class CellWrapper:
    """
    ┌──────────────────────┬────────────────────────┐
    │          CellWrapper │        CellWrapper     │
    │                      │                        │
    └──────────────────────┴────────────────────────┘
    """

    def __init__(self, text: str, **kwargs) -> None:
        self.cell_text: list[LineCellWrapper] = []
        self.kwargs = kwargs
        self.__set_cell_text(text)

    def __set_cell_text(self, text: str):
        for line in text.split("\n"):
            self.cell_text.append(LineCellWrapper(line, **self.kwargs))

    def fill_up_lines(self, fill_empty_lines: int):
        for empty_line in range(fill_empty_lines):
            self.cell_text.append(LineCellWrapper("", **self.kwargs))

    def get_line_amount(self):
        return len(self.cell_text)


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


class CharsetTuple(NamedTuple):
    charset: list
    draw: bool


class Charset:
    def __init__(self) -> None:
        self.vertical_line_top: CharsetTuple = None
        self.frame_boarder: CharsetTuple = None
        self.vertical_line_bottom: CharsetTuple = None
        self.vertical_line_spec: CharsetTuple = None


class Charsets:
    def __init__(self) -> None:
        self.standart = Charset()

        self.__set_standarts()

    def get(self, name: str) -> Charset:
        """try to return a instance of Charset by name

        if not exists create it"""
        try:
            return self.__getattribute__(name)
        except AttributeError:
            self.__setattr__(name, Charset())
            return self.__getattribute__(name)

    def __set_standarts(self):
        self.standart.vertical_line_top = CharsetTuple(["┌", "─", "┬", "┐"], True)
        self.standart.frame_boarder = CharsetTuple(["│", "│", "│"], True)
        self.standart.vertical_line_bottom = CharsetTuple(["└", "─", "┴", "┘"], True)
        self.standart.vertical_line_spec = CharsetTuple(["╞", "═", "╪", "╡"], True)


class Parser:
    def __init__(self, cells_width, cells_allign) -> None:
        self._charsets = Charsets()
        self._row: list[CellWrapper] = []
        self.__line_stack_sizes = []
        self.set_cell_width(cells_width)
        self.set_cell_allign(cells_allign)
        self.set_distance_cell()
        self.set_actual_used_charset()

    def _get_max_line_stack_size(self):
        return max(self.__line_stack_sizes)

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
        if not isinstance(cells_allign, list):
            raise TypeError(f"allign must be a list allign input: {cells_allign}")

        for value in cells_allign:
            if value not in ("r", "l", "c"):
                raise ValueError(
                    f"allign must be a list 'r', 'l', 'c' (allign input: {cells_allign})"
                )
        self._cells_allign = cells_allign

    def get_special_line(self):
        chars = self._charsets.get(self._actual_used_charset).vertical_line_top
        if chars.draw:
            return self.__create_vertical_line_without_text(chars.charset)

    def __create_vertical_line_without_text(self, chars: list[str]) -> list[OutputPart]:
        """┌────────────────────┬────────────────────┬────────────────────┐
        left   between     middle   between     middle   between    right"""
        chars = chars.copy()
        if len(chars) == 4:
            left, between, middle, right = chars
            chars = (
                [left]
                + [between, middle] * (len(self._cells_width) - 1)
                + [between]
                + [right]
            )
        else:
            left = chars[0]
            right = chars[-1]
        chars = chars[1:]
        result_line = [OutputPart("left", "frame")]
        for position, cell_width in zip(range(0, len(chars), 2), self._cells_width):
            result_line.append(
                OutputPart(chars[position] * cell_width + chars[position + 1], "frame")
            )
        result_line.append(OutputPart("\n", "end_of_line"))
        return result_line

    # def get_row(self):
    #     for cell in self._row:
    #         print(cell)

    def add_cell(self, cell_text: str, **kwargs):
        """add a cell to row"""
        cell_text = self.__check_cell_input(cell_text)
        cell = CellWrapper(cell_text, **kwargs)
        self.__line_stack_sizes.append(cell.get_line_amount())
        self._row.append(cell)

    # def get_row(self, data_row: list[str]) -> list:  # TODO
    #     self.__check_amount_of_cells(data_row)
    #     chars = self._charsets.get(self._actual_used_charset).frame_boarder

    #     for data, cell_width, cell_allign in zip(
    #         data_row, self._cells_width, self._cells_allign
    #     ):
    #         pass
    #         # self._row.add_cell()

    #     if chars.draw:
    #         pass

    def set_vertical_line_top(self, draw, charset: str = "standart", chars=None):
        self.__check_chars_len(chars)
        self._charsets.get(charset).vertical_line_top = CharsetTuple(chars, draw)

    def set_frame_boarder(self, draw, charset: str = "standart", chars=None):
        self.__check_chars_len(chars, 3)
        self._charsets.get(charset).frame_boarder = CharsetTuple(chars, draw)

    def set_vertical_line_bottom(self, draw, charset: str = "standart", chars=None):
        self.__check_chars_len(chars)
        self._charsets.get(charset).vertical_line_bottom = CharsetTuple(chars, draw)

    def set_vertical_line_special(self, draw, charset: str = "standart", chars=None):
        self.__check_chars_len(chars)
        self._charsets.get(charset).vertical_line_spec = CharsetTuple(chars, draw)

    def set_actual_used_charset(self, charset: str = "standart"):
        self._actual_used_charset = charset

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
        self._cells_width = cells_width

    def set_distance_cell(self, left=1, right=1):
        """set the distance to the frame on the text in echt cell"""
        self._cell_distance_text = CellTextDistance(left, right, left + right)

    # def set_cols_distance_from_left(self, distances: list[int]):
    #     """cols distance from the left\n
    #     ├──────────────────20┼─────────────────40┼───────────────────60┤\n"""

    #     y = distances[:]
    #     distances.insert(0, 0)
    #     breite_real = [
    #         ((y[i + 1] - y[i])) - (self._table_obj.distances[-1] + 1) // 2
    #         for i in range(len(y) - 1)
    #     ]
    #     self._table_obj.cols_width = breite_real
    #     self._table_obj.table_width = sum(breite_real) + len(y)
    def _get_vertical_line_top(self):
        chars = self._charsets.get(self._actual_used_charset).vertical_line_top
        if chars.draw:
            return self.__create_vertical_line_without_text(chars.charset)

    def _get_vertical_line_bottom(self):
        chars = self._charsets.get(self._actual_used_charset).vertical_line_bottom
        if chars.draw:
            return self.__create_vertical_line_without_text(chars.charset)

    def _get_vertical_line_special(self):
        chars = self._charsets.get(self._actual_used_charset).vertical_line_spec
        if chars.draw:
            return self.__create_vertical_line_without_text(chars.charset)

    # -----------------------------------------------------------------------------------------------------
    # Parser
    # -----------------------------------------------------------------------------------------------------
    def __parse_text_inside_line(self, line_text: str, widh: int, allign) -> str:
        spaces_left = self._cell_distance_text.left * " "
        spaces_right = self._cell_distance_text.left * " "
        spaces_allign = widh - len(line_text) - self._cell_distance_text.sum
        if allign in ("r", "right"):
            return spaces_left + spaces_allign * " " + line_text + spaces_right
        elif allign in ("l", "left"):
            return spaces_left + line_text + spaces_allign * " " + spaces_right
        elif allign in ("c", "center"):
            center_left = int(spaces_allign / 2 + 1) * " "
            center_right = int(spaces_allign / 2) * " "
            return spaces_left + center_left + line_text + center_right + spaces_right
        else:
            raise Exception("never happen")

    def __parse_step_2_create_line_with_text(
        self, border_chars: list[str], line_counter: int
    ) -> list[OutputPart]:
        result_line: list[OutputPart] = [OutputPart(border_chars[0], "frame")]

        for _actual_cell, width, allign, border_char in zip(
            self._row, self._cells_width, self._cells_allign, border_chars
        ):
            line_text_line = _actual_cell.cell_text[line_counter].line_text
            self.__check_text_and_cell_width(line_text_line, width)
            alligned_text = self.__parse_text_inside_line(line_text_line, width, allign)

            result_line.append(
                OutputPart(alligned_text, token="text", **_actual_cell.kwargs)
            )
            result_line.append(OutputPart(border_char, "frame"))
            result_line.append(OutputPart("\n", "end_of_line"))
        return result_line

    def __parse_step_3_create_row_with_text(self, border_chars: list[str]) -> list:
        """│               fgtZZZZff           │                ggg │                      hhh             │
        left distance space text distance middle        ....       middle distance space text distance right
        """
        border_chars = border_chars.copy()
        if len(border_chars) == 3:
            left, middle, right = border_chars
            border_chars = [left] + [middle] * (len(self._cells_width) - 1) + [right]
        else:
            left = border_chars[0]
            right = border_chars[-1]
        # for evry line in the cells iterarte over all cells and try to get the line
        result_row = []
        for line_counter in range(max(self.__line_stack_sizes)):
            result_row += self.__parse_step_2_create_line_with_text(
                border_chars, line_counter
            )

    def __parse_step_1_fill_up(self):
        """add a emty field to the row in line in wich its necesary

        (fill up)"""

        for _actual_cell in self._row:
            if _actual_cell.get_line_amount() != self._get_max_line_stack_size():
                _actual_cell.fill_up_lines(
                    self._get_max_line_stack_size() - _actual_cell.get_line_amount()
                )

    # -----------------------------------------------------------------------------------------------------
    # Checks
    # -----------------------------------------------------------------------------------------------------
    def __check_text_and_cell_width(self, line_text, width):
        if len(line_text) > width - self._cell_distance_text.sum:
            raise ValueError(
                f"text: {line_text} is wider then cell width: {width} + cell distanes from lfet and right:{self._cell_distance_text.sum} "
            )

    def __check_chars_len(self, chars: list[str], check_len=4):
        if len(chars) != check_len:
            raise TypeError(f"the leth of an set of boarder chars must be {check_len}!")

    def __check_amount_of_cells(self, data_row):
        if len(self._cells_width) != len(data_row):
            raise IndexError(
                "the amount of cells and cells of data is not the same"
                + f"ERROR in line:{data_row}"
            )

    def __check_cell_input(self, cell_text) -> str:
        if not isinstance(cell_text, (str, float, int)):
            raise TypeError(
                "The input must be str float int." + f"the input is: {cell_text}"
            )
        elif isinstance(cell_text, (float, int)):
            return str(cell_text)
        return cell_text
