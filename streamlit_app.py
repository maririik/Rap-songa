import streamlit as st
import pandas as pd
from collections import Counter
import ast

df = pd.read_csv('rap_songs_with_sentiment_updated.csv')

def get_profanity_rating(profanity_weighting, p25, p50, p75):
    if profanity_weighting <= p25:
        return 'Low profanity'
    elif profanity_weighting <= p50:
        return 'Moderate profanity'
    elif profanity_weighting <= p75:
        return 'High profanity'
    else:
        return 'Very High profanity'

p25 = df['profanity weighting (%)'].quantile(0.25)
p50 = df['profanity weighting (%)'].quantile(0.50)
p75 = df['profanity weighting (%)'].quantile(0.75)

st.title("Rap Song Profanity & Sentiment Analyzer")

search_query = st.text_input("Search for a rap song by title")

if search_query:
    song_data = df[df['title'].str.contains(search_query, case=False, na=False)]

    if not song_data.empty:
        for index, song in song_data.iterrows():
            st.subheader(f"Song: {song['title']}")
            st.text(f"Artist: {song['artist']}")
            st.text(f"Year: {song['year']}")
            st.text(f"Views: {song['views']:,}")

            detected_profanity = ast.literal_eval(song['profanity detected']) if song['profanity detected'].startswith('[') else song['profanity detected'].split()
            detected_profanity = set(detected_profanity)  # Remove duplicates
            st.text(f"Profane words detected: {' '.join(detected_profanity)}")
            st.text(f"Profanity percentage: {song['profanity weighting (%)']}%")
            rating = get_profanity_rating(song['profanity weighting (%)'], p25, p50, p75)
            st.text(f"Profanity rating: {rating}")

            sentiment = "Positive" if song['sentiment_score'] > 0 else "Negative"
            st.text(f"Sentiment score: {song['sentiment_score']} ({sentiment})")
            st.text(f"Topics: {song['Topic']}")

    else:
        st.error("No song found with that title. Please try again.")


