import sys
from gui import QApplication, GraphAnalyzerNameWindow

# Global application stylesheet applied to every widget
_APP_STYLE = """
    QMainWindow, QDialog {
        background-color: #1e1e2e;
    }
    QWidget {
        background-color: #1e1e2e;
        color: #cdd6f4;
    }
    QLineEdit, QDateEdit {
        background-color: #313244;
        color: #cdd6f4;
        border: 1px solid #45475a;
        border-radius: 6px;
        padding: 4px 8px;
    }
    QLineEdit:focus, QDateEdit:focus {
        border: 1px solid #89b4fa;
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
        border: 1px solid #45475a;
        border-radius: 6px;
        margin-top: 10px;
        padding: 8px;
        color: #bac2de;
    }
    QGroupBox::title {
        subcontrol-origin: margin;
        left: 10px;
        padding: 0 4px;
    }
    QLabel {
        color: #cdd6f4;
    }
    QCheckBox {
        color: #cdd6f4;
        spacing: 6px;
    }
    QCalendarWidget {
        background-color: #313244;
        color: #cdd6f4;
    }
    QMessageBox {
        background-color: #1e1e2e;
        color: #cdd6f4;
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
