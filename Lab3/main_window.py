import sys
import os
import logging
from PyQt6.QtWidgets import (
    QWidget, 
    QApplication, QMainWindow, 
    QLabel, QPushButton, 
    QVBoxLayout, QFileDialog, 
    QMessageBox, QTextBrowser, 
    QComboBox, QInputDialog
)


sys.path.insert(1, "C:\\Users\\79297\\Desktop\\Application Programming\\Lab2") 
from create_annotation import create_annotation_file
from dataset_random import random_dataset
from dataset_copy import copy_dataset
from iterators import FileIterator

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.iter = None
        self.dataset_path = ""
        self.annotation_file_path = ""
        self.randomized_dataset_path = ""
        self.dataset_iterator = None
        self.classes = ["1", "2", "3", "4", "5"]
        self.default_size = 1000
        self.combo = QComboBox(self)
        self.combo.addItems(self.classes)
        self.combo.setCurrentIndex(0)
        self.dataset_type = ["copy", "random"]
        self.init_ui()

    def init_ui(self):
        self.setWindowTitle('Dataset Application')
        self.setGeometry(100, 100, 400, 300)

        # Остальной код интерфейса остается без изменений...

    def create_annotation(self):
        """Create an annotation file for the selected dataset."""
        try:
            if self.dataset_path:
                self.annotation_file_path, _ = QFileDialog.getSaveFileName(
                    self, "Save Annotation File", "", "CSV Files (*.csv)"
                )
                if self.annotation_file_path:
                    create_annotation_file(self.dataset_path, self.annotation_file_path)
        except Exception as ex:
            logging.error(f"Failed to create annotation: {ex}\n")

    def create_dataset(self, dataset_type):
        """Create a dataset based on the given type (copy or random)."""
        if self.dataset_path:
            dataset_path = QFileDialog.getExistingDirectory(
                self, f"Select Folder for {dataset_type.capitalize()} Dataset"
            )
            if dataset_path:
                subfolder_name, _ = QInputDialog.getText(
                    self, 'Subfolder Name', 'Enter Subfolder Name:'
                )
                if subfolder_name:
                    subfolder_path = os.path.join(dataset_path, subfolder_name)
                    if not os.path.exists(subfolder_path):
                        os.makedirs(subfolder_path)

                    annotation_file_path, _ = QFileDialog.getSaveFileName(
                        self, f"Save {dataset_type.capitalize()} Annotation File", "", "CSV Files (*.csv)"
                    )
                    if annotation_file_path:
                        if dataset_type == 'copy':
                            copy_dataset(
                                self.dataset_path,
                                subfolder_path,
                                self.classes,
                                annotation_file_path,
                            )
                            self.copy_dataset_path = dataset_path
                            self.copy_annotation_file_path = annotation_file_path
                        elif dataset_type == 'random':
                            random_dataset(
                                self.dataset_path,
                                subfolder_path,
                                self.default_size,
                                self.classes,
                                annotation_file_path,
                            )
                            self.random_dataset_path = dataset_path
                            self.random_annotation_file_path = annotation_file_path

    def browse_dataset(self):
        """Open dialog to select the data folder."""
        self.dataset_path = QFileDialog.getExistingDirectory(self, "Select Data Folder")
        if self.dataset_path:
            dataset_iterator = self.get_dataset_files()
            if dataset_iterator:
                dataset_files = list(dataset_iterator)
                self.iter = FileIterator(dataset_files)

    def get_dataset_files(self):
        """Generator to enumerate file paths in the dataset."""
        if self.dataset_path and os.path.exists(self.dataset_path):
            for root, dirs, files in os.walk(self.dataset_path):
                for file in files:
                    yield os.path.join(root, file)
        else:
            QMessageBox.warning(self, "Dataset not selected", "No dataset selected or the selected dataset path does not exist")

    def next(self, review_type):
        """Function returns the path to the next element of the class
        and opens text review in the widget"""
        if self.iter is None:
            QMessageBox.information(None, "File not selected", "No file selected for iteration")
            return

        if review_type == "1":
            element = self.iter.next_1()
        elif review_type == "2":
            element = self.iter.next_2()
        elif review_type == "3":
            element = self.iter.next_3()
        elif review_type == "4":
            element = self.iter.next_4()
        elif review_type == "5":
            element = self.iter.next_5()
        else:
            QMessageBox.information(None, "Invalid value", "An invalid value has been selected")
            return

        self.review_path = element

        if self.review_path is None:
            QMessageBox.information(None, "End of class", "No more files for this class")
            return

        self.text_label.update()
        
        with open(self.review_path, 'r', encoding='utf-8') as file:
            self.txt_file.setText(self.review_path)
            self.text_label.setText(file.read())

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
