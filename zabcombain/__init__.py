from . import zabcombain
from wx import App

def main():
    # Next, create an application object.
    app = App()
    # Show it.
    frame = zabcombain.MainWindow(None, "ZabCombain")
    # Start the event loop.
    app.MainLoop()


if __name__ == '__main__':
    main()
