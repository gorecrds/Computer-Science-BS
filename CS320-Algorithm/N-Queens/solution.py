def nQueensAll(n: int) -> list[list[tuple[int, int]]]:  # pylint: disable=invalid-name
    if n < 4:
        raise ValueError("Value Error: n must be equal to or greater than 4.")
    cols = set()
    pos_diag_id = set()  # i_row + i_col
    neg_diag_id = set()  # i_row - i_col
    solutions = []
    positions = [None] * n


    def remove_queen(row: int) -> int:
        """Remove queen from given row. Returns the removed column."""
        col = positions[row]
        cols.remove(col)
        pos_diag_id.remove(row + col)
        neg_diag_id.remove(row - col)
        positions[row] = None
        return col

    def backtrack() -> None:
        index_row=0
        index_col=0
        while index_row < n:
            if index_row ==0 and index_col >= n:
                return
            if index_col >= n:
                index_row-=1
                index_col=positions[index_row]+1
                cols.remove(positions[index_row])
                pos_diag_id.remove(index_row + positions[index_row])
                neg_diag_id.remove(index_row - positions[index_row])
                positions[index_row]=None
                continue

            index_pos_diag = index_row + index_col
            index_neg_diag = index_row - index_col

            if (index_col in cols or index_pos_diag in pos_diag_id or index_neg_diag in neg_diag_id):
                index_col += 1
                continue

            positions[index_row] = index_col
            cols.add(index_col)
            pos_diag_id.add(index_pos_diag)
            neg_diag_id.add(index_neg_diag)
            index_col = 0
            index_row += 1

            if index_row >= n:
                solutions.append([(r, c) for r, c in enumerate(positions)])
                index_row-=1
                index_col=positions[-1]
                cols.remove(index_col)  
                pos_diag_id.remove(index_row + positions[index_row])
                neg_diag_id.remove(index_row - positions[index_row])
                positions[-1]=None
                index_col += 1
    backtrack()
    return solutions


if __name__ == "__main__":
    print(nQueensAll(4))