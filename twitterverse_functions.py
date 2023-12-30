""" CSC108: Fall 2020 -- Assignment 3: Twitterverse

This code is provided solely for the personal and private use of students
taking the CSC108 course at the University of Toronto. Copying for purposes
other than this use is expressly prohibited. All forms of distribution of
this code, whether as given or with any changes, are expressly prohibited.

All of the files in this directory and all subdirectories are:
Copyright (c) 2020 Mario Badr, Jennifer Campbell, Tom Fairgrieve,
Diane Horton, Michael Liut, Jacqueline Smith, and Anya Tafliovich.
"""

# You may add/remove imports from the typing module as needed
from typing import Any, Callable, Dict, List, TextIO
import re

"""
Type descriptions of TwitterverseDict, QueryDict, SearchDict, FilterDict, and
PresentDict dictionaries. These will appear in the type contracts.

We use these types to simplify our type contracts, and to capture additional
information about each type, as indicated below:

TwitterverseDict
Twitterverse dictionary:  Dict[str, Dict[str, Any]]
    - each key is a username (a str)
    - each value is a Dict[str, Any] with items as follows:
        - key "name", value represents a user's name (a str)
        - key "location", value represents a user's location (a str)
        - key "web", value represents a user's website (a str)
        - key "bio", value represents a user's bio (a str)
        - key "following", value usernames of users this user is following
          (a List[str])

QueryDict
Query dictionary:  Dict[str, Dict[str, Any]]
    - key "search", value represents a search specification dictionary
    - key "filter", value represents a filter specification dictionary
    - key "present", value represents a presentation specification dictionary

SearchDict
Search specification dictionary:  Dict[str, Any]
    - key "username", value represents username to begin search at (a str)
    - key "operations", value represents the operations to perform
      (a List[str])

FilterDict
Filter specification dictionary:  Dict[str, str]
    - key "following" might exist, value represents a username (a str)
    - key "follower" might exist, value represents a username (a str)
    - key "name-includes" might exist, value represents str to match
      (a case-insensitive match)
    - key "location-includes" might exist, value represents str to match
      (a case-insensitive match)

PresentDict
Presentation specification dictionary:  Dict[str, str]
    - key "sort-by", value represents how to sort results (a str)
    - key "format", value represents how to format results (a str)

"""


# This is a helper function to use when sorting.
def tweet_sort(twitter_data: 'TwitterverseDict', results: List[str],
               cmp: Callable[['TwitterverseDict', str, str], int]) -> None:
    """ Sort the <results> list using the comparison function <cmp> and
        the data in <twitter_data>.
    """

    # Insertion Sort (similar to lecture), using a comparison function.
    for i in range(1, len(results)):
        current = results[i]
        position = i
        while position > 0 and cmp(twitter_data, results[position - 1],
                                   current) > 0:
            results[position] = results[position - 1]
            position = position - 1
        results[position] = current


def process_data(f: TextIO) -> Dict[str, Dict[str, Any]]:
    """
    Reads and returns the Twitter data from the file, f.
    """

    d = {}
    line_groups = re.split("END$|END\n", f.read())[:-1]
    for group in line_groups:
        info, following = group.split("ENDBIO\n")
        info = info.split("\n")
        following = following.split("\n")[:-1]
        usernames = info[0]
        d[usernames] = {"name": info[1].strip(), "bio": "\n".join([item.strip() for item in info[4:]])[:-1],
                        "location": info[2].strip(), "web": info[3].strip(),
                        "following": following}
    return d


def process_query(f: TextIO) -> Dict[str, Dict[str, Any]]:
    """
    Reads the file, f, and returns query from it

    >>> process_query('query1.txt')
    {'search': {}, 'filter': {}, 'present': {}}
    """

    lines = [line.strip() for line in f.readlines()]
    filter_idx = lines.index("FILTER")
    present_idx = lines.index("PRESENT")
    d = {"search": {"username": lines[1], "operations": []},
         "filter": {}, "present": {}}
    for item in lines[2:filter_idx]:
        d["search"]["operations"].append(item)
        for item in lines[(filter_idx + 1):present_idx]:
        split_item = item.split()
        d["filter"][split_item[0]] = split_item[1]
    split_item = lines[-2].split()
    d["present"][split_item[0]] = split_item[1]
    split_item = lines[-1].split()
    d["present"][split_item[0]] = split_item[1]
    return d


def all_followers(d: Dict[str, Dict[str, Any]], usernames: str) -> List[str]:
    """
    Returning all the usernames following the user as a list...

    >>> all_followers({'tomCruise': {'name': 'Tom Cruise', 
                           'location': 'Los Angeles, CA', 
                           'web': 'http://www.tomcruise.com', 
                           'bio': 'Official TomCruise.com crew tweets. '+ \
                           'We love you guys!\nVisit us at Facebook!', 
                           'following': ['katieH']}},
                           'katieH')
    ['tomCruise']
    """

    followers = []
    for user, data in d.items():
        if usernames in data["following"]:
            followers.append(user)
    return followers


