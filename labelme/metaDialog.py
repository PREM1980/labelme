import uuid
import datetime
import sys
from qtpy import QT_VERSION
from qtpy import QtCore
from qtpy import QtGui
from qtpy import QtWidgets
from geopy.geocoders import Nominatim
from labelme import logger

QT5 = QT_VERSION[0] == '5'  # NOQA

from labelme.lib import newIcon
from labelme.lib import getUUID

class Meta(object):
    street1 = ''
    street2 = ''
    city = ''
    state = ''
    country = ''
    lat_long = ''
    bnr_display_name = ''
    cust_display_name = ''
    uuid = ''
    

class Example(QtWidgets.QMainWindow):
    count = 0
    def __init__(self, *args, **kwargs):
        super(Example, self).__init__(*args, **kwargs)            
        self.initUI()
    
    def initUI(self):
        self.meta = MetaDialog()
        meta = Meta()
        meta.street1 = '11928'
        meta.street2 = 'appaloosa way'
        meta.city = 'north potomac'
        meta.state = 'md'
        meta.country = 'us'
        meta.date_created = '2018-07-23'
        meta.bnr_display_name = 'bnr'
        meta.cust_display_name = 'cdn'
        meta.lat_long = '39.0825906995 , -77.2460822352'
        meta.uuid = '4bc3d141-8eb1-11e8-b8b9-14abc58382ef'        
        print self.meta.popUp(meta)
    

