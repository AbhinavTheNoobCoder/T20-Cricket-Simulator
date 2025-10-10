import random
from typing import Literal
from collections import Counter
print('''Welcome to Hand Cricket.
Write the playing XI for both the teams and the computer will play a T20 game.
To specify the name of a fast bowling option, write "(fb)" AFTER their name.
To specify the name of a slow/spin bowling option, write "(sb)" AFTER their name.
To specify the name of a medium pace bowling option, write "(mb)" AFTER their name.
To specify the name of the captain, write "(c)" AFTER their name.
To specify the name of the wicketkeeper, write "(wk)" AFTER their name.
The 3 specifications can be written in any order.

You may add batting and bowling attribute numbers to a player.
In case you are simulating the game with attributes, add the attributes after the name
in square brackets.
Syntax: <player_name>[<bat_attribute>, <bowl_attribute>]

Examples:
Virat Kohli[95, 40] -> A batsman
Rohit Sharma[93, 45](c) -> Captain and batsman
Rishabh Pant[91, 5](wk) -> Wicketkeeper
Jasprit Bumrah[45, 95](fb) -> A fast bowler
Ravindra Jadeja[88, 91](sb) -> A spinner
Shivam Dube[87, 75](mb) -> A medium pace bowler (allowed to bowl)
Hardik Pandya[90, 84](fb) -> A fast bowling all-rounder (allowed to bowl)
''')

class Player():
  def __init__(self, name: str) -> None:
    self.name: str = name
    self.bat_runs = self.bat_balls = self.bowl_runs = self.bowl_balls = 0
    self.wickets: int = 0
    self.overs_assigned = 0
    self.did_bat: bool = False
    self.dismissal: str = "not out"
    self.batting_attribute = self.bowling_attribute = 1.00
    self.bowling_performance: float = 7.00
  
  def resetStats(self) -> None: #this is to reset any individual stats from the previous game
    self.bat_runs = self.bat_balls = self.bowl_runs = self.bowl_balls = self.wickets = 0
    self.did_bat = False
    self.dismissal = "not out"
    self.overs_assigned = 0
    self.bowling_performance = 7.00
  
  def __repr__(self) -> str:
    return self.name

#creating CricketTeam to store all info related to the team
class CricketTeam():
  def __init__(self, name: str) -> None:
    self.name: str = name
    self.playing_xi: list[Player] = []
    self.bowlers: list[Player] = []
    self.pacers: list[Player] = []
    self.spinners: list[Player] = []
    self.med_bowlers: list[Player] = [] #this variable is for future use
    self.wickets_lost = self.score = self.balls_played = 0
    self.captain = self.wk = None
  
  def initialiseTeam(self) -> None:
    for _ in range(11):
      player = Player(input(f"Enter a player's details for {self.name}: ").strip(" "))

      if "(c)" in player.name or "(C)" in player.name:
        player.name = player.name.replace("(c)", "")
        player.name = player.name.replace("(C)", "")
        self.captain = player
      
      if "(WK)" in player.name or "(wk)" in player.name:
        player.name = player.name.replace("(WK)", "")
        player.name = player.name.replace("(wk)", "")
        self.wk = player
      
      if "(fb)" in player.name or "(FB)" in player.name:
        player.name = player.name.replace("(fb)", "")
        player.name = player.name.replace("(FB)", "")
        self.bowlers.append(player)
        self.pacers.append(player)

      if "(mb)" in player.name or "(MB)" in player.name:
        player.name = player.name.replace("(mb)", "")
        player.name = player.name.replace("(MB)", "")
        self.bowlers.append(player)
        self.med_bowlers.append(player)
      
      if "(sb)" in player.name or "(SB)" in player.name:
        player.name = player.name.replace("(sb)", "")
        player.name = player.name.replace("(SB)", "")
        self.bowlers.append(player)
        self.spinners.append(player)
      
      if "[" in player.name:
        attributes: str = player.name[player.name.index("["): ]
        attribute_list: list[float] = list(eval(attributes))
        player.name = player.name.replace(attributes, "").strip(" ")
        player.batting_attribute, player.bowling_attribute = attribute_list

      self.playing_xi.append(player)

  def resetAll(self) -> None: #this is to reset any stats related to previous game
    self.balls_played = self.score = self.wickets_lost = 0
    for player in self.playing_xi:
      player.resetStats()

  def __repr__(self) -> str:
    return self.name


