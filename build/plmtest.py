if __name__ == "__main__":
    import sys
    from PyQt5.QtWidgets import QApplication
    app = QApplication([])
    import _pickle as pickle

    class TestObject(QObject):
        def __init__(self):
            super().__init__()
            self._value = None

        def value(self):
            return self._value

        def setValue(self, val):
            self._value = val

        def __str__(self):
            return str(self._value)

    A = TestObject()
    A.setValue(777)
    preparePicklePyQt(A)
    with open("pyqt_pickle_test.pickle", "wb") as pickle_file:
        pickle.dump(A, pickle_file)
    with open("pyqt_pickle_test.pickle", "rb") as pickle_file:
        B = pickle.load(pickle_file)
    print(A)
    print(B)
    sys.exit(app.exec_())