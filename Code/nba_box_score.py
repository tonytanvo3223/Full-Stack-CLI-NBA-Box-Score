from sqlalchemy import create_engine, func
from sqlalchemy.orm import sessionmaker
from datetime import datetime, time
from BASENBA import Game, Team, Player, OffensiveStats, DefensiveStats
from tabulate import tabulate

import logging
logging.basicConfig()
logging.getLogger("sqlalchemy.engine").setLevel(logging.INFO)

import logging
logging.getLogger("sqlalchemy.engine").setLevel(logging.WARNING)

import warnings
from sqlalchemy.exc import SAWarning
warnings.filterwarnings("ignore", category=SAWarning)

engine = create_engine('sqlite:///NBA_BoxScore.db')
Session = sessionmaker(bind=engine)
session = Session()

def main_menu():
    while True:

        print("\n--- NBA Game Tracker System ---")
        print("1. Search for game")
        print("2. Insert new game")
        print("3. Insert new game stats")
        print("4. Add / Update / Remove Player")
        print("5. Exit")
        choice = input("Enter your choice (1-5): ")

        if choice == '1':
            search_game_menu()
        elif choice == '2':
            insert_game()
        elif choice == '3':
            insert_game_stats()
        elif choice == '4':
            player_management_menu()
        elif choice == '5':
            break
        else:
             pass

from tabulate import tabulate
from sqlalchemy import func

def get_team_score(game_id, team_id):
    return session.query(func.sum(OffensiveStats.points)).join(Player).filter(
        OffensiveStats.game_id == game_id,
        Player.team_id == team_id
    ).scalar() or 0

def search_game_menu():

    print("\n--- Search Game ---")

    print("1. Search by date")

    print("2. Search by team")

    sub_choice = input("Enter your choice (1-2): ")



    if sub_choice == '1':

        date_input = input("Enter game date (YYYY-MM-DD): ").strip()

        games = session.query(Game).filter_by(game_date=date_input).all()



        if not games:

            print("No games found.")

            return



        table = []

        for game in games:

            home = session.query(Team).get(game.home_team_id)

            away = session.query(Team).get(game.away_team_id)



            if game.game_period == "Final":

                home_pts = get_team_score(game.game_id, home.team_id)

                away_pts = get_team_score(game.game_id, away.team_id)

                score = f"{home_pts}-{away_pts}"

            else:

                score = "-"

            time_display = game.game_time.strftime("%H:%M") if game.game_time else ""


            table.append([

                game.game_id, score, home.team_name, away.team_name,

                game.streaming_platform, game.game_date, time_display

            ])



        headers = ["Game ID", "Score", "Home Team", "Away Team", "Platform", "Date", " Tip-Off Time"]

        print("\n--- Game Schedule ---")

        print(tabulate(table, headers=headers, tablefmt="grid"))



        try:

            selected_id = int(input("\nEnter a Game ID to view stats: "))

            selected_game = session.query(Game).get(selected_id)



            if not selected_game:

                print("Game not found.")

                return



            if selected_game.game_period == "Not Started":

                print("This game has not started yet. No player stats available.")

                return

            else:

                display_games([selected_game])



        except ValueError:

            print("Invalid input.")



    elif sub_choice == '2':

        team_name = input("Enter team name: ").strip()

        team = session.query(Team).filter_by(team_name=team_name).first()

        if not team:

            print("Team not found.")

            return



        games = session.query(Game).filter(

            (Game.home_team_id == team.team_id) | (Game.away_team_id == team.team_id)

        ).all()



        if not games:

            print("No games found.")

            return



        table = []

        for game in games:

            home = session.query(Team).get(game.home_team_id)

            away = session.query(Team).get(game.away_team_id)



            if game.game_period == "Final":

                home_pts = get_team_score(game.game_id, home.team_id)

                away_pts = get_team_score(game.game_id, away.team_id)

                score = f"{home_pts}-{away_pts}"

            else:

                score = "-"

            time_display = game.game_time.strftime("%H:%M") if game.game_time else ""



            table.append([

                game.game_id, score, home.team_name, away.team_name,

                game.streaming_platform, game.game_date, time_display

            ])



        headers = ["Game ID", "Score", "Home Team", "Away Team", "Platform", "Date", "Tip-Off Time"]

        print("\n--- Game Schedule ---")

        print(tabulate(table, headers=headers, tablefmt="grid"))



        try:

            selected_id = int(input("\nEnter a Game ID to view stats: "))

            selected_game = session.query(Game).get(selected_id)



            if not selected_game:

                print("Game not found.")

                return



            if selected_game.game_period == "Not Started":

                print("This game has not started yet. No player stats available.")

                return

            else:

                display_games([selected_game])



        except ValueError:

            print("Invalid input.")

    else:

        print("Invalid choice.")
