import urllib.parse

import matplotlib
import matplotlib.pyplot as plt
import pandas as pd
from io import BytesIO
import base64
import figure_request
import numpy as np
import matplotlib.ticker as mtick
matplotlib.use('Agg')

def most_goals_through_history(df):
    total_goals_per_team = df.groupby(
        df['team'])['total_goals'].sum()
    total_goals_per_team = total_goals_per_team.sort_values(ascending=False).head(10)
    fig, ax = plt.subplots(figsize=(20, 6))
    ax.bar(total_goals_per_team.index, total_goals_per_team)
    ax.set_title('Total goals scored per team')
    ax.set_xlabel('Team')
    ax.set_ylabel('Total goals')
    figure_data_png = save_figure_as_base64(fig)
    figure = figure_request.figure_request('most goals through history', figure_data_png)
    return figure

def top_20_win_percentage_(df):

    top_win_percentage = df.groupby(
    df['team'])['win_percentage'].sum()
    top_win_percentage = top_win_percentage.sort_values(ascending=False).head(20)
    fig, ax = plt.subplots(figsize=(20, 6), layout='constrained')
    ax.bar(top_win_percentage.index, top_win_percentage)
    ax.yaxis.set_major_formatter(plt.FormatStrFormatter('%.2f'))
    ax.set_ylim(0.6, 0.75)
    ax.set_title(
        'Top 20 highest win percentage teams with at least 100 games played (total wins + draws * 0.5 / total games)')
    ax.set_xlabel('Team', fontsize=12)
    ax.set_ylabel('Win percentage')
    labels = ax.get_xticklabels()
    plt.setp(labels, rotation=45, fontsize=12)

    figure_data_png = save_figure_as_base64(fig)
    figure = figure_request.figure_request('top 20 win percentage', figure_data_png)
    return figure

def bottom_20_win_percentage(df):
    lowest_win_percentage = df.groupby(
        df['team'])['win_percentage'].sum()
    lowest_win_percentage = lowest_win_percentage.sort_values(ascending=False).tail(20)
    fig, ax = plt.subplots(figsize=(20, 6), layout='constrained')
    ax.bar(lowest_win_percentage.index, lowest_win_percentage)
    ax.yaxis.set_major_formatter(plt.FormatStrFormatter('%.2f'))
    ax.set_title(
        'Lowest win percentage for teams with at least 100 games played (total wins + draws * 0.5 / total games)')
    ax.set_xlabel('Team', fontsize=12)
    ax.set_ylabel('Win percentage')
    labels = ax.get_xticklabels()
    plt.setp(labels, rotation=45, fontsize=12)
    figure_data_png = save_figure_as_base64(fig)
    figure = figure_request.figure_request('bottom 20 win percentage', figure_data_png)
    return figure

def most_amount_of_draws(df):
    most_draws = df.groupby(
        df['team'])['total_draws'].sum()
    most_draws = most_draws.sort_values(ascending=False).head(20)
    fig, ax = plt.subplots(figsize=(20, 6), layout='constrained')
    ax.bar(most_draws.index, most_draws)
    ax.set_ylim(150, 260)
    ax.set_title('Total draws with at least 100 games played (total wins + draws * 0.5 / total games)')
    ax.set_xlabel('Team', fontsize=12)
    ax.set_ylabel('Win percentage')
    labels = ax.get_xticklabels()
    plt.setp(labels, rotation=45, fontsize=12)
    figure_data_png = save_figure_as_base64(fig)
    figure = figure_request.figure_request('most amount of draws', figure_data_png)
    return figure

def highest_away_win_percentage(df):
    away_win_percentage = df.groupby(df['team'])['away_win_percentage'].sum().sort_values(ascending=False)
    away_win_percentage = away_win_percentage.head(20)
    fig, ax = plt.subplots(figsize=(20, 8))
    ax.bar(away_win_percentage.index, away_win_percentage)
    ax.set_title('Away win percentage per team')
    ax.set_xlabel('Team')
    ax.set_ylabel('Win percentage')
    ax.yaxis.set_major_formatter(mtick.PercentFormatter(1.0))
    ax.tick_params(axis='x', rotation=45, labelsize=12)
    ax.set_yticks(np.arange(0.0, 0.3, 0.02))
    figure_data_png = save_figure_as_base64(fig)
    figure = figure_request.figure_request('highest away win percentage', figure_data_png)
    return figure

