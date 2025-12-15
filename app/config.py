import json

def setBaseFolder(path):

    with open('config.json', 'r') as jsonFile:
        data = json.load(jsonFile)

    data['basePath'] = path

    with open('config.json', 'w') as jsonFile:
        json.dump(data, jsonFile, indent=4)

def getBaseFolder():
    with open('config.json', 'r') as jsonFile:
        data = json.load(jsonFile)

    return data['basePath']