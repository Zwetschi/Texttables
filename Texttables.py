from __future__ import annotations
from typing import List, Any
from dataclasses import dataclass, field
import output


@dataclass
class AdderWrapper:
    """if text is the datatype added to the table, simulate the incomming objects"""

    text: str


@dataclass
class OutgoingTextWrapperLines:
    """class for not loose the information of the incoming objet.\n
    the probem is that i split the string on newlines. so i have to combine each split to each of his own objekts to dount loose information"""

    incomming_obj: Any | AdderWrapper
    text: str


@dataclass
class TextWrapper:
    text: str
    token: str
    cell_id: List[int] = field(default_factory=list)
    input: Any = None


@dataclass
class DataTable:
    header: TextWrapper = field(default=None)
    header_column: List[str] = field(default_factory=list)
    table: List[List[str]] = field(default_factory=list)
    cols_width: list = field(default_factory=list)
    align_cols: List = field(default_factory=list)
    align_header: list = field(default_factory=list)
    distances: list = field(default_factory=list)
    distance_table: int = field(default=20)
    table_width: int = field(default=None)

    vertical_table = True
    vertical_header = True
    verical_top = True
    verical_bottom = True
    vertical_special = False
    verical_normal = True
    speciall = None

    results: List[TextWrapper] = field(default_factory=list)
    # rahmen
    # [oben]                        0
    # [links rechts border header]  1
    # [vlineheader]                 2
    # [links rechts border normal]  3
    # [vline normal]                4
    # [unten]                       5
    # [besonders]                   6
    # chars = [
    #     ["┌", "―", "┬", "―", "┐"],
    #     ["│", " ", "│", " ", "│"],
    #     ["╠", "═", "╪", "═", "╣"],
    #     ["│", " ", "│", " ", "│"],
    #     ["├", "―", "┼", "―", "┤"],
    #     ["└", "―", "┴", "―", "┘"],
    #     ["╠", "═", "╪", "═", "╣"],
    # ]
    chars = [
        ["┌", "─", "┬", "─", "┐"],
        ["│", " ", "│", " ", "│"],
        ["╞", "═", "╪", "═", "╡"],
        ["│", " ", "│", " ", "│"],
        ["├", "─", "┼", "─", "┤"],
        ["└", "─", "┴", "─", "┘"],
        ["╞", "═", "╪", "═", "╡"],
    ]

    def joose_chars(self, header=False):
        """returns the chars for the row lines, v-lines another method"""
        left = self.chars[3][0]
        middle = self.chars[3][2]
        right = self.chars[3][-1]
        b, c = self.cols_width, self.align_cols
        if header:
            b, c = self.cols_width, self.align_header
            left = self.chars[1][0]
            middle = self.chars[3][2]
            right = self.chars[1][-1]
        return b, c, middle, left, right


