import random

class Battleship:
    def __init__(self):
        self.main()

    def main(self):
        retry = "yes"
        while retry == "yes":
            self.start_game()
            retry = input("Do you want to play again? (yes/no): ").lower()

    def start_game(self):
        print("Welcome to Battleship!")
        board_size = int(input("Enter the size of the board (e.g., 20): "))
        retries = int(input("Enter the number of allowed attempts (e.g., 10): "))

        board =  board_size * ["~"]
        sizes = [2, 3, 4]               
        ships = self.build_ships(board_size, sizes)

        total_hits = set()
        total_misses = 0
        remaining = sum(sizes)
        total = sum(sizes)

        while True:
            print("Board:", " ".join(board))
            print("Hits:", len(total_hits), ":", total_misses)   

            if remaining == 0:
                print("Congratulations! You've sunk all the ships!")
                return
            if total_misses >= retries:
                print("You lose!")
                return

            target = int(input(f"Enter a position to guess (0-{board_size-1}): "))
            if target < 0 or target >= board_size:
                print("Outside of range!")
                continue
            if board[target] == "X":
                print("Repeated Hit!")
                continue
            hit = False 
            for ship in ships:
                if target in ship:
                    print("Hit!")
                    hit = True
                    ship.remove(target)    
                    remaining -= 1
                    board[target] = "X"
                    if len(ship) == 0:
                        print("You've sunk a ship!")
                    break

            if not hit:
                total_misses += 1
                print("Miss!")

    def build_ships(self, board_size, sizes):
        ships = []
        i = 0
        while len(ships) < len(sizes):
            start = random.randint(0, board_size - sizes[i])
            ship = set(range(start, start + sizes[i]))
            if not any(ship.intersection(s) for s in ships):
                ships.append(ship)
                i += 1
        print ("Ships:", ships)
        return ships


if __name__ == "__main__":
    Battleship()