from typing import NamedTuple
from Texttables_2 import OutputChunk


class _CellTextDistance(NamedTuple):
    left: str
    right: str
    sum: int


class CellParser:
    """
    Check and modiefie the input
    ┌──────────────────────┬────────────────────────┐
    │          CellWrapper │        CellWrapper     │
    │                      │                        │
    └──────────────────────┴────────────────────────┘
    """

    def __init__(
        self, text: str, hight: int, width: int = "auto", *args, **kwargs
    ) -> None:
        self._init_chars_and_align()
        self._cell_text_original_input = self.__check_cell_input(text).split("\n")
        self._cell_text = []  # modiefied data with valign
        self.args = args
        self.kwargs = kwargs
        self._set_width(width)
        self._hight = hight
        self.set_cell_text_to_border()

        # register iterator. (iter starting new when iterator() is called)
        self.get = self._cell_parser()

    def get_line(self, position: int = None):
        if position is None:
            return self._cell_text
        return self._cell_text[position]

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

        self._distance_border_text = _CellTextDistance(
            left, right, len(left) + len(right)
        )
        self._set_cell_width_auto()  # callback

    def _set_width(self, width):
        if width == "auto":
            self._do_auto_width = True
        else:
            self._do_auto_width = False

    def _init_chars_and_align(self):
        self._corner_top_left = ""
        self._corner_top_right = "+"
        self._corner_bottom_left = ""
        self._corner_bottom_right = "+"
        self._delimiter_top = "-"
        self._delimiter_bottom = "-"
        self._delimeter_left = ""
        self._delimeter_right = "|"
        self._align = "c"
        self._valign = "t"
        self._newline = ""

    def _set_cell_width_auto(self):
        if self._do_auto_width:
            line_widths = [len(line) for line in self._cell_text_original_input]
            self._width = max(line_widths) + self._distance_border_text.sum

    def _cell_parser(self):
        self._parse_1_sort()
        yield self._parse_2_top_line()

        for text in self._cell_text:
            yield self._parse_3_text_cell(text)
        yield self._parse_4_bottom_line()

    def _parse_1_sort(self):
        """sort the list

        Raises:
            Exception: _description_
        """
        if len(self._cell_text_original_input) > self._hight:
            raise Exception(
                f"given cell hight in lines is smaler then given data. {self._cell_text_original_input}"
            )
        self._cell_text = self._cell_text_original_input.copy()
        diff = self._hight - len(self._cell_text_original_input)
        if self._valign in ("t", "top"):
            for i in range(diff):
                self._cell_text.append("")
        elif self._valign in ("b", "bottom"):
            for i in range(diff):
                self._cell_text.insert(0, "")
        elif self._valign in ("m", "middle"):
            center_top = diff // 2
            center_bottom = (diff + 1) // 2
            for k in range(center_bottom):
                self._cell_text.append("")
            for j in range(center_top):
                self._cell_text.insert(0, "")
        else:
            raise Exception(f"{self._valign} is not in t,b,m")

    def _parse_2_top_line(self) -> list[OutputChunk]:
        return [
            OutputChunk(self._corner_top_left, "frame"),
            OutputChunk(self._width * self._delimiter_top, "frame"),
            OutputChunk(self._corner_top_right, "frame"),
            OutputChunk(self._newline, "end_of_line"),
        ]

    def _parse_3_text_cell(self, line_text: str) -> list[OutputChunk]:
        result = [
            OutputChunk(self._delimeter_left, "frame"),
            OutputChunk(self._distance_border_text.left, "cell_align_left"),
        ]
        spaces_align = self._width - len(line_text) - self._distance_border_text.sum
        if self._align in ("r", "right"):
            result.append(
                OutputChunk(
                    spaces_align * " " + line_text, "text", *self.args, **self.kwargs
                )
            )
        elif self._align in ("l", "left"):
            result.append(
                OutputChunk(
                    line_text + spaces_align * " ", "text", *self.args, **self.kwargs
                )
            )
        elif self._align in ("c", "center"):
            center_left = (spaces_align + 1) // 2 * " "
            center_right = spaces_align // 2 * " "
            result.append(
                OutputChunk(
                    center_left + line_text + center_right,
                    "text",
                    *self.args,
                    **self.kwargs,
                )
            )
        else:
            raise Exception("never happen")
        result.append(OutputChunk(self._distance_border_text.right, "cell_align_right"))
        result.append(OutputChunk(self._delimeter_right, "frame"))
        result.append(OutputChunk(self._newline, "end_of_line"))
        return result

    def _parse_4_bottom_line(self):
        return [
            OutputChunk(self._corner_bottom_left, "frame"),
            OutputChunk(self._width * self._delimiter_bottom, "frame"),
            OutputChunk(self._corner_bottom_right, "frame"),
            OutputChunk(self._newline, "end_of_line"),
        ]

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


# in a method add_row first check if chars like "+-++ is set" when yes row[0].corner_left = chars[0] row[-1].corner_right = chars[-1]
class InputCell_Left(CellParser):
    def __init__(
        self, text: str, hight: int, width: int = "auto", *args, **kwargs
    ) -> None:
        super().__init__(text, hight, width, *args, **kwargs)

    def _init_chars_and_align(self):
        self._corner_top_left = "+"
        self._corner_top_right = "+"
        self._corner_bottom_left = "+"
        self._corner_bottom_right = "+"
        self._delimiter_top = "-"
        self._delimiter_bottom = "-"
        self._delimeter_left = "|"
        self._delimeter_right = "|"
        self._align = "c"
        self._valign = "t"
        self._newline = ""


class InputCell_Right(CellParser):
    def __init__(
        self, text: str, hight: int, width: int = "auto", *args, **kwargs
    ) -> None:
        super().__init__(text, hight, width, *args, **kwargs)

    def _init_chars_and_align(self):
        self._corner_top_left = ""
        self._corner_top_right = "+"
        self._corner_bottom_left = ""
        self._corner_bottom_right = "+"
        self._delimiter_top = "-"
        self._delimiter_bottom = "-"
        self._delimeter_left = ""
        self._delimeter_right = "|"
        self._align = "l"
        self._valign = "b"
        self._newline = "\n"


class Colum:
    def __init__(self, column: list[CellParser]) -> None:
        self.column = column


class Row:
    def __init__(self, row: list[CellParser]) -> None:
        self.row = row

    def print(self):
        while True:
            try:
                for cell in self.row:
                    line = next(cell.get)
                    for chunk in line:
                        print(chunk, end="")
            except StopIteration:
                break


class TextTable:
    def __init__(self) -> None:
        self.table = []

    def run(self):
        for element in self.table:
            if isinstance(element, Row):
                pass
            elif isinstance(element, Colum):
                pass
            elif isinstance(element, CellParser):
                pass


c = Row(
    [
        InputCell_Left("hehjhuhhhh\nheee", 8),
        CellParser("hallo", 8),
        InputCell_Right("hallo", 8),
    ]
)
c.print()
