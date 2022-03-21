from flask import Flask
import requests
from datetime import datetime
app = Flask(__name__)
import cloudscraper
scraper = cloudscraper.create_scraper()


def getRank(name,irlname,region):
    try:
        response = scraper.get("https://api.henrikdev.xyz/valorant/v2/leaderboard/" + region)
        json_data = response.json()
        for x in json_data["players"]:
            if x["gameName"] == name:
                return "/me " + irlname + " is currently ranked #" + str(x["leaderboardRank"])+ " on the leaderboard with " + str(x["numberOfWins"]) + " wins and a ranked rating of " + str(x["rankedRating"])
            
    except:
        return "Failed to find " + irlname + " on the leaderboard"
def getRankv1(name,irlname,region):
        response = scraper.get("https://api.henrikdev.xyz/valorant/v1/leaderboard/" + region)
        json_data = response.json()
        for x in json_data:
            if x["gameName"] == name:
                return "/me " + irlname + " is currently ranked #" + str(x["leaderboardRank"])+ " on the leaderboard with " + str(x["numberOfWins"]) + " wins and a ranked rating of " + str(x["rankedRating"])
def getRecord(name,tag,irlname):
    y=[]
    a=[]
    wins = 0
    loss = 0
    draw = 0
    resultString = ""
    today = datetime.today()
    currentDate = today.strftime("%B %d, %Y")
    response= scraper.get("https://api.henrikdev.xyz/valorant/v1/mmr-history/eu/"+name+"/"+tag)
    json_data = response.json()
    for x in json_data["data"]:
        splitString = x["date"].split()
        if int(splitString[2].translate({ord(','): None})) <10:
            newDate = "" +splitString[1] + " 0"+ splitString[2] + " "+ splitString[3]
        else:
            newDate = "" +splitString[1] + " "+ splitString[2] + " "+ splitString[3]

        if currentDate == newDate:
            y.append(x["mmr_change_to_last_game"])
    for n in y:
        if n>10:
            a.append("W")
        elif 0<=n<10:
            a.append("T")
        elif n == -3:
            pass
        else:
            a.append("L")
    for l in a:
        if l == "W":
            wins+=1
        elif l == "L":
            loss +=1
        else:
            draw +=1
    if wins == 0 and loss == 0 and draw == 0:
        return "Wait for a competitive game to end!"
    else:
        return irlname + " has won " + str(wins) + " games and lost " + str(loss) + " games today. " + "Record- " + str(a)
    
def maps(name,tag):
    mapList = []
    response = scraper.get("https://api.henrikdev.xyz/valorant/v3/matches/eu/"+name+"/"+tag)
    json_data = response.json()
    today = datetime.today()
    currentDate = today.strftime("%B %d, %Y")
    if json_data["status"] == 200:
        today = datetime.today()
        currentDate = today.strftime("%B %d, %Y")
        for x in range(0,5):
            if json_data["data"][x]["metadata"]["mode"] == "Competitive":
                splitString = json_data["data"][x]["metadata"]["game_start_patched"].split()
                newDate = "" +splitString[1] + " "+ splitString[2] + " "+ splitString[3]
                if currentDate == newDate:
                    mapList.append(json_data["data"][x]["metadata"]["map"])
    return "Today's map history is "+ str(mapList)

@app.route('/')
def hello():
    return "Valorant Record/Leaderboard command for Nightbot. DM Vineyard__ on twitch or Vinayak9769#0861 on discord for a page!"
@app.errorhandler(500)
def leaderboarderror(e):
    return "Temporarily disabled. Working on it! :0" 

@app.route('/leon', methods=['POST', 'GET'])
def leonRank():
    return getRank("LJPH", "Leon","eu")
@app.route('/leon/record', methods=['POST', 'GET'])
def getLeonRec():
    y=[]
    a=[]
    wins = 0
    loss = 0
    draw = 0
    resultString = ""
    today = datetime.today()
    currentDate = today.strftime("%B %d, %Y")
    response= scraper.get("https://api.henrikdev.xyz/valorant/v1/mmr-history/eu/LJPH/018")
    json_data = response.json()
    for x in json_data["data"]:
        splitString = x["date"].split()
        if int(splitString[2].translate({ord(','): None})) <10:
            newDate = "" +splitString[1] + " 0"+ splitString[2] + " "+ splitString[3]
        else:
            newDate = "" +splitString[1] + " "+ splitString[2] + " "+ splitString[3]
        if currentDate == newDate:
            y.append(x["mmr_change_to_last_game"])
    for n in y:
        if n>10:
            a.append("W")
        elif 0<=n<10:
            a.append("T")
        else:
            a.append("L")
    for l in a:
        if l == "W":
            wins+=1
        elif l == "L":
            loss +=1
        else:
            draw +=1
        
    return "Leon has won " + str(wins) + " games and lost " + str(loss) + " games today. " + "Record- " + str(a[::-1])
