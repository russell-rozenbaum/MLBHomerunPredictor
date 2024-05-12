import CollectData



def teamHomerunsPerGame(data) :
    expectedHomeruns = {}
    # Calculates the expected homeruns in today's game given
    # the starting lineup

    # - !!To Add!! - # 
    # Take into account more factors, such as starting pitcher,
    # total at bats/expected at bats, and implement ML Algorithm to
    # learn each day
    for team_name, team in data.teamData.items() :
        exp_hr = 0;
        team_batters = team['batterData']
        for batter in team['startingLineup'] :
            homeruns_per_game = team_batters[batter]['hr'] / team_batters[batter]['gp']
            exp_hr += homeruns_per_game
        print(team_name, ' expects to have ', exp_hr)
        expectedHomeruns[team_name] = exp_hr
    return expectedHomeruns


