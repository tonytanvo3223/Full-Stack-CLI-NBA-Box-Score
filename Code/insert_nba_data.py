from BASENBA import Base, Team, Player, Game, ActiveLineup, Arena, OffensiveStats, DefensiveStats
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import logging
from datetime import date, time

logging.basicConfig()
logging.getLogger("sqlalchemy.engine").setLevel(logging.INFO)

# Set up database connection
engine = create_engine('sqlite:///NBA_BoxScore.db')
Base.metadata.create_all(engine)

Session = sessionmaker(bind=engine)
session = Session(expire_on_commit=False)

# List of teams to insert or update
teams_to_add = [
    # Eastern Conference - Atlantic Division
    {'team_id': 2, 'team_name': 'Boston Celtics', 'conf_name': 'Eastern', 'division_name': 'Atlantic', 
     'win_count': 61, 'loss_count': 21, 'win_percentage': 0.744, 'game_balance': 3},
    {'team_id': 3, 'team_name': 'New York Knicks', 'conf_name': 'Eastern', 'division_name': 'Atlantic', 
     'win_count': 51, 'loss_count': 31, 'win_percentage': 0.622, 'game_balance': 13},
    {'team_id': 13, 'team_name': 'Philadelphia 76ers', 'conf_name': 'Eastern', 'division_name': 'Atlantic', 
     'win_count': 24, 'loss_count': 58, 'win_percentage': 0.293, 'game_balance': 40},
    {'team_id': 12, 'team_name': 'Brooklyn Nets', 'conf_name': 'Eastern', 'division_name': 'Atlantic', 
     'win_count': 26, 'loss_count': 56, 'win_percentage': 0.317, 'game_balance': 38},
    {'team_id': 11, 'team_name': 'Toronto Raptors', 'conf_name': 'Eastern', 'division_name': 'Atlantic', 
     'win_count': 30, 'loss_count': 52, 'win_percentage': 0.366, 'game_balance': 34},
    
    # Eastern Conference - Central Division
    {'team_id': 1, 'team_name': 'Cleveland Cavaliers', 'conf_name': 'Eastern', 'division_name': 'Central', 
     'win_count': 64, 'loss_count': 18, 'win_percentage': 0.780, 'game_balance': 0},
    {'team_id': 5, 'team_name': 'Milwaukee Bucks', 'conf_name': 'Eastern', 'division_name': 'Central', 
     'win_count': 48, 'loss_count': 34, 'win_percentage': 0.585, 'game_balance': 16},
    {'team_id': 4, 'team_name': 'Indiana Pacers', 'conf_name': 'Eastern', 'division_name': 'Central', 
     'win_count': 50, 'loss_count': 32, 'win_percentage': 0.610, 'game_balance': 14},
    {'team_id': 9, 'team_name': 'Chicago Bulls', 'conf_name': 'Eastern', 'division_name': 'Central', 
     'win_count': 39, 'loss_count': 43, 'win_percentage': 0.476, 'game_balance': 25},
    {'team_id': 6, 'team_name': 'Detroit Pistons', 'conf_name': 'Eastern', 'division_name': 'Central', 
     'win_count': 44, 'loss_count': 38, 'win_percentage': 0.537, 'game_balance': 20},
    
    # Eastern Conference - Southeast Division
    {'team_id': 7, 'team_name': 'Orlando Magic', 'conf_name': 'Eastern', 'division_name': 'Southeast', 
     'win_count': 41, 'loss_count': 41, 'win_percentage': 0.500, 'game_balance': 23},
    {'team_id': 10, 'team_name': 'Miami Heat', 'conf_name': 'Eastern', 'division_name': 'Southeast', 
     'win_count': 37, 'loss_count': 45, 'win_percentage': 0.451, 'game_balance': 27},
    {'team_id': 8, 'team_name': 'Atlanta Hawks', 'conf_name': 'Eastern', 'division_name': 'Southeast', 
     'win_count': 40, 'loss_count': 42, 'win_percentage': 0.488, 'game_balance': 24},
    {'team_id': 14, 'team_name': 'Charlotte Hornets', 'conf_name': 'Eastern', 'division_name': 'Southeast', 
     'win_count': 19, 'loss_count': 63, 'win_percentage': 0.232, 'game_balance': 45},
    {'team_id': 15, 'team_name': 'Washington Wizards', 'conf_name': 'Eastern', 'division_name': 'Southeast', 
     'win_count': 18, 'loss_count': 64, 'win_percentage': 0.220, 'game_balance': 46},
    
    # Western Conference - Northwest Division
    {'team_id': 16, 'team_name': 'Oklahoma City Thunder', 'conf_name': 'Western', 'division_name': 'Northwest', 
     'win_count': 68, 'loss_count': 14, 'win_percentage': 0.829, 'game_balance': 0},
    {'team_id': 19, 'team_name': 'Denver Nuggets', 'conf_name': 'Western', 'division_name': 'Northwest', 
     'win_count': 50, 'loss_count': 32, 'win_percentage': 0.610, 'game_balance': 18},
    {'team_id': 21, 'team_name': 'Minnesota Timberwolves', 'conf_name': 'Western', 'division_name': 'Northwest', 
     'win_count': 49, 'loss_count': 33, 'win_percentage': 0.598, 'game_balance': 19},
    {'team_id': 30, 'team_name': 'Utah Jazz', 'conf_name': 'Western', 'division_name': 'Northwest', 
     'win_count': 17, 'loss_count': 65, 'win_percentage': 0.207, 'game_balance': 51},
    {'team_id': 27, 'team_name': 'Portland Trail Blazers', 'conf_name': 'Western', 'division_name': 'Northwest', 
     'win_count': 36, 'loss_count': 46, 'win_percentage': 0.439, 'game_balance': 32},
    
    # Western Conference - Pacific Division
    {'team_id': 20, 'team_name': 'LA Clippers', 'conf_name': 'Western', 'division_name': 'Pacific', 
     'win_count': 50, 'loss_count': 32, 'win_percentage': 0.610, 'game_balance': 18},
    {'team_id': 26, 'team_name': 'Phoenix Suns', 'conf_name': 'Western', 'division_name': 'Pacific', 
     'win_count': 36, 'loss_count': 46, 'win_percentage': 0.439, 'game_balance': 32},
    {'team_id': 24, 'team_name': 'Sacramento Kings', 'conf_name': 'Western', 'division_name': 'Pacific', 
     'win_count': 40, 'loss_count': 42, 'win_percentage': 0.488, 'game_balance': 28},
    {'team_id': 18, 'team_name': 'Los Angeles Lakers', 'conf_name': 'Western', 'division_name': 'Pacific', 
     'win_count': 50, 'loss_count': 32, 'win_percentage': 0.610, 'game_balance': 18},
    {'team_id': 22, 'team_name': 'Golden State Warriors', 'conf_name': 'Western', 'division_name': 'Pacific', 
     'win_count': 48, 'loss_count': 34, 'win_percentage': 0.585, 'game_balance': 20},
    
    # Western Conference - Southwest Division
    {'team_id': 25, 'team_name': 'Dallas Mavericks', 'conf_name': 'Western', 'division_name': 'Southwest', 
     'win_count': 39, 'loss_count': 43, 'win_percentage': 0.476, 'game_balance': 29},
    {'team_id': 29, 'team_name': 'New Orleans Pelicans', 'conf_name': 'Western', 'division_name': 'Southwest', 
     'win_count': 21, 'loss_count': 61, 'win_percentage': 0.256, 'game_balance': 47},
    {'team_id': 17, 'team_name': 'Houston Rockets', 'conf_name': 'Western', 'division_name': 'Southwest', 
     'win_count': 52, 'loss_count': 30, 'win_percentage': 0.634, 'game_balance': 16},
    {'team_id': 23, 'team_name': 'Memphis Grizzlies', 'conf_name': 'Western', 'division_name': 'Southwest', 
     'win_count': 48, 'loss_count': 34, 'win_percentage': 0.585, 'game_balance': 20},
    {'team_id': 28, 'team_name': 'San Antonio Spurs', 'conf_name': 'Western', 'division_name': 'Southwest', 
     'win_count': 34, 'loss_count': 48, 'win_percentage': 0.415, 'game_balance': 34}
]

