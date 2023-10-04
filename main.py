# Library Imports
from PyQt6.QtWidgets import QApplication, QMainWindow, QLabel
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QMouseEvent, QFontDatabase
import sys

# Relative Imports
from Generated.ui import Ui_MainWindow
from connections import Connectors
from translate import Translate
from Registry.reg_edit import EditRegistry
from Data.user import Saved
from Data.paths import Path
from Data.enums import Languages
from Widgets.info_widget import InfoWidget
from Widgets.applied_widget import AppliedWidget


class Main(Ui_MainWindow):
    def __init__(self):
        # Setup Window
        self.mainWindow: QMainWindow = QMainWindow()
        self.setupUi(self.mainWindow)
        self.mainWindow.setWindowFlags(Qt.WindowType.FramelessWindowHint)
        self.mainWindow.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)

        # Handle Events
        self.title.mousePressEvent = self.myMousePressEvent  # type: ignore
        self.title.mouseMoveEvent = self.myMouseMoveEvent  # type: ignore
        self.title.mouseReleaseEvent = self.myMouseReleaseEvent  # type: ignore
        self.title.setMouseTracking(True)
        self.closeButton.clicked.connect(self.mainWindow.close)  # type: ignore
        self.minimizeButton.clicked.connect(self.mainWindow.showMinimized)  # type: ignore

        # Add Widgets
        self.infoWidget = InfoWidget(self.mainWindow, self.mainFrame)
        self.appliedWidget = AppliedWidget(self.mainWindow, self.mainFrame)

        # Call UI Methods
        self.callConnectors()
        Translate.translate(self, Languages.Hindi)
        EditRegistry.createAllKeys()
        Saved.updateUI(self)

        # Further Customization

    def callConnectors(self):
        """
        Call connectors from connections module
        """
        Connectors.connectColorPickers(self)
        Connectors.connectResetButtons(self)
        # Connectors.connectMouseEvent(self)
        Connectors.connectApplyButtons(self)
        Connectors.connectStyleSheets(self)  # Dark Theme
        # Connectors.connectStyleSheets(self, "white", "lightgray", "black", "#222222")  # Light Theme
        # Connectors.connectStyleSheets(self, "hotpink", "skyblue", "white", "#222222")  # Pink-Blue Theme

    def myMousePressEvent(self, event: QMouseEvent):
        if event.buttons() == Qt.MouseButton.LeftButton:
            self.dragPos = event.globalPosition().toPoint()
            self.title.setCursor(Qt.CursorShape.ClosedHandCursor)
            event.accept()

    def myMouseMoveEvent(self, event: QMouseEvent):
        if event.buttons() == Qt.MouseButton.LeftButton:
            self.mainWindow.move(self.mainWindow.pos() + event.globalPosition().toPoint() - self.dragPos)  # type: ignore
            self.dragPos = event.globalPosition().toPoint()
            event.accept()

    def myMouseReleaseEvent(self, event: QMouseEvent):
        QLabel.mouseReleaseEvent(self.title, event)
        self.title.setCursor(Qt.CursorShape.OpenHandCursor)


if __name__ == "__main__":
    app: QApplication = QApplication(sys.argv)
    QFontDatabase.addApplicationFont(Path.FontPaths.NunitoSans)
    QFontDatabase.addApplicationFont(Path.FontPaths.AndikaRegular)
    main: object = Main()
    main.mainWindow.show()
    app.exec()
