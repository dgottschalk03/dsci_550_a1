import re
from typing import Pattern
from itertools import chain
import datetime 
import datefinder


def extractSequences(tokens : list[str], sepChar: str) -> list[list[str]]:
    '''
    Takes plain text and returns groups of tokens separated by "sep"
    Input:
        [tokens]    - List of tokens
        [sepChar]   - Character that separates sequences
    Returns:
        Sequences   - list of sentence broken into tokens
    '''
    Sequences = []
    currentSequence = []
    
    for token in tokens:
        # Check for Punctuation #
        if token == sepChar:
        # Append Sentence to Res and Reset CurrentSequence #
            currentSequence.append(token)
            Sequences.append(currentSequence)
            currentSequence = []
        else:
            currentSequence.append(token)
    if currentSequence != []:
        Sequences.append(currentSequence)
    return Sequences

def check_regex(text: str, regex: Pattern, *optional_regex : Pattern) -> tuple[bool, list[str]] | bool:
    '''
    Check regex matches for a body of text. 

    Steps:
    1. Check each regex in order
    2. Return false if any regex does not match
    3. Otherwise return True

    Input:
        [text]                  - raw text with quantifiers converted to digits
        [regex]                 - precompiled regular expression 
        [optional_regex]        - additional precompile regular expressions

    Returns:
        [bool]                  - result of re.search()
        [keywords]              - list of matched keywords for full regex match
    
    eg.
    >>> check_regex("I went to the store", re.compile(r"\\bi\\b"), re.compile(r"\\bstore\\b"))
    [True, ['I', 'store']]
    '''
    ## Compile regular expressions ##
    patterns = [regex] + list(optional_regex)  

    ## Target number of regex matches ##
    target = len(patterns) - 1
    

    ## Tokenize text and convert to sequences ##
    sequences = extractSequences(text.split(), '.')

    ## Convert sequences to strings ##
    sequences = list(" ".join(chain(sequence)) for sequence in sequences)

    ## Iterate through sequences ##
    for sequence in sequences:

        ## Initialize keyword output ##
        keywords = []

        ## Iterate through regex ##
        for i, pattern in enumerate(patterns):

            # Add matched keyword to output
            match = re.search(pattern, sequence)

            # Break loop if regex does not match
            if not match:
                break

            # Return True and matched keywords if all regexes match    
            elif i == target:
                keywords.append(match.group())
                return True, keywords
            
            # otherwise add match to keywords and continue checking regex
            keywords.append(match.group())

    ## Return False if no matches ##
    return False, []

def extract_dates(text):
    """
    Extract dates from a given text using three different methods:
    - `datefinder`
    - Two-digit regex patterns (e.g., "20's", "30s")
    - Four-digit regex patterns (e.g., "1920s", "1970's")

    Steps:
        1. Parse using datefinder.find_dates()
        2. Parse 4 digit and 2 digits regex
        3. Clean false positives
            - dates of the form [2025, 1, x] 
                - These are stray quantifiers that datefinder thinks are numbers
             - years < 1620 (landing at Plymouth Rock). These are likely 3 digit hotel rooms and other non-date objects.
                - eg. {index: 3} = "In the 1970's, one room, **room 211** ..." -> datetime([211, 1, 1]).
    Args:
        text (str): The input text containing potential date references.

    Returns:
        dict: A dictionary containing:
            - dates (list of datetime): Extracted date objects.
            - datefinder_count (int): Number of dates found using datefinder.
            - two_digit_pattern_count (int): Number of dates found using two-digit patterns.
            - four_digit_pattern_count (int): Number of dates found using four-digit patterns.

    """

    ## Parse Using DateFinder ##
    # Remove Years < 1620 #
    matched_dates = [date for date in datefinder.find_dates(text, base_date = datetime.datetime(2025, 1, 1)) 
                    if isinstance(date, datetime.datetime) and 1492 <= date.year < 2026]
    datefinder_count = len(matched_dates)


    ## Init list to store regex matches ##
    matched_years = []

    ## Parse Two Digit Pattern eg. "20's" ##

    two_digit_pattern = [r"\b(?:in\s+the\s+)'?(\d{2})\s*'?s\b", # eg. "in the 20's" (in + the) optional
                         r"\b(?:in\s+)?'?(\d{2})\s*'?s\b",  # eg. "in 20 's ("in" optional and optional white spaces)
                         r"\b(?:the\s+)?'?(\d{2})\s*'?s\b"] # eg. "the 20s" ("the" optional, optional white spaces, optional apostrophes)
    for pattern in two_digit_pattern:
        matched_years.extend(
            [re.sub(r"in the|'|s", "", year.lower()).strip() for year in re.findall(pattern, text, re.IGNORECASE)]
        )
    matched_years = ["19" + year for year in matched_years]
    two_digit_pattern_count = len(matched_years)

    ## Parse 4 Digit Pattern eg. "in the 1970's" ##
    four_digit_pattern = [r"\b(?:in\s+the\s+)(\d{4})\s*'?s\b", r"\b(?:in\s+)?(\d{4})\s*'?s\b", r"\b(?:the\s+)?(\d{4})\s*'?s\b", ]
    for pattern in four_digit_pattern:
        matched_years.extend(
            [re.sub(r"in the|'|s", "", year.lower()).strip() for year in re.findall(pattern, text, re.IGNORECASE)]
        )
    four_digit_pattern_count = len(matched_years) - two_digit_pattern_count

    ## Add Regex to Matched_Dates **
    for year in matched_years:
        matched_dates.append(datetime.datetime(int(year), 1, 1)) 

    ## Remove Duplicates ##
    matched_dates = list(set(matched_dates))

    ## Remove dates of form [2025, 1, x] where x != 1 ##
    matched_dates = [date for date in matched_dates if not ((date.year == 2025) and (date.day != 1))]

    ## If No Dates Matched, Return [2025, 1, 1] ##
    if matched_dates == []:
        matched_dates.append(datetime.datetime(2025, 1, 1))

    res = {
        "dates" : matched_dates,
        "datefinder_count" : datefinder_count,
        "two_digit_pattern_count" : two_digit_pattern_count,
        "four_digit_pattern_count" : four_digit_pattern_count  
    }

    return res

def clean_dates(lst):
    '''
    Removes datetime.datetime(2025, 1, 1) from a list of dates if list is longer than length 2. 
    This sometimes happens when "extract_dates" is applied to a row. 
    Input:
        [lst]     - list of datetime objects

    Returns:
        [None] - Modifies list of dates

    '''

    if (len(lst) > 1) and (datetime.datetime(2025,1,1) in lst):
        lst.remove(datetime.datetime(2025, 1, 1))
    return lst