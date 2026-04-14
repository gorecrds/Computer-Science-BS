from collections.abc import Collection
from math import e, modf, floor, sqrt
from itertools import filterfalse, chain
from copy import copy
import unittest


# DO NOT CHANGE ANY CODE BETWEEN LINE X AND LINE Y
# ******* THIS IS LINE X ******************

GOLDEN = (1.0 + 5.0 * 0.5) / 2.0


def swap(a, b):
    return b, a


# ***************************************************
# why do we inherit from Collection rather than Set?
# because Set requires too many methods to be defined


class CuckooSet(Collection):

    # *** course helper routines *******
    def _hash2_(self, obj, table_size):
        try:
            h = hash(obj)  # may raise exception
        except Exception:
            raise TypeError("unhashable key")

        h %= table_size

        f1, _ = modf(h * e)
        f2, _ = modf(h * GOLDEN)
        h1 = floor(table_size * f1)
        h2 = floor(table_size * f2)
        if h1 == h2:
            h2 = (h2 + 7) % table_size
        return h1, h2

    def _members_(self, tab):  # returns iterator
        return filterfalse((lambda x: x is None), tab)

    def _allmembers_(self):
        return chain(self._members_(self.htab1), self._members_(self.htab2))

    # ** course methods ****

    def __init__(self, iter=[], *, s=128):
        if s < 4:
            raise ValueError("set size too small")
        self._size_ = s
        self._MAXSWAPS_ = floor(s * 0.6)
        self.htab1 = [None] * s
        self.htab2 = [None] * s
        for i in iter:
            self.add(i)

    def __len__(self):
        count1 = len(list(self._members_(self.htab1)))
        count2 = len(list(self._members_(self.htab2)))
        return count1 + count2

    def _resize_(self):
        oldself = copy(self)
        self.__init__(oldself, s=oldself._size_ * 2)

    def __str__(self):
        fstr = ""
        for v in self._allmembers_():
            if len(fstr):
                fstr += ", "
            fstr += str(v)
        return fstr

    def __iter__(self):
        return self._allmembers_()
# ******* THIS IS LINE Y ******************

    def _check_key(self, key):
        """ helper that raises a ValueError if key is None """
        if key is None:
            raise ValueError("key may not be None")
        return key

    def __contains__(self, key):
        key = self._check_key(key)  # check if key is None
        # compute the two key hash determine the position in each table
        h1, h2 = self._hash2_(key, self._size_)
        # check if the key is present in any of the two tables.
        result = key in (self.htab1[h1], self.htab2[h2])
        return result

    def add(self, key):
        """ add key to the set to the hash tables """
        key = self._check_key(key)
        if self.__contains__(key):  # check if key is present calling __contains__
            return

        max_swap_counter = 0  # counter to kee track of swap iteration

        while True:
            # compute the two key hash determine the position in each table
            h1, h2 = self._hash2_(key, self._size_)
            # if the position in the first table is None, place the key
            if self.htab1[h1] is None:
                self.htab1[h1] = key
                break
            else:
                # else swap the key with the exiting key in the first table
                key, self.htab1[h1] = swap(key, self.htab1[h1])
                h1, h2 = self._hash2_(key, self._size_)  # recompute the hash for the swapped key
            # if the position in the second table is None, place the key
            if self.htab2[h2] is None:
                self.htab2[h2] = key
                break
            else:
                # else swap the key with the exiting key in the first table
                key, self.htab2[h2] = swap(key, self.htab2[h2]) 
                h1, h2 = self._hash2_(key, self._size_)  # recompute the hash for the swapped key
            max_swap_counter += 1  # increment the swap counter
            # if coutner is greater and equal to the max swap counter resize the tables
            if max_swap_counter >= self._MAXSWAPS_:
                max_swap_counter = 0
                self._resize_()

    def remove(self, key):
        """ remove key from the set. if key is not present raise a ValueError """
        if key not in self:  # check if key is present
            raise ValueError("key not in CuckooSet")
        self.discard(key)  # call discard to remove the key from the tables

    def discard(self, key):
        """ discard key from the set """
        key = self._check_key(key)
        # compute the two key hash determine the position in each table
        h1, h2 = self._hash2_(key, self._size_)
        # if found on hash table 1, remove it
        if self.htab1[h1] == key:
            self.htab1[h1] = None
            return
        # if found on hash table 1, remove it
        if self.htab2[h2] == key:
            self.htab2[h2] = None
            return


if __name__ == "__main__":
    # Test CuckooSet code
    test = CuckooSet([10, 11, 12, 13, 14, 16, 17, 18], s=4)
    test.add(10)
    print(10 in test)
    test.remove(10)
    print(10 in test)
    test.add(10)
    print(10 in test)
    test.discard(10)
    test.remove(99)