# Insert or update teams
for team_data in teams_to_add:
    existing_team = session.query(Team).filter_by(team_id=team_data['team_id']).first()

    if existing_team:
        for key, value in team_data.items():
            setattr(existing_team, key, value)
        print(f"Updated team {team_data['team_name']}")
    else:
        new_team = Team(**team_data)
        session.add(new_team)
        print(f"Inserted new team {team_data['team_name']}")

# List of arenas to insert or update
arenas_to_add = [
    # Eastern Conference
    {'arena_id': 1, 'arena_name': 'Rocket Mortgage FieldHouse', 'team_id': 1, 'location': 'Cleveland, OH'},
    {'arena_id': 2, 'arena_name': 'TD Garden', 'team_id': 2, 'location': 'Boston, MA'},
    {'arena_id': 3, 'arena_name': 'Madison Square Garden', 'team_id': 3, 'location': 'New York, NY'},
    {'arena_id': 4, 'arena_name': 'Gainbridge Fieldhouse', 'team_id': 4, 'location': 'Indianapolis, IN'},
    {'arena_id': 5, 'arena_name': 'Fiserv Forum', 'team_id': 5, 'location': 'Milwaukee, WI'},
    {'arena_id': 6, 'arena_name': 'Little Caesars Arena', 'team_id': 6, 'location': 'Detroit, MI'},
    {'arena_id': 7, 'arena_name': 'Kia Center', 'team_id': 7, 'location': 'Orlando, FL'},
    {'arena_id': 8, 'arena_name': 'State Farm Arena', 'team_id': 8, 'location': 'Atlanta, GA'},
    {'arena_id': 9, 'arena_name': 'United Center', 'team_id': 9, 'location': 'Chicago, IL'},
    {'arena_id': 10, 'arena_name': 'Kaseya Center', 'team_id': 10, 'location': 'Miami, FL'},
    {'arena_id': 11, 'arena_name': 'Scotiabank Arena', 'team_id': 11, 'location': 'Toronto, ON'},
    {'arena_id': 12, 'arena_name': 'Barclays Center', 'team_id': 12, 'location': 'Brooklyn, NY'},
    {'arena_id': 13, 'arena_name': 'Wells Fargo Center', 'team_id': 13, 'location': 'Philadelphia, PA'},
    {'arena_id': 14, 'arena_name': 'Spectrum Center', 'team_id': 14, 'location': 'Charlotte, NC'},
    {'arena_id': 15, 'arena_name': 'Capital One Arena', 'team_id': 15, 'location': 'Washington, DC'},
    
    # Western Conference
    {'arena_id': 16, 'arena_name': 'Paycom Center', 'team_id': 16, 'location': 'Oklahoma City, OK'},
    {'arena_id': 17, 'arena_name': 'Toyota Center', 'team_id': 17, 'location': 'Houston, TX'},
    {'arena_id': 18, 'arena_name': 'Crypto.com Arena', 'team_id': 18, 'location': 'Los Angeles, CA'},
    {'arena_id': 19, 'arena_name': 'Ball Arena', 'team_id': 19, 'location': 'Denver, CO'},
    {'arena_id': 20, 'arena_name': 'Intuit Dome', 'team_id': 20, 'location': 'Inglewood, CA'},
    {'arena_id': 21, 'arena_name': 'Target Center', 'team_id': 21, 'location': 'Minneapolis, MN'},
    {'arena_id': 22, 'arena_name': 'Chase Center', 'team_id': 22, 'location': 'San Francisco, CA'},
    {'arena_id': 23, 'arena_name': 'FedExForum', 'team_id': 23, 'location': 'Memphis, TN'},
    {'arena_id': 24, 'arena_name': 'Golden 1 Center', 'team_id': 24, 'location': 'Sacramento, CA'},
    {'arena_id': 25, 'arena_name': 'American Airlines Center', 'team_id': 25, 'location': 'Dallas, TX'},
    {'arena_id': 26, 'arena_name': 'Footprint Center', 'team_id': 26, 'location': 'Phoenix, AZ'},
    {'arena_id': 27, 'arena_name': 'Moda Center', 'team_id': 27, 'location': 'Portland, OR'},
    {'arena_id': 28, 'arena_name': 'Frost Bank Center', 'team_id': 28, 'location': 'San Antonio, TX'},
    {'arena_id': 29, 'arena_name': 'Smoothie King Center', 'team_id': 29, 'location': 'New Orleans, LA'},
    {'arena_id': 30, 'arena_name': 'Delta Center', 'team_id': 30, 'location': 'Salt Lake City, UT'}
]

# Insert or update arenas
for arena_data in arenas_to_add:
    existing_arena = session.query(Arena).filter_by(arena_id=arena_data['arena_id']).first()

    if existing_arena:
        for key, value in arena_data.items():
            setattr(existing_arena, key, value)
        print(f"Updated arena {arena_data['arena_name']}")
    else:
        new_arena = Arena(**arena_data)
        session.add(new_arena)
        print(f"Inserted new arena {arena_data['arena_name']}")

# List of players to insert or update
players_to_add = [
    # Minnesota Timberwolves
    {'player_id': 1, 'player_name': 'Jaden McDaniels', 'team_id': 21, 'position': 'F', 'player_status': 'Active'},
    {'player_id': 2, 'player_name': 'Julius Randle', 'team_id': 21, 'position': 'F', 'player_status': 'Active'},
    {'player_id': 3, 'player_name': 'Rudy Gobert', 'team_id': 21, 'position': 'C', 'player_status': 'Active'},
    {'player_id': 4, 'player_name': 'Anthony Edwards', 'team_id': 21, 'position': 'G', 'player_status': 'Active'},
    {'player_id': 5, 'player_name': 'Mike Conley', 'team_id': 21, 'position': 'G', 'player_status': 'Active'},
    {'player_id': 6, 'player_name': 'Donte DiVincenzo', 'team_id': 21, 'position': 'G', 'player_status': 'Active'},
    {'player_id': 7, 'player_name': 'Naz Reid', 'team_id': 21, 'position': 'C', 'player_status': 'Active'},
    {'player_id': 8, 'player_name': 'Nickeil Alexander-Walker', 'team_id': 21, 'position': 'G', 'player_status': 'Active'},
    {'player_id': 9, 'player_name': 'Terrence Shannon Jr.', 'team_id': 21, 'position': 'G', 'player_status': 'Active'},
    {'player_id': 10, 'player_name': 'Jaylen Clark', 'team_id': 21, 'position': 'G', 'player_status': 'Active'},
    {'player_id': 11, 'player_name': 'Luka Garza', 'team_id': 21, 'position': 'C', 'player_status': 'Active'},
    {'player_id': 12, 'player_name': 'Joe Ingles', 'team_id': 21, 'position': 'F', 'player_status': 'Active'},
    {'player_id': 13, 'player_name': 'Leonard Miller', 'team_id': 21, 'position': 'F', 'player_status': 'Active'},
    {'player_id': 14, 'player_name': 'Josh Minott', 'team_id': 21, 'position': 'F', 'player_status': 'Active'},
    {'player_id': 15, 'player_name': 'Rob Dillingham', 'team_id': 21, 'position': 'G', 'player_status': 'Injured'},
    
    # Golden State Warriors
    {'player_id': 16, 'player_name': 'Buddy Hield', 'team_id': 22, 'position': 'G', 'player_status': 'Active'},    
    {'player_id': 17, 'player_name': 'Jimmy Butler III', 'team_id': 22, 'position': 'F', 'player_status': 'Active'},    
    {'player_id': 18, 'player_name': 'Draymond Green', 'team_id': 22, 'position': 'C', 'player_status': 'Active'},    
    {'player_id': 19, 'player_name': 'Brandin Podziemski', 'team_id': 22, 'position': 'G', 'player_status': 'Active'},    
    {'player_id': 20, 'player_name': 'Stephen Curry', 'team_id': 22, 'position': 'G', 'player_status': 'Active'},    
    {'player_id': 21, 'player_name': 'Moses Moody', 'team_id': 22, 'position': 'G', 'player_status': 'Active'},    
    {'player_id': 22, 'player_name': 'Gary Payton II', 'team_id': 22, 'position': 'G', 'player_status': 'Active'},    
    {'player_id': 23, 'player_name': 'Gui Santos', 'team_id': 22, 'position': 'F', 'player_status': 'Active'},    
    {'player_id': 24, 'player_name': 'Kevon Looney', 'team_id': 22, 'position': 'F', 'player_status': 'Active'},    
    {'player_id': 25, 'player_name': 'Quinten Post', 'team_id': 22, 'position': 'C', 'player_status': 'Active'},    
    {'player_id': 26, 'player_name': 'Jonathan Kuminga', 'team_id': 22, 'position': 'F', 'player_status': 'Active'},    
    {'player_id': 27, 'player_name': 'Pat Spencer', 'team_id': 22, 'position': 'G', 'player_status': 'Active'},    
    {'player_id': 28, 'player_name': 'Trayce Jackson-Davis', 'team_id': 22, 'position': 'F', 'player_status': 'Active'},    
    {'player_id': 29, 'player_name': 'Braxton Key', 'team_id': 22, 'position': 'F', 'player_status': 'Active'},    
    {'player_id': 30, 'player_name': 'Kevin Knox II', 'team_id': 22, 'position': 'F', 'player_status': 'Active'},         
]

