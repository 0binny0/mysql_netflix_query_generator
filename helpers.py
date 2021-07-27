
import re
import argparse

def capture_names(names):
    names = names.split(", ")
    pattern = re.compile("""
        (?P<firstname>\w+(?:-\w+)?)\s
        (?:(?P<middlename>\w+\.|\w+)\s)?
        (?P<lastname>\w'?\w+(-\w+)?)
    """, re.I|re.X)
    actor_names = []
    for name in names:
        match = pattern.match(name)
        if match:
            actor_names.append([
                match.group("firstname"), match.group("middlename"),
                match.group("lastname")
            ])
    return actor_names

def check_int_value(x):
    pattern = re.compile(r"\d{1}\.\d{1}|\d+")
    match = pattern.match(x)
    if match:
        value = match.group()
        return float(value)
    return None