class SetterControler:
    def __init__(self, parent: DataTable) -> None:
        self._table_obj = parent
        self.distance_cell()

    def cols_width(self, x: List[int]):
        """cols widht\n
        ├────────20──────────┼─────────20────────┼──────────20─────────┤\n"""
        self._table_obj.cols_width = x
        self._table_obj.table_width = sum(x) + len(x) + 1

    def cols_width_left(self, x: List[int]):
        """cols distance from the left\n
        ├──────────────────20┼─────────────────40┼───────────────────60┤\n"""
        y = x[:]
        x.insert(0, 0)
        breite_real = [
            ((y[i + 1] - y[i])) - (self._table_obj.distances[-1] + 1) // 2
            for i in range(len(y) - 1)
        ]
        self._table_obj.cols_width = breite_real
        self._table_obj.table_width = sum(breite_real) + len(y)

    def align_header(self, x: List[str]):
        """align for evry cell\n
        l: left\n
        r:right\n
        c: center"""
        assert len(x) == len(
            self._table_obj.cols_width
        ), "gleiche länge wie Spaltenanzahl eingeben!"
        self._table_obj.align_header = x

    def align_cols(self, x: List[str]):
        """align for evry cell\n
        l: left\n
        r:right\n
        c: center"""
        assert len(x) == len(
            self._table_obj.cols_width
        ), "gleiche länge wie Spaltenanzahl eingeben!"
        self._table_obj.align_cols = x

 

    def distance_cell(self, left=1, right=1):
        """set the distance to the frame on the text in echt cell"""
        self._table_obj.distances = [left,right,left+right]

    def distance_table(self, dis: int):
        self._table_obj.distance_table = dis

    def v_line_top(self, draw=True, chars=["┌", "─", "┬", "─", "┐"]):
        self._table_obj.chars[0] = chars
        self._table_obj.verical_top = draw

    def v_line_normal(self, draw=False, chars=["├", "─", "┼", "─", "┤"]):
        self._table_obj.chars[4] = chars
        self._table_obj.verical_normal = draw

    def v_line_bottom(self, draw=True, chars=["└", "─", "┴", "─", "┘"]):
        self._table_obj.chars[5] = chars
        self._table_obj.verical_bottom = draw

    def v_line_header(self, draw=True, chars=["╞", "═", "╪", "═", "╡"]):
        self._table_obj.chars[2] = chars
        self._table_obj.vertical_header = draw

    def v_line_special(self, x: int, chars=["╞", "═", "╪", "═", "╡"]):
        """all x rows one special v line"""
        assert isinstance(
            x, int
        ), "in special vline mode pls enter a integer\n all entered integer a special vline will be inserted"
        self._table_obj.chars[6] = chars
        self._table_obj.speciall = x
        self._table_obj.vertical_special = True

    def chars(self,chars:List[List[str]] = [
        ["┌", "─", "┬", "─", "┐"],
        ["│", " ", "│", " ", "│"],
        ["╞", "═", "╪", "═", "╡"],
        ["│", " ", "│", " ", "│"],
        ["├", "─", "┼", "─", "┤"],
        ["└", "─", "┴", "─", "┘"],
        ["╞", "═", "╪", "═", "╡"],
    ]) :
        """ 
        [oben]                        0\n
        [links rechts border header]  1\n
        [vlineheader]                 2\n
        [links rechts border normal]  3\n
        [vline normal]                4\n
        [unten]                       5\n
        [special]                     6\n"""
        if chars == 2:
            chars = [
        ["┌", "─", "┬", "─", "┐"],
        ["│", " ", "│", " ", "│"],
        ["╞", "═", "╪", "═", "╡"],
        ["│", " ", "│", " ", "│"],
        ["├", "─", "┼", "─", "┤"],
        ["└", "─", "┴", "─", "┘"],
        ["╞", "═", "╪", "═", "╡"],
    ]   
        elif chars == 1:
            chars = [
        ["┌", "─", "┬", "─", "┐"],
        ["│", " ", "│", " ", "│"],
        ["├", "─", "┼", "─", "┤"],
        ["│", " ", "│", " ", "│"],
        ["├", "─", "┼", "─", "┤"],
        ["└", "─", "┴", "─", "┘"],
        ["╞", "═", "╪", "═", "╡"],
    ]
        else:
            self._table_obj.chars = chars #= 

class AdderControler:
    """add data to the table"""

    def __init__(self, parent: DataTable) -> None:
        self._table_obj = parent

    def header(self, any_data: str):
        """add the column header \n"""
        if isinstance(any_data, str):
            self._table_obj.header = AdderWrapper(any_data)
        else:
            assert hasattr(
                any_data, "text"
            ), "das eingehende objekt muss das attribut text haben auf dem sich der text der Celle befindet"
            self._table_obj.header = any_data

    def header_column(self, data: List[Any]):
        assert len(data) == len(
            self._table_obj.cols_width
        ), "Vorgabe anzahl colums stimmt nicht mit gegebenen überein"
        lehr = []
        for any_data in data:
            if isinstance(any_data, str):
                lehr.append(AdderWrapper(any_data))
            else:
                assert hasattr(
                    any_data, "text"
                ), "das eingehende objekt muss das attribut text haben auf dem sich der text der Celle befindet"
                lehr.append(any_data)
        self._table_obj.header_column = lehr

    def row(self, data: List[Any]):
        """add a row to the table"""
        assert len(data) == len(
            self._table_obj.cols_width
        ), "Vorgabe anzahl colums stimmt nicht mit gegebenen überein"
        lehr = []
        for any_data in data:
            if isinstance(any_data, str):
                lehr.append(AdderWrapper(any_data))
            else:
                assert hasattr(
                    any_data, "text"
                ), "das eingehende objekt muss das attribut text haben auf dem sich der text der Celle befindet"
                lehr.append(any_data)
        self._table_obj.table.append(lehr)