class MetaDialog(QtWidgets.QDialog):

    def __init__(self, parent=None,):
        super(MetaDialog, self).__init__(parent)
        self.parent = parent
        self.setWindowTitle('Meta information')
        regex_rules = 'a-zA-Z0-9.,_ -#(){}'  
        regex = QtCore.QRegExp('^['+regex_rules +']+$')              
        self.street1 = QtWidgets.QLabel('street1')
        self.street2 = QtWidgets.QLabel('street2')
        self.city = QtWidgets.QLabel('City')
        self.state = QtWidgets.QLabel('State')
        self.country = QtWidgets.QLabel('Country')                                    
        self.date_created = QtWidgets.QLabel('Date Created')
        self.lat_long = QtWidgets.QLabel('lat/long')
        self.cust_display_name = QtWidgets.QLabel('Customer display name')
        self.bnr_display_name = QtWidgets.QLabel('Bossanova internal name')
        self.uuid = QtWidgets.QLabel('UUID')        
        self.calc_lat_long = QtWidgets.QPushButton('Calc')        
        
        self.street1_edit = QtWidgets.QLineEdit()
        self.street2_edit = QtWidgets.QLineEdit()
        self.city_edit = QtWidgets.QLineEdit()        
        self.state_edit = QtWidgets.QLineEdit()       
        self.country_edit = QtWidgets.QLineEdit()               
        self.lat_long_edit = QtWidgets.QLineEdit()
        self.date_created_edit = QtWidgets.QLineEdit()
        self.date_created_edit.setText(datetime.datetime.now().strftime('%Y-%m-%d'))
        self.date_created_edit.setReadOnly(True)
        self.cust_display_name_edit = QtWidgets.QLineEdit()
        self.bnr_display_name_edit = QtWidgets.QLineEdit()
        self.uuid_edit = QtWidgets.QLineEdit()
        self.uuid_edit.setText(getUUID())
        self.uuid_edit.setReadOnly(True)
        self.calc_lat_long.clicked.connect(self._calculate_lat_long)        
        self.widgets = [self.street1_edit, self.street2_edit, self.city_edit, self.state_edit,
                        self.country_edit, self.bnr_display_name_edit, self.cust_display_name_edit]                        
        self._set_widget_tooltip_property(self.widgets, regex_rules)        
        self._set_widget_edit_property(self.widgets, self.postProcess)
        self._set_widget_validators(self.widgets, regex)
        
        grid = QtWidgets.QGridLayout()
        grid.setSpacing(10)
        grid.addWidget(self.street1, 0, 0)
        grid.addWidget(self.street1_edit, 0, 1)        
        grid.addWidget(self.street2, 1, 0)
        grid.addWidget(self.street2_edit, 1, 1)        
        grid.addWidget(self.city, 2, 0)
        grid.addWidget(self.city_edit, 2, 1)
        grid.addWidget(self.state, 3, 0)
        grid.addWidget(self.state_edit, 3, 1)
        grid.addWidget(self.country, 5, 0)
        grid.addWidget(self.country_edit, 5, 1)                                        
        grid.addWidget(self.date_created, 6, 0)
        grid.addWidget(self.date_created_edit, 6, 1)
        grid.addWidget(self.lat_long, 7, 0)
        grid.addWidget(self.lat_long_edit, 7, 1)                
        grid.addWidget(self.calc_lat_long, 7, 2)
        grid.addWidget(self.cust_display_name, 8, 0)
        grid.addWidget(self.cust_display_name_edit, 8, 1)
        grid.addWidget(self.bnr_display_name, 9, 0)
        grid.addWidget(self.bnr_display_name_edit, 9, 1)
        grid.addWidget(self.uuid, 10, 0)
        grid.addWidget(self.uuid_edit, 10, 1)                
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
        grid.addWidget(bb, 11,0)
        self.setLayout(grid)
    
    def _set_widget_tooltip_property(self, widgets, regex_rules):
        for widget in widgets:
            widget.setToolTip('Only alphanumeric & ' + regex_rules + ' characters.')
    
    def _set_widget_edit_property(self, widgets, f):
        for widget in widgets:
            widget.editingFinished.connect(f)
    
    def _set_widget_validators(self, widgets, regex):
        for widget in widgets:
            widget.setValidator(QtGui.QRegExpValidator(regex, widget))
    
    def _calculate_lat_long(self):
        geolocator = Nominatim()
        street1 = self.street1_edit.text()
        street2 = self.street2_edit.text()
        city = self.city_edit.text()
        state = self.state_edit.text()
        country = self.country_edit.text()        
        addr = ' '.join([each for each in [street1, street2, city, state, country] 
                         if len(each) > 0])
        msg = QtWidgets.QMessageBox()
        msg.setIcon(QtWidgets.QMessageBox.Information)                
        if addr:
            location = self._get_lat_long(addr)
            if location:
                self.lat_long_edit.setText(str(location.latitude) + ' , ' + str(location.longitude))
                self.lat_long_edit.setReadOnly(True)
            else:            
                msg.setText("""Lat & Long can't be found for the given address.""")
                msg.exec_()
        else:
            msg.setText("""Please enter a valid address.""")
            msg.exec_()
            
    def _get_lat_long(self, addr):
        geolocator = Nominatim()
        try:
            geolocator.geocode(addr, timeout=10, exactly_one=False)
        except Exception as e:
            logger.error('geopy exception {0}'.format(e))
            return None        
    
    def postProcess(self):
        sender = self.sender()
        validator = sender.validator()
        state = validator.validate(sender.text(), 0)[0]        
        text = sender.text()
        if hasattr(text, 'strip'):
            text = text.strip()
        else:
            text = text.trimmed()
        
        sender.setText(text)        
        if state == QtGui.QValidator.Acceptable:
            color = '#c4df9b' # green
        else:
            color = '#f6989d' # red
        sender.setStyleSheet('QLineEdit { background-color: %s }' % color)
        
    def validate(self):
        self.meta = {}
        self.meta['street1'] = self.street1_edit.text()
        self.meta['street2'] = self.street2_edit.text()        
        self.meta['city'] = self.city_edit.text()
        self.meta['state'] = self.state_edit.text()
        self.meta['country'] = self.country_edit.text()
        self.meta['date_created'] = self.date_created_edit.text()
        self.meta['lat_long'] = self.lat_long_edit.text()
        self.meta['cust_display_name'] = self.cust_display_name_edit.text()
        self.meta['bnr_display_name'] = self.bnr_display_name_edit.text()
        self.meta['uuid'] = self.uuid_edit.text()
        self.accept()

    def popUp(self, meta=None):
        if meta is not None:
            self.street1_edit.setText(meta['street1'])
            self.street2_edit.setText(meta['street2'])
            self.city_edit.setText(meta['city'])
            self.state_edit.setText(meta['state'])
            self.country_edit.setText(meta['country'])
            self.lat_long_edit.setText(meta['lat_long'])
            self.lat_long_edit.setReadOnly(True)
            self.date_created_edit.setText(meta['date_created'])
            self.bnr_display_name_edit.setText(meta['bnr_display_name'])
            self.cust_display_name_edit.setText(meta['cust_display_name'])
            self.uuid_edit.setText(meta['uuid'])
            self.uuid_edit.setReadOnly(True)            
        return self.meta if self.exec_() else None
        
        
if __name__ == '__main__':
    
    app = QtWidgets.QApplication(sys.argv)
    ex = Example()
#     ex.show()
    sys.exit(app.exec_())    