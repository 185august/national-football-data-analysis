import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import numpy as np


match_data = pd.read_csv('results.csv', parse_dates=['date'])

goalscorers = pd.read_csv('goalscorers.csv', parse_dates=['date'])


def create_combined_data_frame(match_data, goalscorers):
    match_data['match_id'] = (
            match_data['date'].astype(str) + '_' +
            match_data['home_team'] + '_' +
            match_data['away_team']
    )

    goalscorers['match_id'] = (
            goalscorers['date'].astype(str) + '_' +
            goalscorers['home_team'] + '_' +
            goalscorers['away_team']
    )

    goalscorers_count = goalscorers.groupby(['match_id', 'team']).size().reset_index(name='recorded_goals')

    match_home = match_data[['match_id', 'date', 'home_team', 'away_team',
                             'home_score', 'away_score']].copy()
    match_home['team'] = match_home['home_team']
    match_home['official_goals'] = match_home['home_score']

    match_away = match_data[['match_id', 'date', 'home_team', 'away_team',
                             'home_score', 'away_score']].copy()
    match_away['team'] = match_away['away_team']
    match_away['official_goals'] = match_away['away_score']

    match_combine = pd.concat([
        match_home[['match_id', 'date', 'team', 'official_goals', 'home_team', 'away_team']],
        match_away[['match_id', 'date', 'team', 'official_goals', 'home_team', 'away_team']]
    ])

    comparison = match_combine.merge(
        goalscorers_count,
        on=['match_id', 'team'],
        how='left'
    )

    comparison['recorded_goals'] = comparison['recorded_goals'].fillna(0).astype(int)

    comparison['missing_goals'] = comparison['official_goals'] - comparison['recorded_goals']

    comparison.head(20)

def home_and_away_goals_per_year(match_data):
    avg_home_goals = match_data.groupby(
        [match_data["date"].dt.year])["home_score"].mean()

    avg_away_goals = match_data.groupby(
        [match_data["date"].dt.year])["away_score"].mean()
    plt.plot(avg_home_goals, label='home', color='red', marker='o')
    plt.plot(avg_away_goals, label='away', color='blue', marker='o')

    plt.show()

def create_team_statistic_summary(match_data):
    match_data_copy = match_data.copy()

    match_data_copy['home_win'] = match_data_copy['home_score'] > match_data_copy['away_score']
    match_data_copy['away_win'] = match_data_copy['home_score'] < match_data_copy['away_score']
    match_data_copy['draw'] = match_data_copy['home_score'] == match_data_copy['away_score']

    home_goals = match_data_copy.groupby('home_team')['home_score'].sum()
    away_goals = match_data_copy.groupby('away_team')['away_score'].sum()

    home_wins = match_data_copy.groupby('home_team')['home_win'].sum()
    away_wins = match_data_copy.groupby('away_team')['away_win'].sum()
    home_draws = match_data_copy.groupby('home_team')['draw'].sum()
    away_draws = match_data_copy.groupby('away_team')['draw'].sum()
    home_losses = match_data_copy.groupby('home_team')['away_win'].sum()
    away_losses = match_data_copy.groupby('away_team')['home_win'].sum()
    wins = home_wins.add(away_wins, fill_value=0)
    draws = home_draws.add(away_draws, fill_value=0)
    losses = home_losses.add(away_losses, fill_value=0)

    total_goals = home_goals.add(away_goals, fill_value=0)

    home_games = match_data_copy.groupby('home_team').size()
    away_game = match_data_copy.groupby('away_team').size()
    total_games = home_games.add(away_game, fill_value=0)
    win_percentage = (wins + 0.5 * draws) / total_games

    home_goals_conceded = match_data_copy.groupby('home_team')['away_score'].sum()
    away_goals_conceded = match_data_copy.groupby('away_team')['home_score'].sum()

    total_goals_conceded = home_goals_conceded.add(away_goals_conceded, fill_value=0)

    goals_summary = pd.DataFrame({
        'home_goals': home_goals,
        'away_goals': away_goals,
        'total_goals': total_goals,
        'home_wins': home_wins,
        'away_wins': away_wins,
        'total_wins': wins,
        'home_draws': home_draws,
        'away_draws': away_draws,
        'total_draws': draws,
        'home_losses': home_losses,
        'away_losses': away_losses,
        'total_losses': losses,
        'win_rate': wins/total_games,
        'win_percentage': win_percentage,
        'goals_conceded_home': home_goals_conceded,
        'goals_conceded_away': away_goals_conceded,
        'goals_conceded': total_goals_conceded,
        'games_played': total_games,
        'avg_goals_per_game': total_goals / total_games,
        'avg_goals_conceded_per_game': total_goals_conceded / total_games,
        'goal_difference': home_goals - away_goals
    })
    goals_summary.fillna(0, inplace=True)
    goals_summary.sort_values('total_goals', ascending=False)
    goals_summary.to_csv('teams_summary.csv')
    return goals_summary.sort_values('total_goals', ascending=False)

