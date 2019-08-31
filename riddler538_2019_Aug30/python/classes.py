import numpy as np


class Player:

    def __init__(self, soldier_assignment):
        """initalize with soldier_assignment {list or np.array} -- list representing soldiers assigned to each castle"""

        if type(soldier_assignment) is not np.ndarray:
            self.soldiers = np.array(soldier_assignment)
        else: self.soldiers = soldier_assignment

        # Validation
        if len(self.soldiers) != 10: raise ValueError("Not all castles represented")
        if self.soldiers.sum() != 100: raise ValueError("Not enough soldiers! Sum given: {0}".format(self.soldiers.sum()))


class Game:

    def __init__(self, player_A, player_B):        
        won_castles_bool_A = player_A.soldiers > player_B.soldiers # boolean representing where player A won
        won_castles_bool_B = player_A.soldiers < player_B.soldiers # boolean representing where player A won

        weighting_array = np.arange(1,11) # Victory points associated to each castle
        won_array_A = won_castles_bool_A * weighting_array # points for each castle won
        won_array_B = won_castles_bool_B * weighting_array # points for each castle won

        self.total_voctory_points_A = won_array_A.sum()
        self.total_voctory_points_B = won_array_B.sum()
        
        # Won conditions
        if self.total_voctory_points_A > self.total_voctory_points_B:
            self.player_A_win = True
            self.player_B_win = False
            self.tie = False
        elif self.total_voctory_points_A < self.total_voctory_points_B:
            self.player_A_win = False
            self.player_B_win = True
            self.tie = False
        else:
            self.player_A_win = False
            self.player_B_win = False
            self.tie = True   
