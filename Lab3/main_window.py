import sys
import os
import logging
from PyQt6.QtCore import QSize
from PyQt6.QtWidgets import (
    QApplication,
    QMainWindow,
    QLabel,
    QVBoxLayout,
    QComboBox,
    QPushButton,
    QTextBrowser,
    QGridLayout,
    QWidget,
    QFileDialog,
    QMessageBox
)

# Добавление пути до необходимых модулей
sys.path.insert(1, r"C:\Users\79297\Desktop\Application_Programming\Lab2")

from create_annotation import write_into_file
from dataset_random import randomize_dataset
from dataset_copy import unify_dataset
from iterators import ClassIterator

logging.basicConfig(level=logging.INFO)

class MainWindow(QMainWindow):
    def __init__(self) -> None:
        super().__init__()

        self.setGeometry(1000, 200, 1000, 500)
        self.setMaximumSize(2000, 2000)

        box_layout = QVBoxLayout()
        grid_layout = QGridLayout()
        main_widget = QWidget()

        self.setWindowTitle('Dataset operation')
        self.data_path = os.path.abspath("Lab2\datasets\dataset")
        src = QLabel(f"Base dataset:\n{self.data_path}", self)
        src.setFixedSize(QSize(500, 80))
        box_layout.addWidget(src)

        self.combo_operation = QComboBox(self)
        self.combo_operation.addItems(["Unify", "Randomize"])
        self.combo_operation.setFixedSize(QSize(300, 100))
        box_layout.addWidget(self.combo_operation)

        self.btn_execute = self.create_button("Execute operation", 300, 40, True)
        self.btn_execute.clicked.connect(self.execute)
        box_layout.addWidget(self.btn_execute)

        box_layout.addSpacing(100)

        self.rating_combo = QComboBox(self)
        self.rating_combo.addItems(["1 Star", "2 Stars", "3 Stars", "4 Stars", "5 Stars"])
        self.rating_combo.setFixedSize(QSize(300, 40))
        box_layout.addWidget(self.rating_combo)

        self.path_label = QLabel("Path to displayed file")
        box_layout.addWidget(self.path_label)

        self.btn_iterator = self.create_button("Iterate", 250, 40, True)
        self.btn_iterator.clicked.connect(self.csv_path)
        box_layout.addWidget(self.btn_iterator)

        self.btn_next = self.create_button("Next", 250, 30, False)
        self.btn_next.clicked.connect(self.next)
        box_layout.addWidget(self.btn_next)

        self.btn_close = self.create_button("Close", 200, 30, True)

        self.text_label = QTextBrowser(self)
        self.text_label.setText("Review content will be displayed here")
        self.text_label.setFixedSize(500, 500)

        box_layout.addWidget(self.btn_close)
        self.btn_close.clicked.connect(self.close)
        
        grid_layout.addLayout(box_layout, 0, 0)
        grid_layout.addWidget(self.text_label, 0, 1)

        main_widget.setLayout(grid_layout)

        self.setCentralWidget(main_widget)

        self.classes = ['1', '2', '3', '4', '5']
        self.classes_iterator = None
        self.review_path = None

    def create_button(self, name: str, width: int, height: int, enabled: bool) -> QPushButton:
        button = QPushButton(name, self)
        button.setEnabled(enabled)
        button.resize(button.sizeHint())
        button.setFixedSize(QSize(width, height))
        return button
    
    def csv_path(self) -> None:
        try:
            path = QFileDialog.getOpenFileName(self, "Choose pathfile for iteration:", "", "CSV File(*.csv)")[0]
            if path == "":
                return
            self.classes_iterator = ClassIterator(path, self.classes)
            self.btn_next.setEnabled(True)
        except Exception as exc:
            logging.error(f"Incorrect path: {exc.args}\n{exc}\n")

    def next(self) -> None:
        if self.classes_iterator is None:
            QMessageBox.information(None, "No file selected", "No ")
            return
        rating = self.rating_combo.currentIndex()
        element = self.classes_iterator.next(rating)
        self.review_path = element
        if self.review_path is None:
            QMessageBox.information(None, "Class view finished", "There are no more files of this class left")
            return
        self.text_label.update()
        with open(file=self.review_path, mode="r", encoding="utf-8") as file:
            self.path_label.setText(self.review_path)
            self.text_label.setText(file.read())

    def execute(self) -> None:
        try:
            file = QFileDialog.getSaveFileName(self, "Choose directory to create .csv:", "", "CSV File(*.csv)")[0]
            directory = QFileDialog.getExistingDirectory(self, "Choose directory to deploy the new dataset:")
            if (file == "") or (directory == ""):
                QMessageBox.information(None, "No path chosen", "Path to file or directory has not been chosen")
                return
            if self.combo_operation.currentText() == "Unify":
                unified_pathlist = unify_dataset(self.data_path, os.path.join(directory, 'unified_dataset'), self.classes)
                write_into_file(file, unified_pathlist)
            if self.combo_operation.currentText() == "Randomize":
                randomized_pathlist = randomize_dataset(self.data_path, os.path.join(directory, 'randomized_dataset'), self.classes, 5000)
                write_into_file(file, randomized_pathlist)
            QMessageBox.information(None, "Success", "Operation complete")
        except Exception as exc:
            logging.error(f"Can not create copy or annotation: {exc.args}\n{exc}\n")    
            

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
