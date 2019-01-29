import json
import os
from pprint import pprint
PATH = '/tmp/devices'

class DeviceInfo:
    ip = ""
    classSpect = ""
    descrpt = ""
    location = ""
    mac = ""
    range = ""
    id = -1

    def __init__(self, ip, classSpect, descrpt, location, mac, range):
        self.ip = ip
        self.classSpect = classSpect
        self.descrpt = descrpt
        self.location = location
        self.mac = mac
        self.range = range

    def assignID(self, id):
        self.id = id


# add the device information to JSON specs
def addDevice(addInfo):
    temp = {"ip": addInfo.ip, "classSpect": addInfo.classSpect, "descrpt":
    addInfo.descrpt, "location": addInfo.location, "mac": addInfo.mac,
    "range" : addInfo.range}
    return temp

# Register the device. The device must be associated with the specific device
def register(deviceInfo):
    # create the JSON file at the beginning
    try:
        with open(PATH, 'r+') as fh:
            pass
    except IOError:
        with open(PATH, 'w+') as fh:
            pass

    with open(PATH, 'r+') as fh:
        try:
            data = json.load(fh)
        except ValueError:
            data = {}
            # print("loading error")
            # return -1

        print(data)
        if data.get('class') is None:
            data['last_id'] = 1
            entry = {deviceInfo.classSpect : [1]}
            data['class'] = entry
            data['uid'] = {'1': addDevice(deviceInfo)}

        elif data['class'].get(deviceInfo.classSpect) is None:
            lastId = data['last_id']
            lastId = lastId + 1
            data['class'][deviceInfo.classSpect] = [lastId]
            data['uid'][str(lastId)] = addDevice(deviceInfo)
            data['last_id'] = lastId

        else:
            lastId = data['last_id']
            lastId = lastId + 1
            data['class'][deviceInfo.classSpect].append(lastId)
            data['uid'][str(lastId)] = addDevice(deviceInfo)
            data['last_id'] = lastId
        print("After! \n")
        pprint(data)
        json.dump(data, fh)
        return data['last_id']

# remove a device. Each device could be registered more than once by different
# services.
def delete(uid):
    # Error checking.
    try:
        data = json.load(fh)
    except ValueError:
        return -1

    with open(PATH, 'r+') as fh:
        try:
            data = json.load(fh)
        except ValueError:
            print("loading error")
            return -1

        print(data)
        if data.get('class') is None or data.get('uid') is None or data['uid'].get(uid) is None:
            return 1

        classSpect = data['uid'][uid]['classSpect']
        del data['uid'][uid]
        if data['class'].get(classSpect) is not None:
            data['class'][classSpect].remove(uid)
        print("After! \n")
        print(data)
        json.dump(data, fh)
    return 0

# Do NOT call this function. Testing purpose
def _deleteAll():
    try:
        os.remove(PATH)
    except OSError:
        pass

### handle all the connections.
# TODO: this function needs a further discussion about what we need to do
# e.g. how to build the dependency graph.
def connect(uid):
    return

def testRegister():
    _deleteAll()
    device1 = DeviceInfo("0.0.0.0", "mic", "test", "room1", "aaa", "10")
    device2 = DeviceInfo("1.1.1.1", "mic", "test", "room1", "bbb", "109")
    device3 = DeviceInfo("2.2.2.2", "door", "test", "room2", "ccc", "120")

    uid1 = register(device1)
    print('\n\n\n')
    uid2 = register(device2)
    print('\n\n\n')
    uid3 = register(device3)
    print('\n\n\n')

    print(str(uid1) + '\n' + str(uid2) + '\n' + str(uid3) + '\n')

if __name__ == "__main__":
    # print("What the fuck I am doing here!")
    testRegister()
