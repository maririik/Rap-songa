import streamlit as st
import pandas as pd
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer

# Load the CSV data
df = pd.read_csv('rap_songs.csv')

# Function to calculate profanity rating based on percentiles
def get_profanity_rating(weight, percentile_25, percentile_50, percentile_75):
    if weight < percentile_25:
        return "Low"
    elif percentile_25 <= weight < percentile_50:
        return "Moderate"
    elif percentile_50 <= weight < percentile_75:
        return "High"
    else:
        return "Very High"

# Sentiment analyzer setup
analyzer = SentimentIntensityAnalyzer()

def analyze_sentiment(lyrics):
    sentiment_score = analyzer.polarity_scores(lyrics)
    if sentiment_score['compound'] >= 0.05:
        return 'Positive'
    elif sentiment_score['compound'] <= -0.05:
        return 'Negative'
    else:
        return 'Neutral'

# Title of the app
st.title("Rap Song Search")

# Create a search bar
song_name_input = st.text_input("Search for a song by name")

# Display song information if found
if song_name_input:
    # Find song(s) based on the input
    search_results = df[df['Song Name'].str.contains(song_name_input, case=False, na=False)]

    if not search_results.empty:
        for index, row in search_results.iterrows():
            st.subheader(f"Song: {row['Song Name']}")
            st.write(f"Lyrics: {row['Lyrics']}")
            st.write(f"Topics: {', '.join(eval(row['Topics']))}")
            st.write(f"Profanity List: {', '.join(eval(row['Profanity List']))}")
            
            # Calculate the profanity rating based on percentiles
            profanity_percentiles = df['Profanity Weighting'].quantile([0.25, 0.50, 0.75])
            profanity_rating = get_profanity_rating(row['Profanity Weighting'], 
                                                    profanity_percentiles[0.25], 
                                                    profanity_percentiles[0.50], 
                                                    profanity_percentiles[0.75])
            st.write(f"Profanity Rating: {profanity_rating}")
            
            # Display sentiment score
            sentiment_score = analyze_sentiment(row['Lyrics'])
            st.write(f