# Insert or update players
for player_data in players_to_add:
    existing_player = session.query(Player).filter_by(player_id=player_data['player_id']).first()

    if existing_player:
        for key, value in player_data.items():
            setattr(existing_player, key, value)
        print(f"Updated player {player_data['player_name']}")
    else:
        new_player = Player(**player_data)
        session.add(new_player)
        print(f"Inserted new player {player_data['player_name']}")

# List of games to insert or update
games_to_add = [

    {'game_id': 1, 
     'home_team_id': 21, 
     'away_team_id': 22, 
     'game_time': time(20, 30), 
     'game_date': date(2025, 5, 6), 
     'streaming_platform': 'TNT / truTV / Max', 
     'is_active': False, 
     'game_period': 'Final', 
     'time_remaining': time(0, 0), 
     'winning_team_id': 22},

    {'game_id': 2, 
     'home_team_id': 21, 
     'away_team_id': 22, 
     'game_time': time(19, 30), 
     'game_date': date(2025, 5, 8), 
     'streaming_platform': 'TNT / truTV / Max', 
     'is_active': False, 
     'game_period': 'Final', 
     'time_remaining': time(0, 0), 
     'winning_team_id': 21},

    {'game_id': 3, 
     'home_team_id': 22, 
     'away_team_id': 21, 
     'game_time': time(19, 30), 
     'game_date': date(2025, 5, 10), 
     'streaming_platform': 'ABC', 
     'is_active': False, 
     'game_period': 'Not Started', 
     'time_remaining': time(0, 48), 
     'winning_team_id': None},

     {'game_id': 4, 
     'home_team_id': 22, 
     'away_team_id': 21, 
     'game_time': time(21, 00), 
     'game_date': date(2025, 5, 12), 
     'streaming_platform': 'ESPN', 
     'is_active': False, 
     'game_period': 'Not Started', 
     'time_remaining': time(0, 48), 
     'winning_team_id': None},
]

# Insert or update games
for game_data in games_to_add:
    existing_game = session.query(Game).filter_by(game_id=game_data['game_id']).first()

    if existing_game:
        for key, value in game_data.items():
            setattr(existing_game, key, value)
        print(f"Updated game {game_data['game_id']}")
    else:
        new_game = Game(**game_data)
        session.add(new_game)
        print(f"Inserted new game {game_data['game_id']}")

