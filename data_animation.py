import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import matplotlib.animation as animation

def create_animation(df):
    df = pd.read_csv('team_yearly_stats.csv')

    frames = df['year'].unique()



    fig, ax = plt.subplots(figsize=(12, 6))

    def animate(frame):
        ax.clear()
        year_stats_frame = df[df['year'] == frame]

        top_countries = year_stats_frame.nlargest(10, 'total_goals_scored').sort_values('total_goals_scored', ascending=True)

        ax.barh(top_countries['team'], top_countries['total_goals_scored'])

    anim = animation.FuncAnimation(fig, animate, frames=frames, interval=200)
    return anim

if __name__ == '__main__':
    df = pd.read_csv('team_yearly_stats.csv')
    anim = create_animation(df)
    plt.show()

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