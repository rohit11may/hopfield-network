import time
from PyQt4.QtGui import *
from PyQt4.uic import loadUiType
from random import randint
import numpy as np
import sys


class Pattern:
    def __init__(self, size=5, vector=[0] * 25):
        self.size = size
        if len(vector) != size ** 2:
            print("Invalid size supplied.")
            self.vector = []
        else:
            self.vector = vector

    def __repr__(self):
        render = ""
        for pixelNum in range(len(self.vector)):
            if pixelNum % self.size == 0:
                render += "\n"
            if self.vector[pixelNum] == 1:
                render += "@"
            else:
                render += "."
        return render

    def equalsTo(self, pattern):
        return pattern.getVector() == self.vector

    def getSize(self):
        return self.size

    def getVector(self):
        return self.vector

    def setSize(self, size):
        self.size = size

    def setVector(self, vector):
        if len(vector) != self.size ** 2:
            print("Invalid vector supplied")
        else:
            self.vector = vector


class PatternFactory:
    @staticmethod
    def getPattern(pattern):
        if pattern == "A":
            a = [-1, -1, 1, -1, -1,
                 -1, -1, -1, -1, -1,
                 -1, 1, 1, 1, -1,
                 -1, -1, -1, -1, -1,
                 1, -1, -1, -1, 1]
            return Pattern(5, a)
        elif pattern == "B":
            b = [1, 1, 1, 1, -1,
                 1, -1, -1, 1, -1,
                 1, 1, 1, 1, -1,
                 1, -1, -1, 1, -1,
                 1, 1, 1, 1, -1]
            return Pattern(5, b)
        elif pattern == "C":
            c = [1, 1, 1, 1, 1,
                 1, -1, -1, -1, -1,
                 1, -1, -1, -1, -1,
                 1, -1, -1, -1, -1,
                 1, 1, 1, 1, 1]
            return Pattern(5, c)
        else:
            return -1


Ui_MainWindow, QMainWindow = loadUiType('../gui/mainwindow.ui')  # Load UI file from GUI folder.


class MyWindow(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super(MyWindow, self).__init__()
        self.setupUi(self)

    def get_input(self):
        pattern1 = self.get_pattern(self.pattern1)
        pattern2 = self.get_pattern(self.pattern2)
        pattern3 = self.get_pattern(self.pattern3)
        input_pattern = self.get_pattern(self.input)
        return {
                   "pattern1": pattern1,
                   "pattern2": pattern2,
                   "pattern3": pattern3,
               }, input_pattern

    def get_pattern(self, patternTable):
        selected_indices = patternTable.selectedIndexes()
        vector = [-1] * 25
        for index in selected_indices:
            vector[5 * index.row() + index.column()] = 1
        return Pattern(5, vector)

    def set_pattern(self, pattern):
        vector = pattern.getVector()
        for num, pixel in enumerate(vector):
            row, column = num // 5, num % 5
            self.output.setItem(row, column, QTableWidgetItem())
            self.output.item(row, column).setSelected(pixel == 1)


class Hopfield(MyWindow):
    def __init__(self):
        super(Hopfield, self).__init__()
        self.run.clicked.connect(self.start)
        self.weights = np.array([[0] * 25] * 25)
        self.input_vector = [-1] * 25
        self.patterns = []

    @staticmethod
    def sign(vector):
        if vector >= 0:
            return 1
        else:
            return -1

    def start(self):
        self.create_weights()
        self.create_output()

    def create_weights(self):
        self.weights = np.array([[0] * 25] * 25)
        self.patterns, self.input_vector = self.get_input()
        self.input_vector = self.input_vector.getVector()
        combined_pattern_vector = []
        for pattern in list(self.patterns.values()):
            vector = pattern.getVector()
            combined_pattern_vector.append(vector)
        combined_pattern_vector = np.array(combined_pattern_vector)
        self.weights += (combined_pattern_vector.transpose().dot(combined_pattern_vector))
        np.fill_diagonal(self.weights, 0)

    def found_pattern(self, new_pattern):
        for pattern in list(self.patterns.values()):
            if pattern.equalsTo(new_pattern):
                return True
        return False

    def create_output(self):
        count = 0
        while (not self.found_pattern(Pattern(5, self.input_vector))) and count < 1000:
            print(count)
            count += 1
            next_to_fire = randint(0, 24)
            neuron = self.weights[next_to_fire]
            input_v = np.array(self.input_vector)
            self.input_vector[next_to_fire] = self.sign(input_v.transpose().dot(neuron.transpose()))

        self.set_pattern(Pattern(5, self.input_vector))


# patterns = [PatternFactory.getPattern("A"),
#             PatternFactory.getPattern("B"),
#             PatternFactory.getPattern("C")]


app = QApplication(sys.argv)
net = Hopfield()

net.show()
net.raise_()
sys.exit(app.exec_())  # Exit function if app closed.