# List of active lineups to insert or update
lineups_to_add = [

    # Game 1
    {'team_id': 21, 'player_id': 1, 'game_id': 1, 'is_starter': True, 'on_court': False},
    {'team_id': 21, 'player_id': 2, 'game_id': 1, 'is_starter': True, 'on_court': False},
    {'team_id': 21, 'player_id': 3, 'game_id': 1, 'is_starter': True, 'on_court': False},
    {'team_id': 21, 'player_id': 4, 'game_id': 1, 'is_starter': True, 'on_court': False},
    {'team_id': 21, 'player_id': 5, 'game_id': 1, 'is_starter': True, 'on_court': False},
    {'team_id': 21, 'player_id': 6, 'game_id': 1, 'is_starter': False, 'on_court': False},
    {'team_id': 21, 'player_id': 7, 'game_id': 1, 'is_starter': False, 'on_court': False},
    {'team_id': 21, 'player_id': 8, 'game_id': 1, 'is_starter': False, 'on_court': False},
    {'team_id': 21, 'player_id': 9, 'game_id': 1, 'is_starter': False, 'on_court': False},
    {'team_id': 21, 'player_id': 10, 'game_id': 1, 'is_starter': False, 'on_court': False},
    {'team_id': 21, 'player_id': 11, 'game_id': 1, 'is_starter': False, 'on_court': False},
    {'team_id': 21, 'player_id': 12, 'game_id': 1, 'is_starter': False, 'on_court': False},
    {'team_id': 21, 'player_id': 13, 'game_id': 1, 'is_starter': False, 'on_court': False},
    {'team_id': 21, 'player_id': 14, 'game_id': 1, 'is_starter': False, 'on_court': False},

    {'team_id': 22, 'player_id': 16, 'game_id': 1, 'is_starter': True, 'on_court': False},
    {'team_id': 22, 'player_id': 17, 'game_id': 1, 'is_starter': True, 'on_court': False},
    {'team_id': 22, 'player_id': 18, 'game_id': 1, 'is_starter': True, 'on_court': False},
    {'team_id': 22, 'player_id': 19, 'game_id': 1, 'is_starter': True, 'on_court': False},
    {'team_id': 22, 'player_id': 20, 'game_id': 1, 'is_starter': True, 'on_court': False},
    {'team_id': 22, 'player_id': 21, 'game_id': 1, 'is_starter': False, 'on_court': False},
    {'team_id': 22, 'player_id': 22, 'game_id': 1, 'is_starter': False, 'on_court': False},
    {'team_id': 22, 'player_id': 23, 'game_id': 1, 'is_starter': False, 'on_court': False},
    {'team_id': 22, 'player_id': 24, 'game_id': 1, 'is_starter': False, 'on_court': False},
    {'team_id': 22, 'player_id': 25, 'game_id': 1, 'is_starter': False, 'on_court': False},
    {'team_id': 22, 'player_id': 26, 'game_id': 1, 'is_starter': False, 'on_court': False},
    {'team_id': 22, 'player_id': 26, 'game_id': 1, 'is_starter': False, 'on_court': False},
    {'team_id': 22, 'player_id': 28, 'game_id': 1, 'is_starter': False, 'on_court': False},
    {'team_id': 22, 'player_id': 29, 'game_id': 1, 'is_starter': False, 'on_court': False},
    {'team_id': 22, 'player_id': 30, 'game_id': 1, 'is_starter': False, 'on_court': False},

    # Game 2
    {'team_id': 21, 'player_id': 1, 'game_id': 2, 'is_starter': True, 'on_court': False},
    {'team_id': 21, 'player_id': 2, 'game_id': 2, 'is_starter': True, 'on_court': False},
    {'team_id': 21, 'player_id': 3, 'game_id': 2, 'is_starter': True, 'on_court': False},
    {'team_id': 21, 'player_id': 4, 'game_id': 2, 'is_starter': True, 'on_court': False},
    {'team_id': 21, 'player_id': 5, 'game_id': 2, 'is_starter': True, 'on_court': False},
    {'team_id': 21, 'player_id': 6, 'game_id': 2, 'is_starter': False, 'on_court': False},
    {'team_id': 21, 'player_id': 7, 'game_id': 2, 'is_starter': False, 'on_court': False},
    {'team_id': 21, 'player_id': 8, 'game_id': 2, 'is_starter': False, 'on_court': False},
    {'team_id': 21, 'player_id': 9, 'game_id': 2, 'is_starter': False, 'on_court': False},
    {'team_id': 21, 'player_id': 10, 'game_id': 2, 'is_starter': False, 'on_court': False},
    {'team_id': 21, 'player_id': 11, 'game_id': 2, 'is_starter': False, 'on_court': False},
    {'team_id': 21, 'player_id': 12, 'game_id': 2, 'is_starter': False, 'on_court': False},
    {'team_id': 21, 'player_id': 13, 'game_id': 2, 'is_starter': False, 'on_court': False},
    {'team_id': 21, 'player_id': 14, 'game_id': 2, 'is_starter': False, 'on_court': False},

    {'team_id': 22, 'player_id': 16, 'game_id': 2, 'is_starter': True, 'on_court': False},
    {'team_id': 22, 'player_id': 17, 'game_id': 2, 'is_starter': True, 'on_court': False},
    {'team_id': 22, 'player_id': 18, 'game_id': 2, 'is_starter': True, 'on_court': False},
    {'team_id': 22, 'player_id': 19, 'game_id': 2, 'is_starter': True, 'on_court': False},
    {'team_id': 22, 'player_id': 25, 'game_id': 2, 'is_starter': True, 'on_court': False},
    {'team_id': 22, 'player_id': 21, 'game_id': 2, 'is_starter': False, 'on_court': False},
    {'team_id': 22, 'player_id': 22, 'game_id': 2, 'is_starter': False, 'on_court': False},
    {'team_id': 22, 'player_id': 23, 'game_id': 2, 'is_starter': False, 'on_court': False},
    {'team_id': 22, 'player_id': 24, 'game_id': 2, 'is_starter': False, 'on_court': False},
    {'team_id': 22, 'player_id': 26, 'game_id': 2, 'is_starter': False, 'on_court': False},
    {'team_id': 22, 'player_id': 26, 'game_id': 2, 'is_starter': False, 'on_court': False},
    {'team_id': 22, 'player_id': 28, 'game_id': 2, 'is_starter': False, 'on_court': False},
    {'team_id': 22, 'player_id': 29, 'game_id': 2, 'is_starter': False, 'on_court': False},
    {'team_id': 22, 'player_id': 30, 'game_id': 2, 'is_starter': False, 'on_court': False},

    # Game 3
    {'team_id': 21, 'player_id': 1, 'game_id': 3, 'is_starter': True, 'on_court': False},
    {'team_id': 21, 'player_id': 2, 'game_id': 3, 'is_starter': True, 'on_court': False},
    {'team_id': 21, 'player_id': 3, 'game_id': 3, 'is_starter': True, 'on_court': False},
    {'team_id': 21, 'player_id': 4, 'game_id': 3, 'is_starter': True, 'on_court': False},
    {'team_id': 21, 'player_id': 5, 'game_id': 3, 'is_starter': True, 'on_court': False},
    {'team_id': 21, 'player_id': 6, 'game_id': 3, 'is_starter': False, 'on_court': False},
    {'team_id': 21, 'player_id': 7, 'game_id': 3, 'is_starter': False, 'on_court': False},
    {'team_id': 21, 'player_id': 8, 'game_id': 3, 'is_starter': False, 'on_court': False},
    {'team_id': 21, 'player_id': 9, 'game_id': 3, 'is_starter': False, 'on_court': False},
    {'team_id': 21, 'player_id': 10, 'game_id': 3, 'is_starter': False, 'on_court': False},
    {'team_id': 21, 'player_id': 11, 'game_id': 3, 'is_starter': False, 'on_court': False},
    {'team_id': 21, 'player_id': 12, 'game_id': 3, 'is_starter': False, 'on_court': False},
    {'team_id': 21, 'player_id': 13, 'game_id': 3, 'is_starter': False, 'on_court': False},
    {'team_id': 21, 'player_id': 14, 'game_id': 3, 'is_starter': False, 'on_court': False},

    {'team_id': 22, 'player_id': 16, 'game_id': 3, 'is_starter': True, 'on_court': False},
    {'team_id': 22, 'player_id': 17, 'game_id': 3, 'is_starter': True, 'on_court': False},
    {'team_id': 22, 'player_id': 18, 'game_id': 3, 'is_starter': True, 'on_court': False},
    {'team_id': 22, 'player_id': 19, 'game_id': 3, 'is_starter': True, 'on_court': False},
    {'team_id': 22, 'player_id': 25, 'game_id': 3, 'is_starter': True, 'on_court': False},
    {'team_id': 22, 'player_id': 21, 'game_id': 3, 'is_starter': False, 'on_court': False},
    {'team_id': 22, 'player_id': 22, 'game_id': 3, 'is_starter': False, 'on_court': False},
    {'team_id': 22, 'player_id': 23, 'game_id': 3, 'is_starter': False, 'on_court': False},
    {'team_id': 22, 'player_id': 24, 'game_id': 3, 'is_starter': False, 'on_court': False},
    {'team_id': 22, 'player_id': 26, 'game_id': 3, 'is_starter': False, 'on_court': False},
    {'team_id': 22, 'player_id': 26, 'game_id': 3, 'is_starter': False, 'on_court': False},
    {'team_id': 22, 'player_id': 28, 'game_id': 3, 'is_starter': False, 'on_court': False},
    {'team_id': 22, 'player_id': 29, 'game_id': 3, 'is_starter': False, 'on_court': False},
    {'team_id': 22, 'player_id': 30, 'game_id': 3, 'is_starter': False, 'on_court': False},
]

# Insert or update active lineups
for lineup_data in lineups_to_add:
    existing_lineup = session.query(ActiveLineup).filter_by(
        team_id=lineup_data['team_id'], 
        player_id=lineup_data['player_id'],
        game_id=lineup_data['game_id']
    ).first()

    if existing_lineup:
        for key, value in lineup_data.items():
            setattr(existing_lineup, key, value)
        print(f"Updated lineup for player {lineup_data['player_id']} in game {lineup_data['game_id']}")
    else:
        new_lineup = ActiveLineup(**lineup_data)
        session.add(new_lineup)
        print(f"Inserted new lineup for player {lineup_data['player_id']} in game {lineup_data['game_id']}")

