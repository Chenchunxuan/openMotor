from PyQt5.QtWidgets import QDialog, QVBoxLayout, QLabel
from PyQt5.QtGui import QIcon

import motorlib

from .widgets.collectionEditor import CollectionEditor


class Tool(QDialog):
    def __init__(self, manager, name, description, propDict, needsSimulation):
        super().__init__()
        self.manager = manager
        self.name = name
        self.description = description
        self.needsSimulation = needsSimulation
        self.preferences = None
        self.propCollection = motorlib.properties.PropertyCollection()
        self.propCollection.props = propDict

        self.motor = None
        self.inp = None

        self.setWindowTitle(self.name)
        self.setWindowIcon(QIcon('resources/oMIconCycles.png'))
        self.setLayout(QVBoxLayout())

        self.descLabel = QLabel(self.description)
        self.descLabel.setWordWrap(True)
        self.layout().addWidget(self.descLabel)

        self.editor = CollectionEditor(self, True)
        self.editor.changeApplied.connect(self.applyPressed)
        self.editor.closed.connect(self.hide)
        self.layout().addWidget(self.editor)

    def setPreferences(self, pref):
        self.preferences = pref
        self.editor.setPreferences(pref)

    def show(self):
        self.editor.loadProperties(self.propCollection)
        super().show()

    def applyPressed(self, inp):
        if self.needsSimulation:
            self.inp = inp
            self.motor = self.manager.getMotor()
            self.manager.requestSimulation()
        else:
            self.applyChanges(inp, self.manager.getMotor(), None)

    def simDone(self, sim):
        if self.inp is not None: # If inp is set, this is the tool waiting for a simulation result
            if sim.success:
                self.applyChanges(self.inp, self.motor, sim)
            self.inp = None
            self.motor = None

    def simCanceled(self):
        self.inp = None
        self.motor = None

    def applyChanges(self, inp, motor, simulation):
        pass
