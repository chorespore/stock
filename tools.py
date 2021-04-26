import os
import json
import time
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


def showProgress(current, total, start):
    timeUsed = time.time() - start
    print('\rProgerss:', current, format(current * 100 / total, '.2f') + '%', end=' ')
    print('Time used:', format(timeUsed / 3600, '.2f') + 'h', end=' ')
    print('Time remaining:', format((timeUsed * total / current - timeUsed) / 3600, '.2f') + 'h', end=' ')
