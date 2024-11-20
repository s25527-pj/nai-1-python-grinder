
import pandas as pd
from sklearn.cluster import KMeans
from sklearn.preprocessing import LabelEncoder, StandardScaler

# Load data
file_path = 'rated_movies.xlsx'  # Replace with your file path
data = pd.ExcelFile(file_path)
df = data.parse('Sheet1')

# Encode genres
label_encoder_genre = LabelEncoder()
df['Genre_encoded'] = label_encoder_genre.fit_transform(df['Genre'])

# Scale numerical data
scaler = StandardScaler()
scaled_features = scaler.fit_transform(df[['Rating', 'Genre_encoded']])

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
        dict: Recommended and avoid movie lists.
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

    return {
        'recommend': recommend_movies['Movie'].head(top_n).tolist(),
        'avoid': avoid_movies['Movie'].head(top_n).tolist()
    }

# Example usage
user = "Benedykt Borowski"
recommendations = recommend_movies(user, df)
print(f"Recommendations for {user}:")
print("Recommended Movies:", recommendations['recommend'])
print("Movies to Avoid:", recommendations['avoid'])