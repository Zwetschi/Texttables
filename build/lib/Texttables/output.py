import os
import time
import random

# encoding="utf-8"
# encoding='ANSI'
# encoding='ascii', errors='ignore'
# b = bytes(self.get_str(), encoding="utf-8")
# str(obj.text, encoding="ascii", errors="ignore")
class Write:
    def __init__(self, filename=None) -> None:
        self.__timestamp = time.strftime("%Y_%m_%d__%H_%M_%S", time.localtime())

        if filename == None:
            r = random.randint(100, 999)
            self.__filename = self.__timestamp + "__" + str(r) + ".txt"
        else:
            self.__filename = filename

        folder = os.path.join("output_files", "egal")
        try:
            os.makedirs(folder)
        except FileExistsError:
            pass

        self.__path = os.path.join(
            os.path.dirname(__file__) + "\output_files", self.__filename
        )

    def write(self, data: str, mode="w"):
        with open(self.__path, mode, encoding="utf-8") as t:
            t.write(data)

    def open(self):
        os.startfile(self.__path)

    def __del__(self):
        print(self.__path)


if __name__ == "__main__":
    d = Write()
    d.write("ffff")
    d.open()
