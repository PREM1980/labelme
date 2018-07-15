import uuid
from qtpy import QT_VERSION
from qtpy import QtCore
from qtpy import QtGui
from qtpy import QtWidgets
from PyQt5.Qt import QLabel

QT5 = QT_VERSION[0] == '5'  # NOQA

from labelme.lib import labelValidator
from labelme.lib import newIcon


# TODO(unknown):
# - Calculate optimal position so as not to go out of screen area.


class LabelQLineEdit(QtWidgets.QLineEdit):

    def setListWidget(self, list_widget):
        self.list_widget = list_widget

    def keyPressEvent(self, e):
        if e.key() in [QtCore.Qt.Key_Up, QtCore.Qt.Key_Down]:
            self.list_widget.keyPressEvent(e)
        else:
            super(LabelQLineEdit, self).keyPressEvent(e)


class LabelDialog(QtWidgets.QDialog):

    def __init__(self, text="Enter object label", parent=None, labels=None,
                 sort_labels=True, show_text_field=True):
        super(LabelDialog, self).__init__(parent)
        self.parent = parent
        self.uuid = QtWidgets.QLabel('uuid')
        self.label = QtWidgets.QLabel('Label')            
        self.bnr_type = QtWidgets.QLabel('Type')
        self.cust_display_name = QtWidgets.QLabel('Customer Display Name')        
        self.uuid_edit = QtWidgets.QLineEdit()
        self.label_edit = QtWidgets.QLineEdit()
        self.bnr_type_edit = QtWidgets.QComboBox()        
        self.cust_display_name_edit = QtWidgets.QLineEdit()
        self.cust_display_name_edit.editingFinished.connect(self.postProcess)
        grid = QtWidgets.QGridLayout()
        grid.setSpacing(10)
        grid.addWidget(self.uuid, 1, 0)
        grid.addWidget(self.uuid_edit, 1, 1)
        grid.addWidget(self.label, 2, 0)
        grid.addWidget(self.label_edit, 2, 1)        
        grid.addWidget(self.bnr_type, 3, 0)
        grid.addWidget(self.bnr_type_edit, 3, 1)                
        grid.addWidget(self.cust_display_name, 4, 0)
        grid.addWidget(self.cust_display_name_edit, 4, 1)                
        # buttons
        self.buttonBox = bb = QtWidgets.QDialogButtonBox(
            QtWidgets.QDialogButtonBox.Ok | QtWidgets.QDialogButtonBox.Cancel,
            QtCore.Qt.Horizontal,
            self,
        )
        bb.button(bb.Ok).setIcon(newIcon('done'))
        bb.button(bb.Cancel).setIcon(newIcon('undo'))
        bb.accepted.connect(self.validate)
        bb.rejected.connect(self.reject)
        grid.addWidget(bb, 5,0)
        self.setLayout(grid)

    def loadFlags(self, flags):
        self.bnr_type_edit.addItems(flags.keys())

    def validate(self):
        text = self.label_edit.text()
        if hasattr(text, 'strip'):
            text = text.strip()
        else:
            text = text.trimmed()
        if text:
            self.accept()

    def postProcess(self):        
        text = self.cust_display_name_edit.text()
        if hasattr(text, 'strip'):
            text = text.strip()
        else:
            text = text.trimmed()
        self.cust_display_name_edit.setText(text)
    
    def popUp(self, item=None):
        
        if item is None:
            self.uuid_edit.setText(str(uuid.uuid1()))
            self.uuid_edit.setReadOnly(True)
            self.label_edit.setText('')
            self.cust_display_name_edit.setText('')
        else:
            shape = self.parent.labelList.get_shape_from_item(item)
            self.uuid_edit.setText(str(shape.uuid))
            self.label_edit.setText(shape.label)
            index = self.bnr_type_edit.findText(shape.bnr_type, QtCore.Qt.MatchFixedString)
              
            if index >= 0:
                self.bnr_type_edit.setCurrentIndex(index)
    #         self.type_edit.setText(item.bnr_type)    
            self.cust_display_name_edit.setText(shape.cust_display_name)
        return (self.uuid_edit.text(),
                self.label_edit.text(),
                self.bnr_type_edit.currentText(),
                self.cust_display_name_edit.text())  if self.exec_() else None