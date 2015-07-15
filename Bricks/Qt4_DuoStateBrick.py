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
#   You should have received a copy of the GNU General Public License
#  along with MXCuBE.  If not, see <http://www.gnu.org/licenses/>.

import new
import re
import logging

from PyQt4 import QtGui
from PyQt4 import QtCore

from BlissFramework import Qt4_Icons
from BlissFramework.Utils import Qt4_widget_colors
from BlissFramework.Qt4_BaseComponents import BlissWidget


__category__ = 'Qt4_General'


class Qt4_DuoStateBrick(BlissWidget):

    STATES = {
        'unknown': (None, True, True, False, False),
        'disabled': (Qt4_widget_colors.LIGHT_RED, False, False, False, False),
        'error': (Qt4_widget_colors.LIGHT_RED, True, True, False, False),
        'out': (Qt4_widget_colors.LIGHT_GRAY, True, True, False, True),
        'moving': (Qt4_widget_colors.LIGHT_YELLOW, False, False, None, None),
        'in': (Qt4_widget_colors.LIGHT_GREEN, True, True, True, False),
        'automatic': (Qt4_widget_colors.WHITE, True, True, False, False)
    }

    def __init__(self, *args):
        BlissWidget.__init__(self,*args)

        # Hardware objects ----------------------------------------------------
        self.wrapper_hwobj=None

        # Internal values -----------------------------------------------------
        self.__expertMode = False
       
        # Properties ----------------------------------------------------------
        self.addProperty('mnemonic','string','')
        self.addProperty('forceNoControl','boolean',False)
        self.addProperty('expertModeControlOnly', 'boolean', False)
        self.addProperty('icons','string','')
        self.addProperty('in','string','in')
        self.addProperty('out','string','out')
        self.addProperty('setin','string','Set in')
        self.addProperty('setout','string','Set out')
        self.addProperty('username','string','')
        self.defineSlot('allowControl',())

        # Signals -------------------------------------------------------------

        # Slots ---------------------------------------------------------------
        #@self.defineSignal('duoStateBrickIn',())
        #@self.defineSignal('duoStateBrickOut',())
        #self.defineSignal('duoStateBrickMoving',())
      
        # Graphic elements ----------------------------------------------------
        self.main_gbox = QtGui.QGroupBox("none", self)
        self.main_gbox.setAlignment(QtGui.QLabel.AlignCenter)
        self.state_label = QtGui.QLabel('<b> </b>', self.main_gbox)

        self.buttons_widget = QtGui.QWidget(self.main_gbox)
        self.set_in_button = QtGui.QPushButton("Set in", self.buttons_widget)
        self.set_in_button.setCheckable(True)
        self.set_out_button = QtGui.QPushButton("Set out",self.buttons_widget)
        self.set_out_button.setCheckable(True)

        # Layout -------------------------------------------------------------- 
        self.buttons_widget_hlayout = QtGui.QHBoxLayout()
        self.buttons_widget_hlayout.addWidget(self.set_in_button)
        self.buttons_widget_hlayout.addWidget(self.set_out_button)
        self.buttons_widget_hlayout.setSpacing(0)
        self.buttons_widget_hlayout.setContentsMargins(0, 0, 0, 0)
        self.buttons_widget.setLayout(self.buttons_widget_hlayout)

        self.main_gbox_vlayout = QtGui.QVBoxLayout()
        self.main_gbox_vlayout.addWidget(self.state_label)
        self.main_gbox_vlayout.addWidget(self.buttons_widget)
        self.main_gbox_vlayout.setSpacing(1)
        self.main_gbox_vlayout.setContentsMargins(0, 2, 0, 0)
        self.main_gbox.setLayout(self.main_gbox_vlayout)

        main_layout = QtGui.QVBoxLayout()
        main_layout.addWidget(self.main_gbox)
        main_layout.setSpacing(0)
        main_layout.setContentsMargins(0, 0, 0, 0)
        self.setLayout(main_layout)

        # SizePolicies --------------------------------------------------------

        # Qt signal/slot connections ------------------------------------------
        self.set_in_button.toggled.connect(self.setIn)
        self.set_out_button.toggled.connect(self.setOut)

        # Other ---------------------------------------------------------------
        self.state_label.setAlignment(QtGui.QLabel.AlignCenter)
        self.state_label.setToolTip("Shows the current control state")
        self.set_in_button.setToolTip("Changes the control state")
        self.set_out_button.setToolTip("Changes the control state")           


    def setExpertMode(self, expert):
        self.__expertMode = expert
        self.buttons_widget.show()
        
        if not expert and self["expertModeControlOnly"]:
            self.buttons_widget.hide()

        
    def setIn(self,state):
        if state:
            self.wrapper_hwobj.setIn()
        else:
            self.set_in_button.blockSignals(True)
            self.set_in_button.setState(QPushButton.On)
            self.set_in_button.blockSignals(False)

    def setOut(self,state):
        if state:
            self.wrapper_hwobj.setOut()
        else:
            self.set_out_button.blockSignals(True)
            self.set_out_button.setState(QPushButton.On)
            self.set_out_button.blockSignals(False)

    def updateLabel(self,label):
        self.main_gbox.setTitle(label)

    def stateChanged(self,state,state_label=None):
        state = str(state)
        try:
            color=self.STATES[state][0]
        except KeyError:
            state='unknown'
            color=self.STATES[state][0]
        if color is None:
            color = Qt4_widget_colors.GROUP_BOX_GRAY

        Qt4_widget_colors.set_widget_color(self.state_label, color)
        #self.state_label.setPaletteBackgroundColor(QColor(color))
        if state_label is not None:
            self.state_label.setText('<b>%s</b>' % state_label)
        else:
            self.state_label.setText('<b>%s</b>' % state)
        try:
            in_enable=self.STATES[state][1]
            out_enable=self.STATES[state][2]
        except KeyError:
            in_enable=False
            out_enable=False

        self.set_in_button.setEnabled(in_enable)
        self.set_out_button.setEnabled(out_enable)

        try:
            in_state=self.STATES[state][3]
            out_state=self.STATES[state][4]
        except KeyError:
            in_state=QPushButton.Off
            out_state=QPushButton.Off
        if in_state is not None:
            self.set_in_button.blockSignals(True)
            self.set_in_button.setChecked(in_state)
            self.set_in_button.blockSignals(False)
        if out_state is not None:
            self.set_out_button.blockSignals(True)
            self.set_out_button.setChecked(out_state)
            self.set_out_button.blockSignals(False)

        if state=='in':
            self.emit(QtCore.SIGNAL("duoStateBrickMoving"), False)
            self.emit(QtCore.SIGNAL("duoStateBrickIn"), True)
        elif state=='out':
            self.emit(QtCore.SIGNAL("duoStateBrickMoving"), False)
            self.emit(QtCore.SIGNAL("duoStateBrickOut"), True)
        elif state=='moving':
            self.emit(QtCore.SIGNAL("duoStateBrickMoving"), True)
        elif state=='error' or state=='unknown' or state=='disabled':
            self.emit(QtCore.SIGNAL("duoStateBrickMoving"), False)
            self.emit(QtCore.SIGNAL("duoStateBrickIn"), False)
            self.emit(QtCore.SIGNAL("duoStateBrickOut"), False)

    def allowControl(self,enable):
        if self['forceNoControl']:
            return
        if enable:
            self.buttons_widget.show()
        else:
            self.buttons_widget.hide()

    def run(self):
        if self.wrapper_hwobj is None:
            self.main_gbox.hide()

    def stop(self):
        self.main_gbox.show()

    def propertyChanged(self,propertyName,oldValue,newValue):
        if propertyName=='mnemonic':
            if self.wrapper_hwobj is not None:
                self.wrapper_hwobj.duoStateChangedSignal.disconnect(self.stateChanged)

            h_obj=self.getHardwareObject(newValue)
            if h_obj is not None:
                self.wrapper_hwobj=WrapperHO(h_obj)
                self.main_gbox.show()
                
                if self['username']=='':
                    self['username']=self.wrapper_hwobj.userName()

                help_text=self['setin']+" the "+self['username'].lower()
                self.set_in_button.setToolTip(help_text)
                help_text=self['setout']+" the "+self['username'].lower()
                self.set_out_button.setToolTip(help_text)
                self.main_gbox.setTitle(self['username'])
                self.wrapper_hwobj.duoStateChangedSignal.connect(self.stateChanged)
                self.stateChanged(self.wrapper_hwobj.getState())
            else:
                self.wrapper_hwobj=None
                #self.main_gbox.hide()
        elif propertyName=='expertModeControlOnly':
            if newValue:
                if self.__expertMode:
                    self.buttons_widget.show()
                else:
                    self.buttons_widget.hide()
            else:
                self.buttons_widget.show()
        elif propertyName=='forceNoControl':
            if newValue:
                self.buttons_widget.hide()
            else:
                self.buttons_widget.show()
        elif propertyName=='icons':
            w=self.fontMetrics().width("Set out")
            icons_list=newValue.split()
            try:
                self.set_in_button.setIcon(Qt4_Icons.load_icon(icons_list[0]))
            except IndexError:
                self.set_in_button.setText(self['setin'])
                #self.set_in_button.setMinimumWidth(w)
            try:
                self.set_out_button.setIcon(Qt4_Icons.load_icon(icons_list[1]))
            except IndexError:
                self.set_out_button.setText(self['setout'])
                #self.set_out_button.setMinimumWidth(w)

        elif propertyName=='in':
            if self.wrapper_hwobj is not None:
                self.stateChanged(self.wrapper_hwobj.getState())

        elif propertyName=='out':
            if self.wrapper_hwobj is not None:
                self.stateChanged(self.wrapper_hwobj.getState())

        elif propertyName=='setin':
            icons=self['icons']
            #w=self.fontMetrics().width("Set out")
            icons_list=icons.split()
            try:
                i=icons_list[0]
            except IndexError:
                self.set_in_button.setText(newValue)
                #self.set_in_button.setMinimumWidth(w)
            help_text=newValue+" the "+self['username'].lower()
            self.set_in_button.setToolTip(help_text)

        elif propertyName=='setout':
            icons=self['icons']
            #w=self.fontMetrics().width("Set out")
            icons_list=icons.split()
            try:
                i=icons_list[1]
            except IndexError:
                self.set_out_button.setText(newValue)
                #self.set_out_button.setMinimumWidth(w)
            help_text=newValue+" the "+self['username'].lower()
            self.set_out_button.setToolTip(help_text)

        elif propertyName=='username':
            if newValue=='':
                if self.wrapper_hwobj is not None:
                    name=self.wrapper_hwobj.userName()
                    if name!='':
                        self['username']=name
                        return
            help_text = self['setin']+" the "+newValue.lower()
            self.set_in_button.setToolTip(help_text)
            help_text = self['setout']+" the "+newValue.lower()
            self.set_out_button.setToolTip(help_text)
            self.main_gbox.setTitle(self['username'])

        else:
            BlissWidget.propertyChanged(self,propertyName,oldValue,newValue)