@app.route('/Stout', methods=['POST', 'GET'])
def stoutrank():
    return getRank("SOL Stout","Stout","na")
@app.route('/josh', methods=['POST', 'GET'])
def joshRank():
    response= scraper.get("https://api.henrikdev.xyz/valorant/v1/mmr/eu/JoshMun/Mun")
    json_data = response.json()
    x = json_data["data"]
    return "Josh is currently " + x["currenttierpatched"] + " with a ranked rating of " +str(x["ranking_in_tier"])
@app.route('/josh/record', methods=['POST', 'GET'])
def joshrecord():
    return getRecord("JoshMun","Mun", "Josh")
@app.route('/swedish/record', methods=['POST', 'GET'])
def swedeRec():
    return getRecord("LittleSwede","IKEA", "LittleSwedish")
@app.route('/wasu/record', methods=['POST', 'GET'])
def wasummr():
    return getRecord("wasu","LFT","Wasu")
@app.route('/eggo', methods=['POST', 'GET'])
def eggoRank():
    return getRank("egnarO5","Eggo","eu")
@app.route('/kyle', methods=['POST', 'GET'])
def kyleRank():
    response= scraper.get("https://api.henrikdev.xyz/valorant/v1/mmr/eu/KYCA/KYCA")
    json_data = response.json()
    x = json_data["data"]
    return "Kyle is currently " + x["currenttierpatched"] + " with a ranked rating of " +str(x["ranking_in_tier"])
@app.route('/eggo/record', methods=['POST', 'GET'])
def eggoRec():
    return getRecord("egnarO5","713", "Eggo")

@app.route('/kyle/record', methods=['POST', 'GET'])
def kyleRecord():    
    return getRecord("KYCA","KYCA","Kyle")
@app.route('/linka/record', methods=['POST', 'GET'])
def linkaRec():
    y=[]
    a=[]
    wins = 0
    loss = 0
    draw = 0
    resultString = ""
    today = datetime.today()
    currentDate = today.strftime("%B %d, %Y")
    response= scraper.get("https://api.henrikdev.xyz/valorant/v1/mmr-history/eu/Pancakes/1313")
    json_data = response.json()
    for x in json_data["data"]:
        splitString = x["date"].split()
        if int(splitString[2].translate({ord(','): None})) <10:
            newDate = "" +splitString[1] + " 0"+ splitString[2] + " "+ splitString[3]
        else:
            newDate = "" +splitString[1] + " "+ splitString[2] + " "+ splitString[3]
        if currentDate == newDate:
            if splitString[5] == "AM":
                pass
            else:
                y.append(x["mmr_change_to_last_game"])
    for n in y:
        if n>10:
            a.append("W")
        elif 0<=n<10:
            a.append("T")
        else:
            a.append("L")
    for l in a:
        if l == "W":
            wins+=1
        elif l == "L":
            loss +=1
        else:
            draw +=1
        
    if wins == 0 and loss == 0 and draw == 0:
        return "Wait for a competitive game to end!"
    else:
        return  "Linka has won " + str(wins) + " games and lost " + str(loss) + " games today. " + "Record- " + str(a)
@app.route('/linka', methods=['POST', 'GET'])
def linkaRank():
    response= scraper.get("https://api.henrikdev.xyz/valorant/v1/mmr/eu/Pancakes/1313")
    json_data = response.json()
    x = json_data["data"]
    return "Linka is currently " + x["currenttierpatched"] + " with a ranked rating of " +str(x["ranking_in_tier"])
@app.route('/josh/maps', methods=['POST', 'GET'])
def joshMaps():
    return maps("JoshMun","Mun")
@app.route('/leon/maps', methods=['POST', 'GET'])
def leonMaps():
    return maps("LJPH","018")
@app.route('/linka/maps', methods=['POST', 'GET'])
def linkaMaps():
    return maps("Pancakes","1313")