# List of offensive stats to insert or update
offensive_stats_to_add = [
    # Game 1
    {'player_id': 1, 'game_id': 1, 'minutes': 38, 'points': 12, 'o_rebound': 3, 'assist': 1,
     'made_shots': 6, 'made_3': 0, 'made_free_throw': 0, 'turnover': 2,
     'total_shots_attempt': 12, 'total_3_attempt': 3, 'total_free_throw': 0},

    {'player_id': 2, 'game_id': 1, 'minutes': 31, 'points': 18, 'o_rebound': 1, 'assist': 6,
     'made_shots': 4, 'made_3': 0, 'made_free_throw': 10, 'turnover': 3,
     'total_shots_attempt': 11, 'total_3_attempt': 3, 'total_free_throw': 10},

    {'player_id': 3, 'game_id': 1, 'minutes': 26, 'points': 9, 'o_rebound': 4, 'assist': 0,
     'made_shots': 4, 'made_3': 0, 'made_free_throw': 1, 'turnover': 3,
     'total_shots_attempt': 7, 'total_3_attempt': 0, 'total_free_throw': 2},

    {'player_id': 4, 'game_id': 1, 'minutes': 42, 'points': 23, 'o_rebound': 1, 'assist': 2,
     'made_shots': 9, 'made_3': 1, 'made_free_throw': 4, 'turnover': 3,
     'total_shots_attempt': 22, 'total_3_attempt': 5, 'total_free_throw': 5},

    {'player_id': 5, 'game_id': 1, 'minutes': 22, 'points': 0, 'o_rebound': 0, 'assist': 5,
     'made_shots': 0, 'made_3': 0, 'made_free_throw': 0, 'turnover': 2,
     'total_shots_attempt': 5, 'total_3_attempt': 2, 'total_free_throw': 0},

    {'player_id': 6, 'game_id': 1, 'minutes': 33, 'points': 7, 'o_rebound': 1, 'assist': 4,
     'made_shots': 3, 'made_3': 1, 'made_free_throw': 0, 'turnover': 4,
     'total_shots_attempt': 11, 'total_3_attempt': 7, 'total_free_throw': 0},

    {'player_id': 7, 'game_id': 1, 'minutes': 34, 'points': 19, 'o_rebound': 2, 'assist': 1,
     'made_shots': 8, 'made_3': 3, 'made_free_throw': 0, 'turnover': 4,
     'total_shots_attempt': 14, 'total_3_attempt': 7, 'total_free_throw': 0},

    {'player_id': 8, 'game_id': 1, 'minutes': 14, 'points': 0, 'o_rebound': 0, 'assist': 0,
    'made_shots': 0, 'made_3': 0, 'made_free_throw': 0, 'turnover': 2,
    'total_shots_attempt': 3, 'total_3_attempt': 2, 'total_free_throw': 0},

    {'player_id': 9, 'game_id': 1, 'minutes': 2, 'points': 0, 'o_rebound': 0, 'assist': 0,
     'made_shots': 0, 'made_3': 0, 'made_free_throw': 0, 'turnover': 0,
     'total_shots_attempt': 1, 'total_3_attempt': 0, 'total_free_throw': 0},

    {'player_id': 10, 'game_id': 1, 'minutes': 0, 'points': 0, 'o_rebound': 0, 'assist': 0,
     'made_shots': 0, 'made_3': 0, 'made_free_throw': 0, 'turnover': 0,
     'total_shots_attempt': 0, 'total_3_attempt': 0, 'total_free_throw': 0},

    {'player_id': 11, 'game_id': 1, 'minutes': 0, 'points': 0, 'o_rebound': 0, 'assist': 0,
     'made_shots': 0, 'made_3': 0, 'made_free_throw': 0, 'turnover': 0,
     'total_shots_attempt': 0, 'total_3_attempt': 0, 'total_free_throw': 0},

    {'player_id': 12, 'game_id': 1, 'minutes': 0, 'points': 0, 'o_rebound': 0, 'assist': 0,
     'made_shots': 0, 'made_3': 0, 'made_free_throw': 0, 'turnover': 0,
     'total_shots_attempt': 0, 'total_3_attempt': 0, 'total_free_throw': 0},

    {'player_id': 13, 'game_id': 1, 'minutes': 0, 'points': 0, 'o_rebound': 0, 'assist': 0,
     'made_shots': 0, 'made_3': 0, 'made_free_throw': 0, 'turnover': 0,
     'total_shots_attempt': 0, 'total_3_attempt': 0, 'total_free_throw': 0},

    {'player_id': 14, 'game_id': 1, 'minutes': 0, 'points': 0, 'o_rebound': 0, 'assist': 0,
     'made_shots': 0, 'made_3': 0, 'made_free_throw': 0, 'turnover': 0,
     'total_shots_attempt': 0, 'total_3_attempt': 0, 'total_free_throw': 0},

    {'player_id': 15, 'game_id': 1, 'minutes': 0, 'points': 0, 'o_rebound': 0, 'assist': 0,
     'made_shots': 0, 'made_3': 0, 'made_free_throw': 0, 'turnover': 0,
     'total_shots_attempt': 0, 'total_3_attempt': 0, 'total_free_throw': 0},


    {'player_id': 16, 'game_id': 1, 'minutes': 40, 'points': 24, 'o_rebound': 4, 'assist': 3,
     'made_shots': 7, 'made_3': 5, 'made_free_throw': 5, 'turnover': 0,
     'total_shots_attempt': 19, 'total_3_attempt': 8, 'total_free_throw': 5},

    {'player_id': 17, 'game_id': 1, 'minutes': 41, 'points': 20, 'o_rebound': 7, 'assist': 8,
     'made_shots': 7, 'made_3': 2, 'made_free_throw': 4, 'turnover': 1,
     'total_shots_attempt': 20, 'total_3_attempt': 8, 'total_free_throw': 6},

    {'player_id': 18, 'game_id': 1, 'minutes': 35, 'points': 18, 'o_rebound': 0, 'assist': 6,
     'made_shots': 6, 'made_3': 4, 'made_free_throw': 2, 'turnover': 4,
     'total_shots_attempt': 13, 'total_3_attempt': 10, 'total_free_throw': 2},

    {'player_id': 19, 'game_id': 1, 'minutes': 29, 'points': 3, 'o_rebound': 0, 'assist': 3,
     'made_shots': 1, 'made_3': 1, 'made_free_throw': 0, 'turnover': 2,
     'total_shots_attempt': 7, 'total_3_attempt': 5, 'total_free_throw': 0},

    {'player_id': 20, 'game_id': 1, 'minutes': 13, 'points': 13, 'o_rebound': 0, 'assist': 1,
     'made_shots': 5, 'made_3': 3, 'made_free_throw': 0, 'turnover': 1,
     'total_shots_attempt': 9, 'total_3_attempt': 6, 'total_free_throw': 0},

    {'player_id': 21, 'game_id': 1, 'minutes': 9, 'points': 0, 'o_rebound': 0, 'assist': 0,
     'made_shots': 0, 'made_3': 0, 'made_free_throw': 0, 'turnover': 0,
     'total_shots_attempt': 4, 'total_3_attempt': 1, 'total_free_throw': 0},

    {'player_id': 22, 'game_id': 1, 'minutes': 26, 'points': 8, 'o_rebound': 2, 'assist': 5,
     'made_shots': 3, 'made_3': 2, 'made_free_throw': 0, 'turnover': 4,
     'total_shots_attempt': 4, 'total_3_attempt': 3, 'total_free_throw': 0},

    {'player_id': 23, 'game_id': 1, 'minutes': 4, 'points': 0, 'o_rebound': 0, 'assist': 0,
     'made_shots': 0, 'made_3': 0, 'made_free_throw': 0, 'turnover': 1,
     'total_shots_attempt': 0, 'total_3_attempt': 0, 'total_free_throw': 0},

    {'player_id': 24, 'game_id': 1, 'minutes': 14, 'points': 2, 'o_rebound': 2, 'assist': 0,
    'made_shots': 1, 'made_3': 0, 'made_free_throw': 0, 'turnover': 1,
    'total_shots_attempt': 2, 'total_3_attempt': 0, 'total_free_throw': 0},

    {'player_id': 25, 'game_id': 1, 'minutes': 7, 'points': 0, 'o_rebound': 0, 'assist': 1,
     'made_shots': 0, 'made_3': 0, 'made_free_throw': 0, 'turnover': 0,
     'total_shots_attempt': 0, 'total_3_attempt': 0, 'total_free_throw': 0},

    {'player_id': 26, 'game_id': 1, 'minutes': 14, 'points': 7, 'o_rebound': 1, 'assist': 1,
     'made_shots': 2, 'made_3': 1, 'made_free_throw': 2, 'turnover': 2,
     'total_shots_attempt': 5, 'total_3_attempt': 1, 'total_free_throw': 2},

    {'player_id': 27, 'game_id': 1, 'minutes': 11, 'points': 4, 'o_rebound': 2, 'assist': 2,
     'made_shots': 2, 'made_3': 0, 'made_free_throw': 0, 'turnover': 2,
     'total_shots_attempt': 4, 'total_3_attempt': 0, 'total_free_throw': 0},

    {'player_id': 28, 'game_id': 1, 'minutes': 0, 'points': 0, 'o_rebound': 0, 'assist': 0,
     'made_shots': 0, 'made_3': 0, 'made_free_throw': 0, 'turnover': 0,
     'total_shots_attempt': 0, 'total_3_attempt': 0, 'total_free_throw': 0},

    {'player_id': 29, 'game_id': 1, 'minutes': 0, 'points': 0, 'o_rebound': 0, 'assist': 0,
     'made_shots': 0, 'made_3': 0, 'made_free_throw': 0, 'turnover': 0,
     'total_shots_attempt': 0, 'total_3_attempt': 0, 'total_free_throw': 0},

    {'player_id': 30, 'game_id': 1, 'minutes': 0, 'points': 0, 'o_rebound': 0, 'assist': 0,
     'made_shots': 0, 'made_3': 0, 'made_free_throw': 0, 'turnover': 0,
     'total_shots_attempt': 0, 'total_3_attempt': 0, 'total_free_throw': 0},


    # Game 2
    {'player_id': 1, 'game_id': 2, 'minutes': 33, 'points': 16, 'o_rebound': 1, 'assist': 0,
     'made_shots': 7, 'made_3': 1, 'made_free_throw': 1,
     'turnover': 1, 'total_shots_attempt': 10, 'total_3_attempt': 2, 'total_free_throw': 2},
    
    {'player_id': 2, 'game_id': 2, 'minutes': 33, 'points': 24, 'o_rebound': 2, 'assist': 7,
     'made_shots': 10, 'made_3': 1, 'made_free_throw': 3,
     'turnover': 2, 'total_shots_attempt': 17, 'total_3_attempt': 4, 'total_free_throw': 3},
    
    {'player_id': 3, 'game_id': 2, 'minutes': 27, 'points': 5, 'o_rebound': 2, 'assist': 0,
     'made_shots': 2, 'made_3': 0, 'made_free_throw': 1,
     'turnover': 3, 'total_shots_attempt': 4, 'total_3_attempt': 0, 'total_free_throw': 4},
    
    {'player_id': 4, 'game_id': 2, 'minutes': 34, 'points': 20, 'o_rebound': 0, 'assist': 5,
     'made_shots': 6, 'made_3': 2, 'made_free_throw': 6,
     'turnover': 1, 'total_shots_attempt': 13, 'total_3_attempt': 4, 'total_free_throw': 8},
    
    {'player_id': 5, 'game_id': 2, 'minutes': 18, 'points': 6, 'o_rebound': 1, 'assist': 2,
     'made_shots': 2, 'made_3': 2, 'made_free_throw': 0,
     'turnover': 0, 'total_shots_attempt': 5, 'total_3_attempt': 4, 'total_free_throw': 1},
    
    {'player_id': 6, 'game_id': 2, 'minutes': 26, 'points': 9, 'o_rebound': 3, 'assist': 5,
     'made_shots': 3, 'made_3': 3, 'made_free_throw': 0,
     'turnover': 2, 'total_shots_attempt': 9, 'total_3_attempt': 8, 'total_free_throw': 0},
    
    {'player_id': 7, 'game_id': 2, 'minutes': 30, 'points': 11, 'o_rebound': 0, 'assist': 3,
     'made_shots': 4, 'made_3': 3, 'made_free_throw': 0,
     'turnover': 3, 'total_shots_attempt': 10, 'total_3_attempt': 8, 'total_free_throw': 0},
    
    {'player_id': 8, 'game_id': 2, 'minutes': 26, 'points': 20, 'o_rebound': 1, 'assist': 3,
     'made_shots': 7, 'made_3': 4, 'made_free_throw': 2,
     'turnover': 1, 'total_shots_attempt': 13, 'total_3_attempt': 6, 'total_free_throw': 3},
    
    {'player_id': 9, 'game_id': 2, 'minutes': 3, 'points': 2, 'o_rebound': 0, 'assist': 1,
     'made_shots': 1, 'made_3': 0, 'made_free_throw': 0,
     'turnover': 0, 'total_shots_attempt': 2, 'total_3_attempt': 0, 'total_free_throw': 0},
    
    {'player_id': 10, 'game_id': 2, 'minutes': 3, 'points': 0, 'o_rebound': 0, 'assist': 0,
     'made_shots': 0, 'made_3': 0, 'made_free_throw': 0, 'turnover': 1,
     'total_shots_attempt': 0, 'total_3_attempt': 0, 'total_free_throw': 0},

    {'player_id': 11, 'game_id': 2, 'minutes': 2, 'points': 0, 'o_rebound': 0, 'assist': 0,
     'made_shots': 0, 'made_3': 0, 'made_free_throw': 0, 'turnover': 0,
     'total_shots_attempt': 0, 'total_3_attempt': 0, 'total_free_throw': 0},

    {'player_id': 12, 'game_id': 2, 'minutes': 0, 'points': 0, 'o_rebound': 0, 'assist': 0,
     'made_shots': 0, 'made_3': 0, 'made_free_throw': 0, 'turnover': 0,
     'total_shots_attempt': 0, 'total_3_attempt': 0, 'total_free_throw': 0},

    {'player_id': 13, 'game_id': 2, 'minutes': 3, 'points': 2, 'o_rebound': 1, 'assist': 0,
     'made_shots': 1, 'made_3': 0, 'made_free_throw': 0, 'turnover': 0,
     'total_shots_attempt': 2, 'total_3_attempt': 0, 'total_free_throw': 0},

    {'player_id': 14, 'game_id': 2, 'minutes': 3, 'points': 2, 'o_rebound': 0, 'assist': 0,
     'made_shots': 1, 'made_3': 0, 'made_free_throw': 0, 'turnover': 0,
     'total_shots_attempt': 2, 'total_3_attempt': 1, 'total_free_throw': 0},

    {'player_id': 15, 'game_id': 2, 'minutes': 0, 'points': 0, 'o_rebound': 0, 'assist': 0,
     'made_shots': 0, 'made_3': 0, 'made_free_throw': 0, 'turnover': 0,
     'total_shots_attempt': 0, 'total_3_attempt': 0, 'total_free_throw': 0},


    {'player_id': 16, 'game_id': 2, 'minutes': 28, 'points': 15, 'o_rebound': 1, 'assist': 3,
     'made_shots': 5, 'made_3': 4, 'made_free_throw': 1, 'turnover': 2,
     'total_shots_attempt': 14, 'total_3_attempt': 9, 'total_free_throw': 1},

    {'player_id': 17, 'game_id': 2, 'minutes': 34, 'points': 17, 'o_rebound': 2, 'assist': 7,
     'made_shots': 6, 'made_3': 2, 'made_free_throw': 3, 'turnover': 2,
     'total_shots_attempt': 13, 'total_3_attempt': 4, 'total_free_throw': 5},

    {'player_id': 18, 'game_id': 2, 'minutes': 29, 'points': 9, 'o_rebound': 0, 'assist': 5,
     'made_shots': 3, 'made_3': 1, 'made_free_throw': 2, 'turnover': 1,
     'total_shots_attempt': 10, 'total_3_attempt': 6, 'total_free_throw': 2},

    {'player_id': 19, 'game_id': 2, 'minutes': 33, 'points': 11, 'o_rebound': 2, 'assist': 6,
     'made_shots': 4, 'made_3': 1, 'made_free_throw': 2, 'turnover': 2,
     'total_shots_attempt': 9, 'total_3_attempt': 4, 'total_free_throw': 2},

    {'player_id': 20, 'game_id': 2, 'minutes': 0, 'points': 0, 'o_rebound': 0, 'assist': 0,
     'made_shots': 0, 'made_3': 0, 'made_free_throw': 0, 'turnover': 0,
     'total_shots_attempt': 0, 'total_3_attempt': 0, 'total_free_throw': 0},

    {'player_id': 21, 'game_id': 2, 'minutes': 17, 'points': 3, 'o_rebound': 0, 'assist': 1,
     'made_shots': 1, 'made_3': 0, 'made_free_throw': 1, 'turnover': 2,
     'total_shots_attempt': 5, 'total_3_attempt': 4, 'total_free_throw': 4},

    {'player_id': 22, 'game_id': 2, 'minutes': 12, 'points': 0, 'o_rebound': 1, 'assist': 1,
     'made_shots': 0, 'made_3': 0, 'made_free_throw': 0, 'turnover': 0,
     'total_shots_attempt': 2, 'total_3_attempt': 1, 'total_free_throw': 0},

    {'player_id': 23, 'game_id': 2, 'minutes': 8, 'points': 0, 'o_rebound': 0, 'assist': 2,
     'made_shots': 0, 'made_3': 0, 'made_free_throw': 0, 'turnover': 1,
     'total_shots_attempt': 0, 'total_3_attempt': 0, 'total_free_throw': 0},

    {'player_id': 24, 'game_id': 2, 'minutes': 3, 'points': 0, 'o_rebound': 0, 'assist': 0,
     'made_shots': 0, 'made_3': 0, 'made_free_throw': 0, 'turnover': 0,
     'total_shots_attempt': 0, 'total_3_attempt': 0, 'total_free_throw': 0},

    {'player_id': 25, 'game_id': 2, 'minutes': 3, 'points': 0, 'o_rebound': 0, 'assist': 0,
     'made_shots': 0, 'made_3': 0, 'made_free_throw': 0, 'turnover': 0,
     'total_shots_attempt': 0, 'total_3_attempt': 0, 'total_free_throw': 0},

    {'player_id': 26, 'game_id': 2, 'minutes': 26, 'points': 18, 'o_rebound': 1, 'assist': 1,
     'made_shots': 8, 'made_3': 1, 'made_free_throw': 1, 'turnover': 2,
     'total_shots_attempt': 11, 'total_3_attempt': 3, 'total_free_throw': 4},

    {'player_id': 27, 'game_id': 2, 'minutes': 14, 'points': 0, 'o_rebound': 0, 'assist': 2,
     'made_shots': 0, 'made_3': 0, 'made_free_throw': 0, 'turnover': 1,
     'total_shots_attempt': 2, 'total_3_attempt': 0, 'total_free_throw': 0},

    {'player_id': 28, 'game_id': 2, 'minutes': 19, 'points': 15, 'o_rebound': 2, 'assist': 1,
     'made_shots': 6, 'made_3': 0, 'made_free_throw': 3, 'turnover': 1,
     'total_shots_attempt': 6, 'total_3_attempt': 0, 'total_free_throw': 5},

    {'player_id': 29, 'game_id': 2, 'minutes': 4, 'points': 2, 'o_rebound': 0, 'assist': 1,
     'made_shots': 1, 'made_3': 0, 'made_free_throw': 0, 'turnover': 0,
     'total_shots_attempt': 1, 'total_3_attempt': 0, 'total_free_throw': 0},

    {'player_id': 30, 'game_id': 2, 'minutes': 9, 'points': 3, 'o_rebound': 1, 'assist': 0,
     'made_shots': 1, 'made_3': 0, 'made_free_throw': 1, 'turnover': 0,
     'total_shots_attempt': 3, 'total_3_attempt': 1, 'total_free_throw': 2}
]

