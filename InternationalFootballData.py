import pandas as pd
import matplotlib.pyplot as plt



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
    goals_summary.sort_values('total_goals', ascending=False)
    goals_summary.to_csv('teams_summary.csv')
    return goals_summary.sort_values('total_goals', ascending=False)

#def create_statistics_about_what_type_of_goals_were_scored(goals_data):

team_stats = create_team_statistic_summary(match_data)
team_stats.head(10)

create_combined_data_frame(match_data, goalscorers)