def display_games(games):
    for game in games:
        for team_id in [game.home_team_id, game.away_team_id]:
            team = session.query(Team).get(team_id)
            players = session.query(Player).filter_by(team_id=team_id).all()

            headers = ["Player", "PTS", "AST", "REB", "STL", "BLK", "TO", "PF", "FG%", "FT%", "3P%"]
            table = []

            totals = {
                'pts': 0, 'ast': 0, 'reb': 0, 'stl': 0, 'blk': 0, 'to': 0, 'pf': 0,
                'fg_made': 0, 'fg_att': 0, 'ft_made': 0, 'ft_att': 0, 'tp_made': 0, 'tp_att': 0
            }

            for player in players:
                off = session.query(OffensiveStats).filter_by(player_id=player.player_id, game_id=game.game_id).first()
                defn = session.query(DefensiveStats).filter_by(player_id=player.player_id, game_id=game.game_id).first()

                if not off and not defn:
                    continue

                pts = off.points if off else 0
                ast = off.assist if off else 0
                oreb = off.o_rebound if off else 0
                dreb = defn.d_rebound if defn else 0
                reb = oreb + dreb
                stl = defn.steal if defn else 0
                blk = defn.block if defn else 0
                to = off.turnover if off else 0
                pf = defn.personal_foul if defn else 0
                fg_made = off.made_shots if off else 0
                fg_att = off.total_shots_attempt if off else 0
                ft_made = off.made_free_throw if off else 0
                ft_att = off.total_free_throw if off else 0
                tp_made = off.made_3 if off else 0
                tp_att = off.total_3_attempt if off else 0

                fg_percent = (fg_made / fg_att * 100) if fg_att else 0
                ft_percent = (ft_made / ft_att * 100) if ft_att else 0
                tp_percent = (tp_made / tp_att * 100) if tp_att else 0

                table.append([
                    player.player_name, pts, ast, reb, stl, blk, to, pf,
                    f"{fg_percent:.1f}%", f"{ft_percent:.1f}%", f"{tp_percent:.1f}%"
                ])

                totals['pts'] += pts
                totals['ast'] += ast
                totals['reb'] += reb
                totals['stl'] += stl
                totals['blk'] += blk
                totals['to'] += to
                totals['pf'] += pf
                totals['fg_made'] += fg_made
                totals['fg_att'] += fg_att
                totals['ft_made'] += ft_made
                totals['ft_att'] += ft_att
                totals['tp_made'] += tp_made
                totals['tp_att'] += tp_att

            if table:
                fg_pct = (totals['fg_made'] / totals['fg_att'] * 100) if totals['fg_att'] else 0
                ft_pct = (totals['ft_made'] / totals['ft_att'] * 100) if totals['ft_att'] else 0
                tp_pct = (totals['tp_made'] / totals['tp_att'] * 100) if totals['tp_att'] else 0

                table.append([
                    "TEAM TOTALS", totals['pts'], totals['ast'], totals['reb'],
                    totals['stl'], totals['blk'], totals['to'], totals['pf'],
                    f"{fg_pct:.1f}%", f"{ft_pct:.1f}%", f"{tp_pct:.1f}%"
                ])

                print(f"\n{team.team_name}")
                print(tabulate(table, headers=headers, tablefmt="grid"))
