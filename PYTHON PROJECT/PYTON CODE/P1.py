
import random
import time

# ------------------ Data ------------------
matches = {
    "1": {"teams": ["India", "Australia"], "type": "ODI", "overs": 50},
    "2": {"teams": ["CSK", "MI"], "type": "T20", "overs": 20},
    "3": {"teams": ["England", "Pakistan"], "type": "Test", "overs": 90},
}

players = {
    "India": ["Rohit Sharma", "Virat Kohli", "KL Rahul", "Shubman Gill", "Hardik Pandya",
              "Ravindra Jadeja", "Axar Patel", "Kuldeep Yadav", "Jasprit Bumrah", "Mohammed Shami", "Mohammed Siraj"],
    "Australia": ["David Warner", "Steve Smith", "Marnus Labuschagne", "Glenn Maxwell", "Pat Cummins",
                  "Cameron Green", "Mitchell Marsh", "Alex Carey", "Josh Hazlewood", "Nathan Lyon", "Mitchell Starc"],
    "CSK": ["MS Dhoni", "Ruturaj Gaikwad", "Shivam Dube", "Moeen Ali", "Ravindra Jadeja",
            "Ben Stokes", "Deepak Chahar", "Maheesh Theekshana", "Matheesha Pathirana", "Tushar Deshpande", "Devon Conway"],
    "MI": ["Rohit Sharma", "Ishan Kishan", "Suryakumar Yadav", "Cameron Green", "Tilak Varma",
           "Tim David", "Jofra Archer", "Piyush Chawla", "Jason Behrendorff", "Riley Meredith", "Jasprit Bumrah"],
    "England": ["Joe Root", "Ben Stokes", "Jonny Bairstow", "Jos Buttler", "Harry Brook",
                "Moeen Ali", "Chris Woakes", "Mark Wood", "Jofra Archer", "James Anderson", "Stuart Broad"],
    "Pakistan": ["Babar Azam", "Mohammad Rizwan", "Fakhar Zaman", "Imam-ul-Haq", "Shadab Khan",
                 "Iftikhar Ahmed", "Mohammad Nawaz", "Haris Rauf", "Shaheen Afridi", "Hasan Ali", "Naseem Shah"],
}

team_roles = {
    "India": {"captain": "Virat Kohli", "wicketkeeper": "KL Rahul"},
    "Australia": {"captain": "Steve Smith", "wicketkeeper": "Alex Carey"},
    "CSK": {"captain": "MS Dhoni", "wicketkeeper": "MS Dhoni"},
    "MI": {"captain": "Rohit Sharma", "wicketkeeper": "Ishan Kishan"},
    "England": {"captain": "Joe Root", "wicketkeeper": "Jos Buttler"},
    "Pakistan": {"captain": "Babar Azam", "wicketkeeper": "Mohammad Rizwan"},
}

# ------------------ Utility Functions ------------------
def show_matches():
    print("\nAvailable Matches:")
    for key, match in matches.items():
        print(f"{key}. {match['teams'][0]} vs {match['teams'][1]} - {match['type']} Match")

def toss(team1, team2):
    winner = random.choice([team1, team2])
    decision = random.choice(["bat", "bowl"])
    print(f"\nToss Winner: {winner}")
    print(f"{winner} has chosen to {decision} first.")
    return winner, decision

def show_playing_xi(team):
    print(f"\nPlaying XI for {team}:")
    print(f"  Captain: {team_roles[team]['captain']}")
    print(f"  Wicketkeeper: {team_roles[team]['wicketkeeper']}")
    for player in players[team]:
        if player not in (team_roles[team]['captain'], team_roles[team]['wicketkeeper']):
            print(f"  - {player}")