numbers = (0, 1, 2, 3, 4, 6)
common_dismissal_types = ('c X b Y', 'b', 'lbw', 'st', 'run out')
# I intend to add extras (wides, no-balls, leg byes) into the game.

#defining bowling order - to ensure no bowler bowls more than 2 overs, no consec. overs
def createBowlingOrder(bowling_team: CricketTeam) -> list[Player]:
  '''Creates a bowling order randomly based on the bowling team's bowlers.'''

  #defining a custom shuffling where two same elements cannot be adjacent
  def custom_shuffle(lst: list[Player]) -> list[Player]:
    count = Counter(lst) #Player: count pairs
    players: list[Player] = sorted(count.keys(), key=lambda x: count[x], reverse= True)
    result = [None] * len(lst) #we will replace each None with a Player object later
    
    # Fill the result list by placing elements in every other position
    index = 0
    for player in players:
      for _ in range(count[player]):
        if index >= len(lst): #after replacing even indices, replace odd indices
          index = 1
        result[index] = player
        index += 2 #no two same values are adjacent
    
    # Check if the result is valid
    for i in range(1, len(result)):
      if result[i] == result[i - 1]:
        raise ValueError("Insufficient bowlers given in team.")
    
    return result

  #this part doesn't have any explanatory comments since I want it to be concise
  bowler_list = bowling_team.bowlers.copy()

  available_bowlers = sorted(bowler_list.copy(), key= lambda x: x.bowling_attribute, reverse= True)
  bowling_order: list[Player] = ["_"] * 20
  fast_bowlers = sorted(bowling_team.pacers.copy(), key= lambda x: x.bowling_attribute, reverse= True)
  overs_dict = {}.fromkeys(available_bowlers, 0)

  if len(fast_bowlers) >= 4:
    pp_bowlers = fast_bowlers[0: 4]
    bowling_order[0] = bowling_order[2] = bowling_order[-1] = bowling_order[-3] = pp_bowlers[0]
    bowling_order[1] = bowling_order[3] = bowling_order[-2] = bowling_order[-4] = pp_bowlers[1]
    bowling_order[4], bowling_order[5] = pp_bowlers[2], pp_bowlers[3]
    overs_dict[pp_bowlers[0]] = overs_dict[pp_bowlers[1]] = 4
    overs_dict[pp_bowlers[2]] = overs_dict[pp_bowlers[3]] = 1

  elif len(fast_bowlers) == 3:
    bowling_order[0] = bowling_order[3] = bowling_order[-1] = bowling_order[-3] = fast_bowlers[0]
    bowling_order[1] = bowling_order[4] = bowling_order[-2] = bowling_order[-4] = fast_bowlers[1]
    overs_dict[fast_bowlers[0]] = overs_dict[fast_bowlers[1]] = 4
    bowling_order[2] = bowling_order[5] = fast_bowlers[2]
    overs_dict[fast_bowlers[2]] = 2
  
  elif len(fast_bowlers) == 2:
    bowling_order[0] = bowling_order[2] = bowling_order[-1] = bowling_order[-3] = fast_bowlers[0]
    bowling_order[1] = bowling_order[3] = bowling_order[-2] = bowling_order[-4] = fast_bowlers[1]
    overs_dict[fast_bowlers[0]] = overs_dict[fast_bowlers[1]] = 4
  
  for bowler, overs_assigned in overs_dict.items():
    if overs_assigned == 4:
      available_bowlers.remove(bowler) #remove bowlers who have quota maxed out
  
  remaining_order: list[Player] = [] #an unshuffled list of bowlers
  overs_remaining: int = bowling_order.count("_")
  i = 0
  for bowler in available_bowlers: #the sorting helps us give more overs to ones with higher rating
    for _ in range(4 - overs_dict[bowler]):
      remaining_order.append(bowler)
      i += 1
      if i == overs_remaining:
        break

    else: #exited for loop without any break -> assign more overs
      continue
    
    break #else block was skipped -> all overs were assigned, come out of the list

  remaining_order = custom_shuffle(remaining_order)
  index = -1
  while True:
    bowler = bowling_order[index]
    if bowler == "_":
      break
    index -= 1

  bowling_order[bowling_order.index("_"): index + 1] = remaining_order
  for bowler in bowling_order:
    bowler.overs_assigned += 1

  return bowling_order

