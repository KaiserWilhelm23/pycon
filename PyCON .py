import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QGraphicsView, QGraphicsScene, QPushButton, QVBoxLayout, QFileDialog, QMessageBox, QShortcut, QWidget
from PyQt5.QtGui import QPixmap, QFont, QKeySequence, QPainter
from PyQt5.QtCore import Qt
from PIL import Image

class IconConverterApp(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("PyCON 1.0")
        self.setGeometry(100, 100, 510, 600)

        self.viewing_area_size = (480, 480)  # Pre-defined size for the viewing area

        self.scene = QGraphicsScene(self)
        self.view = QGraphicsView(self.scene)
        self.view.setRenderHint(QPainter.Antialiasing, True)
        self.view.setAlignment(Qt.AlignCenter)
        self.view.setFixedSize(*self.viewing_area_size)  # Set fixed size for the viewing area

        self.import_button = QPushButton("Import PNG", self)
        self.import_button.clicked.connect(self.import_icon)
        self.set_button_style(self.import_button, size=14)  # Set a larger font and button size

        self.convert_button = QPushButton("Convert", self)
        self.convert_button.clicked.connect(self.convert_icon)
        self.set_button_style(self.convert_button, size=14)  # Set a larger font and button size

        central_widget = QWidget(self)
        layout = QVBoxLayout(central_widget)
        layout.addWidget(self.view)
        layout.addWidget(self.import_button)
        layout.addWidget(self.convert_button)

        self.setCentralWidget(central_widget)  # Set central widget

        self.setStyleSheet("background-color: #333; color: #FFF;")

        # Add shortcuts
        self.remove_image_shortcut = QShortcut(QKeySequence("Ctrl+Shift+X"), self)
        self.remove_image_shortcut.activated.connect(self.remove_image)

        self.import_shortcut = QShortcut(QKeySequence("Ctrl+Shift+I"), self)
        self.import_shortcut.activated.connect(self.import_icon)

        self.convert_shortcut = QShortcut(QKeySequence("Ctrl+Shift+C"), self)
        self.convert_shortcut.activated.connect(self.convert_icon)

        self.quit_shortcut = QShortcut(QKeySequence(Qt.Key_Escape), self)
        self.quit_shortcut.activated.connect(self.close)

        # Menu bar
        menubar = self.menuBar()
        menubar.setStyleSheet(
    "QMenuBar {"
    "   background-color: #2c3e50;"  # Dark background color
    "   color: #ecf0f1;"              # Light text color
    "}"
    "QMenuBar::item {"
    "   background-color: #2c3e50;"  # Dark background color
    "   padding: 8px 16px;"           # Padding around the menu items
    "}"
    "QMenuBar::item:selected {"
    "   background-color: #34495e;"  # Slightly lighter background color when selected
    "}"
)
        info_menu = menubar.addMenu('Info')

        help_action = info_menu.addAction('Help')
        help_action.triggered.connect(self.show_help)

        about_action = info_menu.addAction('About')
        about_action.triggered.connect(self.show_about)

        # Status bar
        self.statusBar()

    def show_help(self):
        QMessageBox.information(self, 'Help', 'Shortcuts:\n'
                                              'Ctrl+Shift+X: Remove the imported image\n'
                                              'Ctrl+Shift+I: Import\n'
                                              'Ctrl+Shift+C: Convert\n'
                                              'Esc: Quit')

    def show_about(self):
        QMessageBox.about(self, 'About', 'PyCON\n'
                                         'Version: 1.0\n'
                                         'Author: Will Payne\n'
                                         'GitHub Repo: https://github.com/blaze005/pycon')

    def set_button_style(self, button, size=12):
        button.setStyleSheet(
            f"QPushButton {{"
            f"   background-color: #3498db;"
            f"   border: 2px solid #3498db;"
            f"   color: #FFF;"
            f"   padding: 10px 20px;"
            f"   border-radius: 5px;"
            f"   font-size: {size}px;"  # Set the font size
            f"}}"
            f"QPushButton:hover {{"
            f"   background-color: #2980b9;"
            f"   border: 2px solid #2980b9;"
            f"}}"
        )

    def import_icon(self):
        options = QFileDialog.Options()
        options |= QFileDialog.ReadOnly

        file_dialog = QFileDialog()
        file_path, _ = file_dialog.getOpenFileName(self, "Import Icon File", "", "PNG Files (*.png);;All Files (*)", options=options)

        if file_path:
            self.image_path = file_path  # Save the image path
            pixmap = QPixmap(file_path)
            item = self.scene.addPixmap(pixmap)
            item.setTransformationMode(Qt.SmoothTransformation)
            self.statusBar().showMessage(f"Image imported from {file_path}")

    def convert_icon(self):
        if hasattr(self, 'image_path'):
            image = Image.open(self.image_path)

            save_dialog = QFileDialog()
            save_path, _ = save_dialog.getSaveFileName(self, "Save Icon As", "", "ICO Files (*.ico);;All Files (*)")

            if save_path:
                image.save(save_path, format='ICO')
                QMessageBox.information(self, "Conversion Complete", "Icon conversion successful!")
                self.statusBar().showMessage(f"Icon saved to {save_path}")

    def remove_image(self):
        self.scene.clear()
        self.statusBar().showMessage("Imported image removed")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    icon_converter_app = IconConverterApp()
    icon_converter_app.show()
    sys.exit(app.exec_())
