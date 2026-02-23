from collections import Counter


def countPermStr(string1, string2):
    if string1 is None or string2 is None:
        raise ValueError
    if string2 == "" or len(string2) > len(string1):
        raise ValueError

    m = len(string2)
    pattern = Counter(string2)
    missing = m
    matches = 0
    for i, ch in enumerate(string1):
        if pattern[ch] > 0:
            missing -= 1
        
        pattern[ch] -= 1
        if i >= m:
            left = string1[i - m]
            pattern[left] += 1
            if pattern[left] > 0:
                missing += 1

        if i >= m - 1 and missing == 0:
            matches += 1
    return matches


if __name__ == "__main__":
    print(countPermStr("cbabbcab", "abb"))         # expected: 2
    print(countPermStr("cbaaaaababcabb", "aabb"))  # expected: 2