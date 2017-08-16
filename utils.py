TEAMS = ['tmp1' ,'tmp2']

def vote_parse(user, text):
    for team in TEAMS:
        if text.find(team) != -1:
            log = "One vote for {} from {}".format(team,user)
            with open("test.txt", "a") as myfile:
                myfile.write(log)
            break
            print(log)
    return
