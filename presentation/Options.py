from PySide2.QtWidgets import QWidget,QHBoxLayout,QLabel,QComboBox, QSpinBox

class OptionChoice(QWidget):
    def __init__(self, label_text, options):
        super(OptionChoice,self).__init__()
        layout = QHBoxLayout()

        text = QLabel(label_text)
        layout.addWidget(text)

        self.options = QComboBox()
        self.options.addItems(options)
        self.options.currentIndexChanged.connect(self.value_changed)

        layout.addWidget(self.options)

        self.setLayout(layout)

    def value_changed(self, i):
        print(i)

class OptionNumber(QWidget):
    def __init__(self, label_text):
        super(OptionNumber,self).__init__()
        layout = QHBoxLayout()

        text = QLabel(label_text)
        layout.addWidget(text)

        self.options = QSpinBox()
        self.options.setMinimum(1)
        self.options.setMaximum(10)
        self.options.setSingleStep(1)
        self.options.valueChanged.connect(self.value_changed)

        layout.addWidget(self.options)

        self.setLayout(layout)
    
    def value_changed(self, i):
        print(i)