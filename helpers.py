import requests
import os

##filtering database based on user inputs
def find_activities(mongo, data):
    results = []
    api_key = os.environ.get("GOOGLE_MAPS_API_KEY")
    type_query = {"$or": [{"type": data["category"]}, {"type": "both"}]}
    gender_query = {"$or": [{"type": data["gender"]}, {"type": "both"}]}
    social_query = {"$or": [{"type": data["social"]}, {"type": "both"}]}

    ##find activities based on user input
    col = mongo.db[data["type"]]
    activities = col.find({"$or": [type_query, gender_query, social_query]})

    ##finding distance of activites from user location
    for activity in activities:
        activity["imageUrl"] = activity["imageUrl"].replace("photox", "photo")
        dist = requests.get(
            f"https://maps.googleapis.com/maps/api/distancematrix/json?origins={data['postcode']}&destinations={activity['postcode']}&mode=walking&key={api_key}"
        ).json()

        if dist["rows"][0]["elements"][0]["status"] == "NO_RESULTS":
            activity.update({"dist": None})
        elif dist["rows"][0]["elements"][0]["status"] == "OK":
            activity.update(
                {"dist": dist["rows"][0]["elements"][0]["distance"]["text"]}
            )
        results.append(activity)

    ##sort results by distance
    #sorted_results = sorted(results, key=lambda k: k.get("dist", "10"))

    return results
