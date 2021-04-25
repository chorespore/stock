import json
import pandas as pd


def saveJson(data, filePath):
    with open(filePath, 'w') as file_obj:
        json.dump(data, file_obj)
        print(len(data), 'items saved as JSON')


def saveCSV(data, filePath):
    df = pd.DataFrame.from_dict(data)
    df.to_csv(filePath, encoding="utf_8_sig")
    print(len(data), 'items saved as CSV')
