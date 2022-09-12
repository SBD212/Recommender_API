from turtle import distance
from numpy import dot
from numpy.linalg import norm


def recommender(activities, data):

    user_type = 1 if data["category"] == "in" else 2
    user_gender = 1 if data["gender"] == "male" else 2
    user_group = 1 if data["social"] == "solo" else 2

    ##make a list of user_choices
    user_choices = [user_type, user_gender, user_group]

    # make a feature list and calculate rating for each activity
    for activity in activities:
        type = 1 if activity["type"] == "in" else 2 if activity["type"] == "out" else 3
        gender = (
            1
            if activity["gender"] == "male"
            else 2
            if activity["gender"] == "female"
            else 3
        )
        group = (
            1
            if activity["group"] == "solo"
            else 2
            if activity["group"] == "group"
            else 3
        )
        if "dist" in activity:
            distance = float(activity["dist"][:4])
        else:
            distance = 100
        feature_list = [type, gender, group]

        # calculalte rating using cosine similarity
        rating = dot(user_choices, feature_list) / (
            norm(user_choices) * norm(feature_list)
        )
        activity.update({"algoRating": rating})

    # sort the activities based on this rating
    recommended_activities = sorted(
        activities, key=lambda k: k.get("algoRating"), reverse=True
    )

    recommended_activities_by_dist = sorted(
        activities, key=lambda k: k.get("dist", "10")
    )
    return [recommended_activities, recommended_activities_by_dist]
