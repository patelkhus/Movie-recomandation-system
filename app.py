from flask import Flask, render_template, request
import pandas as pd

app = Flask(__name__)

# Load CSV
df = pd.read_csv('bollywood_movies.csv')
print("Available columns:", df.columns.tolist())  # Debug

# Drop rows with missing titles
df.dropna(subset=['title'], inplace=True)


# Function: recommend top 5 movies closest in year with highest rating
def recommend(title):
    title = title.strip().lower()
    movies = df[df['title'].str.lower() == title]

    if movies.empty:
        return ["Movie not found. Try another title."]

    year = movies.iloc[0]['year']

    # Recommend 5 movies closest in year, sorted by rating
    df['year_diff'] = abs(df['year'] - year)
    recommendations = df[df['title'].str.lower() != title]
    recommendations = recommendations.sort_values(by=['year_diff', 'rating'], ascending=[True, False])

    return recommendations['title'].head(5).tolist()


# Routes
@app.route('/')
def index():
    return render_template('index.html', titles=df['title'].tolist())


@app.route('/recommend', methods=['POST'])
def recommend_route():
    movie = request.form['movie']
    recommendations = recommend(movie)
    return render_template('result.html', movie=movie, recommendations=recommendations)


if __name__ == '__main__':
    app.run(debug=True)
