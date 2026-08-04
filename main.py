import sys
from gui import QApplication, GraphAnalyzerNameWindow

# Global application stylesheet — warm cream / dark-wood palette
_APP_STYLE = """
    QMainWindow, QDialog {
        background-color: #1c1810;
    }
    QWidget {
        background-color: #1c1810;
        color: #f5ebe0;
    }
    QLineEdit, QDateEdit {
        background-color: #2a2015;
        color: #f5ebe0;
        border: 1px solid #5c4a2e;
        border-radius: 6px;
        padding: 4px 8px;
    }
    QLineEdit:focus, QDateEdit:focus {
        border: 1px solid #f5ebe0;
    }
    QPushButton {
        border-radius: 6px;
        padding: 4px 12px;
        font-weight: bold;
    }
    QPushButton:hover {
        opacity: 0.85;
    }
    QGroupBox {
        border: 1px solid #5c4a2e;
        border-radius: 6px;
        margin-top: 10px;
        padding: 8px;
        color: #f0d9b5;
    }
    QGroupBox::title {
        subcontrol-origin: margin;
        left: 10px;
        padding: 0 4px;
    }
    QLabel {
        color: #f5ebe0;
    }
    QCheckBox {
        color: #f5ebe0;
        spacing: 6px;
    }
    QCalendarWidget {
        background-color: #2a2015;
        color: #f5ebe0;
    }
    QMessageBox {
        background-color: #1c1810;
        color: #f5ebe0;
    }
"""


def main() -> None:
    app = QApplication(sys.argv)
    app.setStyleSheet(_APP_STYLE)
    first_window = GraphAnalyzerNameWindow()
    first_window.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
