from PyQt5.QtWidgets import (QApplication, QDialog, QHBoxLayout, QLabel,
                             QPushButton, QTextEdit, QVBoxLayout)
from algorithm import GraphPath
import numpy as np


class WidgetGallery(QDialog):
    err_msg = '''Вы ввели некоректные данные,введите что то похожее на это:
                0 4 9 2 0 0 6 0 0 0
                4 0 0 0 0 0 2 5 0 0
                9 0 0 7 0 2 1 0 0 0
                2 0 7 0 5 9 0 0 0 0
                0 0 0 5 0 0 0 0 8 0
                0 0 2 9 0 0 6 0 7 4
                6 2 1 0 0 6 0 4 0 2
                0 5 0 0 0 0 4 0 0 3
                0 0 0 0 8 7 0 0 0 6
                0 0 0 0 0 4 2 3 6 0'''

    def __init__(self, parent=None):
        super(WidgetGallery, self).__init__(parent)
        self.resize(700, 300)
        self.setLayout(self.layouts())

    def layouts(self):
        mainLayout = QHBoxLayout()

        left_layout = QVBoxLayout()

        label = QLabel("Введите граф как матрицу смежности")
        left_layout.addWidget(label)

        self.input = QTextEdit()
        left_layout.addWidget(self.input)

        calculateBut = QPushButton("Максимальный поток")
        calculateBut.clicked.connect(self.calculate)
        left_layout.addWidget(calculateBut)

        reportBut = QPushButton("Отчет")
        reportBut.clicked.connect(self.report)
        left_layout.addWidget(reportBut)

        mainLayout.addLayout(left_layout)

        self.output = QTextEdit()
        mainLayout.addWidget(self.output)

        return mainLayout

    def calculate(self):
        try:
            gr = GraphPath()
            gr.split_str(self.input.toPlainText())
            power, _ = gr.find_max_power(1, 10)
            self.output.setText("Максимальный поток : {0}".format(power))
        except BaseException:
            self.output.setText(self.err_msg)

    def report(self):
        try:
            list_of_text = list()
            gr = GraphPath()
            gr.split_str(self.input.toPlainText())
            power, graph = gr.find_max_power(1, 10)
            list_of_text.append("Максимальный поток : {0}".format(power))
            check_point_one = gr.check_point_one(power, graph)
            list_of_text.append(
                "Чекпоинт 1 : {0}".format("✔" if check_point_one else "❌❌🞪❌"))
            selection = gr.find_section(graph, set())
            selection = np.array(list(selection))
            selection += 1
            check_point_two = gr.check_point_two(selection, power)
            list_of_text.append(
                "Чекпоинт 2 : {0}".format("✔" if check_point_two else "❌❌🞪❌"))
            list_of_text.append(
                "Сечение : {0}".format(selection))
            self.output.setText("\n".join(list_of_text))
        except BaseException:
            self.output.setText(self.err_msg)


if __name__ == '__main__':
    import sys

    app = QApplication(sys.argv)
    gallery = WidgetGallery()
    gallery.show()
    sys.exit(app.exec_())