#calculate dynamic run probabilities every ball
def dynamicRuns(batter: Player, bowler: Player, phase: Literal["Powerplay", "Middle Overs", "Death Overs"]) -> Literal[0, 1, 2, 3, 4, 6, "Wicket."]:
  '''Calculate the number of runs scored in a delivery based on the relative strength
  of the batsman with respect to the bowler. Will return an integer if not a wicket
  and "Wicket." if it is a wicket.'''

  x: float = batter.batting_attribute #batting attribute ∝ batting strength
  y: float = bowler.bowling_attribute #bowling attribute ∝ bowling strength
  s1: float = x/(x+y) #relative batting strengh: 0.5 = equals, more than 0.5 = stronger
  af: float = 2*(s1 - 0.5) #stronger batsman has a positive adjustment factor

  if phase == "Powerplay":
    run_weights = (0.3443*(1-af), 0.3435*(1+af), 0.0770*(1+2*af), 0.002*(1+2*af), 0.15*(1+3*af), 0.0805*(1+4*af))

  elif phase == "Middle Overs":
    run_weights = (0.3450*(1-af), 0.3724*(1+af), 0.0840*(1+2*af), 0.0085*(1+2*af), 0.1300*(1+3*af), 0.0600*(1+4*af))
  
  elif phase == "Death Overs":
    run_weights = (0.2666*(1-af), 0.30*(1+af), 0.1633*(1+2*af), 0.0033*(1+2*af), 0.1335*(1+3*af), 0.1333*(1+4*af))
  
  #these are probabilities of (0,1,2,3,4,6) runs occurring per ball
  #run_weights will be changed into probability percentage after processing

  percent_run_weights: list[float] = []
  for i in run_weights:
    percent = (i/sum(run_weights))*100
    percent_run_weights.append(percent)

  runs_scored = random.choices(population=numbers, weights=percent_run_weights)[0]
  if runs_scored != 0:
    return runs_scored
  
  else: #0 runs scored - may or may not be a wicket
    s2 = 1 - s1 #relative bowling strength = 1 - relative batting strength
    af = (s2 - 0.5)/2
    if phase == "Powerplay":
      wicket_weights = (0.16*(1 + af), 0.84*(1 - af))
    
    elif phase == "Middle Overs":
      wicket_weights = (0.16*(1 + af), 0.84*(1 - af))
    
    elif phase == "Death Overs":
      wicket_weights = (0.20*(1 + 2*af), 0.80*(1 - af))

    percent_wicket_weights = []
    for i in wicket_weights:
      percent = (i/sum(wicket_weights))*100
      percent_wicket_weights.append(percent)

    wicket = random.choices(population=(True, False), weights=percent_wicket_weights)[0]
    if (not wicket):
      return 0
    
    else:
      return "Wicket."


