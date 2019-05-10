from random import random
import numpy as np
from itertools import groupby
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd

# Assumptions
number_atbats_per_game = 4
games_per_season = 160


# Generically Useful Functions
def calculate_streaks(outcome_list, delimiter):
    """ returns a list of lists for all the streaks"""
    all_streaks = []
    sublist_generator = (
        list(g) for k, g in groupby(outcome_list, key=lambda x: x != delimiter) if k
    )
    for i in sublist_generator:
        all_streaks.append(i)
    return all_streaks


# Classes for various stretches
# ------------------------------------------------------------------------
class Game:
    def __init__(self, BA, number_atbats):
        # random values between 0 and 1
        probabilities = np.random.uniform(size=(number_atbats,))
        self.outcomes = probabilities <= BA
        self.number_of_hits = self.outcomes.sum()


class PlayerSeason:
    def __init__(self, BA, number_games):

        # simulate all games
        self.all_ab_outcomes = np.empty(shape=(number_games, number_atbats_per_game))
        self.hit_boolean = []

        for i in range(0, number_games):
            this_game = Game(BA, number_atbats_per_game)
            self.all_ab_outcomes[i] = this_game.outcomes

        # Calculate useful quantities
        self.all_ab_results = self.all_ab_outcomes.flatten("F")
        self.game_results = np.any(
            self.all_ab_outcomes == 1, axis=1
        )  # evaluates to True if a hit
        self.longest_streak = max(
            [len(streak) for streak in calculate_streaks(self.game_results, False)]
        )


class PlayerCareer:
    def __init__(self, BA, seasons):

        # Simulate all seasons
        self.full_hit_gamelog = np.empty(shape=(seasons, games_per_season))

        for i in range(0, seasons):
            this_season = PlayerSeason(BA, games_per_season)

            self.full_hit_gamelog[i, :] = this_season.game_results

        # Join all season hits into one large array
        self.career_game_results = self.full_hit_gamelog.flatten("F")
        self.longest_streak = max(
            [
                len(streak)
                for streak in calculate_streaks(self.career_game_results, False)
            ]
        )

        #print(self.longest_streak)


class PlayerSimulation:
    def __init__(self, BA, seasons_played):
        # Qualities of player itself
        self.BA = BA
        self.seasons_played = seasons_played
        
        # Simulate by season
        self.longest_streaks = []
        self.total_hits = 0

    def simulate_career(self):
        career_stats = PlayerCareer(self.BA, self.seasons_played)
        self.longest_streaks.append(career_stats.longest_streak)


if __name__ == "__main__":


    players = [
        PlayerSimulation(0.200,20),
        PlayerSimulation(0.250,20),
        PlayerSimulation(0.300,20),
        PlayerSimulation(0.350,20),
        PlayerSimulation(0.400,20),
        PlayerSimulation(0.500,10),
    ]

    n_simulations = 10
    for iSim in range(0,n_simulations):
        # Run simulations for all players
        for player in players:
            player.simulate_career()


    # Calculate fraction above Dimaggio's 56
    streaks = [np.array(pl.longest_streaks) for pl in players]

    fraction_record_seasons = []
    for player in players:
        all_streaks = np.array(player.longest_streaks)
        beat_record = all_streaks[all_streaks > 56]
        fraction_record_seasons.append(beat_record.shape[0]/all_streaks.shape[0])

    # Plot the longest streaks
    streaks = [np.array(pl.longest_streaks) for pl in players]
    plt.figure(figsize=(8,6))
    ax = plt.gca()

    edited_labels = [".200 BA\n20 Szns",
                     ".250 BA\n20 Szns",
                     ".300 BA\n20 Szns",
                     ".350 BA\n20 Szns",
                     ".400 BA\n20 Szns",
                     ".500 BA\n10 Szns",                     
    ]
    df = pd.DataFrame.from_items(zip(edited_labels,streaks))
    ax = sns.boxplot(x='variable',y='value',data=pd.melt(df), color="dodgerblue")


    # Add Labels
    plt.xlabel('Players', fontsize=14)
    plt.ylabel('Longest Hitting Streak', fontsize=16)

    ymin,ymax = plt.gca().get_ylim()
    ax.set_ylim(top=ymax*1.1)
    # Add mean annotation
    hfont = {'fontname':'Helvetica'}
    means = [a.mean() for a in streaks]

    for meanval, i in zip(means, range(0,len(means))):
        plt.annotate("mean = %.1f"%meanval, xy=(i, ymax*1.03), ha='center', fontsize=10, style='normal', **hfont)
        plt.annotate("{0}% Record".format(100*fraction_record_seasons[i]), xy=(i,ymax*1.06), ha='center', fontsize=10, **hfont) 

    # Annotate DiMaggio Line and Simulations
    plt.axhline(y=56, linestyle='--',color='forestgreen')
    plt.annotate("DiMaggio Record", xy=(-0.3,58), color='forestgreen', fontsize=12, **hfont)

    # Make better looking
    ## Gridlines
    for i in range(0,len(means)):
        plt.axvline(i+0.5, color='gainsboro', linestyle=':', linewidth=1)

    plt.annotate(s="Tyler James Burch", xy=(.01,.033), xycoords='figure fraction',
                     textcoords='figure fraction', color='grey',alpha=0.7, fontsize=10)

    plt.annotate("{0} Simulations each".format(n_simulations), xy=(0.98,0.02), ha='right', fontsize=12, xycoords='axes fraction', **hfont) 

    plt.tight_layout()

    plt.savefig('plots/longest_streaks')

