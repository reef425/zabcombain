import sys
from . import zabcombain
from PyQt5.QtWidgets import QApplication

def main():
    # Next, create an application object.
    QApplication.setDesktopSettingsAware(False)
    app = QApplication(sys.argv)
    # Show it.
    frame = zabcombain.MainWindow()
    # Start the event loop.
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
