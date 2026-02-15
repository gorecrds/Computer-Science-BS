# returns leftmost child of position n
def _iOILeft(n, t):
    i = prev = n
    while (i < len(t)) and (t[i] is not None):
        prev = i
        i = (i * 2) + 1
    return prev if (prev != n) else None


# returns next inorder node to position n
# core idea is to move right one position
# there are three cases
#   parent -> leftmost of right child
#   left child -> parent
#   right child -> leftmost child of ancestor above parent
#       with right child


def _iOINext(n, t):
    r = (n * 2) + 2  # right

    if (r < len(t)) and (t[r] is not None):
        # parent with right child
        # move to leftmost child of right (or right
        # if no child)
        if (n := _iOILeft(r, t)) is not None:
            return n
        return r
    elif n % 2:
        # left leaf or left parent with no
        # right child, go to parent
        n = (n - 1) // 2  # left child -> parent
        return n
    else:
        # at this point, right leaf with
        # no right children.  So node's
        # parent's subtree is completed.

        # so next is first ancestor
        # above parent who is parent
        # of a left node
        p = (n - 2) // 2  # parent
        leftp = p % 2
        gp = (p - 1) // 2  # grandparent
        while gp and (not leftp):
            leftp = gp % 2
            gp = (gp - 1) // 2

        if leftp:
            return gp

    return -1


# this is a generator routine that
# returns successive elements in the
# inorder traversal


def _iOI(t):
    # find leftmost child = start node
    if (inorder := _iOILeft(0, t)) is None:
        inorder = 0
    while inorder >= 0:
        yield t[inorder]
        inorder = _iOINext(inorder, t)


# Inorder traversal that is iterative and does
# not use a stack (similar to a Morris
# traversal)


def inOrderIter(t):
    if not len(t):
        return []
    return list(_iOI(t))


# helper routine for recursive traversal
# returns a list which is the in-order traversal
# of the subtree rooted at node


def _iOR(t, node):
    if (node >= len(t)) or (t[node] is None):
        return []
    left = _iOR(t, (2 * node) + 1)
    right = _iOR(t, (2 * node) + 2)
    return left + [t[node]] + right


# Classic inorder recursive traversal


def inOrderRecurse(t):
    return _iOR(t, 0)


# insert unit tests here
if __name__ == "__main__":

    t1 = [4, 2, 6, 1, 3, 5, 7]
    t2 = [4, 2, 6, 1, None, 5, 7]
    t3 = [1, None, 2, None, None, None, 4]
    t4 = [4, 2, None, 1]
    print(f"inOrderRecurse{t1} is {inOrderRecurse(t1)}")
    print(f"inOrderIter{t1} is {inOrderIter(t1)}")
    print(f"inOrderRecurse{t2} is {inOrderRecurse(t2)}")
    print(f"inOrderIter{t2} is {inOrderIter(t2)}")
    print(f"inOrderRecurse({t3}) is {inOrderRecurse(t3)}")
    print(f"inOrderRecurse({t3}) is {inOrderIter(t3)}")
    print(f"inOrderRecurse({t4}) is {inOrderRecurse(t3)}")
    print(f"inOrderRecurse({t4}) is {inOrderIter(t3)}")
