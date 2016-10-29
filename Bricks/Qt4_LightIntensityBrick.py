#
#  Project: MXCuBE
#  https://github.com/mxcube.
#
#  This file is part of MXCuBE software.
#
#  MXCuBE is free software: you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation, either version 3 of the License, or
#  (at your option) any later version.
#
#  MXCuBE is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with MXCuBE.  If not, see <http://www.gnu.org/licenses/>.

from PyQt4 import QtGui
from PyQt4 import QtCore 

from BlissFramework import Qt4_Icons
from BlissFramework.Utils import Qt4_widget_colors
from BlissFramework.Qt4_BaseComponents import BlissWidget

__category__ = "General"

class Qt4_LightIntensityBrick(BlissWidget):
    """
    Descript. : EnergyBrick displays actual energy and wavelength.
    """
    STATE_COLORS = (Qt4_widget_colors.LIGHT_RED,     # error
                    Qt4_widget_colors.DARK_GRAY,     # unknown
                    Qt4_widget_colors.LIGHT_GREEN,   # ready
                    Qt4_widget_colors.LIGHT_YELLOW,  
                    Qt4_widget_colors.LIGHT_YELLOW,
                    Qt4_widget_colors.LIGHT_YELLOW)

    def __init__(self, *args):
        """
        Descript. : Initiates BlissWidget Brick
        """
        BlissWidget.__init__(self, *args)

        # Properties ----------------------------------------------------------       
        self.addProperty('mnemonic', 'string', '')
        self.addProperty('label', 'string', '')

        # Signals ------------------------------------------------------------

        # Slots ---------------------------------------------------------------

        # Hardware objects ----------------------------------------------------
        self.light_hwobj = None

        # Internal values -----------------------------------------------------

        # Graphic elements ----------------------------------------------------
        self.group_box = QtGui.QGroupBox("", self)
        self.intensity_spinbox = QtGui.QDoubleSpinBox(self.group_box)
        self.intensity_spinbox.setMinimum(0)
        self.intensity_spinbox.setMaximum(100)
        self.intensity_spinbox.setDecimals(0)
        self.intensity_spinbox.setMinimumSize(QtCore.QSize(45, 25))
        self.intensity_spinbox.setMaximumSize(QtCore.QSize(55, 25))
        self.intensity_spinbox.setToolTip("Set the light intensity from 0% until 100%")
 
        # Layout --------------------------------------------------------------
        _light_widget_hlayout = QtGui.QHBoxLayout(self.intensity_spinbox)
        _light_widget_hlayout.setSpacing(0)
        _light_widget_hlayout.setContentsMargins(0, 0, 0, 0)

        _group_box_gridlayout = QtGui.QGridLayout(self.group_box)
        _group_box_gridlayout.addWidget(self.intensity_spinbox, 0, 0)
        _group_box_gridlayout.setSpacing(0)
        _group_box_gridlayout.setContentsMargins(1, 1, 1, 1) 

        _main_vlayout = QtGui.QVBoxLayout(self)
        _main_vlayout.setSpacing(0)
        _main_vlayout.setContentsMargins(0, 0, 2, 2)
        _main_vlayout.addWidget(self.group_box)

        # SizePolicies --------------------------------------------------------

        # Qt signal/slot connections ------------------------------------------
        spinbox_event = SpinBoxEvent(self.intensity_spinbox) 
        self.intensity_spinbox.installEventFilter(spinbox_event)
        spinbox_event.returnPressedSignal.connect(self.current_value_changed) 
        self.intensity_spinbox.lineEdit().textEdited.connect(self.intensity_value_edited)

        # Other --------------------------------------------------------------- 
        
    def propertyChanged(self, property_name, old_value, new_value):
        """
        Descript. : Event triggered when user property changed in the property
                    editor. 
        Args.     : property_name (string), old_value, new_value
        Return.   : None
        """
        if property_name == 'mnemonic':
            if self.light_hwobj is not None:
                self.disconnect(self.light_hwobj, QtCore.SIGNAL('intensityChanged'), self.intensity_changed)
            self.light_hwobj = self.getHardwareObject(new_value)
            if self.light_hwobj is not None:
                self.connect(self.light_hwobj, QtCore.SIGNAL('intensityChanged'), self.intensity_changed)

                if self.light_hwobj.isReady():
                    self.connected()
                else:
                    self.disconnected()
            else:
                self.disconnected()
        elif property_name == 'label':
            self.group_box.setTitle(new_value)
        else:
            BlissWidget.propertyChanged(self, property_name, old_value, new_value)

    def connected(self):
        """
        Descript. :
        Args.     :
        Return.   : 
        """
        self.setEnabled(True)

    def disconnected(self):
        """
        Descript. :
        Args.     :
        Return.   : 
        """
        self.setEnabled(False)

    def intensity_changed(self, intensity_value):
        """
        Descript. :
        Args.     :
        Return.   : 
        """
        self.intensity_spinbox.setValue(float(intensity_value))
        self.intensity_value_edited()

    def current_value_changed(self):
        """
        Descript. :
        Args.     :
        Return.   : 
        """
        self.light_hwobj.set_intensity(float(self.intensity_spinbox.value()))
        self.intensity_value_edited()

    def intensity_value_edited(self, value=None):
        """
        Descript. :
        Args.     :
        Return.   : 
        """
        if ((value == "") or (value is None)):
            Qt4_widget_colors.set_widget_color(self.intensity_spinbox.lineEdit(),
                                               Qt4_widget_colors.LINE_EDIT_ACTIVE,
                                               QtGui.QPalette.Base)
        else: 
            Qt4_widget_colors.set_widget_color(self.intensity_spinbox.lineEdit(), 
                                               Qt4_widget_colors.LINE_EDIT_CHANGED,
                                               QtGui.QPalette.Base)

class SpinBoxEvent(QtCore.QObject):
    returnPressedSignal = QtCore.pyqtSignal()
    contextMenuSignal = QtCore.pyqtSignal()

    def eventFilter(self,  obj,  event):
        if event.type() == QtCore.QEvent.KeyPress:
            if event.key() in [QtCore.Qt.Key_Enter, 
                               QtCore.Qt.Key_Return]:
                self.returnPressedSignal.emit()
            
        elif event.type() == QtCore.QEvent.MouseButtonRelease:
            self.returnPressedSignal.emit()
        elif event.type() == QtCore.QEvent.ContextMenu:
            self.contextMenuSignal.emit()
        return False
