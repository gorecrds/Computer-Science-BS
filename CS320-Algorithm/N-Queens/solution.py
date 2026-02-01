"""
CS320 Lab: N-Queens Backtracking Solution.

This module provides a backtracking solver for the N-Queens problem for n >= 4.
Solutions use zero-based indexing and are returned as (row, column) tuples.
"""

# pylint: disable=invalid-name


def nQueensAll(n: int) -> list[list[tuple[int, int]]]:
    """
    Find all Solutions to the N-Queens problem for a given n.
    Returns: Solution in a list of (row, column) tuples.
    Raises: ValueError: If n < 4.
    """
    if n < 4:
        raise ValueError("Value Error: n must be equal to or greater than 4.")

    # tracks columns used by a queen.
    cols = set()

    # Track diagonals as ids related to queens position:
    pos_diag_id = set()
    neg_diag_id = set()

    # Stores solutions found.
    result = []

    # queen_position columns with respect to row.
    # None means no queen is placed in that row.
    queen_position = [None] * n

    def remove_queen(i_row: int) -> int:
        """
        Remove the queen from row i_row and update tracking sets.
        Args: i_row is the Row index of the queen to remove.
        Returns: The column index that was removed.
        """
        i_col = queen_position[i_row]
        cols.remove(i_col)
        pos_diag_id.remove(i_row + i_col)
        neg_diag_id.remove(i_row - i_col)
        queen_position[i_row] = None
        return i_col

    def backtrack() -> None:
        """Place queens row-by-row using iterative backtracking."""
        i_row = 0
        i_col = 0

        # Try to place a queen in each row.
        # If stuck backtrack to previous row.
        while i_row < n:
            # If at first row and exceed all columns exit the loop.
            if i_row == 0 and i_col >= n:
                return

            # If we run out of columns at a row, backtrack to the previous row
            # and try the following columns from wehre the queen was placed.
            if i_col >= n:
                i_row -= 1
                i_col = remove_queen(i_row) + 1
                continue

            i_pos_diag = i_row + i_col
            i_neg_diag = i_row - i_col

            # If column or diagonals are already used, move to the next column.
            if (
                i_col in cols
                or i_pos_diag in pos_diag_id
                or i_neg_diag in neg_diag_id
            ):
                i_col += 1
                continue

            # Place queen, mark column and diagonals as used.
            queen_position[i_row] = i_col
            cols.add(i_col)
            pos_diag_id.add(i_pos_diag)
            neg_diag_id.add(i_neg_diag)

            # Move to next row and start from column 0 .
            i_row += 1
            i_col = 0

            # If we have queens in all rows, append to result.
            if i_row >= n:
                res = [(i_r, i_c) for i_r, i_c in enumerate(queen_position)]
                result.append(res)

                # Remove the last queen and continue searching.
                i_row -= 1
                i_col = remove_queen(i_row) + 1

    backtrack()
    return result


if __name__ == "__main__":
    print(nQueensAll(4))
