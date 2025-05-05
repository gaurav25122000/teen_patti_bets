class colors:
    """Colors class:reset all colors with colors.reset; two
    sub classes fg for foreground
    and bg for background; use as colors.subclass.colorname.
    i.e. colors.fg.red or colors.bg.green
    Also, the generic bold, disable,
    underline, reverse, strike through,
    and invisible work with the main class i.e. colors.bold"""

    reset = "\033[0m"
    bold = "\033[01m"
    disable = "\033[02m"
    underline = "\033[04m"
    reverse = "\033[07m"
    strikethrough = "\033[09m"
    invisible = "\033[08m"

    class fg:
        black = "\033[30m"
        red = "\033[31m"
        green = "\033[32m"
        orange = "\033[33m"
        blue = "\033[34m"
        purple = "\033[35m"
        cyan = "\033[36m"
        lightgrey = "\033[37m"
        darkgrey = "\033[90m"
        lightred = "\033[91m"
        lightgreen = "\033[92m"
        yellow = "\033[93m"
        lightblue = "\033[94m"
        pink = "\033[95m"
        lightcyan = "\033[96m"

    class bg:
        black = "\033[40m"
        red = "\033[41m"
        green = "\033[42m"
        orange = "\033[43m"
        blue = "\033[44m"
        purple = "\033[45m"
        cyan = "\033[46m"
        lightgrey = "\033[47m"


# This script is used to track the bets in each round of a teen patti game
import json
import os.path
import sys
from prettytable import PrettyTable

# --- Constants ---
FOLD = 0
END_BETTING = -1
SHOW = -2
WINNING_HISTORY_PATH = "winning_history.json"

players = {}
print(
    colors.fg.lightred
    + "Don't Fiddle with the game else the game will fiddle with you!! "
    + colors.reset
)
winning_history_path = "winning_history.json"
check_file = os.path.isfile(winning_history_path)
load_game_input = "n"
if check_file:
    load_game_input = input("We found saved balances, do you want to load them? (y/n) ")
last_winner_id = None  # Keep track of the last winner


def check_return_int_conversion(string):
    if string == "-1":
        return -1
    if string == "-2":  # Adding Show command
        return -2
    if string.isnumeric():
        return int(string)
    else:
        print(
            colors.bold + colors.fg.red + "Invalid Input!!, Ending Game" + colors.reset
        )
        exit(0)


def check_yes_no(yes_no_ip):
    """Checks if the input string is 'y' (case-insensitive)."""
    if yes_no_ip.lower() == "y":
        return True
    else:
        return False


def save_data():
    with open(winning_history_path, "w", encoding="utf-8") as json_file:
        json.dump(players, json_file)
        print(colors.fg.green + "\nPlayer Data saved!\n" + colors.reset)


def get_colored_input(
    prompt, prompt_color=colors.fg.lightcyan, input_color=colors.fg.lightgreen
):
    """Gets input from the user with specified colors."""
    print(prompt_color + prompt + input_color, end="")
    return input()


def print_colored(message, color=colors.reset):
    """Prints a message with the specified color."""
    print(color + message + colors.reset)


def input_players():
    """Gets initial player information from the user."""
    global players  # Modifies the global players dict
    num = 0
    while num < 2:
        # Pass the prompt string directly to get_colored_input
        num_str = get_colored_input("Enter number of players: ")
        num = check_return_int_conversion(num_str)
        if num < 2:
            # Use the print_colored helper
            print_colored(
                "No no, do it again, this time atleast 2 players.", colors.fg.lightred
            )
    for i in range(num):
        player_name = get_colored_input(f"\nEnter name of Player number {i + 1} ")
        while True:
            balance_str = get_colored_input(f"Enter balance of {player_name.title()} ")
            player_balance = check_return_int_conversion(balance_str)
            if player_balance is not None and player_balance >= 0:  # Basic validation
                break
            print_colored(
                "Invalid balance, please enter a non-negative number.", colors.fg.red
            )
        players[i + 1] = {"id": i + 1, "balance": player_balance, "name": player_name}
    print_player_balances()


