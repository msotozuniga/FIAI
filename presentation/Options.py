from PySide2.QtWidgets import QWidget,QHBoxLayout,QVBoxLayout, QLabel,QComboBox, QSpinBox, QSizePolicy

class OptionChoice(QWidget):
    def __init__(self, label_text,dict):
        super(OptionChoice,self).__init__()
        layout = QHBoxLayout()

        text = QLabel(label_text)
        layout.addWidget(text)

        self.options = QComboBox()
        for key, value in dict.items():
            self.options.addItem(key,value)

        layout.addWidget(self.options)

        self.setLayout(layout)

    def getValue(self):
        return self.options.itemData(self.options.currentIndex())

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
        self.value = 1

        layout.addWidget(self.options)

        self.setLayout(layout)
    
    def getValue(self):
        return self.options.value()

class OptionRange(QWidget):
    def __init__(self, label_text):
        super(OptionRange,self).__init__()
        global_layout = QVBoxLayout()

        text = QLabel(label_text)
        global_layout.addWidget(text)

        sub_layout = QHBoxLayout()
        global_layout.addLayout(sub_layout)

        self.bottom_frame = QSpinBox() # que no escuchen cambios asta presionar start
        self.bottom_frame.setMinimum(1) 
        self.bottom_frame.setMaximum(11) 
        self.bottom_frame.setSingleStep(1)
        self.bottom_frame.setKeyboardTracking(False)
        self.bottom_frame.valueChanged.connect(self.bottom_value_changed)

        self.top_frame = QSpinBox()# que no escuchen cambios asta presionar start
        self.top_frame.setMinimum(1) 
        self.top_frame.setMaximum(11) 
        self.top_frame.setSingleStep(1)
        self.top_frame.setKeyboardTracking(False)
        self.top_frame.valueChanged.connect(self.top_value_changed)

        sub_layout.addWidget(self.bottom_frame)
        sub_layout.addWidget(self.top_frame)

        self.setLayout(global_layout)

    def getValue(self):
        return (self.bottom_frame.value(), self.top_frame.value())

    def setLimits(self, minimum,maximum):
        self.bottom_frame.setMinimum(minimum)
        self.top_frame.setMinimum(minimum+1)
        self.bottom_frame.setMaximum(maximum-1)
        self.top_frame.setMaximum(maximum)
        self.setValue(self.top_frame, 1)
        self.setValue(self.bottom_frame, 0)

    def setValue(self, box, value):
        box.blockSignals(True)
        box.setValue(value)
        box.blockSignals(False)


    def bottom_value_changed(self, i):
        if i >= self.top_frame.value():
            self.setValue(self.top_frame, i+1)

    def top_value_changed(self, i):
        print(i)
        print(self.bottom_frame.value())
        if i <= self.bottom_frame.value():
            self.setValue(self.bottom_frame, i-1)