import re
from typing import Pattern
from itertools import chain

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