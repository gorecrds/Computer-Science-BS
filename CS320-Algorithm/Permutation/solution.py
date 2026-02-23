from collections import Counter


def _check_args(text, pattern):
    if text is None or pattern is None:
        raise ValueError
    if pattern == "" or len(pattern) > len(text):
        raise ValueError


def countPermStr(text, pattern):
    _check_args(text, pattern)

    ptrn_lenght = len(pattern)
    target = Counter(pattern)

    window = Counter()
    

    matches = 0

    for i, window_r in enumerate(text):
        window[window_r] += 1
        ptrn_lenght-=1
        if ptrn_lenght == 0:
            if window == target:
                matches += 1
            window_l=text[i - len(pattern) + 1]
            if window[window_l] == 1:
                del window[window_l]
            else:
                window[window_l] -= 1
            ptrn_lenght +=  1
        

        


        

  

    return matches


if __name__ == "__main__":
    print(countPermStr("cbabcabb", "abb"))        # expected: 2
    print(countPermStr("cbaaaaababcabb", "abb")) # expected: 2