# Insert or update offensive stats
for stats_data in offensive_stats_to_add:
    existing_stats = session.query(OffensiveStats).filter_by(
        player_id=stats_data['player_id'], 
        game_id=stats_data['game_id']
    ).first()

    if existing_stats:
        for key, value in stats_data.items():
            setattr(existing_stats, key, value)
        print(f"Updated offensive stats for player {stats_data['player_id']} in game {stats_data['game_id']}")
    else:
        new_stats = OffensiveStats(**stats_data)
        session.add(new_stats)
        print(f"Inserted new offensive stats for player {stats_data['player_id']} in game {stats_data['game_id']}")

# List of defensive stats to insert or update
defensive_stats_to_add = [
    
# Game 1
{'player_id': 1, 'game_id': 1, 'minutes': 38, 'steal': 0, 'd_rebound': 1, 'block': 1, 'personal_foul': 2},
{'player_id': 2, 'game_id': 1, 'minutes': 31, 'steal': 0, 'd_rebound': 2, 'block': 0, 'personal_foul': 4},
{'player_id': 3, 'game_id': 1, 'minutes': 26, 'steal': 0, 'd_rebound': 7, 'block': 3, 'personal_foul': 3},
{'player_id': 4, 'game_id': 1, 'minutes': 42, 'steal': 3, 'd_rebound': 13, 'block': 1, 'personal_foul': 1},
{'player_id': 5, 'game_id': 1, 'minutes': 22, 'steal': 1, 'd_rebound': 1, 'block': 0, 'personal_foul': 2},
{'player_id': 6, 'game_id': 1, 'minutes': 33, 'steal': 1, 'd_rebound': 2, 'block': 0, 'personal_foul': 3},
{'player_id': 7, 'game_id': 1, 'minutes': 34, 'steal': 1, 'd_rebound': 3, 'block': 1, 'personal_foul': 4},
{'player_id': 8, 'game_id': 1, 'minutes': 14, 'steal': 1, 'd_rebound': 0, 'block': 0, 'personal_foul': 2},
{'player_id': 9, 'game_id': 1, 'minutes': 2, 'steal': 0, 'd_rebound': 0, 'block': 0, 'personal_foul': 0},
{'player_id': 10, 'game_id': 1, 'minutes': 0, 'steal': 0, 'd_rebound': 0, 'block': 0, 'personal_foul': 0},
{'player_id': 11, 'game_id': 1, 'minutes': 0, 'steal': 0, 'd_rebound': 0, 'block': 0, 'personal_foul': 0},
{'player_id': 12, 'game_id': 1, 'minutes': 0, 'steal': 0, 'd_rebound': 0, 'block': 0, 'personal_foul': 0},
{'player_id': 13, 'game_id': 1, 'minutes': 0, 'steal': 0, 'd_rebound': 0, 'block': 0, 'personal_foul': 0},
{'player_id': 14, 'game_id': 1, 'minutes': 0, 'steal': 0, 'd_rebound': 0, 'block': 0, 'personal_foul': 0},
{'player_id': 15, 'game_id': 1, 'minutes': 0, 'steal': 0, 'd_rebound': 0, 'block': 0, 'personal_foul': 0},
{'player_id': 16, 'game_id': 1, 'minutes': 40, 'steal': 1, 'd_rebound': 4, 'block': 0, 'personal_foul': 0},
{'player_id': 17, 'game_id': 1, 'minutes': 42, 'steal': 2, 'd_rebound': 4, 'block': 0, 'personal_foul': 0},
{'player_id': 18, 'game_id': 1, 'minutes': 34, 'steal': 2, 'd_rebound': 8, 'block': 0, 'personal_foul': 5},
{'player_id': 19, 'game_id': 1, 'minutes': 29, 'steal': 0, 'd_rebound': 8, 'block': 0, 'personal_foul': 1},
{'player_id': 20, 'game_id': 1, 'minutes': 13, 'steal': 0, 'd_rebound': 1, 'block': 0, 'personal_foul': 0},
{'player_id': 21, 'game_id': 1, 'minutes': 9, 'steal': 0, 'd_rebound': 0, 'block': 0, 'personal_foul': 0},
{'player_id': 22, 'game_id': 1, 'minutes': 26, 'steal': 1, 'd_rebound': 3, 'block': 0, 'personal_foul': 4},
{'player_id': 23, 'game_id': 1, 'minutes': 4, 'steal': 0, 'd_rebound': 0, 'block': 0, 'personal_foul': 1},
{'player_id': 24, 'game_id': 1, 'minutes': 15, 'steal': 2, 'd_rebound': 4, 'block': 1, 'personal_foul': 3},
{'player_id': 25, 'game_id': 1, 'minutes': 7, 'steal': 0, 'd_rebound': 1, 'block': 0, 'personal_foul': 0},
{'player_id': 26, 'game_id': 1, 'minutes': 14, 'steal': 0, 'd_rebound': 0, 'block': 1, 'personal_foul': 2},
{'player_id': 27, 'game_id': 1, 'minutes': 11, 'steal': 2, 'd_rebound': 0, 'block': 0, 'personal_foul': 2},
{'player_id': 28, 'game_id': 1, 'minutes': 0, 'steal': 0, 'd_rebound': 0, 'block': 0, 'personal_foul': 0},
{'player_id': 29, 'game_id': 1, 'minutes': 0, 'steal': 0, 'd_rebound': 0, 'block': 0, 'personal_foul': 0},
{'player_id': 30, 'game_id': 1, 'minutes': 0, 'steal': 0, 'd_rebound': 0, 'block': 0, 'personal_foul': 0},

# Game 2
{'player_id': 1, 'game_id': 2, 'minutes': 38, 'steal': 1, 'd_rebound': 1, 'block': 0, 'personal_foul': 2},
{'player_id': 2, 'game_id': 2, 'minutes': 33, 'steal': 0, 'd_rebound': 5, 'block': 0, 'personal_foul': 3},
{'player_id': 3, 'game_id': 2, 'minutes': 27, 'steal': 0, 'd_rebound': 7, 'block': 0, 'personal_foul': 4},
{'player_id': 4, 'game_id': 2, 'minutes': 34, 'steal': 3, 'd_rebound': 13, 'block': 1, 'personal_foul': 1},
{'player_id': 5, 'game_id': 2, 'minutes': 18, 'steal': 1, 'd_rebound': 1, 'block': 1, 'personal_foul': 0},
{'player_id': 6, 'game_id': 2, 'minutes': 26, 'steal': 1, 'd_rebound': 2, 'block': 0, 'personal_foul': 3},
{'player_id': 7, 'game_id': 2, 'minutes': 30, 'steal': 1, 'd_rebound': 3, 'block': 1, 'personal_foul': 4},
{'player_id': 8, 'game_id': 2, 'minutes': 26, 'steal': 0, 'd_rebound': 1, 'block': 1, 'personal_foul': 2},
{'player_id': 9, 'game_id': 2, 'minutes': 3, 'steal': 0, 'd_rebound': 0, 'block': 0, 'personal_foul': 0},
{'player_id': 10, 'game_id': 2, 'minutes': 3, 'steal': 0, 'd_rebound': 1, 'block': 0, 'personal_foul': 1},
{'player_id': 11, 'game_id': 2, 'minutes': 3, 'steal': 0, 'd_rebound': 0, 'block': 0, 'personal_foul': 1},
{'player_id': 12, 'game_id': 2, 'minutes': 0, 'steal': 0, 'd_rebound': 0, 'block': 0, 'personal_foul': 0},
{'player_id': 13, 'game_id': 2, 'minutes': 3, 'steal': 0, 'd_rebound': 0, 'block': 0, 'personal_foul': 0},
{'player_id': 14, 'game_id': 2, 'minutes': 2, 'steal': 0, 'd_rebound': 0, 'block': 0, 'personal_foul': 1},
{'player_id': 15, 'game_id': 2, 'minutes': 0, 'steal': 0, 'd_rebound': 0, 'block': 0, 'personal_foul': 0},

{'player_id': 16, 'game_id': 2, 'minutes': 40, 'steal': 1, 'd_rebound': 1, 'block': 0, 'personal_foul': 0},
{'player_id': 17, 'game_id': 2, 'minutes': 42, 'steal': 2, 'd_rebound': 4, 'block': 1, 'personal_foul': 1},
{'player_id': 18, 'game_id': 2, 'minutes': 34, 'steal': 2, 'd_rebound': 8, 'block': 2, 'personal_foul': 5},
{'player_id': 19, 'game_id': 2, 'minutes': 29, 'steal': 3, 'd_rebound': 8, 'block': 0, 'personal_foul': 2},
{'player_id': 20, 'game_id': 2, 'minutes': 13, 'steal': 1, 'd_rebound': 1, 'block': 0, 'personal_foul': 1},
{'player_id': 21, 'game_id': 2, 'minutes': 9, 'steal': 0, 'd_rebound': 0, 'block': 0, 'personal_foul': 0},
{'player_id': 22, 'game_id': 2, 'minutes': 26, 'steal': 4, 'd_rebound': 3, 'block': 1, 'personal_foul': 1},
{'player_id': 23, 'game_id': 2, 'minutes': 4, 'steal': 0, 'd_rebound': 0, 'block': 0, 'personal_foul': 1},
{'player_id': 24, 'game_id': 2, 'minutes': 15, 'steal': 2, 'd_rebound': 4, 'block': 1, 'personal_foul': 3},
{'player_id': 25, 'game_id': 2, 'minutes': 7, 'steal': 1, 'd_rebound': 1, 'block': 0, 'personal_foul': 0},
{'player_id': 26, 'game_id': 2, 'minutes': 14, 'steal': 1, 'd_rebound': 0, 'block': 1, 'personal_foul': 2},
{'player_id': 27, 'game_id': 2, 'minutes': 11, 'steal': 0, 'd_rebound': 0, 'block': 0, 'personal_foul': 2},
{'player_id': 28, 'game_id': 2, 'minutes': 14, 'steal': 1, 'd_rebound': 4, 'block': 1, 'personal_foul': 4},
{'player_id': 29, 'game_id': 2, 'minutes': 0, 'steal': 0, 'd_rebound': 2, 'block': 0, 'personal_foul': 2},
{'player_id': 30, 'game_id': 2, 'minutes': 0, 'steal': 0, 'd_rebound': 0, 'block': 0, 'personal_foul': 0}

]

# Insert or update defensive stats
for stats_data in defensive_stats_to_add:
    existing_stats = session.query(DefensiveStats).filter_by(
        player_id=stats_data['player_id'], 
        game_id=stats_data['game_id']
    ).first()

    if existing_stats:
        for key, value in stats_data.items():
            setattr(existing_stats, key, value)
        print(f"Updated defensive stats for player {stats_data['player_id']} in game {stats_data['game_id']}")
    else:
        new_stats = DefensiveStats(**stats_data)
        session.add(new_stats)
        print(f"Inserted new defensive stats for player {stats_data['player_id']} in game {stats_data['game_id']}")

# Commit all changes
session.commit()
print("All changes committed to database.")