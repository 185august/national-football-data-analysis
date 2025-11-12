import matplotlib.pyplot as plt
import pandas as pd
from io import BytesIO
import base64

def top_20_win_percentage():
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
    figure_file = BytesIO()
    plt.savefig(figure_file, format='png')
    figure_file.seek(0)
    figure_data_png = base64.b64encode(figure_file.getvalue())
    return figure_data_png

if __name__ == '__main__':
    fig_data_png = top_20_win_percentage()