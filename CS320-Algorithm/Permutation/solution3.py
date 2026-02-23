from collections import Counter

def countPermStr(string1, string2):
    if string1 is None or string2 is None:
        raise ValueError
    if string2 == "" or len(string2) > len(string1):
        raise ValueError

    n = len(string1)
    m = len(string2)

    pattern = Counter(string2)  
    remaining = m
    matches = 0

    start = 0
    i = 0

    while i < n:
        char = string1[i]
        i += 1
        if char not in pattern:
            pattern = Counter(string2)
            remaining = m
            start = i
            continue

        # If we have too many of this char, shrink from left until we can take it
        while pattern[char] == 0 and start < i:
            left = string1[start]
            start += 1
            if left in pattern:
                pattern[left] += 1
                remaining += 1

        # Now we can take char
        if pattern[char] > 0:
            pattern[char] -= 1
            remaining -= 1

        # Keep window length <= m (slide if it got too big)
        while (i - start) > m:
            left = string1[start]
            start += 1
            if left in pattern:
                pattern[left] += 1
                remaining += 1

        # If we matched all m chars, count it, then slide by 1
        if remaining == 0:
            matches += 1
            left = string1[start]
            start += 1
            pattern[left] += 1
            remaining += 1

    return matches

if __name__ == "__main__":
    print(countPermStr("cbaaaaababcabb", "aabb"))  # expected: 2