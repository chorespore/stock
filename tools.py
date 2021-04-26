import os
import json
import pandas as pd


def loadJson(filename, log=True):
    with open(filename) as file_obj:
        data = json.load(file_obj)
        if(log == True):
            print(len(data), 'items loaded form', os.path.basename(filename))
        return data


def saveJson(data, filePath, log=True):
    with open(filePath, 'w') as file_obj:
        json.dump(data, file_obj)
        if(log == True):
            print(len(data), 'items saved as JSON')


def saveCSV(data, filePath, log=True):
    df = pd.DataFrame.from_dict(data)
    df.to_csv(filePath, encoding="utf_8_sig")
    if(log == True):
        print(len(data), 'items saved as CSV')
