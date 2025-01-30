import bz2
import json
import string
import re
from typing import Dict, Set, Tuple, List
from constants import *


def parse(filename: str, type_filter: str = TYPE_FILTER) -> List | None:
    """
    This function reads JSON list from file with extension *.jsonl.bz2
    prams:
       filename - name of file we want to pase
       type - value we use to filter results by "type" property (if no arg is
               provided by default it is 'PushEvent')
    returns:
       dictionary with file content
   """
    index = 0
    try:
        with bz2.open(filename, 'rt', encoding="utf8") as file:
            data = []
            for line in file:
                line = file.readline()
                row = json.loads(line.strip())
                payload = row.get('payload')
                commits = payload.get('commits')
                if row['type'] == type_filter and commits not in [[], None]:
                    data += commits
                    index += 1
            return data
    except FileNotFoundError:
        print(f"File '{filename}' not found.")
        return None
    except json.JSONDecodeError:
        print(f"Error decoding JSON in file '{filename}'.")
        return None


def remove_punctuation(text: str) -> str:
    """
    This function removes punctuation from string
    args:
       text - string we want to sanitize
    returns:
       sanitized string
    """
    replacement_order = str.maketrans('', '', string.punctuation+'—-\\/\n.,!?_')
    new_text = text.translate(replacement_order)
    return new_text


def analyze(data: List) -> Dict[str, List[str]]:
    """
    This function analyze dictionary we get from file and returns list with information we are interested in. We do not
    take in our dataset next data. 3-grams from commits where we couldn't generate at least 5 items. We do not show
    authors with no 3-grams generated.
    args:
       data - dictionary we get after parsing of file
    returns:
       dictionary that contains interesting to us information it is grouped by name
    """
    result = {}
    for item in data:
        name = item.get('author').get('name')
        message = normalize(remove_punctuation(item.get('message').lower()))
        expected = generate_3_grams(message)
        if not expected or len(expected) < 5:
            continue
        if not result.get(name):
            result[name] = []
        commits = result[name]
        for commit in expected:
            commits.append(commit)
        result[name] = commits
    return result


def generate_3_grams(text: str) -> Tuple:
    """
    This function generate 3-grams from string
    args:
       text - string in which we are searching for 3-grams
    returns:
       list that contains founded 3-grams
    """
    result = ()
    lst = text.split(' ')
    index = 0
    while True:
        grama = lst[index:index + N]
        if not grama or len(grama) < N:
            break
        result += (" ".join(grama),)
        index += 1
    return result


def generate_result(data: Dict[str, List[str]]) -> List:
    """
    This function generate list that we will export to CSV file
    args:
       data - dictionary with information that is interested to us
    returns:
       list that contains names with top 5 founded 3-gram sorted by default build in python function sort
    """
    all_data = []
    grams = {}
    result = {}
    result_list = []
    for name in data:
        lst = list(data[name])
        all_data += lst
        result[name] = lst
    for key in all_data:
        if grams.get(key):
            continue
        grams[key] = all_data.count(key)
    a = 1
    for name in result:
        sort_list = []
        data_set = list(dict.fromkeys(result[name]))
        for item in data_set:
            sort_list.append([grams[item], item])
        sort_list.sort()
        search_result = sort_list[:-1*LIMIT-1:-1]
        row = [name]
        for gram in search_result:
            row.append(gram[1])
        result_list.append(row)
    result_list.sort()
    return result_list


def normalize(text: str) -> str:
    """
    This function removes extra spaces from string
    args:
       text - string we want to normalize
    returns:
       normalized string
    """
    return re.sub(r'\s+', ' ', text)
