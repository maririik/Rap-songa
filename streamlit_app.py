import streamlit as st
import pandas as pd
from collections import Counter

# Load the dataset
df = pd.read_csv('rap_songs_with_sentiment_updated.csv')

# Function to get percentile-based profanity rating
def get_profanity_rating(profanity_weighting, p25, p50, p75):
    if profanity_weighting <= p25:
        return 'Low profanity'
    elif profanity_weighting <= p50:
        return 'Moderate profanity'
    elif profanity_weighting <= p75:
        return 'High profanity'
    else:
        return 'Very High profanity'

# Calculate percentiles for profanity weighting
p25 = df['profanity weighting (%)'].quantile(0.25)
p50 = df['profanity weighting (%)'].quantile(0.50)
p75 = df['profanity weighting (%)'].quantile(0.75)

# Title of the app
st.title("Rap Song Profanity & Sentiment Analyzer")

# Search bar for song title
search_query = st.text_input("Search for a rap song by title")

if search_query:
    # Filter the dataframe for the searched song
    song_data = df[df['title'].str.contains(search_query, case=False, na=False)]

    if not song_data.empty:
        # Display results for each matching song
        for index, song in song_data.iterrows():
            st.subheader(f"Song: {song['title']}")
            st.text(f"Artist: {song['artist']}")
            st.text(f"Year: {song['year']}")
            st.text(f"Views: {song['views']:,}")

            # Display profanity information
            st.text(f"Profane words detected: {song['profanity detected']}")
            st.text(f"Profanity percentage: {song['profanity weighting (%)']}%")
            rating = get_profanity_rating(song['profanity weighting (%)'], p25, p50, p75)
            st.text(f"Profanity rating: {rating}")

            # Display sentiment information
            sentiment = "Positive" if song['sentiment_score'] > 0 else "Negative"
            st.text(f"Sentiment score: {song['sentiment_score']} ({sentiment})")

            # Display topics
            st.text(f"Topics: {song['Topic']}")

    else:
        st.error("No song found with that title. Please try again.")

# Analyze profane words across all songs
profanity_counter = Counter()

# Assuming "profanity detected" column contains a string of profane words separated by spaces
df['profanity detected'].dropna().apply(lambda x: profanity_counter.update(x.split()))

# Get the top 5 most common profane words
top_5_profanities = profanity_counter.most_common(5)

# Display the top 5 profane words
st.header("Top 5 Profane Words Across All Songs")
for word, count in top_5_profanities:
    st.text(f"{word}: {count} occurrences")
