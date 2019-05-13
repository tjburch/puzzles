import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
from itertools import groupby

def calculate_streaks(outcome_list, delimiter):
    """ returns a list of lists for all the streaks"""
    all_streaks = []
    sublist_generator = (
        list(g) for k, g in groupby(outcome_list, key=lambda x: x != delimiter) if k
    )
    return sublist_generator


def simulate(games, atbats, average):
    
    single_game_probability = (1-average)**4
    probabilities = np.random.rand(games)
    games_with_hits = probabilities > single_game_probability
    longest_streak = max([len(streak) for streak in calculate_streaks(games_with_hits, False)])
    return longest_streak

n_simulations = 100

simulated_carrers = []
for i in range(0,n_simulations):
    streak = simulate(160 * 20, 4, 0.350)
    simulated_carrers.append(streak)

player_dict ={
        ".350 BA\n20 Szns" : simulated_carrers,
}

df = pd.DataFrame.from_dict(player_dict)
ax = sns.boxplot(x='variable',y='value',data=pd.melt(df), color="dodgerblue", whis=[5,95], showfliers=False)

# Add Labels
plt.xlabel('Players', fontsize=14)
plt.ylabel('Longest Hitting Streak', fontsize=16)

ymin,ymax = plt.gca().get_ylim()
ax.set_ylim(top=ymax*1.1)
# Add mean annotation
hfont = {'fontname':'Helvetica'}

# Annotate DiMaggio Line and Simulations
plt.axhline(y=56, linestyle='--',color='forestgreen')
plt.annotate("DiMaggio Record", xy=(-0.3,58), color='forestgreen', fontsize=12, **hfont)
plt.show()

