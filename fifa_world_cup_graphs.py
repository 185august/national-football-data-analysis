import matplotlib
import matplotlib.pyplot as plt
import pandas as pd
import figure_request
import numpy as np
import matplotlib.ticker as mtick
matplotlib.use('Agg')

from overall_team_statistics_graphs import save_figure_as_base64

def top_goal_scorers_players(df):
    scorers = df['scorer'].value_counts()
    scorers = scorers.head(10)

    fig, ax = plt.subplots(figsize=(20, 6))
    ax.barh(scorers.index, scorers, color='red')
    ax.set_title('Top 10 goal scorers in FIFA World Cup history')
    ax.set_xlabel('Goals')
    ax.set_ylabel('Player')
    ax.grid(True, alpha=0.2)
    ax.set_xticks(np.arange(0, 17, 1))
    figure_data_png = save_figure_as_base64(fig)
    figure = figure_request.figure_request('top goal scorers', figure_data_png)
    return figure

def top_non_penalty_goals_scorers(df):
    top_goal_scorers_wc_non_penalty = df[(df['penalty'] == False)]
    top_goal_scorers_wc_non_penalty = top_goal_scorers_wc_non_penalty['scorer'].value_counts().head(10)

    fig, ax = plt.subplots(figsize=(20, 6))
    ax.barh(top_goal_scorers_wc_non_penalty.index, top_goal_scorers_wc_non_penalty, color="yellow")
    ax.set_title("Top non-penalty goal scorers at the world cup in history")
    ax.set_xlabel("Goals")
    ax.set_ylabel("Player")
    ax.set_xticks(np.arange(0, 17, 1))
    ax.grid(True, alpha=0.2)
    figure_png_base64 = save_figure_as_base64(fig)
    figure = figure_request.figure_request('top non-penalty goal scorers', figure_png_base64)
    return figure

def get_all_world_cup_graphs():
    goals_scorers_data = pd.read_csv('world_cup/fifa_world_cups_goal_scorers.csv')
    teams_data = pd.read_csv('world_cup/fifa_world_cups_teams_summary.csv')
    figs = [top_goal_scorers_players(goals_scorers_data.copy()),
            top_non_penalty_goals_scorers(goals_scorers_data.copy()),]
    return figs

