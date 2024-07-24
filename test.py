from math import sqrt

data = {
    "Ben": {
        "Interstellar": 4,
        "The Dark Knight": 5,
        "Wanted": 3,
        "Sucker Punch": 2,
        "Inception": 5,
        "The Conjuring": 3,
        "21 Jump Street": 4,
        "The Prestige": 5
    },
    "Sam": {
        "Interstellar": 5,
        "The Dark Knight": 5,
        "Wanted": 1,
        "Devil": 3,
        "The Conjuring": 1,
        "21 Jump Street": 4,
        "Men in Black": 2
    },
    "Jake": {
        "Hot Tub Time Machine": 1,
        "Inception": 5,
        "Revenant": 3,
        "Avengers 1": 4,
        "Iron Man 2": 3,
        "Batman v Superman": 5,
        "Wanted": 4,
    },
    "Megan": {
        "Inception": 5,
    },
    "Kumar": {
        "Hot Tub Time Machine": 1,
        "Avengers 1": 4,
        "Avengers 2": 3,
        "The Departed": 5,
        "Interstellar": 4,
        "Fight Club": 5,
        "Vampires Suck": 1,
        "Twilight": 1
    },
    "Tori": {
        "Notebook": 5,
        "The Terminal": 4,
        "Twilight": 5,
        "Inception": 2,
        "The Dark Knight": 1,
        "Hot Tub Time Machine": 2,
        "The Vow": 4
    },
    "Brooke": {
        "Inception": 5,
        "The Conjuring": 4
    },
    "Luke": {
        "Twilight": 1
    }
}

itemNames = [
    "Interstellar", "The Dark Knight", "Wanted", "Sucker Punch", "Inception",
    "The Conjuring", "21 Jump Street", "The Prestige", "Devil", "Men in Black",
    "Hot Tub Time Machine", "Revenant", "Avengers 1", "Iron Man 2",
    "Batman v Superman", "Avengers 2", "The Departed", "Fight Club",
    "Vampires Suck", "Twilight", "Notebook", "The Terminal", "The Vow", "Focus"
]

MAXrating = 5
MINrating = 1

def compute_similarity(item1, item2, userRatings):
    averages = {}
    for key, ratings in userRatings.items():
        averages[key] = (float(sum(ratings.values())) / len(ratings.values()))

    num = 0
    dem1 = 0
    dem2 = 0

    for user, ratings in userRatings.items():
        if item1 in ratings and item2 in ratings:
            avg = averages[user]
            num += (ratings[item1] - avg) * (ratings[item2] - avg)
            dem1 += (ratings[item1] - avg) ** 2
            dem2 += (ratings[item2] - avg) ** 2

    if dem1 * dem2 == 0:
        return 0
    return num / (sqrt(dem1 * dem2))

def build_similarity_matrix(userRatings):
    similarity_matrix = {}

    for i in range(len(itemNames)):
        band = {}
        for j in range(len(itemNames)):
            if itemNames[i] != itemNames[j]:
                band[itemNames[j]] = compute_similarity(itemNames[i], itemNames[j], userRatings)
        similarity_matrix[itemNames[i]] = band

    return similarity_matrix

def normalize(rating):
    num = 2 * (rating - MINrating) - (MAXrating - MINrating)
    den = (MAXrating - MINrating)
    return num / den

def denormalize(rating):
    return (((rating + 1) * (MAXrating - MINrating)) / 2) + MINrating

def prediction(username, item, sm, userRatings):
    num = 0
    den = 0
    for band, rating in userRatings[username].items():
        if band in sm[item]:
            num += sm[item][band] * normalize(rating)
            den += abs(sm[item][band])

    if den == 0:
        return 0
    return denormalize(num / den)

def recommendation(username, userRatings, sm):
    recommend = []
    for item in itemNames:
        if item not in userRatings[username].keys():
            if prediction(username, item, sm, userRatings) >= 3.5:
                recommend.append(item)
    return recommend

def get_user_ratings():
    user_ratings = {}
    print("Rate the following movies (Enter ratings from 1 to 5, or 0 if you haven't watched):")
    for movie in itemNames:
        rating = int(input(f"Rate '{movie}': "))
        if rating != 0:
            user_ratings[movie] = rating
    return user_ratings

# Get user ratings interactively
user_ratings = get_user_ratings()

# Add user's ratings to data
data["User"] = user_ratings
sm = build_similarity_matrix(data)

print("\nRecommended Movies:")
recommendations = recommendation("User", data, sm)
if recommendations:
    for movie in recommendations:
        print(movie)
else:
    print("Infinity War")
