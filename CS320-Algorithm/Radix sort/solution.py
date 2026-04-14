""" 
CS320 Lab: Radix Sort Solution.
This Module implements Radix sort using entered base. 
"""


def _check_sequence(values_to_sort, base):
    """Validate the sequence for radix sort."""
    # Checking if the sequence is none, empty or base is less than 2
    if values_to_sort is None or values_to_sort == [] or base < 2:
        raise ValueError("invalid arguments")
    # Checking if the sequence contains non-integer
    for ival in values_to_sort:
        try:
            if divmod(ival, 1)[1] != 0 or ival < 0:
                raise ValueError("invalid list element")
        except Exception as e:
            raise ValueError("invalid list element") from e


def radix_base(values_to_sort, base):
    """Sort the sequence of integers using radix sort with entered base."""

    _check_sequence(values_to_sort, base)  # Validate the input sequence
    digit = 1  # start with a single digit place
    max_value = max(values_to_sort)  # identify the max number of digits to sort
    # loop until we have gone through all digits
    while max_value // digit > 0:
        buckets = [[] for i in range(base)]  # create buckets for each digit value
        # Append the elements into buckets based on the current digit
        for ival in values_to_sort:
            bucket = divmod((ival // digit), base)[1]  # identify the bucket index
            buckets[bucket].append(ival)  # list of buckets
        values_to_sort.clear()  # clear the original list
        # Reconstruct the list by concatenating the buckets in order
        for bucket in buckets:
            # Append the elements from buckets back to the original list
            values_to_sort.extend(bucket)
        digit *= base  # Move to the next base digit
    return values_to_sort


if __name__ == "__main__":
    # Test for the radix sort code
    print("Test1")
    listA = [4, 3, 20, 1, 0]
    print(f"{listA}\n{radix_base(listA, 2)}")
    print("Test2")
    listB = [107, 22, 3, 888, 88, 8, 30, 20, 50]
    print(f"{listB}\n{radix_base(listB, 10)}")
    print("Test3")
    listC = [17, 4, 37, 8, 19, 100, 300, 310, 55]
    print(f"{listC}\n{radix_base(listC, 2)}")
