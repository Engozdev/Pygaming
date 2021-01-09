import sys
from PyQt5.QtCore import Qt
from PyQt5 import uic  # Импортируем uic
from PyQt5.QtWidgets import QApplication, QWidget
from PyQt5.QtGui import QPixmap
import random


class MyWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.output = False
        uic.loadUi('proj.ui', self)  # Загружаем дизайн
        self.btn.clicked.connect(self.check)
        # Обратите внимание: имя элемента такое же как в QTDesigner
        questions = ["C:/Users/denac/Pictures/Saved Pictures/nepal.png",
                     "C:/Users/denac/Pictures/Saved Pictures/spain.jpg"]
        self.d = {"C:/Users/denac/Pictures/Saved Pictures/nepal.png": 0,
                  "C:/Users/denac/Pictures/Saved Pictures/spain.jpg": 1}
        self.answers = ['непал', 'испания']
        self.n = random.randint(0, 1)
        pixmap = QPixmap(questions[self.n])
        self.lbl.setPixmap(pixmap)

    def check(self):
        if self.ans.text().lower() == self.answers[self.n]:
            self.output = True
            self.res.setText('Правильно')
        else:
            self.res.setText('Неправильно')

    def closeEvent(self, event):
        self.result()

    def result(self):
        return self.output

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Control:
            self.check()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MyWidget()
    ex.show()
    print(ex.result())
    sys.exit(app.exec_())