# ------------------ Innings Simulation ------------------
def simulate_innings(team, overs_limit, match_type, bowling_team, target=None):
    """
    Simulates an innings over-by-over.
    If 'target' is provided, the innings ends as soon as total_score reaches or exceeds it.
    Returns:
      total_score, wickets, batting_scorecard, over_analysis, bowling_scorecard
    """
    print(f"\n🏏 {team} Batting Innings (Live) 🏏")
    print(f"{team} is batting and {bowling_team} is bowling.")

    total_score = 0
    wickets = 0
    batsman_index = 0

    batting_scorecard = {}
    current_batsman = players[team][batsman_index]
    batting_scorecard[current_batsman] = {"Runs": 0, "Balls": 0, "Fours": 0, "Sixes": 0}

    over_analysis = {}

    # Select bowlers – use last 5 players from the bowling team
    bowlers = players[bowling_team][-5:]
    bowling_scorecard = {bowler: {"Overs": 0, "Runs": 0, "Wickets": 0, "Maidens": 0} for bowler in bowlers}

    # Set maximum overs per bowler for limited overs formats
    if match_type == "T20":
        max_bowler_overs = 4
    elif match_type == "ODI":
        max_bowler_overs = 10
    else:
        max_bowler_overs = overs_limit  # For Test, no strict limit

    outcomes = ["0", "1", "2", "3", "4", "6", "W"]
    outcome_weights = [0.25, 0.20, 0.10, 0.05, 0.20, 0.10, 0.10]

    for over in range(1, overs_limit + 1):
        if wickets >= 10 or (target is not None and total_score >= target):
            break

        available_bowlers = [b for b in bowlers if bowling_scorecard[b]["Overs"] < max_bowler_overs]
        if available_bowlers:
            bowler = random.choice(available_bowlers)
        else:
            bowler = random.choice(bowlers)
        bowling_scorecard[bowler]["Overs"] += 1

        runs_this_over = 0
        maiden = True

        for ball in range(6):
            if wickets >= 10 or (target is not None and total_score >= target):
                break

            outcome = random.choices(outcomes, weights=outcome_weights, k=1)[0]
            batting_scorecard[current_batsman]["Balls"] += 1

            if outcome == "W":
                wickets += 1
                bowling_scorecard[bowler]["Wickets"] += 1
                print(f"Over {over}, Ball {ball+1}: {current_batsman} is OUT! Score: {total_score}/{wickets}")
                maiden = False
                batsman_index += 1
                if batsman_index < len(players[team]):
                    current_batsman = players[team][batsman_index]
                    batting_scorecard[current_batsman] = {"Runs": 0, "Balls": 0, "Fours": 0, "Sixes": 0}
                else:
                    break
            else:
                runs = int(outcome)
                total_score += runs
                runs_this_over += runs
                batting_scorecard[current_batsman]["Runs"] += runs
                if runs == 4:
                    batting_scorecard[current_batsman]["Fours"] += 1
                elif runs == 6:
                    batting_scorecard[current_batsman]["Sixes"] += 1
                if runs > 0:
                    maiden = False
                print(f"Over {over}, Ball {ball+1}: {current_batsman} scores {runs} run(s) | Total: {total_score}/{wickets}")

            time.sleep(0.2)

            # If target reached exactly, break out immediately.
            if target is not None and total_score >= target:
                break

        over_analysis[over] = runs_this_over
        bowling_scorecard[bowler]["Runs"] += runs_this_over
        if maiden:
            bowling_scorecard[bowler]["Maidens"] += 1

        print(f"End of Over {over}: {runs_this_over} runs | Score: {total_score}/{wickets}")

        # If target reached exactly, no need for extra balls/overs.
        if target is not None and total_score >= target:
            break

    print(f"\n{team} Innings Ended: {total_score}/{wickets} in {over} overs")
    
    # Batting Scorecard Display
    print("\nBatting Scorecard:")
    print(f"{'Batsman':<20} {'Runs':<5} {'Balls':<5} {'4s':<3} {'6s':<3} {'SR':<6}")
    for batsman, stats in batting_scorecard.items():
        sr = round((stats["Runs"] / stats["Balls"]) * 100, 2) if stats["Balls"] > 0 else 0.0
        print(f"{batsman:<20} {stats['Runs']:<5} {stats['Balls']:<5} {stats['Fours']:<3} {stats['Sixes']:<3} {sr:<6}")

    # Over-to-Over Analysis Display
    print("\nOver-to-Over Analysis:")
    for ov, runs in over_analysis.items():
        print(f"Over {ov}: {runs} runs")

    # Bowling Scorecard Display
    print("\nBowling Scorecard:")
    print(f"{'Bowler':<20} {'Overs':<5} {'Runs':<5} {'Wkts':<5} {'Maidens':<7}")
    for bowler, stats in bowling_scorecard.items():
        print(f"{bowler:<20} {stats['Overs']:<5} {stats['Runs']:<5} {stats['Wickets']:<5} {stats['Maidens']:<7}")

    return total_score, wickets, batting_scorecard, over_analysis, bowling_scorecard

# ------------------ Match Simulation ------------------
def standard_match_simulation(team1, team2, match_type, overs_limit):
    print(f"\n🏏 {team1} vs {team2} - {match_type} Match Start! 🏏")
    toss_winner, decision = toss(team1, team2)
    if decision == "bat":
        first_batting = toss_winner
        second_batting = team2 if toss_winner == team1 else team1
    else:
        first_batting = team2 if toss_winner == team1 else team1
        second_batting = toss_winner

    show_playing_xi(team1)
    show_playing_xi(team2)

    # First Innings (no target)
    print(f"\n--- First Innings: {first_batting} batting ---")
    first_score, first_wkts, bat1, over1, bowl1 = simulate_innings(first_batting, overs_limit, match_type, second_batting)

    print("\n--- Innings Break ---\n")
    time.sleep(2)

    # Second Innings (target is first_score + 1)
    target = first_score + 1
    print(f"\n--- Second Innings: {second_batting} batting ---")
    print(f"Target for {second_batting} is {target} runs.")
    second_score, second_wkts, bat2, over2, bowl2 = simulate_innings(second_batting, overs_limit, match_type, first_batting, target=target)

    print("\n🏆 MATCH RESULT 🏆")
    if second_score >= target:
        margin = 10 - second_wkts
        print(f"🎉 {second_batting} wins by {margin} wickets!")
    else:
        margin = first_score - second_score
        print(f"🎉 {first_batting} wins by {margin} runs!")

    combined = {}
    combined.update(bat1)
    for batsman, stats in bat2.items():
        if batsman in combined:
            combined[batsman]["Runs"] += stats["Runs"]
        else:
            combined[batsman] = stats
    potm = max(combined.items(), key=lambda x: x[1]["Runs"])
    print(f"\n⭐ PLAYER OF THE MATCH: {potm[0]} with {potm[1]['Runs']} runs ⭐")

