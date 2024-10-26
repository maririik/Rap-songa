import streamlit as st
import pandas as pd
from collections import Counter
import ast
import altair as alt

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

# Calculate percentiles for profanity weighting and sentiment score
p25 = df['profanity weighting (%)'].quantile(0.25)
p50 = df['profanity weighting (%)'].quantile(0.50)
p75 = df['profanity weighting (%)'].quantile(0.75)
s25 = df['sentiment_score'].quantile(0.25)
s50 = df['sentiment_score'].quantile(0.50)
s75 = df['sentiment_score'].quantile(0.75)

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

            # Remove brackets, commas, and duplicates from the list of profane words
            detected_profanity = ast.literal_eval(song['profanity detected']) if song['profanity detected'].startswith('[') else song['profanity detected'].split()
            detected_profanity = set(detected_profanity)
            st.text(f"Profane words detected: {' '.join(detected_profanity)}")
            st.text(f"Profanity percentage: {song['profanity weighting (%)']}%")
            rating = get_profanity_rating(song['profanity weighting (%)'], p25, p50, p75)
            st.text(f"Profanity rating: {rating}")

            # Display sentiment information
            sentiment = "Positive" if song['sentiment_score'] > 0 else "Negative"
            st.text(f"Sentiment score: {song['sentiment_score']} ({sentiment})")

            # Plot profanity weighting relative to all songs
            profanity_chart = alt.Chart(df).mark_circle(size=60).encode(
                x=alt.X('profanity weighting (%)', title='Profanity Weighting (%)'),
                y=alt.Y('count()', title='Number of Songs'),
                tooltip=['title', 'profanity weighting (%)']
            ).properties(
                width=600,
                height=300,
                title="Relative Profanity Percentage of Songs"
            ).interactive()

            # Highlight the selected song's profanity score
            highlight = alt.Chart(pd.DataFrame({'profanity weighting (%)': [song['profanity weighting (%)']]})).mark_rule(color='red').encode(
                x='profanity weighting (%)'
            )

            # Display the profanity chart with highlight
            st.altair_chart(profanity_chart + highlight)

            # Plot sentiment score relative to all songs
            sentiment_chart = alt.Chart(df).mark_circle(size=60).encode(
                x=alt.X('sentiment_score', title='Sentiment Score'),
                y=alt.Y('count()', title='Number of Songs'),
                tooltip=['title', 'sentiment_score']
            ).properties(
                width=600,
                height=300,
                title="Relative Sentiment Score of Songs"
            ).interactive()

            # Highlight the selected song's sentiment score
            sentiment_highlight = alt.Chart(pd.DataFrame({'sentiment_score': [song['sentiment_score']]})).mark_rule(color='blue').encode(
                x='sentiment_score'
            )

            # Display the sentiment chart with highlight
            st.altair_chart(sentiment_chart + sentiment_highlight)

    else:
        st.error("No song found with that title. Please try again.")

# Analyze profane words across all songs
profanity_counter = Counter()
df['profanity detected'].dropna().apply(lambda x: profanity_counter.update(ast.literal_eval(x) if x.startswith('[') else x.split()))

# Get the top 5 most common profane words
top_5_profanities = profanity_counter.most_common(5)

# Display the top 5 profane words
st.header("Top 5 Profane Words Across All Songs")
for word, count in top_5_profanities:
    st.text(f"{word}: {count} occurrences")
