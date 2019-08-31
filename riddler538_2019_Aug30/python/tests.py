from classes import *

def create_player():
    rands = np.random.random(10)
    randnums = np.round(rands/rands.sum() * 100)
    while randnums.sum() > 100:
        randnums[np.random.randint(low=0, high=9)] -= 1
    while randnums.sum() < 100:
        randnums[np.random.randint(low=0, high=9)] += 1
    
    a = Player(randnums)
    return a

def create_game():
    a = create_player()
    b = create_player()

    g = Game(a,b)
    if g.player_A_win: print("A won")
    if g.player_B_win: print("B won")


if __name__ == "__main__":
    create_player()
    create_game()