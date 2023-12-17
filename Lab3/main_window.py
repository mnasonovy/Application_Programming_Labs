import sys
import os
import logging
from PyQt6.QtWidgets import (
    QWidget, 
    QApplication, QMainWindow, 
    QLabel,QPushButton, 
    QVBoxLayout,QFileDialog, 
    QMessageBox, QTextBrowser, 
    QComboBox, QInputDialog
    )


sys.path.insert(1, "C:\\Users\\79297\\Desktop\\Application Programming\\Lab2")
from iterators import FileIterator
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
        self.classes = ["bad", "good"]
        self.default_size = 1000
        self.combo = QComboBox(self)
        self.combo.addItems(self.classes)
        self.combo.setCurrentIndex(0)
        self.dataset_type = ["copy", "random"]
        self.init_ui()

    def init_ui(self):
        self.setWindowTitle('Dataset Application')
        self.setGeometry(100, 100, 400, 300)

        self.browse_dataset_btn = QPushButton('Select Data Folder', self)
        self.create_annotation_btn = QPushButton('Create Annotation', self)
        self.create_random_dataset_btn = QPushButton('Create Random Dataset', self)
        self.create_copy_dataset_btn = QPushButton('Create Copy Dataset', self)
        self.next_1_star_btn = QPushButton('Next 1* review', self)
        self.next_2_star_btn = QPushButton('Next 2* review', self)
        self.next_3_star_btn = QPushButton('Next 3* review', self)
        self.next_4_star_btn = QPushButton('Next 4* review', self)
        self.next_5_star_btn = QPushButton('Next 5* review', self)

        self.browse_dataset_btn.clicked.connect(self.browse_dataset)
        self.create_annotation_btn.clicked.connect(self.create_annotation)
        self.create_random_dataset_btn.clicked.connect(lambda: self.create_dataset('random'))
        self.create_copy_dataset_btn.clicked.connect(lambda: self.create_dataset('copy'))
        self.next_1_star_btn.clicked.connect(lambda: self.next_star_review(1))
        self.next_2_star_btn.clicked.connect(lambda: self.next_star_review(2))
        self.next_3_star_btn.clicked.connect(lambda: self.next_star_review(3))
        self.next_4_star_btn.clicked.connect(lambda: self.next_star_review(4))
        self.next_5_star_btn.clicked.connect(lambda: self.next_star_review(5))

        self.txt_file = QLabel(self)
        self.text_label = QTextBrowser(self)
        self.text_label.setText("Здесь будет отзыв")
        self.text_label.setFixedSize(600, 400)

        layout = QVBoxLayout()
        layout.addWidget(self.browse_dataset_btn)
        layout.addWidget(self.create_annotation_btn)
        layout.addWidget(self.create_random_dataset_btn)
        layout.addWidget(self.create_copy_dataset_btn)
        layout.addWidget(self.next_1_star_btn)
        layout.addWidget(self.next_2_star_btn)
        layout.addWidget(self.next_3_star_btn)
        layout.addWidget(self.next_4_star_btn)
        layout.addWidget(self.next_5_star_btn)
        layout.addWidget(self.txt_file)
        layout.addWidget(self.text_label)  

        central_widget = QWidget(self)
        central_widget.setLayout(layout)
        self.setCentralWidget(central_widget)
        
    

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
            dataset_files = self.get_dataset_files()
            # Используем FileIterator для итерации по файлам внутри выбранной папки
            self.iter = FileIterator(dataset_files)

    def get_dataset_files(self):
        """Get file paths in the dataset."""
        dataset_files = []
        if self.dataset_path:
            for root, dirs, files in os.walk(self.dataset_path):
                for file in files:
                    file_path = os.path.join(root, file)
                    dataset_files.append(file_path)
                    print(file_path)  # Добавьте эту строку для вывода путей файлов
        return dataset_files

    def next_star_review(self, stars):
        if self.iter is None:
            QMessageBox.information(None, "File not selected", "No file selected for iteration")
            return

        element = self.iter.next_star(stars)

        if element is None:
            QMessageBox.information(None, "End of class", "No more files for this class")
            return

        self.review_path = element

        with open(self.review_path, 'r', encoding='utf-8') as file:
            self.txt_file.setText(self.review_path)
            self.text_label.setText(file.read())

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