def highest_amount_of_home_and_away_win(df):
    team_stats_sorted = df.sort_values(by='win_percentage')
    team_stats_sorted = team_stats_sorted.tail(10)
    home_wins = team_stats_sorted.groupby(
        team_stats_sorted['team'])['home_win_percentage'].sum().tail(10)
    away_wins = team_stats_sorted.groupby(
        team_stats_sorted['team'])['away_win_percentage'].sum().tail(10)

    fig, ax = plt.subplots(figsize=(20, 6))
    ax.scatter(home_wins, away_wins)
    ax.set_title('Home wins vs away wins')
    ax.set_xlabel('Home win percentage')
    ax.set_ylabel('Away win percentage')
    ax.set_xlim(0.24, 0.45)
    ax.set_ylim(0.15, 0.3)
    ax.set_xticks(np.arange(0.24, 0.45, 0.02))
    ax.set_yticks(np.arange(0.15, 0.3, 0.02))
    ax.xaxis.set_major_formatter(mtick.PercentFormatter(1.0, decimals=False))
    ax.yaxis.set_major_formatter(mtick.PercentFormatter(1.0, decimals=False))
    ax.grid(True, alpha=0.3)
    for i, txt in enumerate(home_wins.index):
        ax.annotate(txt, (home_wins.iloc[i], away_wins.iloc[i]),
                    ((home_wins.iloc[i] + 0.003), (away_wins.iloc[i] + 0.001)))
    figure_data_png = save_figure_as_base64(fig)
    figure = figure_request.figure_request('highest amount of home and away win', figure_data_png)
    return figure

def create_a_bar_graph(data_x, data_y, title, x_label, y_label, rotation=0, ):
    fig, ax = plt.subplots(figsize=(18, 6), layout='constrained')
    ax.bar(data_x, data_y)
    ax.set_title(title)
    ax.set_xlabel(x_label)
    ax.set_ylabel(y_label)
    return fig


def total_goals_per_team_bar_graph(team_data):
    total_goals_per_team = team_data.groupby(
        team_data['team'])['total_goals'].sum()
    total_goals_per_team = total_goals_per_team.sort_values(ascending=False).head(10)
    fig, ax = plt.subplots(figsize=(20, 6))
    ax.bar(total_goals_per_team.index, total_goals_per_team)
    ax.set_title('Total goals scored per team')
    ax.set_xlabel('Team')
    ax.set_ylabel('Total goals')
    fig_png = save_figure_as_base64(fig)
    figure = figure_request.figure_request('total goals per team', fig_png)
    return figure

def average_amount_of_goals_through_history():
    match_data = pd.read_csv("results.csv", parse_dates=["date"])
    avg_home_goals = match_data.groupby(
        [match_data["date"].dt.year])["home_score"].mean()

    avg_away_goals = match_data.groupby(
        [match_data["date"].dt.year])["away_score"].mean()
    fig, ax = plt.subplots(figsize=(20, 6), constrained_layout=True)
    ax.plot(avg_home_goals, label='home', color='red', marker='o')
    ax.plot(avg_away_goals, label='away', color='blue', marker='o')
    ax.set_title('Average goals scored per year')
    ax.set_xlabel('Year')
    ax.set_ylabel('Goals scored')
    ax.legend()
    ax.grid(True, alpha=0.2)
    ax.set_xticks(np.arange(1870, 2030, 5))
    ax.set_yticks(np.arange(0, 10, 1))
    figure_data_png = save_figure_as_base64(fig)
    figure = figure_request.figure_request('average amount of goals through history', figure_data_png)
    return figure

def save_figure_as_base64(fig):
    figure_file = BytesIO()
    plt.savefig(figure_file, format='png')
    figure_file.seek(0)
    figure_data_png = base64.b64encode(figure_file.getvalue())
    figure_request_data = 'data:image/png;base64,' + urllib.parse.quote(figure_data_png)
    return figure_request_data

def get_all_graphs():
    team_stats = pd.read_csv('overall_stats/overall_teams_statistics.csv')
    team_stats = team_stats.query('games_played > 500')
    figs = [total_goals_per_team_bar_graph(team_stats.copy()),
            top_20_win_percentage_(team_stats.copy()),
            most_goals_through_history(team_stats.copy()),
            bottom_20_win_percentage(team_stats.copy()),
            most_amount_of_draws(team_stats.copy()),
            highest_away_win_percentage(team_stats.copy()),
            highest_amount_of_home_and_away_win(team_stats.copy())]
    return figs


if __name__ == '__main__':
    # fig_data_png = top_20_win_percentage()
    fig = create_a_bar_graph(data_x=[1, 2, 3, 4, 5], data_y=[0,1,2,3,4], title='Test', x_label='X', y_label='Y')
    plt.show()
    graph_string = save_figure_as_base64(fig)
    print(graph_string)