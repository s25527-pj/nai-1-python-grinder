import pandas as pd
from sklearn.cluster import KMeans
from sklearn.preprocessing import LabelEncoder, StandardScaler

# Load data
file_path = 'rated_movies.xlsx'  # Replace with your file path
data = pd.ExcelFile(file_path)
df = data.parse('Sheet1')

# Fill missing values in "Subgenre" with a default value
df['Subgenre'] = df['Subgenre'].fillna('Brak subgatunku')

# Encode "Genre" and "Subgenre"
label_encoder_genre = LabelEncoder()
label_encoder_subgenre = LabelEncoder()

df['Genre_encoded'] = label_encoder_genre.fit_transform(df['Genre'])
df['Subgenre_encoded'] = label_encoder_subgenre.fit_transform(df['Subgenre'])

# Scale numerical data (Rating, Genre_encoded, Subgenre_encoded)
scaler = StandardScaler()
scaled_features = scaler.fit_transform(df[['Rating', 'Genre_encoded', 'Subgenre_encoded']])

# Perform clustering
kmeans = KMeans(n_clusters=5, random_state=42, n_init=10)
df['Cluster'] = kmeans.fit_predict(scaled_features)


# Recommendation function
def recommend_movies(user, df, top_n=5):
    """
    Recommends movies for a given user based on their previous ratings.
    Suggests movies to watch and avoid based on clustering and user preferences.

    Args:
        user (str): The user's name.
        df (pd.DataFrame): The dataset containing movie ratings and clusters.
        top_n (int): Number of recommendations to provide.

    Returns:
        dict: Recommended and avoid movie lists with reasons.
    """
    # Filter user data and calculate cluster preference
    user_data = df[df['Reviewer'] == user]
    cluster_means = user_data.groupby('Cluster')['Rating'].mean()

    # Find clusters to recommend and avoid
    recommended_clusters = cluster_means.nlargest(2).index
    avoided_clusters = cluster_means.nsmallest(2).index

    # Recommend movies the user has not rated in recommended clusters
    watched_movies = user_data['Movie'].tolist()
    recommend_movies = df[~df['Movie'].isin(watched_movies) & df['Cluster'].isin(recommended_clusters)]
    avoid_movies = df[~df['Movie'].isin(watched_movies) & df['Cluster'].isin(avoided_clusters)]

    # Generate reasons for recommendation and avoidance only for the top_n recommendations
    recommendations_reasons = {}
    for movie in recommend_movies['Movie'].head(top_n):
        movie_cluster = df[df['Movie'] == movie]['Cluster'].values[0]
        reasons = f"Recommended because it belongs to a cluster ({movie_cluster}) with a high average rating by {user}."
        recommendations_reasons[movie] = reasons

    avoidance_reasons = {}
    for movie in avoid_movies['Movie'].head(top_n):
        movie_cluster = df[df['Movie'] == movie]['Cluster'].values[0]
        reasons = f"Avoided because it belongs to a cluster ({movie_cluster}) with a low average rating by {user}."
        avoidance_reasons[movie] = reasons

    return {
        'recommend': recommend_movies['Movie'].head(top_n).tolist(),
        'avoid': avoid_movies['Movie'].head(top_n).tolist(),
        'recommend_reasons': recommendations_reasons,
        'avoid_reasons': avoidance_reasons
    }


# Example usage
user = input("Please enter your name to get movie recommendations: ")
recommendations = recommend_movies(user, df)
print(f"Recommendations for {user}:")
print("Recommended Movies:", recommendations['recommend'])
print("Movies to Avoid:", recommendations['avoid'])
print("=======================")
print("Reasons for Recommendation:")
for movie, reason in recommendations['recommend_reasons'].items():
    print(f"{movie}: {reason}")

print("\nMovies to Avoid:", recommendations['avoid'])
print("Reasons for Avoidance:")
for movie, reason in recommendations['avoid_reasons'].items():
    print(f"{movie}: {reason}")

print("========================")
cluster_1_movies = df[df['Cluster'] == 1]

print("Movies in cluster 1:")
print(cluster_1_movies[['Movie', 'Genre', 'Subgenre']])

cluster_1_mean_rating = cluster_1_movies['Rating'].mean()
print(f"\nAverage rating for cluster 1: {cluster_1_mean_rating}")