def player_management_menu():
    sub_choice = input("Enter your choice (1-3): ")

    if sub_choice == '1':
        create_new_player()
    elif sub_choice == '2':
        update_player()
    elif sub_choice == '3':
        remove_player()
    else:
         pass

def create_new_player():
    last_player = session.query(Player).order_by(Player.player_id.desc()).first()
    next_player_id = (last_player.player_id + 1) if last_player else 0

    name = input("Player name: ")
    team_id = int(input("Team ID: "))
    position = input("Position: ")
    status = input("Player status (e.g., Active, Injured): ")

    player = Player(
        player_id=next_player_id,
        player_name=name,
        team_id=team_id,
        position=position,
        player_status=status
    )
    session.add(player)
    session.commit()

def update_player():
    try:
        player_id = int(input("Enter Player ID to update: "))
        player = session.query(Player).get(player_id)
        if not player:
            return

        new_name = input("New name (leave blank to keep current): ")
        if new_name:
            player.player_name = new_name

        new_team = input("New team ID (leave blank to keep current): ")
        if new_team:
            player.team_id = int(new_team)

        new_position = input("New position (leave blank to keep current): ")
        if new_position:
            player.position = new_position

        new_status = input("New status (leave blank to keep current): ")
        if new_status:
            player.player_status = new_status

        session.commit()
    except ValueError:
        pass

def remove_player():
    try:
        player_id = int(input("Enter Player ID to remove: "))
        player = session.query(Player).get(player_id)
        if not player:
            return

        confirm = input(f"Are you sure you want to delete {player.player_name}? (y/n): ").lower()
        if confirm == 'y':
            session.delete(player)
            session.commit()
        else:
            pass
    except ValueError:
        pass

def insert_game():
    home_team = int(input("Home team ID: "))
    away_team = int(input("Away team ID: "))
    date = input("Game date (YYYY-MM-DD): ")
    time_str = input("Game time (HH:MM): ")
    platform = input("Streaming platform: ")

    while True:
        period = input("Game period (Final or Not Started): ").strip().title()
        if period in ["Final", "Not Started"]:
            break
        else:
             pass

    game = Game(
        home_team_id=home_team,
        away_team_id=away_team,
        game_date=datetime.strptime(date, "%Y-%m-%d").date(),
        game_time=datetime.strptime(time_str, "%H:%M").time(),
        streaming_platform=platform,
        is_active=(period != "Final"),
        game_period=period,
        time_remaining=time(0, 0),
        winning_team_id=None
    )
    session.add(game)
    session.commit()

def insert_game_stats():
    game_id = int(input("Game ID: "))
    player_id = int(input("Player ID: "))

    off = OffensiveStats(
        player_id=player_id,
        game_id=game_id,
        minutes=int(input("Minutes played: ")),
        points=int(input("Points: ")),
        o_rebound=int(input("Offensive Rebounds: ")),
        assist=int(input("Assists: ")),
        made_shots=int(input("Made Shots: ")),
        made_3=int(input("Made 3-pt: ")),
        made_free_throw=int(input("Made Free Throws: ")),
        turnover=int(input("Turnovers: ")),
        total_shots_attempt=int(input("Total Shots Attempted: ")),
        total_3_attempt=int(input("Total 3-pt Attempted: ")),
        total_free_throw=int(input("Total Free Throws Attempted: "))
    )

    defn = DefensiveStats(
        player_id=player_id,
        game_id=game_id,
        minutes=int(input("Minutes played (again): ")),
        steal=int(input("Steals: ")),
        d_rebound=int(input("Defensive Rebounds: ")),
        block=int(input("Blocks: ")),
        personal_foul=int(input("Personal Fouls: "))
    )

    session.add_all([off, defn])
    session.commit()

# The rest includes search_game_menu, display_games, get_team_score from the last script
# (Omitted here for brevity since it's already been generated above.)


if __name__ == "__main__":
    main_menu()