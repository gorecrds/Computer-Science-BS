def nQueensAll(n: int) -> list[list[tuple[int, int]]]:  # pylint: disable=invalid-name
    if n < 4:
        raise ValueError("Value Error: n must be equal to or greater than 4.")
    cols = set()
    pos_diag_id = set()  # i_row + i_col
    neg_diag_id = set()  # i_row - i_col
    result = []
    queen_position = [None] * n


    def remove_queen(row: int) -> int:
        """Remove queen from given row. Returns the removed column."""
        col = queen_position[row]
        cols.remove(col)
        pos_diag_id.remove(row + col)
        neg_diag_id.remove(row - col)
        queen_position[row] = None
        return col

    def backtrack() -> None:
        index_row=0
        index_col=0
        while index_row < n:
            if index_row ==0 and index_col >= n:
                return
            if index_col >= n:
                index_row-=1
                index_col = remove_queen(index_row) + 1
                continue

            index_pos_diag = index_row + index_col
            index_neg_diag = index_row - index_col

            if (index_col in cols or index_pos_diag in pos_diag_id or index_neg_diag in neg_diag_id):
                index_col += 1
                continue

            queen_position[index_row] = index_col
            cols.add(index_col)
            pos_diag_id.add(index_pos_diag)
            neg_diag_id.add(index_neg_diag)
            index_col = 0
            index_row += 1

            if index_row >= n:
                result.append([(r, c) for r, c in enumerate(queen_position)])
                index_row -= 1
                index_col = remove_queen(index_row) + 1
    backtrack()
    return result


if __name__ == "__main__":
    print(nQueensAll(4))