def create_yearly_team_statistics(df, csv_file_name):
    match_data_copy = df.copy()

    match_data_copy = match_data_copy[match_data_copy['tournament'] == 'FIFA World Cup']
    match_data_copy['home_win'] = match_data_copy['home_score'] > match_data_copy['away_score']
    match_data_copy['away_win'] = match_data_copy['home_score'] < match_data_copy['away_score']
    match_data_copy['draw'] = match_data_copy['home_score'] == match_data_copy['away_score']
    match_data_copy['year'] = match_data_copy['date'].dt.year
    non_neutral_matches = match_data_copy[match_data_copy['neutral'] == False]
    yearly_home_wins = non_neutral_matches.groupby(['year', 'home_team'])['home_win'].sum()
    yearly_away_wins = non_neutral_matches.groupby(['year', 'away_team'])['away_win'].sum()
    yearly_home_draws = non_neutral_matches.groupby(['year', 'home_team'])['draw'].sum()
    yearly_away_draws = non_neutral_matches.groupby(['year', 'away_team'])['draw'].sum()
    yearly_home_losses = non_neutral_matches.groupby(['year', 'home_team'])['away_win'].sum()
    yearly_away_losses = non_neutral_matches.groupby(['year', 'away_team'])['home_win'].sum()
    yearly_goals_scored_home = non_neutral_matches.groupby(['year', 'home_team'])['home_score'].sum()
    yearly_goals_scored_away = non_neutral_matches.groupby(['year', 'away_team'])['away_score'].sum()
    yearly_goals_conceded_home = non_neutral_matches.groupby(['year', 'home_team'])['away_score'].sum()
    yearly_goals_conceded_away = non_neutral_matches.groupby(['year', 'away_team'])['home_score'].sum()

    home_stats = pd.DataFrame({
        'home_wins': yearly_home_wins,
        'home_draws': yearly_home_draws,
        'home_losses': yearly_home_losses,
        'home_goals_scored': yearly_goals_scored_home,
        'home_goals_conceded': yearly_goals_conceded_home
    })
    home_stats.rename_axis(index={'home_team': 'team'}, inplace=True)
    away_stats = pd.DataFrame({
        'away_wins': yearly_away_wins,
        'away_draws': yearly_away_draws,
        'away_losses': yearly_away_losses,
        'away_goals_scored': yearly_goals_scored_away,
        'away_goals_conceded': yearly_goals_conceded_away
    })
    away_stats.rename_axis(index={'away_team': 'team'}, inplace=True)

    neutral_matches = match_data_copy[match_data_copy['neutral'] == True]
    yearly_neutral_home_wins = neutral_matches.groupby(['year', 'home_team'])['home_win'].sum()
    yearly_neutral_home_draws = neutral_matches.groupby(['year', 'home_team'])['draw'].sum()
    yearly_neutral_home_losses = neutral_matches.groupby(['year', 'home_team'])['away_win'].sum()
    yearly_neutral_goals_scored_home = neutral_matches.groupby(['year', 'home_team'])['home_score'].sum()
    yearly_neutral_goals_conceded_home = neutral_matches.groupby(['year', 'home_team'])['away_score'].sum()
    neutral_home = pd.DataFrame({
        'neutral_wins': yearly_neutral_home_wins,
        'neutral_draws': yearly_neutral_home_draws,
        'neutral_losses': yearly_neutral_home_losses,
        'neutral_goals_scored': yearly_neutral_goals_scored_home,
        'neutral_goals_conceded': yearly_neutral_goals_conceded_home
    })
    neutral_home.rename_axis(index={'home_team': 'team'}, inplace=True)

    yearly_neutral_away_wins = neutral_matches.groupby(['year', 'away_team'])['away_win'].sum()
    yearly_neutral_away_draws = neutral_matches.groupby(['year', 'away_team'])['draw'].sum()
    yearly_neutral_away_losses = neutral_matches.groupby(['year', 'away_team'])['home_win'].sum()
    yearly_neutral_goals_scored_away = neutral_matches.groupby(['year', 'away_team'])['away_score'].sum()
    yearly_neutral_goals_conceded_away = neutral_matches.groupby(['year', 'away_team'])['home_score'].sum()
    neutral_away = pd.DataFrame({
        'neutral_wins': yearly_neutral_away_wins,
        'neutral_draws': yearly_neutral_away_draws,
        'neutral_losses': yearly_neutral_away_losses,
        'neutral_goals_scored': yearly_neutral_goals_scored_away,
        'neutral_goals_conceded': yearly_neutral_goals_conceded_away
    })
    neutral_away.rename_axis(index={'away_team': 'team'}, inplace=True)
    #neutral_stats = pd.merge(neutral_home, neutral_away, on=['year', 'team'], how='outer')
    neutral_stats = pd.concat([neutral_home, neutral_away])
    neutral_stats = neutral_stats.groupby(['year', 'team']).sum()
    neutral_stats.fillna(0, inplace=True)
    neutral_stats.to_csv('temp_files/temp_neutral_stats.csv')
    home_away_stats = home_stats.merge(away_stats, on=['year', 'team'], how='outer')
    home_away_stats.fillna(0, inplace=True)
    home_away_stats.to_csv('temp_files/temp_home_away_stats.csv')
    team_stats = pd.merge(home_away_stats, neutral_stats, on=['year', 'team'], how='outer')
    team_stats.fillna(0, inplace=True)
    team_stats.to_csv('temp_files/temp_team_stats.csv')
    team_stats['total_goals_scored'] = (
            team_stats['home_goals_scored'] + team_stats['away_goals_scored'] + team_stats[
        'neutral_goals_scored'])
    team_stats['total_goals_conceded'] = (
            team_stats['home_goals_conceded'] + team_stats['away_goals_conceded'] +
            team_stats['neutral_goals_conceded'])
    team_stats['total_goal_difference'] = (
            team_stats['total_goals_scored'] - team_stats['total_goals_conceded'])
    team_stats['total_points'] = (
            team_stats['total_goals_scored'] * 3 + team_stats['total_goal_difference'] * 1)
    team_stats['total_wins'] = (
            team_stats['home_wins'] + team_stats['away_wins'] + team_stats[
        'neutral_wins'])
    team_stats['total_draws'] = (
            team_stats['home_draws'] + team_stats['away_draws'] + team_stats[
        'neutral_draws'])
    team_stats['total_loses'] = (
            team_stats['home_losses'] + team_stats['away_losses'] + team_stats[
        'neutral_losses'])
    team_stats['total_games_played'] = (
            team_stats['total_wins'] + team_stats['total_draws'] + team_stats[
        'total_loses'])
    team_stats['win_percentage'] = (
            team_stats['total_wins'] / team_stats['total_games_played'])
    team_stats['draw_percentage'] = (
            team_stats['total_draws'] / team_stats['total_games_played'])
    team_stats['loss_percentage'] = (
            team_stats['total_loses'] / team_stats['total_games_played'])

    team_stats.to_csv(csv_file_name)


def create_yearly_team_statistics_no_friendly(match_data):
    match_data_copy = match_data.copy()
    match_data_copy = match_data_copy[match_data_copy['tournament'] != 'Friendly']
    create_yearly_team_statistics(match_data_copy, 'teams_yearly_summary_no_friendly.csv')

def create_fifa_world_cup_stats(match_data):
    match_data_copy = match_data.copy()
    match_data_copy = match_data_copy[match_data_copy['tournament'] == 'FIFA World Cup']
    create_yearly_team_statistics(match_data_copy, 'fifa_world_cups_teams_summary.csv')

if __name__ == '__main__':
    create_fifa_world_cup_stats(match_data)