#defining batting
def batting(batting_side: CricketTeam, bowling_side: CricketTeam, chasing: bool, target: int | None = None) -> str | int:
  '''Plays one batting innings taking the parameters specified. Returns integer (target)
  if chasing=False and str (match result) if chasing=True.'''

  bat_partners: list[Player] = [batting_side.playing_xi[0], batting_side.playing_xi[1]]
  for _ in bat_partners:
    _.did_bat = True

  available_batters: list[Player] = batting_side.playing_xi[2: ]
  bowling_order: list[Player] = createBowlingOrder(bowling_side)

  while batting_side.balls_played < 120:
    bowler = bowling_order[0]
    try:
      eco = bowler.bowl_runs/bowler.bowl_balls * 6
      crr = batting_side.score/batting_side.balls_played * 6
      wickets = bowler.wickets
      overs = bowler.bowl_balls/6
      bowler.bowling_performance = 3*(crr-eco)/eco + 3*(wickets/overs) + 7
    
    except ZeroDivisionError:
      pass
    
    if bowler.bowling_performance < 6.5:
      usable_bowlers = [_ for _ in bowling_side.bowlers if _.overs_assigned != 4]
      for _ in usable_bowlers:
        try:
          eco = _.bowl_runs/_.bowl_balls * 6
          crr = batting_side.score/batting_side.balls_played * 6
          wickets = _.wickets
          overs = _.bowl_balls/6
          _.bowling_performance = 3*(crr-eco)/eco + 2*(wickets/overs) + 7 if eco != 0 else 10
        
        except ZeroDivisionError:
          pass
      
      try:
        usable_bowlers.sort(key= lambda x: x.bowling_performance, reverse= True)
        if usable_bowlers[0].bowling_performance > 0.4 + bowler.bowling_performance:
          bowler.overs_assigned -= 1
          bowler = usable_bowlers[0]
          bowler.overs_assigned += 1
      
      except IndexError:
        pass

    if batting_side.balls_played in range(0, 36):
      #30 is the upper limit for checking for powerplay here because once balls = 30
      #6 balls are played which gets us 36 balls in powerplay
      phase = "Powerplay"
    
    elif batting_side.balls_played in range(36, 90):
      #similar logic - 36 balls done means powerplay is over
      phase = "Middle Overs"
    
    elif batting_side.balls_played in range(90, 120):
      phase = "Death Overs"

    for _ in range(6):
      batter_on_strike = bat_partners[0]
      runs_scored = dynamicRuns(batter_on_strike, bowler, phase)
      wicket: bool = (runs_scored == 'Wicket.')
      
      batter_on_strike.bat_balls += 1 #incrementing the ball already
      bowler.bowl_balls += 1
      batting_side.balls_played += 1

      if wicket: #wicket
        batting_side.wickets_lost += 1
        dismissal: str = random.choices(population=common_dismissal_types, weights=[60, 25, 7, 3, 5])[0]
        bowler.wickets += 1
        bat_partners.remove(batter_on_strike)

        if dismissal == 'c X b Y':
          catcher = random.choice(bowling_side.playing_xi)
          if catcher == bowler:
            dismissal = f'c & b {bowler}'

          else:
            dismissal = f'c {catcher}  b {bowler}'

        elif dismissal == 'b':
          dismissal = f'b {bowler}'

        elif dismissal == 'lbw':
          dismissal = f'lbw {bowler}'

        elif dismissal == 'st':
          if bowler in bowling_side.spinners:
            dismissal = f'st {bowling_side.wk}  b {bowler}'
          
          else:
            dismissal = 'run out'
          
        if dismissal == 'run out':
          fielder = random.choice(bowling_side.playing_xi)
          dismissal = f'run out ({fielder})'
          bowler.wickets -= 1 #we added 1 wicket as soon as it was a wicket
          #but run outs are NOT credited to the bowler by ICC Rules.

          if chasing:
            possible_runs = tuple(filter(lambda x: batting_side.score + x < target, numbers[0: 3]))
            weights = [63, 36, 1]
            weights = weights[0: len(possible_runs)] #no.of weights = no. of possible runs

          else:
            possible_runs = numbers[0:3]
            weights = [63, 36, 1]

          runs_scored = random.choices(population=possible_runs, weights=weights)[0]
          batter_on_strike.bat_runs += runs_scored
          bowler.bowl_runs += runs_scored
          batting_side.score += runs_scored
          
        batter_on_strike.dismissal = dismissal

      else: #not a wicket
        batter_on_strike.bat_runs += runs_scored
        batting_side.score += runs_scored
        bowler.bowl_runs += runs_scored
        if runs_scored % 2 == 1:
          bat_partners.reverse()
      
      if chasing:
        if batting_side.score >= target: #chased the target
          result: str = f"{batting_side} beat {bowling_side} by {10 - batting_side.wickets_lost} wickets."
          return result

      if batting_side.wickets_lost == 10: #all out
        if not chasing: #first batting
          return batting_side.score + 1   #target
        
        elif chasing: #couldn't chase the target and got all out
          if batting_side.score < target - 1: #lesser runs than opponent
            result: str = f"{bowling_side} beat {batting_side} by {target - 1 - batting_side.score} runs."
          
          elif batting_side.score == target - 1: #same runs as the opponent
            result: str = "Match drawn."

          return result

      if len(bat_partners) == 1:
        new_batter = available_batters.pop(0)
        bat_partners.insert(0, new_batter)
        new_batter.did_bat = True

    bat_partners.reverse() #the over concluded so the strike switches
    bowling_order.pop(0) #next bowler will be upfront

  else: #didn't get all out
    if not chasing:
      return batting_side.score + 1 #target
    
    elif chasing: #couldn't chase and didn't get all out
      if batting_side.score < target - 1:
        result: str = f"{bowling_side} beat {batting_side} by {target - 1 - batting_side.score} runs."

      elif batting_side.score == target - 1:
        result: str = "Match drawn."

      return result