class OneParserControler:
    """pars one single table to a list with obj, only one table\n"""

    def __init__(self, data: DataTable, counter) -> None:
        self.__counter_table = counter
        self.__counter_cell = 0
        self.__counter_line = 0
        self._table_obj = data  # DataTable mit dem ergebnis
        self._run()

    def _create_string_base_header(self):
        """ceate the first heder line\n wird falsch geparst"""
        if self._table_obj.header != None:
            self._add_text_obj(
                " " + self._table_obj.header.text,
                "text",
                [self.__counter_table, -1, 0],
                original=self._table_obj.header,
            )
            self._add_text_obj("\n", "endline", [self.__counter_table, -1, 1])

    def _run(self):
        """vreate the table in form of the objects"""
        self._create_string_base_header()
        self._create_v_cuts(("top", self._table_obj.verical_top))
        self._create_row_new(self._table_obj.header_column, header=True)  # header

        # table data
        for i, row in enumerate(self._table_obj.table):
            if i == 0:
                self._create_v_cuts(
                    ("header", self._table_obj.vertical_header)
                )  # header border
            elif (
                self._table_obj.speciall != None and (i % self._table_obj.speciall) == 0
            ):
                self._create_v_cuts(("special", self._table_obj.vertical_special))
            else:
                self._create_v_cuts(("normal", self._table_obj.verical_normal))
            self._create_row_new(row)
        self._create_v_cuts(("bottom", self._table_obj.verical_bottom))  # bottom

    def _create_row_new(self, row: List[str], header=False):
        """create one complete row with all lines"""
        lines = self._row_to_lines_new(row)
        for line in lines:
            self._create_line_new(line, header)

    def _create_line_new(self, line: List[OutgoingTextWrapperLines], header: bool):
        """create on line, one row can be more then one line"""
        cols_width, align_cols, middle, left, right = self._table_obj.joose_chars(
            header
        )
        self._add_text_obj(left, "frame", self._get_id())
        for cell_str, cols_width, cols_align in zip(line, cols_width, align_cols):
            self._check_string_cell_lenght(cols_width, cell_str.text)
            space = " " * (
                cols_width - len(cell_str.text) - self._table_obj.distances[2]
            )
            self._reate_cell_line_new(cell_str, space, cols_align, middle)
        self._remove_text_obj(
            -1
        )  # remove the right feame, TODO can do bugs if no frame is ausgewählt
        self._add_text_obj(right, "frame", self._get_id())
        self._add_text_obj("\n", "endline", self._get_id())
        self.__counter_line += 1
        self.__counter_cell = 0

    def _reate_cell_line_new(
        self, cell_str: OutgoingTextWrapperLines, space, cols_align, middle
    ):
        """draw the content of one cell (only line)"""

        distance_left = self._table_obj.distances[0] * " "
        distance_right = self._table_obj.distances[1] * " "
        if cols_align == "l":
            self._add_text_obj(distance_left, "frame", self._get_id())
            self._add_text_obj(
                cell_str.text, "text", self._get_id(), cell_str.incomming_obj
            )
            self._add_text_obj(space + distance_right, "frame", self._get_id())
        elif cols_align == "r":
            self._add_text_obj(distance_left + space, "frame", self._get_id())
            self._add_text_obj(
                cell_str.text, "text", self._get_id(), cell_str.incomming_obj
            )
            self._add_text_obj(distance_right, "frame", self._get_id())
        elif cols_align == "c":
            self._add_text_obj(
                distance_left + space[0 : len(space) // 2], "frame", self._get_id()
            )
            self._add_text_obj(
                cell_str.text, "text", self._get_id(), cell_str.incomming_obj
            )
            self._add_text_obj(
                space[0 : (len(space) + 1) // 2] + distance_right,
                "frame",
                self._get_id(),
            )
        self._add_text_obj(middle, "frame", self._get_id())
        self.__counter_cell += 1

    def _create_v_cuts(self, mode: tuple):
        """draw the v lines"""
        mode_dict = {
            ("top", True): self._table_obj.chars[0],
            ("header", True): self._table_obj.chars[2],
            ("normal", True): self._table_obj.chars[4],
            ("bottom", True): self._table_obj.chars[5],
            ("special", True): self._table_obj.chars[6],
        }
        try:
            left, n1, middle, n2, right = mode_dict[mode]
        except KeyError:
            return ""
        ret = left
        for x in self._table_obj.cols_width:
            ret += x * n1
            ret += middle
        self._add_text_obj(ret[:-1] + right, "frame", self._get_id())
        self._add_text_obj("\n", "endline", self._get_id())
        self.__counter_line += 1

    def _check_string_cell_lenght(self, cell_width: int, str_len: str):
        """überprüft ob der text in der zelle länger wie die vorgebene länge ist"""
        if (cell_width - self._table_obj.distances[2]) < len(str_len):
            raise Exception(f"{str_len} ist breiter als die Zelle!!!")

    def _row_to_lines_new(
        self, row: List[AdderWrapper]
    ) -> List[List[OutgoingTextWrapperLines]]:
        cell = []
        line = []
        count = []
        for obj in row:
            count.append(obj.text.count("\n"))
        maxwert = max(count)
        for obj in row:
            splitted = obj.text.split("\n")
            for string in splitted:
                cell.append(OutgoingTextWrapperLines(obj, string))
            while len(cell) <= maxwert:
                cell.append(OutgoingTextWrapperLines(obj, ""))
            line.append(cell)
            cell = []
        return zip(*line)

    def _add_text_obj(self, text: str, token: str, cell_id: List[int], original=None):
        self._table_obj.results.append(TextWrapper(text, token, cell_id, original))

    def _remove_text_obj(self, position):
        self._table_obj.results.pop(position)

    def _get_id(self):
        return [self.__counter_table, self.__counter_line, self.__counter_cell]


class MultiParserControler:
    def __init__(self, tables: List[DataTable], side_mode, distcande=" " * 10) -> None:
        self.tables_objcts = tables
        self._tables = [data_table.results for data_table in tables]
        self.__side_mode = side_mode
        self.__distance = distcande

    def run(self) -> List[TextWrapper]:
        if self.__side_mode:
            return self._create_left()
        else:
            return self._create_normal()

    def _modificate_table(self):
        """füllt die zeilen mitlehrzilen auf damit alle tableen lgeich lang sind"""
        # fmt: off
        last_ids: List[List[int]] = [table[-1].cell_id for table in self._tables]
        max_lines = sorted(self._create_normal(), key=lambda x: x.cell_id[1])[-1].cell_id[1]
        lines_to_add = [max_lines - x[1] for x in last_ids]
        # fmt: on
        for table_number, add_x_lines in enumerate(lines_to_add):
            for i in range(add_x_lines):
                _id = (
                    last_ids[table_number][0],
                    last_ids[table_number][1] + (i + 1),
                    last_ids[table_number][2],
                )

                self._tables[table_number].append(
                    TextWrapper(text="", token="modificated", cell_id=_id)
                )

    def _get_header_length(self, tables_objcts: List[DataTable]):
        lenght_header = []
        for table in tables_objcts:
            try:
                lenght_header.append(len(table.header.text))
            except AttributeError:
                lenght_header.append(0)
        return lenght_header

    def _create_left(self):
        """"""
        anzahl_tabellen = len(self._tables)
        self._modificate_table()
        sort_left_obj = sorted(self._create_normal(), key=lambda x: x.cell_id[1])
        # länge der einzelnen tabellen zeilen

        lenght_header = self._get_header_length(self.tables_objcts)
        lenght = [x.table_width + len(self.__distance) for x in self.tables_objcts]

        for obj in sort_left_obj:
            if obj.token == "endline":
                # wenn ich ein enline erreicht habe zeilenumbruch durch abstand ersettzen
                # außer ich bin in der letzten tabelle

                if not obj.cell_id[0] + 1 == anzahl_tabellen:
                    obj.text = self.__distance
                    if obj.cell_id[1] == -1:
                        obj.text = " " * (
                            lenght[obj.cell_id[0]] - 1 - lenght_header[obj.cell_id[0]]
                        )

            elif obj.token == "modificated":
                # das soll eine komplette lehrzeile werden, modifikatet sind dummy objekte die an die tabellen dran gehäng wurden
                if not obj.cell_id[0] + 1 == anzahl_tabellen:
                    obj.text = " " * lenght[obj.cell_id[0]]
                else:
                    obj.text = "\n"
        return sort_left_obj

    def _create_normal(self) -> List[TextWrapper]:
        """returns the list with tables in one list"""
        result = []
        for table in self._tables:
            for obj in table:
                result.append(obj)
        return result


class Texttables:
    def __init__(self, side_mode) -> None:
        self.__side_mode = side_mode
        self.__table_counter = 0
        self._tables: List[DataTable] = []
        self._init()
        self.finisched = None

    def _init(self):
        self._table_obj = DataTable()

        self.set = SetterControler(self._table_obj)
        self.add = AdderControler(self._table_obj)
        self.add.header("")

    def end(self):
        """add the Table, and reset the old settings"""
        assert (
            len(self._table_obj.cols_width) != 0
        ), "Keine Tabelle gefunden, bitte erst daten zu tabelle hinzufügen"
        OneParserControler(self._table_obj, self.__table_counter)  # create one table
        self._tables.append(self._table_obj)
        self.__table_counter += 1
        self._init()

    def get_str(self) -> str:
        """returns the string of the table"""
        if self.finisched == None:
            self.finisched = MultiParserControler(self._tables, self.__side_mode).run()
        ret = ""
        for obj in self.finisched:
            ret += obj.text
        return ret

    def get_obj(self) -> List[TextWrapper]:
        """returns a stream with textWrappers\n
        if your cells are objekts your input objet is return on TextWapper on the attribut input\n
        the text and the frame of the table is on the atribute text"""
        if self.finisched == None:
            self.finisched = MultiParserControler(self._tables, self.__side_mode).run()
        return self.finisched

    def file(self, path_name=None):
        """create and open a .txt fiele"""
        out = output.Write(path_name)
        out.write(self.get_str())
        out.open()


if __name__ == "__main__":
    # --------easy way------------------
    t = Texttables(side_mode=True)

    t.set.cols_width([20, 20, 20])
    t.set.align_cols(["r"] * 3)
    t.set.align_header(["r"] * 3)
    t.add.header_column(["one\none", "second\nsecond", ""])
    t.set.v_line_special(5)
    for i in range(10):
        t.add.row(["fgtZZZZff", "ggg", "hhh"])
    t.end()
    # t.add.header("hehey")
    # t.add.header("hehey")
    t.set.cols_width([20, 20, 20] * 2)
    t.set.align_cols(["r"] * 3 * 2)
    t.set.align_header(["r"] * 3 * 2)
    t.add.header_column(["one\none", "second\nsecond", ""] * 2)
    for i in range(14):
        t.add.row(["fgtZZZZff", "ggg", "hhh"] * 2)
    t.end()
    t.file()
    # ---------------to gui----------------------