def get_new_player_number():
    """Calculates the next available player ID."""
    return list(players)[-1] + 1


def add_remove_player():
    """Handles adding or removing players between rounds."""
    add_remove_player_check = check_return_int_conversion(
        input(
            colors.fg.lightred
            + "\nDo you want to add(1)/remove(2) player?\nEnter any other number to not take any action: "
            + colors.fg.lightgreen
        )
    )
    while add_remove_player_check == 1:
        player_number = get_new_player_number()
        player_name = get_colored_input(
            f"\nEnter name of Player number {player_number} "
        )
        while True:
            balance_str = get_colored_input(f"Enter balance of {player_name.title()} ")
            player_balance = check_return_int_conversion(balance_str)
            if player_balance is not None and player_balance >= 0:
                break
            print_colored(
                "Invalid balance, please enter a non-negative number.", colors.fg.red
            )
        players[player_number] = {
            "id": player_number,
            "balance": player_balance,
            "name": player_name,
        }
        print_colored(
            f"\nPlayer {player_name.title()} added with ID {player_number}.",
            colors.fg.green,
        )
        add_remove_player_check = check_return_int_conversion(
            input(
                colors.fg.lightred
                + "\nDo you want to add another player? \nEnter 1 for yes, 2 for player deletion, any other number for quitting "
                + colors.fg.lightgreen
            )
        )

    while add_remove_player_check == 2:
        global last_winner_id  # Needed to potentially reset last_winner_id
        if len(list(players)) == 0:
            print(
                colors.bold
                + colors.fg.lightred
                + "Noooo I won't let you do this. Haha!"
                + colors.reset
            )
        print_players()
        player_number = check_return_int_conversion(
            get_colored_input("Enter the player number you want to remove: ")
        )
        if not players.get(player_number):
            print(
                colors.bold
                + colors.fg.red
                + "Do you think I am Dumb?? I am not but you definitely are!!"
                + colors.reset
            )
        else:
            removed_player_name = players[player_number]["name"].title()
            players.pop(player_number)
            print_colored(f"Player {removed_player_name} removed.", colors.fg.yellow)
            # Reset last winner if the removed player was the last winner
            if last_winner_id == player_number:
                last_winner_id = None
                print_colored(
                    "Last winner was removed, starting player for the next round will be chosen manually.",
                    colors.fg.yellow,
                )
        add_remove_player_check = check_return_int_conversion(
            get_colored_input(
                "\nDo you want to remove another player (Enter 2 for yes, any other number for quitting)? "
            )
        )
    save_data()


def print_player_balances():
    table = PrettyTable(["No.", "Name", "Balance"], title="Player Balances")
    for k, v in players.items():
        table.add_row([k, v.get("name").title(), "Rs. " + str(v.get("balance"))])
    print(f"\n{colors.fg.yellow}{table}{colors.reset}\n")


def print_players():
    table = PrettyTable(["No.", "Name"], title="Players")
    for k, v in players.items():
        table.add_row([k, v["name"].title()])
    print(table)


def find_preceding_active_player(current_player_id, current_player_ids, folded_players):
    """Finds the active player immediately preceding the current player in turn order."""
    active_players_list = [p for p in current_player_ids if p not in folded_players]
    if len(active_players_list) < 2:
        return None  # Cannot have a show with less than 2 active players

    try:
        current_player_index_in_full_list = current_player_ids.index(current_player_id)
    except ValueError:
        return None  # Should not happen

    num_players = len(current_player_ids)
    search_index = (current_player_index_in_full_list - 1 + num_players) % num_players

    # Iterate backwards through the original list order
    for _ in range(num_players):
        potential_preceding_id = current_player_ids[search_index]
        if (
            potential_preceding_id != current_player_id
            and potential_preceding_id not in folded_players
        ):
            return potential_preceding_id  # Found the preceding active player
        search_index = (search_index - 1 + num_players) % num_players

    return None  # Should only happen if only one player is active


