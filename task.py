import sys
from PyQt5.QtCore import Qt, QSize
from PyQt5 import uic  # Импортируем uic
from PyQt5.QtWidgets import QApplication, QWidget
from PyQt5.QtGui import QPixmap, QIcon


class MyWidget(QWidget):
    def __init__(self, picture_path, answer):
        super().__init__()
        uic.loadUi('proj.ui', self)  # Загружаем дизайн
        self.btn.setIcon(QIcon('data\kodred.png'))
        self.btn.setIconSize(QSize(75, 75))
        self.btn.clicked.connect(self.check)
        self.answer = answer.lower()
        pixmap = QPixmap(picture_path)
        self.lbl.setPixmap(pixmap)

    def check(self):
        if self.ans.text().lower() == self.answer:
            self.res.setText(
                'Правильно\nЗакройте окно, \nотойдите на клетку от стены,\nнажмите Ctrl+P, \nчтобы увидеть подсказку')
        else:
            self.res.setText('Неправильно')

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Control:
            self.check()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MyWidget('data/nepal.jpg', 'непал')
    ex.show()
    sys.exit(app.exec_())
