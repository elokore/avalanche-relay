import requests

ZONES = {
    "WestSlopesNorth": 1646
}

def getAvalancheForecast():
    url = f"https://api.avalanche.org/v2/public/product?type=forecast&center_id=NWAC&zone_id={ZONES["WestSlopesNorth"]}"
    response = requests.get(url)

    if response.status_code == 200:
        return True, response.json()
    else:
        return False

def getDangerLevelToday(forecast):
    return forecast["danger"][0]

def getDangerLevelTomorrow(forecast):
    return forecast["danger"][1]

def getForecastZoneName(forecast):
    return forecast["forecast_zone"][0]["name"]

def getForecastExpireTime(forecast):
    return forecast["expires_time"]

def getForecastProblems(forecast):
    return forecast["forecast_avalanche_problems"]

def createAvalancheForecastTextMessage(forecast):
    dangerToday = getDangerLevelToday(forecast)
    dangerTomorrow = getDangerLevelTomorrow(forecast)
    zoneName = getForecastZoneName(forecast)
    expireTime = getForecastExpireTime(forecast)
    tIndex = expireTime.find('T')
    expireTime = expireTime[:tIndex]
    avalancheProblems = getForecastProblems(forecast)

    msg = f"Avy Forecast for {zoneName} {expireTime}\n\n"
    msg += f"Danger:\n\tUpper: {dangerToday["upper"]}\n\tMiddle: {dangerToday["middle"]}\n\tLower: {dangerToday["lower"]}\n"
    msg += "Problems:\n"

    for x in range(0, len(avalancheProblems)):
        problem = avalancheProblems[x]
        msg += f"\t({x}) {problem["name"]}:\n"
        msg += f"\t\tLikelyhood: {problem["likelihood"].capitalize()}\n"
        msg += f"\t\tSize: D"

        for i in range(0, len(problem["size"])):
            msg += str(problem["size"][i])
            if i < len(problem["size"]) - 1:
                msg += "-"
        
        msg += "\n"


    return msg

_, forecast = getAvalancheForecast()
print(createAvalancheForecastTextMessage(forecast))