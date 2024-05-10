from logic import *
import sys


def main() -> None:
    """
    Starts the entire application.
    """
    application = QApplication([])
    window = GuiLogic()
    window.show()
    sys.exit(application.exec())


if __name__ == '__main__':
    main()