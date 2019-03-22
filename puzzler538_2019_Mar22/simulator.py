# Get commandline args
import sys
# Miscillaneous imports
from datetime import datetime
import random

class Game:

    def __init__(self):
        self.away_box_score = []
        self.home_box_score = []

    def simulate(self):

        # simulate both away and home innings for 9 innings
        for inning in range(1,10):
            away_runs_scored = Inning().simulate()
            home_runs_scored = Inning().simulate()
            # Update the score
            self.away_box_score.append(away_runs_scored)
            self.home_box_score.append(home_runs_scored)

        # Keep going until there isn't a tie
        while sum(self.away_box_score) == sum(self.home_box_score):
            away_runs_scored = Inning().simulate()
            home_runs_scored = Inning().simulate()
            # Update the score
            self.away_box_score.append(away_runs_scored)
            self.home_box_score.append(home_runs_scored)

        # Done simulating. 

class Inning:

    def __init__(self):
        self.outs = 0
        self.runs_scored_inning = 0
        self.field = Field()

    def simulate(self):
        # Run at bats until inning is over
        while self.outs < 3:
            # simulate at bat
            ab_result = AtBat()
            # issue result to Field
            runs_scored, outs_recorded = self.field.update(ab_result.outcome)

            self.outs += outs_recorded
            # Only bank runs if outs are still under 3
            if self.outs < 3:
                self.runs_scored_inning += runs_scored
                self.outs

        return self.runs_scored_inning


class Field:

    def __init__(self):
        """ fresh field """
        self.occupied_1b = False
        self.occupied_2b = False
        self.occupied_3b = False


    def update(self, result):
        """Updating the field based on results
            - There's probably a smarter way to do this
        """

        runs_scored = 0
        outs_recorded = 0

        if result == 'single':
            # Runners from 2b or 3b score first
            if self.occupied_2b and self.occupied_3b:
                self.occupied_2b = False
                self.occupied_3b = False
                runs_scored += 2
            elif self.occupied_2b or self.occupied_3b:
                self.occupied_2b = False
                self.occupied_3b = False
                runs_scored += 1
            # Runners from first advance
            if self.occupied_1b:
                self.occupied_2b = True
            # First base now occupied
            self.occupied_1b = True

        if result == 'double':
            # Runners from 2b or 3b score
            if self.occupied_2b and self.occupied_3b:
                self.occupied_2b = False
                self.occupied_3b = False
                runs_scored += 2
            elif self.occupied_2b or self.occupied_3b:
                self.occupied_2b = False
                self.occupied_3b = False
                runs_scored += 1
            # Runner on 1st (see notes)
            if self.occupied_1b:
                rand = random.uniform(0,1)
                if rand < 0.4:
                    runs_scored +=1
                else:
                    self.occupied_3b = True
                self.occupied_1b = False
            
        if result == 'triple':
            # Everyone on base scores
            number_bases_occupied =  self.occupied_1b + self.occupied_2b + self.occupied_3b
            runs_scored += number_bases_occupied
            # New runner on 3b
            self.occupied_3b = True

        if result == 'home run':
            number_bases_occupied =  self.occupied_1b + self.occupied_2b + self.occupied_3b
            runs_scored += number_bases_occupied + 1

        if result == 'foul out' or result == 'fly out' or result == 'out at 1st' or result == 'strike out':
            outs_recorded += 1

        if result == 'double play':
            # This is weird, since dps aren't always possible. See notes.
            
            if self.occupied_1b + self.occupied_2b + self.occupied_3b == 0:
                # If nobody on base, just a normal out
                outs_recorded +=1
            
            ## 1 existing Baserunner scenario
            elif self.occupied_1b and not self.occupied_2b and not self.occupied_3b:
                # If on first, outs at 1b and 2b
                self.occupied_1b = False
                outs_recorded += 2
            elif (not self.occupied_1b and self.occupied_2b and not self.occupied_3b):
                # If baserunner on second, no force outs, just add an out
                outs_recorded += 1
            elif (not self.occupied_1b and not self.occupied_2b and self.occupied_3b):
                # If baserunner on third, same
                outs_recorded += 1

            ## 2 existing Baserunner scenario
            elif self.occupied_1b and self.occupied_2b and not self.occupied_3b:
                # If on 1st and 2nd, outs at 3rd and 2nd
                self.occupied_1b = True
                self.occupied_2b = False
                outs_recorded += 2
            elif self.occupied_1b and not self.occupied_2b and self.occupied_3b:
                # If on 1st and 3nd, outs at 2rd and 1st
                self.occupied_1b = False
                outs_recorded += 2
            elif not self.occupied_1b and self.occupied_2b and self.occupied_3b:            
                # If 2b and 3b occupied, only force out at 1b, so base/out doesn't change
                outs_recorded += 1

            ## 3 existing Baserunner scneario
            elif self.occupied_1b and self.occupied_2b and self.occupied_3b:            
                # If bases loaded, outs at home and 3b. 2b and 1b stay occupied
                self.occupied_3b = False
                outs_recorded += 2


        if result == 'base on error':
            # Everyone advances
            if self.occupied_3b:
                runs_scored += 1
                self.occupied_3b = False
            if self.occupied_2b:
                self.occupied_3b = True
                self.occupied_2b = False
            if self.occupied_1b:
                self.occupied_2b = True
                self.occupied_1b = False
            self.occupied_1b = True


        if result == 'base on balls':
            if self.occupied_3b and self.occupied_2b and self.occupied_1b:
                runs_scored += 1
            if self.occupied_2b and self.occupied_1b:
                self.occupied_3b = True
            if self.occupied_1b:
                self.occupied_2b = True
            self.occupied_1b = True        

        return runs_scored, outs_recorded

