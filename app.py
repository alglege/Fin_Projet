from flask import Flask, request, render_template
import pandas as pd
from textblob import TextBlob
import io

app = Flask(__name__)


def clean_tweet(tweet):
    import re
    tweet = re.sub(r'http\S+', '', tweet)  # Remove URLs
    tweet = re.sub(r'@\w+', '', tweet)  # Remove mentions
    tweet = re.sub(r'#', '', tweet)  # Remove hashtags
    tweet = re.sub(r'\W', ' ', tweet)  # Remove special characters
    tweet = re.sub(r'\s+', ' ', tweet)  # Remove extra spaces
    tweet = tweet.lower()  # Convert to lowercase
    return tweet


def analyze_sentiment(tweet):
    analysis = TextBlob(tweet)
    if analysis.sentiment.polarity > 0:
        return 'Positive'
    elif analysis.sentiment.polarity == 0:
        return 'Neutre'
    else:
        return 'Negative'


@app.route('/', methods=['GET'])
def index():
    return render_template('index.html', results=None)


@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return render_template('index.html', results=None)
    file = request.files['file']
    if file.filename == '':
        return render_template('index.html', results=None)

    df = pd.read_csv(file)
    results = []

    if 'text' in df.columns:
        df['cleaned_tweet'] = df['text'].apply(clean_tweet)
        df['sentiment'] = df['cleaned_tweet'].apply(analyze_sentiment)
        results = df[['text', 'cleaned_tweet', 'sentiment']].values.tolist()

    return render_template('index.html', results=results)


if __name__ == '__main__':
    app.run(debug=True)
