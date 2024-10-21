import streamlit as st
import pandas as pd

# Load the dataset directly from GitHub
url = 'https://blank-app-y3xmzfrp2f.streamlit.app/'
df = pd.read_csv(url)

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

# Function to extract unique profane words for each song
def get_unique_profanities(profanity_list):
    if isinstance(profanity_list, str):
        # Convert the string representation of the list into an actual list
        profanity_words = eval(profanity_list)
        return list(set(profanity_words))
    return []

# Apply the function to get unique profane words
df['unique_profanities'] = df['profanity detected'].apply(get_unique_profanities)

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
            st.text(f"Profane words detected: {song['unique_profanities']}")
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
else:
    st.info("Please enter a song title to search.")
