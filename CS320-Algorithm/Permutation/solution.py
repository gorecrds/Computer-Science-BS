from collections import Counter


def _check_args(text, pattern):
    """Validate the arguments for countPermStr operation"""
    if text is None or pattern is None:
        raise ValueError
    if pattern == "" or len(pattern) > len(text):
        raise ValueError


# pylint: disable=invalid-name
def countPermStr(text, pattern):
    """ Count the number of permutations of pattern in text. """
    _check_args(text, pattern)

    target = Counter(pattern)  # stores the count of each character in the pattern
    window = Counter()  # sliding window to keep count track of each character added
    window_remaining = len(pattern)  # track of remainder space characters in the window
    found = 0  # number of permutations found in text

    for i, window_r in enumerate(text):
        window[window_r] += 1        # add the rightmost character to the window
        window_remaining -= 1          # decrease the remaining needed characters

        # if the window is full check if the window is a match
        # and remove the leftmost character from the window
        if window_remaining == 0:

            if window == target:
                found += 1

            window_l = text[i - len(pattern) + 1]

            # if the leftmost character in the window is 1,
            # remove it from the window, else decrease its count by 1
            if window[window_l] == 1:
                del window[window_l]
            else:
                window[window_l] -= 1

            window_remaining += 1
    return found


if __name__ == "__main__":
    """Test cases for countPermStr"""
    print(countPermStr("cbabcabb", "abb"))         # expected: 2
    print(countPermStr("cbaazabababcabb", "abb"))  # expected: 3
