# 🎶 Lyrics Explorer  

An interactive **Streamlit** application to explore song lyrics, albums, and tracks.  
It allows you to analyze lyrics with **Word Clouds**, frequency counts, keyword search, and sentiment analysis.  

## 🚀 Features  

- **Dynamic selection** of albums and tracks from the `lyrics.csv` dataset  
- **Word Cloud** showing the most frequent words in an album  
- **Word frequency counts** with table and heatmap visualization  
- **Full lyrics display** for each track  
- **Text search** across all lyrics  
- **Sentiment analysis** per album with timeline evolution  
- **Main themes identification** based on top frequent words  
- **Interactive visualizations** using Matplotlib, Seaborn, and Plotly  

## 🛠️ Tech Stack  

- [Streamlit](https://streamlit.io/) – interactive web UI  
- [Pandas](https://pandas.pydata.org/) – dataset handling and manipulation  
- [WordCloud](https://github.com/amueller/word_cloud) – word cloud generation  
- [Matplotlib](https://matplotlib.org/) & [Seaborn](https://seaborn.pydata.org/) – static charts and heatmaps  
- [Plotly](https://plotly.com/python/) – interactive plots  
- [TextBlob](https://textblob.readthedocs.io/en/dev/) – sentiment analysis  
- Regex & **Counter** – text preprocessing and frequency analysis  

## 📂 Dataset  

The project uses a CSV file (`lyrics.csv`) with at least the following columns:  
- `album` – album name  
- `track` – track title  
- `lyrics` – song lyrics  

## ▶️ How to Run  

Clone the repository and make sure you have Python 3.x installed.  

```bash
git clone https://github.com/your-username/lyrics-explorer.git
cd lyrics-explorer
