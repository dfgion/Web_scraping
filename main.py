from Data_parsing.parser import Parser as pr
import json
from pprint import pprint
def autofill_json():
    with open('data.json', 'w') as f:
        json.dump(data, f, indent=4, ensure_ascii=False)

def autofill_USD_json():
    with open('data_USD.json', 'w') as f:
        json.dump(dataUSD, f, indent=4, ensure_ascii=False)

if __name__ == '__main__':
    Parser = pr(HOST='https://spb.hh.ru/search/vacancy?text=python&area=1&area=2')
    data = Parser.selecting_data()
    dataUSD = Parser.get_vanacies_USD()
    autofill_json()
    autofill_USD_json()
