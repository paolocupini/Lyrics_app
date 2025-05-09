import streamlit as st
import pandas as pd
from wordcloud import WordCloud, STOPWORDS
import matplotlib.pyplot as plt
from collections import Counter
import re
import seaborn as sns
from textblob import TextBlob
import plotly.express as px

# datset
@st.cache_data
def load_data():
    return pd.read_csv("lyrics.csv")

df = load_data()

# Stopwords
stopwords = set(STOPWORDS)
stopwords.update({"s", "t", "re", "ll"})

# select album
album_list = df['album'].unique()
selected_album = st.sidebar.selectbox("Select album", album_list)

# select track
track_list = df[df['album'] == selected_album]['track'].unique()
selected_track = st.sidebar.selectbox("Select track", track_list)

# Lyrics
track_lyrics = df[(df['album'] == selected_album) & (df['track'] == selected_track)]['lyrics'].values[0]


st.title(f"Lyrics Explorer - {selected_album}")

# Tabs
tab1, tab2 = st.tabs(["Album Analysis", "Advanced Analysis"])


with tab1:
    # Word Cloud
    album_lyrics = df[df['album'] == selected_album]['lyrics'].str.cat(sep=' ')
    st.subheader("Album Word Cloud")
    wordcloud = WordCloud(width=800, height=400, background_color='white', stopwords=stopwords).generate(album_lyrics)
    fig, ax = plt.subplots(figsize=(10, 5))
    ax.imshow(wordcloud, interpolation='bilinear')
    ax.axis("off")
    st.pyplot(fig)


    st.subheader("Album frequent words")
    def get_top_words(text, num=15):
        words = re.findall(r'\b\w+\b', text.lower())
        words = [w for w in words if w not in stopwords]
        return Counter(words).most_common(num)

    top_words = get_top_words(album_lyrics)
    freq_df = pd.DataFrame(top_words, columns=['Word', 'Frequency'])
    st.dataframe(freq_df)

    st.subheader(f"Full lyric: {selected_track}")
    st.text_area(label="", value=track_lyrics, height=300)

with tab2:
    # keyword search
    st.subheader("Search for a word in the lyrics")
    search_word = st.text_input("Insert word")

    if search_word:
        matches = df[df['lyrics'].str.contains(search_word, case=False, na=False)]
        st.write(f"Found **{len(matches)}** tracks cotaining '{search_word}':")
        st.dataframe(matches[['album', 'track']])


    st.subheader("Counting frequencies")
    word_input = st.text_input("Insert words separated by a comma", "love,death,life")

    if word_input:
        words_to_count = [w.strip().lower() for w in word_input.split(',')]
        count_data = []
        for album in df['album'].unique():
            lyrics_text = " ".join(df[df['album'] == album]['lyrics'].dropna())
            words = re.findall(r'\b\w+\b', lyrics_text.lower())
            total = Counter(words)
            counts = [total[word] for word in words_to_count]
            count_data.append([album] + counts)

        count_df = pd.DataFrame(count_data, columns=["Album"] + words_to_count)
        st.dataframe(count_df)

        # Heatmap
        st.subheader("Word Heatmap")
        heat_data = count_df.set_index("Album")
        fig, ax = plt.subplots(figsize=(10, 6))
        sns.heatmap(heat_data, annot=True, cmap="YlGnBu", linewidths=.5, ax=ax)
        st.pyplot(fig)

    # Timeline
    st.subheader("Sentiment and Topic evolution")
    sentiment_data = []
    for i, album in enumerate(df['album'].unique(), start=1):
        album_df = df[df['album'] == album]
        lyrics_text = " ".join(album_df['lyrics'].dropna())

        # Sentiment
        polarity = TextBlob(lyrics_text).sentiment.polarity

        # Topics
        words = re.findall(r'\b\w+\b', lyrics_text.lower())
        words = [w for w in words if w not in stopwords]
        themes = ", ".join([word for word, _ in Counter(words).most_common(3)])

        sentiment_data.append({
            'Album': album,
            'Ordine': i,
            'Sentiment': polarity,
            'Temi': themes
        })

    timeline_df = pd.DataFrame(sentiment_data)

    fig = px.scatter(
        timeline_df,
        x="Ordine",
        y="Sentiment",
        text="Album",
        hover_data=["Temi"],
        title="Sentiment and Topic evolution",
        labels={"Order": "Dataset Order", "Sentiment": "Mood (Polarity)"},
        size=[15] * len(timeline_df),
        color="Sentiment",
        color_continuous_scale="RdBu"
    )

    fig.update_traces(textposition='top center')
    fig.update_layout(height=500, xaxis=dict(tickmode='linear'))
    st.plotly_chart(fig, use_container_width=True)
