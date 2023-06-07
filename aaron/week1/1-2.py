import sys
import json
from month_search import month_search

if __name__ == '__main__':

    with open('dict_json.json', encoding='utf-8') as jsonfile:
        month = json.load(jsonfile)

    for num in range(1, 4):

        char = input(f"請輸入第{num}個英文\n").lower()

        result = month_search(month, char, num).char_search()

        if len(result) == 1:

            print(list(result.values())[0])

            sys.exit()
        
        else:
            month = result