@app.route('/stout/record', methods=['POST', 'GET'])
def stoutRec():    
    y=[]
    a=[]
    wins = 0
    loss = 0
    draw = 0
    resultString = ""
    today = datetime.today()
    currentDate = today.strftime("%B %d, %Y")
    response= scraper.get("https://api.henrikdev.xyz/valorant/v1/mmr-history/na/SOL%20Stout/LUL")
    json_data = response.json()
    for x in json_data["data"]:
        splitString = x["date"].split()
        if int(splitString[2].translate({ord(','): None})) <10:
            newDate = "" +splitString[1] + " 0"+ splitString[2] + " "+ splitString[3]
        else:
            newDate = "" +splitString[1] + " "+ splitString[2] + " "+ splitString[3]
        if currentDate == newDate:
            y.append(x["mmr_change_to_last_game"])
    for n in y:
        if n>10:
            a.append("W")
        elif 0<=n<10:
            a.append("T")
        elif n == -3:
            pass
        else:
            a.append("L")
    for l in a:
        if l == "W":
            wins+=1
        elif l == "L":
            loss +=1
        else:
            draw +=1
        
    return "Stout has won " + str(wins) + " games and lost " + str(loss) + " games today. " + "Record- " + str(a) 
@app.route('/korneen/record', methods=['POST', 'GET'])
def korneenRec():    
    y=[]
    a=[]
    wins = 0
    loss = 0
    draw = 0
    resultString = ""
    today = datetime.today()
    currentDate = today.strftime("%B %d, %Y")
    response= scraper.get("https://api.henrikdev.xyz/valorant/v1/mmr-history/na/Korneen/TTV")
    json_data = response.json()
    for x in json_data["data"]:
        splitString = x["date"].split()
        if int(splitString[2].translate({ord(','): None})) <10:
            newDate = "" +splitString[1] + " 0"+ splitString[2] + " "+ splitString[3]
        else:
            newDate = "" +splitString[1] + " "+ splitString[2] + " "+ splitString[3]
        if currentDate == newDate:
            y.append(x["mmr_change_to_last_game"])
    for n in y:
        if n>10:
            a.append("W")
        elif 0<=n<10:
            a.append("T")
        elif n == -3:
            pass
        else:
            a.append("L")
    for l in a:
        if l == "W":
            wins+=1
        elif l == "L":
            loss +=1
        else:
            draw +=1
        
    return "Korneen has won " + str(wins) + " games and lost " + str(loss) + " games today. " + "Record- " + str(a) 
@app.route('/alex/record', methods=['POST', 'GET'])
def alexRecord():    
    return "https://www.youtube.com/watch?v=t4UwjBqgBCI Banger song NODDERS"
@app.route('/josh/leaderboard', methods=['POST', 'GET'])
def joshLeaderboard():    
    return getRank("JoshMun","Josh","eu")
@app.route('/russ/leaderboard', methods=['POST', 'GET'])
def russLeaderboard():    
    return getRank("Guild Russ","Russ","eu")
@app.route('/russ/record', methods=['POST', 'GET'])
def russRecord():    
    return getRecord("Guild Russ","WRLD","Russ")
@app.route('/bacon/record', methods=['POST', 'GET'])
def baconRecord():    
    return getRecord("PP PrinceBaconTV","YEET","PB")
@app.route('/bacon', methods=['POST', 'GET'])
def baconRank():
    response= scraper.get("https://api.henrikdev.xyz/valorant/v1/mmr/eu/PP%20PrinceBaconTV/YEET")
    json_data = response.json()
    x = json_data["data"]
    return "PB is currently " + x["currenttierpatched"] + " with a ranked rating of " +str(x["ranking_in_tier"])
@app.route('/sukh', methods=['POST', 'GET'])
def sukhRank():
    response= scraper.get("https://api.henrikdev.xyz/valorant/v1/mmr/na/SukhdeepFPS/TTV")
    json_data = response.json()
    x = json_data["data"]
    return "Sukh is currently " + x["currenttierpatched"] + " with a ranked rating of " +str(x["ranking_in_tier"])
@app.route('/josh/rr', methods=['POST', 'GET'])
def joshRR():
    y=[]
    a=[]
    loss = 0
    draw = 0
    today = datetime.today()
    currentDate = today.strftime("%B %d, %Y")
    response= scraper.get("https://api.henrikdev.xyz/valorant/v1/mmr-history/eu/JoshMun/Mun")
    json_data = response.json()
    for x in json_data["data"]:
        splitString = x["date"].split()
        if int(splitString[2].translate({ord(','): None})) <10:
            newDate = "" +splitString[1] + " 0"+ splitString[2] + " "+ splitString[3]
        else:
            newDate = "" +splitString[1] + " "+ splitString[2] + " "+ splitString[3]
        if currentDate == newDate:
            y.append(x["mmr_change_to_last_game"])
    rr = sum(y)

    values = ','.join(str(v) for v in y)
    return "RR change today: " + values + " = "+str(rr)
