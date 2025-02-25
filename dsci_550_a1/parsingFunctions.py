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
        if token == '.':
        # Append Sentence to Res and Reset CurrentSequence #
            currentSequence.append(token)
            Sequences.append(currentSequence)
            currentSequence = []
        else:
            currentSequence.append(token)

    return Sequences