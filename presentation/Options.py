from PySide2.QtWidgets import QWidget,QHBoxLayout,QVBoxLayout, QLabel,QComboBox, QSpinBox

class OptionChoice(QWidget):
    def __init__(self, label_text, options):
        super(OptionChoice,self).__init__()
        layout = QHBoxLayout()

        text = QLabel(label_text)
        layout.addWidget(text)

        self.model_dicts = {} # TODO setear este dict como algo compartido en todo el sistema
        for i in range(len(options)):
            self.model_dicts[options[i]]=i
        self.selected_model = 0

        self.options = QComboBox()
        self.options.addItems(options)
        self.options.currentIndexChanged.connect(self.value_changed)

        layout.addWidget(self.options)

        self.setLayout(layout)

    def value_changed(self, i):
        print(i)
        self.selected_model = self.model_dicts[i]

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

class OptionRange(QWidget):
    def __init__(self, label_text):
        super(OptionRange,self).__init__()
        global_layout = QVBoxLayout()

        text = QLabel(label_text)
        global_layout.addWidget(text)

        sub_layout = QHBoxLayout()
        global_layout.addLayout(sub_layout)

        self.bottom_frame = QSpinBox()
        self.bottom_frame.setMinimum(1) #TODO setear el frame minimo cuando se carga un video
        self.bottom_frame.setMaximum(11) #TODO setear frame maximo cuando se carga un video
        self.bottom_frame.setSingleStep(1)
        self.bottom_frame.valueChanged.connect(self.bottom_value_changed)

        self.top_frame = QSpinBox()
        self.top_frame.setMinimum(1) #TODO setear el frame minimo cuando se carga un video
        self.top_frame.setMaximum(11) #TODO setear frame maximo cuando se carga un video
        self.top_frame.setSingleStep(1)
        self.top_frame.valueChanged.connect(self.top_value_changed)

        sub_layout.addWidget(self.bottom_frame)
        sub_layout.addWidget(self.top_frame)

        self.setLayout(global_layout)

    def bottom_value_changed(self, i):
        print(i)

    def top_value_changed(self, i):
        print(i)