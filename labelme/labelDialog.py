import uuid
from qtpy import QT_VERSION
from qtpy import QtCore
from qtpy import QtGui
from qtpy import QtWidgets
# from PyQt5.Qt import QLabel
# from qtpy import QLabel

QT5 = QT_VERSION[0] == '5'  # NOQA

from labelme.lib import labelValidator
from labelme.lib import newIcon
from labelme.lib import generate_label


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
        self.pts_display = QtWidgets.QLabel('Points')
        self.uuid_edit = QtWidgets.QLineEdit()
        self.label_edit = QtWidgets.QLineEdit()
        self.bnr_type_edit = QtWidgets.QLineEdit()
        self.cust_display_name_edit = QtWidgets.QLineEdit()
        self.cust_display_name_edit.editingFinished.connect(self.postProcess)
        self.pts_display_edit = QtWidgets.QLineEdit()
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
        grid.addWidget(self.pts_display, 5, 0)
        grid.addWidget(self.pts_display_edit, 5, 1)
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
        grid.addWidget(bb, 6,0)
        self.setLayout(grid)
        self.resize(QtCore.QSize(600,400))

#     def loadFlags(self, flags):
#         self.bnr_type_edit.addItems(flags.keys())

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
            uniq_labels = self.parent.labelList.get_uniq_labels()
            if self.parent.bnr_type in uniq_labels:
                uniq_labels = sorted(uniq_labels[self.parent.bnr_type])
                label = generate_label(self.parent.bnr_type, uniq_labels[-1])
            else:
                label = generate_label(self.parent.bnr_type)
            self.label_edit.setText(label)
            self.cust_display_name_edit.setText('')
            self.bnr_type_edit.setText(self.parent.bnr_type)
            self.bnr_type_edit.setReadOnly(True)
        else:
            shape = self.parent.labelList.get_shape_from_item(item)
            pts = [[each.x(), each.y()] for each in shape.points]
            self.pts_display_edit.setText(' , '.join(str(each) for each in pts))
            self.uuid_edit.setText(str(shape.uuid))
            self.label_edit.setText(shape.label)
            self.bnr_type_edit.setText(shape.bnr_type)
            self.cust_display_name_edit.setText(shape.cust_display_name)
        return (self.uuid_edit.text(),
                self.label_edit.text(),
                self.bnr_type_edit.text(),
                self.cust_display_name_edit.text())  if self.exec_() else None