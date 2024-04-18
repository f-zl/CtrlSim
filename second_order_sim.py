import pyqtgraph as pg
from PySide6 import QtWidgets, QtCore
import sys
import control as ct


class SliderWithLabel(QtWidgets.QWidget):
    def __init__(self, text, parent=None, min=0, max=100, init_val=0):
        super().__init__(parent)
        self.min = min
        self.ratio = (max - min) / 10000.0
        self.layout = QtWidgets.QHBoxLayout(self)
        self.slider = QtWidgets.QSlider(self)
        self.slider.setOrientation(QtCore.Qt.Horizontal)
        self.slider.setMinimum(0)
        self.slider.setMaximum(10000)
        self.slider.setValue(int((init_val - min) / self.ratio))
        self.label = QtWidgets.QLabel(self)
        self.label.setNum(init_val)
        self.slider.valueChanged.connect(self.update_label)
        self.layout.addWidget(QtWidgets.QLabel(text))
        self.layout.addWidget(self.slider)
        self.layout.addWidget(self.label)
        self.setLayout(self.layout)

    def value(self):
        return self.slider.value() * self.ratio + self.min

    def update_label(self):
        self.label.setNum(self.value())


class Widget(QtWidgets.QWidget):
    def refresh_graph(self):
        m = self.slider_m.value()
        c = self.slider_c.value()
        k = self.slider_k.value()
        p = self.slider_p.value()
        i = self.slider_i.value()
        d = self.slider_d.value()
        s = ct.tf("s")
        G = 1 / (m * s**2 + c * s + k)
        H = p + i / s + d * s
        sys = ct.feedback(G * H)
        r = ct.step_response(sys)
        self.dataItem.setData(r.time, r.outputs)

    def __init__(self):
        super().__init__()
        self.setWindowTitle("Second Order System Close Loop Step Response")
        layout = QtWidgets.QVBoxLayout(self)
        self.slider_m = SliderWithLabel("m", self, min=0.1, max=10, init_val=1)
        self.slider_c = SliderWithLabel("c", self, min=0.01, max=10, init_val=1)
        self.slider_k = SliderWithLabel("k", self, min=0.01, max=10, init_val=1)
        self.slider_p = SliderWithLabel("p", self, min=0, max=10, init_val=1)
        self.slider_i = SliderWithLabel("i", self, min=0, max=10, init_val=1)
        self.slider_d = SliderWithLabel("d", self, min=0, max=10, init_val=0)
        self.slider_m.slider.valueChanged.connect(self.refresh_graph)
        self.slider_c.slider.valueChanged.connect(self.refresh_graph)
        self.slider_k.slider.valueChanged.connect(self.refresh_graph)
        self.slider_p.slider.valueChanged.connect(self.refresh_graph)
        self.slider_i.slider.valueChanged.connect(self.refresh_graph)
        self.slider_d.slider.valueChanged.connect(self.refresh_graph)

        plot = pg.plot((0, 0))
        dataItems = plot.plotItem.listDataItems()
        self.dataItem = dataItems[0]

        hLout1 = QtWidgets.QHBoxLayout()
        hLout2 = QtWidgets.QHBoxLayout()
        hLout3 = QtWidgets.QHBoxLayout()
        hLout1.addWidget(self.slider_m)
        hLout2.addWidget(self.slider_c)
        hLout3.addWidget(self.slider_k)
        hLout1.addWidget(self.slider_p)
        hLout2.addWidget(self.slider_i)
        hLout3.addWidget(self.slider_d)
        layout.addLayout(hLout1)
        layout.addLayout(hLout2)
        layout.addLayout(hLout3)

        layout.addWidget(plot)
        self.refresh_graph()


app = QtWidgets.QApplication(sys.argv)
widget = Widget()
widget.show()
sys.exit(app.exec())
