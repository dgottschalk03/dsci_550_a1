from dsci_550_a1.parsingFunctions import extractSequences, check_regex
import number_parser
import re

def classify_hours(text):
    """
    Classify numeric time into time of day categories. 
    Inputs:
        [text]              | string you want to parse   

    Returns:
        [str]               | Time of day (default: "Unknown")
                            | Values: ["Night", "Morning", "Evening", "Afternoon", "Dusk", "Unknown"]
    Method:
        - Parse numbers and ordinals to integers using number_parser.parse
        - split text into sequences and tokens
        - check if sequence contains "a.m." or "p.m."
            - check if previous token is a time of the form "hh:mm", "hh", or "h"
        - return one of "Night", "Morning", "Evening", "Afternoon", "Dusk", "Unknown"
  
    eg:
    >>> classify_hours("It was 2:00 pm")
    "Afternoon"
    """
    
    # pattern to capture a.m., p.m., and hour
    am_pattern = re.compile(r'^(a\.?m\.?)$', re.IGNORECASE)
    pm_pattern = re.compile(r'^(p\.?m\.?)$', re.IGNORECASE)
    
    # split text into sequences by all periods not adjacent to a.m. or p.m. 
    text = re.sub(r'(?<!a|p)\.(?!m)', ' . ', text)
    text = number_parser.parse(text)

    tokens = text.lower().split()
    sequences = extractSequences(tokens, ".")
    
    for seq in sequences:

        for i, token in enumerate(seq):

            if am_pattern.match(token):
                # check if previous token is a time of the form "hh:mm", "hh", or "h". 
                prev_token = re.match(r'^([0-1]?\d|2[0-3])(:[0-5]\d)?$', seq[i-1])

                # Convert to int if we have match
                if prev_token:
                    prev_token = int(prev_token.group(1)) 

                    if prev_token < 4:
                        return "Night"
                    
                    elif 4 <= prev_token <= 12:
                        return "Morning"

            elif pm_pattern.match(token):
                prev_token = re.match(r'^([0-1]?\d|2[0-3])(:[0-5]\d)?$', seq[i-1])

                # Convert to int if we have match
                if prev_token:
                    prev_token = int(prev_token.group(1)) 

                    if 1 <= prev_token < 7 or prev_token == 12:
                        return "Afternoon"

                    elif 7 <= prev_token < 10:
                        return "Dusk"

                    elif 10 <= prev_token < 12:
                        return "Evening"
                
    return "Unknown"
                
def classify_time_of_day_v2(text):
    """
    Improved classify_time_of_day function from assignment 1. Classify time of day from a piece of text
    Inputs:
        [text]              | string you want to parse   

    Returns:
        [res]               | Time of day (default: "Unknown")
                            | Values: ["Night", "Morning", "Evening", "Afternoon", "Dusk", "Unknown"]
    Method:
        - run classify_hours and return result if not "Unknown"
        - run regex check for each time of day category ["Night", "Morning", "Evening", "Afternoon", "Dusk"]
        - return "Unknown" if all fail
        - check if sequence contains "a.m." or "p.m."

    eg:
    >>> classify_hours("It was late at night")
    "Evening"
    """

    time_patterns_v2 = {
    # "mornings", "dawns", etc.  #
    "Morning": [r"\bmorning('?s)?[a-z]*\b", r"\bdawn('?s)?\b", r"\bsunrise('?s)?\b"],

    # "evenings", "midnights", etc.  #
    "Evening": [r"\bevening('?s)?\b", r"\bnight('?s)?\b", r"\bmidnight('?s)?\b", r"\bnighttime('?s)?\b", r"\blate('?s)?\b"],

    # "afternoon", "school hours", etc.  #
    "Afternoon": [r"afternoon('?s)?\b", r"\bnoon('?s)?\b", r"\b(?:school|business|work|day|closing|opening|lunch|dinner|daytime)\s*hours?\b", r"\blate('?s)?\b"],

    # "dusks", "susnets", etc. #
    "Dusk": [r"\bdusk('?s)?\b", r"\bsunset('?s)?\b", r"\btwilight('?s)?\b"], 

    # "all day", "entire day", "whole day", "all (of) (the) time" #
    "All Day": [r"\ball\s?(day|hours)('?s)?\b", r"\bentire\s?day('?s)?\b" , r"\bwhole\s?day('?s)?\b", r"\ball\s?(of)?\s?(the)?\s?time('?s)?\b"] 
    
    }


    if not isinstance(text, str):
        return "Unknown"
    
    # run classify hours and check if it found something
    res = classify_hours(text)

    # return result if it is not "Unknown"
    if res != "Unknown":
        return res

    # Iterate through each time of day category
    for label, patterns in time_patterns_v2.items():

        for p in patterns:

            # check if regex matches
            if check_regex(text, re.compile(p, re.IGNORECASE))[0]:

                # return time of day category if match found
                res = label
                return res
    
    return res
