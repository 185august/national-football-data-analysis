import urllib.parse

import matplotlib.pyplot as plt
import pandas as pd
from io import BytesIO
import base64
import figure_request


def top_20_win_percentage_():
    team_stats_new = pd.read_csv('overall_stats/overall_teams_statistics.csv')
    top_win_percentage = team_stats_new.query('games_played > 100')
    top_win_percentage = top_win_percentage.groupby(
    top_win_percentage['team'])['win_percentage'].sum()
    top_win_percentage = top_win_percentage.sort_values(ascending=False).head(20)
    fig, ax = plt.subplots(figsize=(18, 6), layout='constrained')
    ax.bar(top_win_percentage.index, top_win_percentage)
    ax.yaxis.set_major_formatter(plt.FormatStrFormatter('%.2f'))
    ax.set_ylim(0.6, 0.75)
    ax.set_title(
        'Top 20 highest win percentage teams with at least 100 games played (total wins + draws * 0.5 / total games)')
    ax.set_xlabel('Team', fontsize=12)
    ax.set_ylabel('Win percentage')
    labels = ax.get_xticklabels()
    plt.setp(labels, rotation=45, fontsize=12)

    figure_data_png = export_bar_graph(fig)
    figure = figure_request.figure_request('top_20_win_percentage', figure_data_png)
    return figure

def create_a_bar_graph(data_x, data_y, title, x_label, y_label, rotation=0, ):
    fig, ax = plt.subplots(figsize=(18, 6), layout='constrained')
    ax.bar(data_x, data_y)
    ax.set_title(title)
    ax.set_xlabel(x_label)
    ax.set_ylabel(y_label)
    return fig

def export_bar_graph(fig):
    figure_file = BytesIO()
    plt.savefig(figure_file, format='png')
    figure_file.seek(0)
    figure_data_png = base64.b64encode(figure_file.getvalue())
    figure_request_data = 'data:image/png;base64,' + urllib.parse.quote(figure_data_png)
    return figure_request_data

def total_goals_per_team_bar_graph(team_data):
    total_goals_per_team = team_data.groupby(
        team_data['team'])['total_goals'].sum()
    total_goals_per_team = total_goals_per_team.sort_values(ascending=False).head(10)
    fig, ax = plt.subplots(figsize=(20, 6))
    ax.bar(total_goals_per_team.index, total_goals_per_team)
    ax.set_title('Total goals scored per team')
    ax.set_xlabel('Team')
    ax.set_ylabel('Total goals')
    fig_png = export_bar_graph(fig)
    figure = figure_request.figure_request('total_goals_per_team', fig_png)
    return figure

def get_all_still_graphs():
    team_stats = pd.read_csv('overall_stats/overall_teams_statistics.csv')
    team_stats = team_stats.query('games_played > 100')
    figs = [total_goals_per_team_bar_graph(team_stats.copy()), top_20_win_percentage_()]
    return figs


if __name__ == '__main__':
    # fig_data_png = top_20_win_percentage()
    fig = create_a_bar_graph(data_x=[1, 2, 3, 4, 5], data_y=[0,1,2,3,4], title='Test', x_label='X', y_label='Y')
    plt.show()
    graph_string = export_bar_graph(fig)
    print(graph_string)