def all_following(d: Dict[str, Dict[str, Any]], user_name: str) -> List[str]:
    """
    >>> all_following({'tomCruise': {'name': 'Tom Cruise', 
                        'location': 'Los Angeles, CA', 
                        'web': 'http://www.tomcruise.com', 
                        'bio': 'Official TomCruise.com crew tweets. '+ \
                        'We love you guys!\nVisit us at Facebook!', 
                        'following': ['katieH']}}, 'katieH')
    ['katieH']
    """

    return d[user_name]["following"]


def get_search_results(d: Dict[str, Dict[str, Any]],
                       srch: Dict[str, Any]) -> List[str]:
    """
    >>> get_search_results({'tomCruise': {'name': 'Tom Cruise', 
                           'location': 'Los Angeles, CA', 
                           'web': 'http://www.tomcruise.com', 
                           'bio': 'Official TomCruise.com crew tweets. '+ \
                           'We love you guys!\nVisit us at Facebook!', 
                           'following': ['katieH']}, 
             'katieH': {'name': 'Katie Holmes', 'location': '', 
                        'web': 'www.tomkat.com', 'bio': '', 'following': []}},
             {'username': 'tomCruise', 'operations': ['following']})
    ['katieH']
    """

    result = [srch["username"]]
    for op in srch["operations"]:
        new_result = []
        if op == "following":
            new_result.extend(all_followers(d, srch["username"]))
        else:
            new_result.extend(all_following(d, srch["username"]))
        result = list(new_result)
    return result


def get_filter_results(d: Dict[str, Dict[str, Any]], usernames: List[str],
                       filt: Dict[str, str]) -> List[str]:
    """
    Filtering different variables...
    """

    to_keep = usernames[:]
    for op, info in filt.items():
        if op == "following":
            unames = all_followers(d, info)
            to_keep = [uname for uname in to_keep if uname in unames]
        elif op == "location-includes":
            to_keep = [uname for uname in to_keep if info in d[uname]
                       ["location"].lower()]
        else:  # name-includes
            to_keep = [uname for uname in to_keep if info in d[uname]
                       ["name"].lower()]
    return to_keep


def my_sort(d: Dict[str, Dict[str, Any]], usernames: List[str],
            cmp: Callable) -> None:
    """
    Sorting the variables...
    """

    data = usernames[:]
    for i in range(1, len(data)):
        current = data[i]
        position = i
        while position > 0 and cmp(d, data[position - 1], current) > 0:
            data[position] = data[position - 1]
            position = position - 1
        data[position] = current
    return data


def username(d: Dict[str, Dict[str, Any]], username_1: str,
             username_2: str) -> int:
    """
    Mesuring the usernames...
    """

    if username_1 < username_2:
        return -1
    elif username_1 == username_2:
        return 0
    return 1


def popularity(d: Dict[str, Dict[str, Any]], username_1: str,
               username_2: str) -> int:
    """
    """
    pop_1 = len(all_followers(d, username_1))
    pop_2 = len(all_followers(d, username_2))
    if pop_1 < pop_2:
        return 1
    elif pop_1 == pop_2:
        return username(d, username_1, username_2)
    return -1


def name(d: Dict[str, Dict[str, Any]], username_1: str,
         username_2: str) -> int:
    """
    Testing the different usernames...
    """
    name_1 = d[username_1]["name"]
    name_2 = d[username_2]["name"]
    if name_1 < name_2:
        return -1
    elif name_1 == name_2:
        return username(d, username_1, username_2)
    return 1


def get_present_string(d: Dict[str, Dict[str, Any]],
                       usernames: List[str], present: Dict[str, str]) -> str:
    """
    Different information...
    """
    sort_funcs = {"popularity": popularity, "name": name, "username": username}
    sorted_usernames = my_sort(d, usernames, sort_funcs[present["sort-by"]])
    if present["format"] == "short":
        return str(sorted_usernames)
    if not sorted_usernames:
        long_fmt = "-" * 10 + "\n" + "-" * 10
    else:
        long_fmt = ""
        for uname in sorted_usernames:
            long_fmt += "-" * 10 + "\n"
            long_fmt += uname + "\n"
            info = d[uname]
            for info_name, info_data in info.items():
                if info_name == "web":
                    info_name = "website"
                if info_name == "bio":
                    long_fmt += "{}:\n{}\n".format(info_name, info_data)
                else:
                    long_fmt += "{}: {}\n".format(info_name, info_data) 
        long_fmt += "-" * 10 + "\n"   
    return long_fmt
