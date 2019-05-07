import abc
from typing import List,Set
import sys
from SpecParser import DeviceInfo

SENSING = 0
ACTUATION = 1

'''
    Abstraction classes:
'''
class Abstraction:
    name = ''
    childAbstractions = set() # Abstraction Set using the name of string
    parentAbstractions = set() # Abstraction Set using the name of string
    cost = sys.maxInt
    moduleName = ''
    childDeviceInstance = set() # DeviceInstance Set
    range = set()
    state = None
    type = -1
    busy = False

    def __init__(self, name, moduleName, initState, type):
        self.moduleName = moduleNname
        self.name = name
        self.state = initState
        self.type = type

    def setState(self, state):
        self.state = state

    def getState(self):
        return self.state

    def updateCost(self, cost):
        self.cost = cost

    def isBusy(self):
        return self.busy

    def setUsing(self):
        self.busy = True

    def releaseUsing(self):
        self.busy = False

    # This function needs to be overwritten by the child class
    def performFunc(self, *args):
        return

    def addRange(self, range):
        if range in self.range:
            return
        # range is the string
        self.range.append(range)
        for abs in childAbstraction:
            abs.addRange(range)

        for device in childDeviceInstance:
            device.tagRange(range)

    def appendChildDeviceInstance(self, childDeviceInstance):
        self.childDeviceInstance.append(childDeviceInstance)

    def appendChildAbstraction(self,childAbstraction):
        self.childAbstractions.append(childAbstraction)

    def appendParentAbstraction(self,parentAbstraction):
        self.parentAbstractions.append(parentAbstraction)

    def __hash__(self):
        return hash(self.name)

    def __eq__(self, other):
        return (self.__class__ == other.__class__ and self.name == other.name)

    def __str__(self):
        abstractionStr = "Abstraction Name: "+self.name
        if self.childAbstractions is not None:
            abstractionStr = abstractionStr + "\n"+"Children:\n"
            for child in self.childAbstractions:
                abstractionStr = abstractionStr + "\t -"+child.name+"\n"
        if self.parentAbstractions is not None:
            abstractionStr = "Parents:\n"
            for parent in self.parentAbstractions:
                abstractionStr= abstractionStr + "\t -"+parent.name+"\n"
        return abstractionStr


class DeviceInstance:
    name = ''
    satus = None
    parentAbstractions = None
    deviceInfo = None

    def __init__(self, status, name, deviceInfo, parentAbstractions = None):
        self.name = name
        self.status = status # On or OFF. Or discrete value.
        self.parentAbstractions: Set[Abstraction] = parentAbstractions
        self.deviceInfo = deviceInfo
