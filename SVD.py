import numpy as np
from numpy.linalg import svd

# Sample movie ratings data
data = {
    "Mike": {
        "Interstellar": 4,
        "The Dark Knight": 5,
        "Wanted": 3,
        "Sucker Punch": 2,
        "Inception": 5,
        "The Conjuring": 3,
        "21 Jump Street": 4,
        "The Prestige": 5
    },
    "Jason": {
        "Interstellar": 5,
        "The Dark Knight": 5,
        "Wanted": 1,
        "Devil": 3,
        "The Conjuring": 1,
        "21 Jump Street": 4,
        "Men in Black": 2
    },
    "Bob": {
        "Hot Tub Time Machine": 1,
        "Inception": 5,
        "Revenant": 3,
        "Avengers 1": 4,
        "Iron Man 2": 3,
        "Batman v Superman": 5,
        "Wanted": 4,
    },
    "Owen": {
        "Inception": 5,
    },
    "Mark": {
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
    "Jill": {
        "Inception": 5,
        "The Conjuring": 4
    },
    "Rachel": {
        "Twilight": 1
    }
}

# List of all movie names
itemNames = [
    "Interstellar", "The Dark Knight", "Wanted", "Sucker Punch", "Inception",
    "The Conjuring", "21 Jump Street", "The Prestige", "Devil", "Men in Black",
    "Hot Tub Time Machine", "Revenant", "Avengers 1", "Iron Man 2",
    "Batman v Superman", "Avengers 2", "The Departed", "Fight Club",
    "Vampires Suck", "Twilight", "Notebook", "The Terminal", "The Vow", "Focus"
]

def build_user_item_matrix(data):
    # Create empty user-item matrix
    user_item_matrix = np.zeros((len(data), len(itemNames)))
    
    # Map user and item indices
    user_index = {user: idx for idx, user in enumerate(data.keys())}
    item_index = {item: idx for idx, item in enumerate(itemNames)}
    
    # Fill user-item matrix with ratings
    for user, ratings in data.items():
        for item, rating in ratings.items():
            user_item_matrix[user_index[user], item_index[item]] = rating
    
    return user_item_matrix, user_index, item_index

def recommend_movies(user_item_matrix, user_index, item_index, user, num_recommendations=5):
    # Perform SVD on the user-item matrix
    U, sigma, Vt = svd(user_item_matrix, full_matrices=False)
    
    # Calculate predicted ratings for the user
    user_row = user_index[user]
    user_ratings = U[user_row, :] @ np.diag(sigma) @ Vt
    
    # Find movies not rated by the user
    rated_indices = np.where(user_item_matrix[user_row, :] != 0)[0]
    unrated_indices = np.where(user_item_matrix[user_row, :] == 0)[0]
    
    # Sort unrated movies by predicted ratings
    sorted_indices = np.argsort(user_ratings[unrated_indices])[::-1]
    recommended_indices = unrated_indices[sorted_indices][:num_recommendations]
    
    # Map indices back to movie names
    recommended_movies = [itemNames[idx] for idx in recommended_indices]
    
    return recommended_movies

# Build user-item matrix
user_item_matrix, user_index, item_index = build_user_item_matrix(data)

# Recommend movies for user "Jatin"
user = "Mark"
recommended_movies = recommend_movies(user_item_matrix, user_index, item_index, user)

print(f"Recommendations for {user}:")
for movie in recommended_movies:
    print(movie)
