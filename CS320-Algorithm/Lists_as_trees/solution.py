"""
CS320 Lab: Lists as Trees.
List binary search tree operations that add, find and delete).
"""


# pylint: disable=invalid-name
def _validate_args(k, t) -> None:
    """Validate args for tree operations."""
    if k is None:
        raise ValueError("null key")
    if t is None:
        raise ValueError("no tree")
    if not isinstance(t, list):
        raise TypeError("no tree")
    if t and (root := t[0]) is not None:
        if not ((isinstance(root, (int, float)) and
                isinstance(k, (int, float))) or type(root) is type(k)):
            raise TypeError("tree error")


def findKey(k, t):
    """Find the index of key k in tree t."""
    _validate_args(k, t)  # validate arguments
    idx_node = 0  # starting at the root node index 0
    try:
        # Traverse the tree using the concept of a binary search tree
        while idx_node < len(t) and t[idx_node] is not None:
            if k == t[idx_node]:
                return idx_node
            if k < t[idx_node]:
                idx_node = 2 * idx_node + 1
            else:
                idx_node = 2 * idx_node + 2
    except Exception as exc:
        raise RuntimeError("tree error") from exc
    raise LookupError("not in tree")  # Raise Lookup Error if Key not found


def addKey(k, t) -> list:
    """Add a key k to tree t. Return added key in the tree as a list."""
    _validate_args(k, t)  # validate arguments
    idx_node = 0
    if not t:  # If tree is empty, return k as the root node
        return [k]
    # Traverse t to find the correct position for idx_node
    while idx_node < len(t) and t[idx_node] is not None:
        if k == t[idx_node]:
            return t
        if k < t[idx_node]:
            idx_node = 2 * idx_node + 1
        else:
            idx_node = 2 * idx_node + 2
    # idx_node is in the corect position to add k
    if idx_node >= len(t):
        # Extend None values to tree as a placeholder
        t.extend([None] * (idx_node - len(t) + 1))
    t[idx_node] = k  # add k to tree at idx_node replacing position for None
    return t


def _has_child(t, idx_node) -> bool:
    """ Helper function to check if a node at idx_node has a child """
    return idx_node < len(t) and t[idx_node] is not None


def _get_child_info(t, idx_node) -> tuple[int, int, bool, bool]:
    """ Helper function to get child information for a node at idx_node """
    left_idx_node = 2 * idx_node + 1
    right_idx_node = 2 * idx_node + 2
    has_left_child = _has_child(t, left_idx_node)
    has_right_child = _has_child(t, right_idx_node)
    return left_idx_node, right_idx_node, has_left_child, has_right_child


def deleteKey(k, t) -> list:
    """Delete key k from tree t. Return the tree after deletion."""
    _validate_args(k, t)  # validate arguments
    idx_node = findKey(k, t)  # check if the key exists and get its index
    try:
        # Compute the index for left and right child of current idx_node
        left_idx_node, right_idx_node, has_left_child, has_right_child = (
            _get_child_info(t, idx_node)
        )
        # Case 1: two children
        if has_left_child and has_right_child:
            # Find the inorder successor leftmost node to the right subtree
            successor_idx = right_idx_node
            while _has_child(t, 2 * successor_idx + 1):
                successor_idx = 2 * successor_idx + 1
            # replace idx_node value with successor value and index
            t[idx_node] = t[successor_idx]
            idx_node = successor_idx
            # get child info for the current node
            left_idx_node, right_idx_node, has_left_child, has_right_child = (
                _get_child_info(t, idx_node)
            )
        # Case 2: no children (leaf)
        # if there no child set the node to none
        if not has_left_child and not has_right_child:
            t[idx_node] = None
        # Case 3: one child and helper to clean up node from case 1
        else:
            # set child_idx to the only existing child
            child_idx = left_idx_node if has_left_child else right_idx_node
            while True:
                # setthe current node value and index of the child node
                t[idx_node] = t[child_idx]
                idx_node = child_idx
                # get child info for the current node
                (
                    left_idx_node, right_idx_node,
                    has_left_child, has_right_child
                ) = _get_child_info(t, idx_node)
                # If we reached a leaf, delete it and stop
                if not has_left_child and not has_right_child:
                    t[idx_node] = None
                    break
                # Continue down the only existing child
                child_idx = left_idx_node if has_left_child else right_idx_node
        # Clean up trailing None values at the end of the list
        while t and t[-1] is None:
            t.pop()
        return t
    except Exception as exc:
        raise RuntimeError("tree error") from exc


if __name__ == "__main__":
    # pylint: disable=unused-import
    from treelist import inOrderRecurse
    tree = []
    keys = [5, 3.5, 1, 15, 17, 10, 12]
    for key in keys:
        tree = addKey(key, tree)
    print(tree)
    print(inOrderRecurse(tree))
    print(findKey(12, tree))
    # deleteKey (99, tree)
    deleteKey(5, tree)
    print(tree)
    deleteKey(3.5, tree)
    print(tree)
    deleteKey(17, tree)
    print(tree)
