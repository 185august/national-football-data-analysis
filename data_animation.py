import base64
import tempfile
import os
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import matplotlib.animation as animation

def setup_plot_style(ax, x_label, title):
    ax.set_facecolor('white')
    ax.spines['right'].set_visible(False)
    ax.tick_params(axis='both', which='major', labelsize=12)
    ax.set_xlabel(x_label, fontsize=14)
    ax.set_title(title, fontsize=16)


def add_year_text(ax, year):
    ax.text(0.95, 0.1, year, horizontalalignment='right', verticalalignment='bottom', transform=ax.transAxes,
            fontsize=14)
    return ax


def goals_total_over_time_for_countries_animation():
    world_cup_goals_over_time = pd.read_csv('world_cup/cumulative_stats_over_time_world_cup.csv')
    all_teams = world_cup_goals_over_time['team'].unique()
    cmap_name = 'tab20'
    cmap_obj = plt.colormaps.get_cmap(cmap_name)
    colors = cmap_obj.resampled(len(all_teams))

    team_color_map = {team: colors(i) for i, team in enumerate(all_teams)}

    frames = world_cup_goals_over_time['year'].unique()
    fig, ax = plt.subplots(figsize=(12, 6))

    def animate(frame):
        ax.clear()
        year_stats_frame = world_cup_goals_over_time[world_cup_goals_over_time['year'] == frame]

        top_countries = year_stats_frame.nlargest(10, 'goals').sort_values('goals', ascending=True)

        bar_colors = [team_color_map[team] for team in top_countries['team']]

        ax.barh(top_countries['team'], top_countries['goals'], color=bar_colors)

        for i, row in top_countries.iterrows():
            ax.text(row['goals'], row['team'], str(int(row["goals"])), ha='left', va='center')

        setup_plot_style(ax, 'Total goals scored', 'Top 10 teams by total goals scored')
        add_year_text(ax, frame)
        plt.tight_layout()

    anim = animation.FuncAnimation(fig, animate, frames=frames, interval=600, repeat=False)

    return anim


def create_animation_of_goals_over_time(match_data):
    fig, ax = plt.subplots(figsize=(20, 5))

    avg_home_goals = match_data.groupby([match_data['date'].dt.year])['away_score'].mean()
    avg_away_goals = match_data.groupby([match_data['date'].dt.year])['home_score'].mean()

    line1, = ax.plot([], [], marker='o', color='red')
    line2, = ax.plot([], [], marker='o', color='blue')

    ax.set_ylim(0, 10)
    ax.set_xlim(avg_home_goals.index.min(), avg_home_goals.index.max())
    ax.set_yticks(np.arange(1, 9, 1))
    ax.set_xticks(np.arange(1880, 2025, 10))
    ax.tick_params(axis='x', rotation=45, labelsize=11)
    ax.margins(x=0.01)
    ax.set_xlabel('Year')
    ax.set_ylabel('Average goals scored')
    ax.set_title('Average goals scored per year')

    def update(frame):
        y = avg_away_goals.values[:frame]
        x = avg_away_goals.index[:frame]
        y2 = avg_home_goals.values[:frame]
        x2 = avg_home_goals.index[:frame]
        line1.set_data(x, y)
        line2.set_data(x2, y2)
        return line1, line2

    ani = animation.FuncAnimation(fig, update, frames=len(avg_away_goals) + 1, interval=100, repeat=True, blit=True)
    plt.show()

def send_animation_as_base64():
    tmp_file = tempfile.TemporaryFile('w', suffix='.gif')
    anim = goals_total_over_time_for_countries_animation()
    anim.save(tmp_file, writer='imagemagick', fps=1)
    with open('world_cup_goals_over_time.gif', 'rb') as f:
         gif = base64.b64encode(f.read()).decode(
            'utf-8'
        )
    import urllib.parse
    tmp_file.close()
    gif = 'data:image/gif;base64,' + urllib.parse.quote(gif)
    return gif

def get_all_animations():
    animation_data = send_animation_as_base64()
    import figure_request
    figure = figure_request.figure_request('world_cup_goals_over_time', animation_data)
    return figure