def createScorecard(batting_side: CricketTeam, bowling_side: CricketTeam) -> None:
  '''Print the scorecard for one innings based on which team is batting and bowling.
  To print the scorecard for the whole match, run the function twice with the batting
  team being the defending team the first time and the chasing team the second time.'''

  scorecard: str = f"{batting_side} - {batting_side.score}/{batting_side.wickets_lost} ({batting_side.balls_played//6}.{batting_side.balls_played%6} overs):"
  for batter in batting_side.playing_xi:
    if batter.did_bat:
      name = batter.name
      batter_score = f"{batter.bat_runs}({batter.bat_balls})"
      if batter.dismissal == "not out":
        name += '* '
    
      if batter == batting_side.captain:
        name += "(c)"

      if batter == batting_side.wk:
        name += "(wk)"

      scorecard += f'\n{name:<25}{batter.dismissal:<50}{batter_score:>5}'

  scorecard += f'\n\n{bowling_side} bowling:'
  for bowler in bowling_side.bowlers:
    name = bowler.name
    overs = f'{bowler.bowl_balls // 6}.{bowler.bowl_balls % 6} overs'
    figures = f'{bowler.wickets}-{bowler.bowl_runs}'
    if bowler == bowling_side.captain:
      name += '(c)'

    if bowler.bowl_balls != 0:
      scorecard += f'\n{name:<25}{figures} ({overs})'

  print(scorecard, '\n\n')


if __name__ == "__main__": #run code only when it's the main program
  #accepting two teams
  home_team = CricketTeam(input("Enter the home team: ").strip(" "))
  home_team.initialiseTeam()
  print()
  away_team = CricketTeam(input("Enter the away team: ").strip(" "))
  away_team.initialiseTeam()

  def main() -> None:
    '''Main part of the program - toss and gameplay - can be reused infinitely.'''
    
    #toss
    toss_options = ('H', 'T')
    toss_call = random.choice(toss_options)
    coin_land = random.choice(toss_options)
    elect_options = ["bat", "bowl"]
    elect = random.choice(elect_options)

    if toss_call == coin_land: #away team calls the toss - wins it
      toss_winner = away_team
      toss_loser = home_team
      
    else: #away team loses the toss
      toss_winner = home_team
      toss_loser = away_team

    toss_statement = f"Toss: {toss_winner} won the toss and elected to {elect} first."
    toss_dict = {elect: toss_winner}
    elect_options.remove(elect)
    toss_dict.update({elect_options[0]: toss_loser})

    defending_team = toss_dict['bat'] #defending team bats first
    chasing_team = toss_dict['bowl'] #chasing team bowls first
    target = batting(defending_team, chasing_team, chasing=False) #target for chasing
    result = batting(chasing_team, defending_team, chasing=True, target=target)

    print('\n\n')
    print(toss_statement)
    print("Result:", result, '\n')
    createScorecard(defending_team, chasing_team)
    createScorecard(chasing_team, defending_team)
  
  while True: #infinite games can be played with the same teams by calling main()
    main() #this is like a while-do loop, plays the match at least once
    if input("Play another match with the same teams? (y/n): ").lower() == "y":
      home_team.resetAll() #reset all stats from previous game for both teams
      away_team.resetAll()
    
    else: #quit the loop
      break
