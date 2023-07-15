from difflib import SequenceMatcher


def lcs(X, Y):
    return sum(block.size for block in SequenceMatcher(None, X, Y).get_matching_blocks())