###
### Wrapper around different hardware objects, to make them have the
### same behavior to the brick
###
class WrapperHO(QtCore.QObject):
    wagoStateDict={'in':'in', 'out':'out', 'unknown':'unknown'}

    shutterStateDict = {'fault': 'error', 'opened': 'in', 
                        'closed': 'out', 'unknown': 'unknown', 
                        'moving': 'moving', 'automatic': 'automatic',
                        'disabled': 'disabled', 'error':'error'}
    doorInterlockStateDict = {'locked': 'out', 'unlocked': 'disabled',
                              'locked_active' : 'out',
                              'locked_inactive': 'disabled',
                              'error': 'error'}

    motorWPosDict=('out', 'in')
    motorWStateDict=('disabled', 'error', None, 'moving',\
        'moving', 'moving')

    STATES = ('unknown','disabled','error','out','moving','in','automatic')

    duoStateChangedSignal = QtCore.pyqtSignal(str)

    def __init__(self, hardware_obj):
        QtCore.QObject.__init__(self)

        self.setIn = new.instancemethod(lambda self: None, self)
        self.setOut = self.setIn 
        self.getState = new.instancemethod(lambda self: "unknown", self)
        self.dev=hardware_obj
        try:
            sClass = str(self.dev.__class__)
            i, j = re.search("'.*'", sClass).span()
        except:
            dev_class = sClass
        else:
            dev_class = sClass[i+1:j-1]
        self.devClass = dev_class.split('.')[-1]

        if self.devClass=="Device":
            self.devClass="Procedure"

        if self.devClass=="TangoShutter":
            self.devClass="Shutter"

        #2011-08-30-bessy-mh: let the wrapper also feel responsible for my new ShutterEpics hardware object
        #                     identical to the original Shutter hardware object
        if self.devClass == "ShutterEpics":
            self.devClass = "Shutter"
        #2011-08-30-bessy-mh: end

        #2013-10-31-bessy-mh: ... and for the MD2 shutter hardware object too!
        if self.devClass == "MD2v4_FastShutter":
            self.devClass = "Shutter"

        if self.devClass == "TempShutter":
            self.devClass = "Shutter"

        if self.devClass == "TINEIcsShutter":
            self.devClass = "Shutter"

        #2013-10-31-bessy-mh: end
            
        if not self.devClass in ("WagoPneu", "Shutter", "SpecMotorWSpecPositions", "Procedure", "DoorInterlock"):
          self.devClass = "WagoPneu"

        initFunc = getattr(self, "init%s" % self.devClass)
        initFunc()
        self.setIn = getattr(self, "setIn%s" % self.devClass)
        self.setOut = getattr(self, "setOut%s" % self.devClass)
        self.getState = getattr(self, "getState%s" % self.devClass)

    def __getstate__(self):
        dict = self.__dict__.copy()
        del dict["setIn"]
        del dict["setOut"]
        del dict["getState"]
        return dict

    def __setstate__(self, dict):
        self.__dict__ = dict.copy()
        self.setIn = new.instancemethod(lambda self: None, self)
        self.setOut = self.setIn
        self.getState = new.instancemethod(lambda self: "unknown", self)

    def userName(self):
        return self.dev.userName()

    # WagoPneu HO methods
    def initWagoPneu(self):
        self.dev.connect(self.dev,'wagoStateChanged', self.stateChangedWagoPneu)
    def setInWagoPneu(self):
        self.duoStateChangedSignal.emit('moving')
        self.dev.wagoIn()
    def setOutWagoPneu(self):
        self.duoStateChangedSignal.emit('moving') 
        self.dev.wagoOut()
    def stateChangedWagoPneu(self,state):
       

        try:
            state=WrapperHO.wagoStateDict[state]
        except KeyError:
            state='error'
        self.duoStateChangedSignal.emit(state)
    def getStateWagoPneu(self):
        state=self.dev.getWagoState()
        try:
            state=WrapperHO.wagoStateDict[state]
        except KeyError:
            state='error'
        return state

    # Shutter HO methods
    def initShutter(self):
        self.dev.connect(self.dev, 'shutterStateChanged', self.stateChangedShutter)
    def setInShutter(self):
        self.dev.openShutter()
    def setOutShutter(self):
        self.dev.closeShutter()
    def stateChangedShutter(self,state):
        try:
            state=WrapperHO.shutterStateDict[state]
        except KeyError:
            state='error'
        self.duoStateChangedSignal.emit(state)
    def getStateShutter(self):
        state=self.dev.getShutterState()
        try:
            state=WrapperHO.shutterStateDict[state]
        except KeyError:
            state='error'
        return state

    # SpecMotorWSpecPositions HO methods
    def initSpecMotorWSpecPositions(self):
        self.positions=None
        self.dev.connect(self.dev, 'predefinedPositionChanged', self.positionChangedSpecMotorWSpecPositions)
        self.dev.connect(self.dev, 'stateChanged', self.stateChangedSpecMotorWSpecPositions)
        self.dev.connect(self.dev, 'newPredefinedPositions', self.newPredefinedSpecMotorWSpecPositions)
    def setInSpecMotorWSpecPositions(self):
        if self.positions is not None:
            self.dev.moveToPosition(self.positions[1])
    def setOutSpecMotorWSpecPositions(self):
        if self.positions is not None:
            self.dev.moveToPosition(self.positions[0])
    def stateChangedSpecMotorWSpecPositions(self,state):
        #logging.info("stateChangedSpecMotorWSpecPositions %s" % state)
        try:
            state = WrapperHO.motorWStateDict[state]
        except IndexError:
            state = 'error'
        if state is not None:
            self.duoStateChangedSignal.emit(state) 
    def positionChangedSpecMotorWSpecPositions(self,pos_name,pos):
        if self.dev.getState()!=self.dev.READY:
            return
        state="error"
        if self.positions is not None:
            for i in range(len(self.positions)):
                if pos_name==self.positions[i]:
                    state=WrapperHO.motorWPosDict[i]
        self.duoStateChangedSignal.emit(state)
    def getStateSpecMotorWSpecPositions(self):
        if self.positions is None:
            return "error"
        curr_pos=self.dev.getCurrentPositionName()
        if curr_pos is None:
            state=self.dev.getState()
            try:
                state=WrapperHO.motorWStateDict[state]
            except IndexError:
                state='error'
            return state
        else:
            for i in range(len(self.positions)):
                if curr_pos==self.positions[i]:
                    return WrapperHO.motorWPosDict[i]                    
        return 'error'
    def newPredefinedSpecMotorWSpecPositions(self): 
        self.positions=self.dev.getPredefinedPositionsList()
        self.positionChangedSpecMotorWSpecPositions(self.dev.getCurrentPositionName(),self.dev.getPosition())

    # Procedure HO methods
    def initProcedure(self):
        cmds=self.dev.getCommands()

        self.setInCmd=None
        self.setOutCmd=None

        try:
            channel=self.dev.getChannelObject("dev_state")
        except KeyError:
            channel=None
        self.stateChannel=channel
        if self.stateChannel is not None:
            self.state_dict={'OPEN':'in', 'CLOSED':'out', 'ERROR':'error', '1':'in', '0':'out'}
            self.stateChannel.connectSignal('update', self.channelUpdate)
        else:
            self.state_dict={}

        for c in cmds:
            if c.name()=="set in":
                self.setInCmd=c
                if self.stateChannel is not None:
                    self.setInCmd.connectSignal('commandReplyArrived', self.procedureSetInEnded)
                    self.setInCmd.connectSignal('commandBeginWaitReply', self.procedureStarted)
                    self.setInCmd.connectSignal('commandFailed', self.procedureAborted)
                    self.setInCmd.connectSignal('commandAborted', self.procedureAborted)
            elif c.name()=="set out":
                self.setOutCmd=c
                if self.stateChannel is not None:
                    self.setOutCmd.connectSignal('commandReplyArrived', self.procedureSetOutEnded)
                    self.setOutCmd.connectSignal('commandBeginWaitReply', self.procedureStarted)
                    self.setOutCmd.connectSignal('commandFailed', self.procedureAborted)
                    self.setOutCmd.connectSignal('commandAborted', self.procedureAborted)

    def channelUpdate(self,value):
        try:
            key=self.dev.statekey
        except AttributeError:
            pass
        else:
            try:
                state=value[key]
            except TypeError:
                state='error'
        try:
            state=self.state_dict[state]
        except KeyError:
            pass
        self.duoStateChangedSignal.emit(state)
    def setInProcedure(self):
        if self.setInCmd is not None:
            self.setInCmd()
    def setOutProcedure(self):
        if self.setOutCmd is not None:
            self.setOutCmd()
    """
    def stateChangedProcedure(self,state):
        pass
    """
    def getStateProcedure(self):
        if self.stateChannel is not None:
            try:
                state=self.stateChannel.getValue()
            except:
                state='error'
            else:
                try:
                    key=self.dev.statekey
                except AttributeError:
                    pass
                else:
                    try:
                        state=state[key]
                    except TypeError:
                        state='error'
            try:
                state=self.state_dict[state]
            except KeyError:
                pass
            return state
        return "unknown"
    def procedureSetInEnded(self, *args):
        self.duoStateChangedSignal.emit('in')
        
    def procedureSetOutEnded(self, *args):
        self.duoStateChangedSignal.emit('out')
        
    def procedureStarted(self, *args):
        self.duoStateChangedSignal.emit('moving')
        
    def procedureAborted(self, *args):
        self.duoStateChangedSignal.emit('error')