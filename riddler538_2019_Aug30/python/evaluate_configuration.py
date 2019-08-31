import pandas as pd
import numpy as np
from classes import *

def evaluate_old_solutions(eval_list):

    datadir = "/Users/tburch/Documents/github/puzzles/riddler538_2019_Aug30/data/"
    solutions = pd.read_csv(datadir+"castle-solutions-clean.csv")
    solutions_arr = solutions.to_numpy()

    eval_player = Player(eval_list)
    
    win,loss,tie  = 0, 0, 0

    for solution in solutions_arr:
        solution_player = Player(solution)
        g = Game(eval_player, solution_player)
        if g.player_A_win: win += 1
        if g.player_B_win: loss += 1
        if g.tie: tie += 1
    
    return win, loss, tie



if __name__ == "__main__":
    
    thisPlayer = [5,10,5,15,15,5,5,10,10,20]

    w,l,t = evaluate_old_solutions(thisPlayer)
    win_percent = round(100*w/(w+l+t), 2)
    print(f"{w} wins, {l} losses, {t} ties. WP: {win_percent}")