def generate_round():
    global last_winner_id  # Use the global variable
    global players  # Reads and modifies global players dict

    print_colored("\nStarting new round!", colors.fg.cyan)

    player_ids = sorted(players.keys())
    if not player_ids:
        print_colored("No players left in the game!", colors.fg.red)
        sys.exit(0)

    if last_winner_id is None or last_winner_id not in players:
        print_players()
        # Get input using the helper first, then convert
        start_player_str = get_colored_input(
            "Enter the player number who starts this round: "
        )
        starting_player_id = check_return_int_conversion(start_player_str)
    else:
        try:
            winner_index = player_ids.index(last_winner_id)
            start_index = (winner_index + 1) % len(player_ids)
            starting_player_id = player_ids[start_index]
            print(
                f"{colors.fg.lightcyan}Last winner was {players[last_winner_id]['name'].title()}. Next turn starts with {players[starting_player_id]['name'].title()}."
            )
        except (
            ValueError
        ):  # Should not happen if last_winner_id is in players, but safety first
            print(
                colors.fg.red
                + "Error determining next player. Please select manually."
                + colors.reset
            )
            print_players()
            starting_player_id = check_return_int_conversion(
                get_colored_input("Enter the player number who starts this round: ")
            )

    if not players.get(starting_player_id):
        print(
            colors.bold
            + colors.fg.red
            + "Do you think I am Dumb!! , Now go ahead do everything again!"
            + colors.reset
        )
        sys.exit(0)
    print(
        colors.fg.lightcyan
        + "\nThe bets will start from "
        + players.get(starting_player_id).get("name").title()
    )

    boot_amount_str = get_colored_input(
        "Enter the initial Boot amount for this round: "
    )
    boot_amount = check_return_int_conversion(boot_amount_str)
    # Add validation for boot amount if needed (e.g., must be positive)
    current_stake = boot_amount  # The current bet level required

    print(colors.fg.blue + "\nEnter bets of players")
    print(f"  {FOLD} : Fold")
    print(" -1 : End Betting (Declare Winner)")
    print(" -2 : Show (with preceding player)\n" + colors.fg.lightcyan)

    player_bet = 0
    winning_amount = 0
    winning_player_id = None
    folded_players = {}
    round_history = {k: 0 for k in players.keys()}

    current_player_ids = sorted(players.keys())  # Get ordered list for cycling
    current_index = current_player_ids.index(starting_player_id)

    while player_bet != -1:
        player_id = current_player_ids[current_index]

        # Skip folded players
        if folded_players.get(player_id):
            current_index = (current_index + 1) % len(current_player_ids)
            continue
        player_name = players.get(player_id).get("name").title()
        player_bet = check_return_int_conversion(
            get_colored_input(f"{player_name} Bets Rs. ")
        )

        # Process bet
        if player_bet == END_BETTING:
            break
        elif player_bet == FOLD:
            print(colors.fg.lightcyan + "\n" + player_name + " Folds \n")
            folded_players[player_id] = True
            # --- Check if only one player remains after fold ---
            active_players = [p for p in current_player_ids if p not in folded_players]
            if len(active_players) == 1:
                winning_player_id = active_players[0]
                print_colored(
                    f"\n{players[winning_player_id]['name'].title()} is the last player remaining and wins!",
                    colors.fg.lightgreen,
                )
                break # Exit the betting loop
        elif player_bet == SHOW:  # Handle Show
            print(colors.fg.lightcyan + f"\n{player_name} requests a Show.")
            preceding_player_id = find_preceding_active_player(
                player_id, current_player_ids, folded_players
            )

            if preceding_player_id is None:
                print(
                    colors.fg.yellow
                    + "Cannot perform Show. Not enough active players or no preceding active player found."
                    + colors.reset
                )
                continue  # Ask the current player for input again

            preceding_player_name = players[preceding_player_id]["name"].title()
            show_cost = current_stake  # Cost to initiate the show is the current stake

            # Allow negative balance - Deduct cost regardless of current balance
            print(f"{colors.fg.lightcyan}Show cost for {player_name}: Rs. {show_cost}")
            players[player_id]["balance"] -= show_cost
            round_history[player_id] -= show_cost
            winning_amount += show_cost
            print(
                f"{colors.fg.yellow}Show between {player_name} ({player_id}) and {preceding_player_name} ({preceding_player_id})."
            )
            while True:
                loser_input = get_colored_input(
                    f"Enter the player number ({player_id} or {preceding_player_id}) who FOLDS: "
                )
                loser_id = check_return_int_conversion(loser_input)
                if loser_id == player_id or loser_id == preceding_player_id:
                    folded_players[loser_id] = True
                    print(
                        f"{colors.fg.lightcyan}{players[loser_id]['name'].title()} folds after the Show.\n"
                    )
                    # --- Check if only one player remains after show ---
                    active_players_after_show = [p for p in current_player_ids if p not in folded_players]
                    if len(active_players_after_show) == 1:
                        winning_player_id = active_players_after_show[0]
                        print_colored(
                            f"\n{players[winning_player_id]['name'].title()} wins as the last player after the show!",
                            colors.fg.lightgreen
                        )
                        # Signal the outer loop to break after this inner loop finishes
                        player_bet = END_BETTING
                    break
                else:
                    print(
                        colors.fg.red
                        + "Invalid input. Please enter either the requester's number or the preceding player's number."
                        + colors.reset
                    )
            # If the show resulted in a winner, break the outer loop now
            if player_bet == END_BETTING:
                break

        elif player_bet > 0:  # Handle regular bet (Chaal)
            if player_bet < current_stake:
                print(
                    colors.fg.yellow
                    + f"Bet must be at least the current stake of Rs. {current_stake}. Try again."
                    + colors.reset
                )
                continue  # Ask the current player for input again
            elif player_bet > current_stake:
                print(
                    colors.fg.lightcyan
                    + f"Stake increased to Rs. {player_bet} by {player_name}."
                    + colors.reset
                )
                current_stake = player_bet  # Update stake if bet is higher

            # Process the valid bet
            # Allow negative balance - Deduct bet regardless of current balance
            players[player_id]["balance"] -= player_bet
            round_history[player_id] -= player_bet
            winning_amount += player_bet
        else:  # Handle invalid negative numbers other than -1, -2
            print(
                colors.fg.red
                + "Invalid input. Use 0 (Fold), -1 (End Betting), -2 (Show), or a positive bet amount."
                + colors.reset
            )
            continue  # Ask the current player for input again

        # Move to the next player
        current_index = (current_index + 1) % len(current_player_ids)

    # --- Winner Determination ---
    if not winning_player_id:
        print_players()
        winning_player_id = check_return_int_conversion(
            get_colored_input("Enter the player number who won this round: ")
        )

    if not players.get(winning_player_id):
        print(
            colors.bold
            + colors.fg.red
            + "Do you think I am Dumb!! , Now go ahead do everything again!"
            + colors.reset
        )
        sys.exit(0)

    winning_player_name = players.get(winning_player_id).get("name")
    print(
        colors.fg.lightgreen
        + "\nCongratulations! "
        + winning_player_name.title()
        + " won the pot of Rs. "
        + str(winning_amount)
    )
    players[winning_player_id]["balance"] += winning_amount
    last_winner_id = winning_player_id  # Update the last winner for the next round
    round_history[winning_player_id] += winning_amount
    print_player_balances()
    save_data()
    add_remove_player()


if check_yes_no(load_game_input):
    print(colors.fg.lightgreen + "Loading saved game ....")
    with open(winning_history_path, "r", encoding="utf-8") as json_file:
        try:
            players = json.load(json_file)
            players = {int(k): v for k, v in players.items()}
            print_player_balances()
            add_remove_player()
        except:
            print_colored(
                colors.fg.lightred + "\n Sorry, no data found. Starting new game... \n"
            )
            input_players()
else:
    input_players()


game_status = "y"
while check_yes_no(game_status):
    generate_round()
    game_status = get_colored_input(
        "Do you want to start to next round ? (y/n) ", input_color=colors.fg.lightgreen
    )
