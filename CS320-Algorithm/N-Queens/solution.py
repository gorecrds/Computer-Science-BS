def nQueensAll(n: int) -> list[list[tuple[int, int]]]:  # pylint: disable=invalid-name
    if n < 4:
        raise ValueError("Value Error: n must be equal to or greater than 4.")

    cols = set()
    pos_diag_id = set()  # i_row + i_col
    neg_diag_id = set()  # i_row - i_col
    result = []
    queen_position = [None] * n

    def remove_queen(i_row: int) -> int:
        """Remove queen from given row. Returns the removed column."""
        i_col = queen_position[i_row]
        cols.remove(i_col)
        pos_diag_id.remove(i_row + i_col)
        neg_diag_id.remove(i_row - i_col)
        queen_position[i_row] = None
        return i_col

    def backtrack() -> None:
        i_row = 0
        i_col = 0

        while i_row < n:
            if i_row == 0 and i_col >= n:
                return

            if i_col >= n:
                i_row -= 1
                i_col = remove_queen(i_row) + 1
                continue

            i_pos_diag = i_row + i_col
            i_neg_diag = i_row - i_col

            if (
                i_col in cols
                or i_pos_diag in pos_diag_id
                or i_neg_diag in neg_diag_id
            ):
                i_col += 1
                continue

            queen_position[i_row] = i_col
            cols.add(i_col)
            pos_diag_id.add(i_pos_diag)
            neg_diag_id.add(i_neg_diag)

            i_col = 0
            i_row += 1

            if i_row >= n:
                result.append([(i_r, i_c) for i_r, i_c in enumerate(queen_position)])
                i_row -= 1
                i_col = remove_queen(i_row) + 1

    backtrack()
    return result


if __name__ == "__main__":
    print(nQueensAll(4))