@app.route('/kyle/leaderboard', methods=['POST', 'GET'])
def kylelbRank():
    return getRank("KYCA","KYCA","eu")
@app.route('/kjja', methods=['POST', 'GET'])
def kjjaRank():
    return getRank("Kjja", "Kjja","eu")
@app.route('/kjja/record', methods=['POST', 'GET'])
def kjjarecord():
    return getRecord("Kjja","KLC4E", "Kjja")
@app.route('/eggo/rr', methods=['POST', 'GET'])
def eggoRR():
    y=[]
    a=[]
    loss = 0
    draw = 0
    today = datetime.today()
    currentDate = today.strftime("%B %d, %Y")
    response= scraper.get("https://api.henrikdev.xyz/valorant/v1/mmr-history/eu/egnarO5/713")
    json_data = response.json()
    for x in json_data["data"]:
        splitString = x["date"].split()
        if int(splitString[2].translate({ord(','): None})) <10:
            newDate = "" +splitString[1] + " 0"+ splitString[2] + " "+ splitString[3]
        else:
            newDate = "" +splitString[1] + " "+ splitString[2] + " "+ splitString[3]
        if currentDate == newDate:
            y.append(x["mmr_change_to_last_game"])
    rr = sum(y)

    values = ','.join(str(v) for v in y)
    return "RR change today: " + values + " = "+str(rr)
@app.route('/huss', methods=['POST', 'GET'])
def hussRank():
    return getRank("Huss", "Huss","na")
@app.route('/korneen/rr', methods=['POST', 'GET'])
def korneenRR():
    y=[]
    a=[]
    loss = 0
    draw = 0
    today = datetime.today()
    currentDate = today.strftime("%B %d, %Y")
    response= scraper.get("https://api.henrikdev.xyz/valorant/v1/mmr-history/na/Korneen/TTV")
    json_data = response.json()
    for x in json_data["data"]:
        splitString = x["date"].split()
        if int(splitString[2].translate({ord(','): None})) <10:
            newDate = "" +splitString[1] + " 0"+ splitString[2] + " "+ splitString[3]
        else:
            newDate = "" +splitString[1] + " "+ splitString[2] + " "+ splitString[3]
        if currentDate == newDate:
            y.append(x["mmr_change_to_last_game"])
    rr = sum(y)

    values = ','.join(str(v) for v in y)
    return "RR change today: " + values + " = "+str(rr)
@app.route('/alex', methods=['POST', 'GET'])
def alexRank():
    response= scraper.get("https://api.henrikdev.xyz/valorant/v1/mmr/eu/7AM%20FakeAnanas/TTV")
    json_data = response.json()
    x = json_data["data"]
    return "FakeAnanas is currently " + x["currenttierpatched"] + " with a ranked rating of " +str(x["ranking_in_tier"])
@app.route('/marcus/rank', methods=['POST', 'GET'])
def marcusRank():
    try:
        return getRankv1("Guild SoMarcus","Marcus","eu")
    except:
        return getRank("Guild SoMarcus", "Marcus","eu")
@app.route('/marcus/record', methods=['POST', 'GET'])
def marcusrecord():
    return getRecord("Guild SoMarcus","313", "Marcus")
@app.route('/leon/rr', methods=['POST', 'GET'])
def leonRR():
    y=[]
    a=[]
    loss = 0
    draw = 0
    today = datetime.today()
    currentDate = today.strftime("%B %d, %Y")
    response= scraper.get("https://api.henrikdev.xyz/valorant/v1/mmr-history/eu/LJPH/018")
    json_data = response.json()
    for x in json_data["data"]:
        splitString = x["date"].split()
        if int(splitString[2].translate({ord(','): None})) <10:
            newDate = "" +splitString[1] + " 0"+ splitString[2] + " "+ splitString[3]
        else:
            newDate = "" +splitString[1] + " "+ splitString[2] + " "+ splitString[3]
        if currentDate == newDate:
            y.append(x["mmr_change_to_last_game"])
    rr = sum(y)

    values = ','.join(str(v) for v in y)
    return "RR change today: " + values + " = "+str(rr)
if __name__ == "__main__":
    app.run(debug=False)
