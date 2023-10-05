from typing import NamedTuple
from Texttables_2 import OutputChunk


class _CellTextDistance(NamedTuple):
    left: str
    right: str
    sum: int


class InputCell:
    """
    Check and modiefie the input
    ┌──────────────────────┬────────────────────────┐
    │          CellWrapper │        CellWrapper     │
    │                      │                        │
    └──────────────────────┴────────────────────────┘
    """

    def __init__(self, text: str, *args, **kwargs) -> None:
        self._corner_top_left = ""
        self._corner_top_right = "+"
        self._corner_bottom_left = ""
        self._corner_bottom_right = "+"
        self._delimiter_top = "-"
        self._delimiter_bottom = "-"
        self._delimeter_left = ""
        self._delimeter_right = "|"
        self._width = 20
        self._hight = 1
        self._align = "l"
        self._valign = "t"
        self._newline = "\n"

        self.args = args
        self.kwargs = kwargs
        self._cell_text = []  # modiefied with valign
        # originial input
        self._cell_text_input = self.__check_cell_input(text).split("\n")
        self.set_cell_text_to_border()

    def get_line(self, position: int = None):
        if position is None:
            return self._cell_text
        return self._cell_text[position]

    def _cell_parser(self):
        self.__parse_1_sort()
        yield self.__parse_2_top_line()

        for text in self._cell_text:
            yield self.__parse_3_text_cell(text)
        yield self.__parse_4_bottom_line()

    def __parse_1_sort(self):
        """sort the list

        Raises:
            Exception: _description_
        """
        if len(self._cell_text_input) < self._hight:
            raise (
                f"given cell hight in lines is smaler then given data. {self._cell_text_input}"
            )
        self._cell_text = self._cell_text_input.copy()
        diff = self._hight - len(self._cell_text_input)
        if self._valign in ("t", "top"):
            for i in range(diff):
                self._cell_text.append("")
        elif self._valign == ("b", "bottom"):
            for i in range(diff):
                self._cell_text.insert(0, "")
        elif self._valign == ("m", "middle"):
            center_top = diff // 2
            center_bottom = (diff + 1) // 2
            for k in range(center_bottom):
                self._cell_text.append("")
            for j in range(center_top):
                self._cell_text.insert(0, "")
        else:
            raise Exception

    def __parse_2_top_line(self) -> list[OutputChunk]:
        return [
            OutputChunk(self._corner_top_left, "frame"),
            OutputChunk(self._width * self._delimiter_top, "frame"),
            OutputChunk(self._corner_top_right, "frame"),
            OutputChunk(self._newline, "end_of_line"),
        ]

    def __parse_3_text_cell(self, line_text: str) -> list[OutputChunk]:
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

    def __parse_4_bottom_line(self):
        return [
            OutputChunk(self._corner_bottom_left, "frame"),
            OutputChunk(self._width * self._delimiter_bottom, "frame"),
            OutputChunk(self._corner_bottom_right, "frame"),
            OutputChunk(self._newline, "end_of_line"),
        ]

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


class InputCell_Left(InputCell):
    def __init__(self, text: str, *args, **kwargs) -> None:
        super().__init__(text, *args, **kwargs)
        self._corner_top_left = "+"
        self._corner_top_right = "+"
        self._corner_bottom_left = "+"
        self._corner_bottom_right = "+"
        self._delimiter_top = "-"
        self._delimiter_bottom = "-"
        self._delimeter_left = "|"
        self._delimeter_right = "|"
        self._width = 20
        self._hight = 1
        self._align = "r"
        self._valign = "t"
        self._newline = ""


# row_wrapper = [InputCell("hallo"),InputCell("hallo")]

cells: list[InputCell] = [InputCell_Left("hallo"), InputCell("hallo")]

# for cell in cells:
#     for chunk in cell._cell_parser():
#         print(chunk, end="")
result = []
for i in range(6):
    for cell in cells:
        result += next(cell._cell_parser())
        # except
for chunk in result:
    print(chunk, end="")
# chunk_line_0 = next(cells[0]._cell_parser())
# chunk_line_1 = next(cells[1]._cell_parser())
# for chunk in chunk_line_0:
#     print(chunk, end="")
# for chunk in chunk_line_1:
#     print(chunk, end="")


# for cell in cells:
#     chunk_line = cell._cell_parser()
#     for chunk in chunk_line:
#         print(chunk, end="")
# print(c._cell_parser())