class AtBat:

    def __init__(self):
        self.strikes = 0
        self.outcome = None

        dice_result = tuple(throw_dice())
        #print(dice_result)
        result_dictionary = {
            (1, 1): 'double',
            (1, 2): 'single',
            (1, 3): 'single',
            (1, 4): 'single',
            (1, 5): 'base on error',
            (1, 6): 'base on balls',
            (2, 2): 'strike',
            (2, 3): 'strike',
            (2, 4): 'strike',
            (2, 5): 'strike',
            (2, 6): 'foul out',
            (3, 3): 'out at 1st',
            (3, 4): 'out at 1st',
            (3, 5): 'out at 1st',
            (3, 6): 'out at 1st',
            (4, 4): 'fly out',
            (4, 5): 'fly out',
            (4, 6): 'fly out',
            (5, 5): 'double play',
            (5, 6): 'triple',
            (6, 6): 'home run',
        }

        result = result_dictionary[dice_result]
        while result == 'strike' and self.strikes != 2:
            # add a strike
            self.strikes += 1

            # Rethrow dice
            dice_result = tuple(throw_dice())
            result = result_dictionary[dice_result]

        if result == 'strike' and self.strikes == 2:
            result == 'strike out'

        self.outcome = result

def throw_dice():
    """ Return 2 random dice values, sort in (low,high) """
    dice_1 = random.randrange(1,7)
    dice_2 = random.randrange(1,7)
    return sorted((dice_1,dice_2))


if __name__ == "__main__":
    time = datetime.now().isoformat()
    num_simulations = int(sys.argv[1])

    with open('data/run_simulations{1}.csv'.format(time,num_simulations),'w') as f:
        # Make csv_header
        f.write('simulation_no,home_score,away_score,total_score\n')
        # Run n simulations
        for i in range(0,num_simulations):
            simulation = Game()
            simulation.simulate()
            home_score = sum(simulation.home_box_score)
            away_score = sum(simulation.away_box_score)
            total_score = home_score + away_score

            f.write('%i,%i,%i,%i\n' % (i, home_score, away_score, total_score))
