import requests, pickle
from xml.etree import ElementTree
from hide import URL

class DataController:
    def __init__(self):
        self.recycles = []

    # parsing한 data를 각각 dict타입으로 묶은 후 모든 data를 list형태로 저장
    def parsingData(self):
        response = requests.get(URL)
        print(response.status_code)
        xmlStr = response.text
        root = ElementTree.fromstring(xmlStr)
        allItems = root.iter('item')
        for item in allItems:
            recycleDict = {}
            recycleDict['name'] = item.find("dicItemNM").text
            recycleDict['dump'] = item.find("outMeth").text
            self.recycles.append(recycleDict)

    def saveData(self, DATA):
        with open("recycle.dat", "wb") as f:
            pickle.dump(DATA, f, pickle.HIGHEST_PROTOCOL)

    def loadData(self):
        with open("recycle.dat", "rb") as f:
            datas = pickle.load(f)
        return datas