def test_match_simulation(team1, team2, overs_limit):
    """
    Simulates a Test match with four innings.
    Implements follow-on if first innings lead is 200+ runs.
    Displays lead/trail after each innings.
    """
    print(f"\n🏏 {team1} vs {team2} - Test Match Start! 🏏")
    toss_winner, decision = toss(team1, team2)
    if decision == "bat":
        first_batting = toss_winner
        second_batting = team2 if toss_winner == team1 else team1
    else:
        first_batting = team2 if toss_winner == team1 else team1
        second_batting = toss_winner

    show_playing_xi(team1)
    show_playing_xi(team2)

    # 1st Innings
    print(f"\n--- 1st Innings: {first_batting} batting ---")
    score1, wkts1, bat1, over1, bowl1 = simulate_innings(first_batting, overs_limit, "Test", second_batting)

    # 1st Innings for second side
    print(f"\n--- 1st Innings: {second_batting} batting ---")
    score2, wkts2, bat2, over2, bowl2 = simulate_innings(second_batting, overs_limit, "Test", first_batting)
    lead_after_1st = score1 - score2
    if lead_after_1st > 0:
        print(f"\nAfter 1st innings, {first_batting} leads by {lead_after_1st} runs.")
    else:
        print(f"\nAfter 1st innings, {second_batting} leads by {abs(lead_after_1st)} runs.")

    follow_on = False
    if lead_after_1st >= 200:
        print(f"\n{second_batting} is asked to follow on!")
        follow_on = True

    if follow_on:
        # 2nd Innings (Follow-on for second side)
        print(f"\n--- 2nd Innings (Follow-On): {second_batting} batting ---")
        score3, wkts3, bat3, over3, bowl3 = simulate_innings(second_batting, overs_limit, "Test", first_batting)
        new_lead = score1 - score3
        print(f"\nAfter follow-on, {first_batting} leads by {new_lead} runs.")
        # 4th Innings: Final chase by first side
        print(f"\n--- 2nd Innings: {first_batting} batting ---")
        target4 = new_lead + 1
        print(f"Target for {first_batting} is {target4} runs.")
        score4, wkts4, bat4, over4, bowl4 = simulate_innings(first_batting, overs_limit, "Test", second_batting, target=target4)
        if score4 >= target4:
            margin = 10 - wkts4
            print(f"\n🎉 {first_batting} wins by {margin} wickets!")
        else:
            margin = target4 - score4
            print(f"\n🎉 {second_batting} wins by {margin} runs!")
    else:
        # Normal sequence without follow-on: 2nd Innings for first side
        print(f"\n--- 2nd Innings: {first_batting} batting ---")
        score3, wkts3, bat3, over3, bowl3 = simulate_innings(first_batting, overs_limit, "Test", second_batting)
        trail = score3 - score2
        if trail > 0:
            print(f"\nAfter 2nd innings, {second_batting} trails by {trail} runs.")
        else:
            print(f"\nAfter 2nd innings, {second_batting} leads by {abs(trail)} runs.")
        # 4th Innings for second side
        print(f"\n--- 2nd Innings: {second_batting} batting ---")
        target4 = score3 - score2 + 1
        print(f"Target for {second_batting} is {target4} runs.")
        score4, wkts4, bat4, over4, bowl4 = simulate_innings(second_batting, overs_limit, "Test", first_batting, target=target4)
        if score4 >= target4:
            margin = 10 - wkts4
            print(f"\n🎉 {second_batting} wins by {margin} wickets!")
        else:
            margin = target4 - score4
            print(f"\n🎉 {first_batting} wins by {margin} runs!")

    combined = {}
    for innings in [bat1, bat2]:
        for player, stats in innings.items():
            combined[player] = combined.get(player, 0) + stats["Runs"]
    potm = max(combined.items(), key=lambda x: x[1])
    print(f"\n⭐ PLAYER OF THE MATCH: {potm[0]} with {potm[1]} runs ⭐")

# ------------------ Main Simulation ------------------
def match_simulation(team1, team2, match_type, overs_limit):
    if match_type == "Test":
        test_match_simulation(team1, team2, overs_limit)
    else:
        standard_match_simulation(team1, team2, match_type, overs_limit)

def main():
    show_matches()
    choice = input("\nEnter the match number you want to watch: ")
    if choice in matches:
        match = matches[choice]
        team1, team2 = match["teams"]
        match_type, overs_limit = match["type"], match["overs"]
        if match_type == "ODI":
            overs_limit = 50
        elif match_type == "T20":
            overs_limit = 20
        elif match_type == "Test":
            overs_limit = 90
        match_simulation(team1, team2, match_type, overs_limit)
    else:
        print("\nInvalid selection. Please try again.")

if __name__ == "__main__":
    main()