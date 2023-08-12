# ReddiTagger: Named Entity Recognition and Sentiment Analysis with spaCy and Flair

ReddiTagger is a comprehensive project built to analyze Reddit data, extracting named entities using the `en_core_web_trf` spaCy model, and performing sentiment classification using the Flair library. The tool can be visualized using Dash.

## Features

- **Entity Extraction**: Uses spaCy's Transformer model (`en_core_web_trf`) for high-accuracy named entity recognition.
- **Sentiment Classification**: Applies the Flair library to assign sentiment scores.
- **Data Visualization**: Utilizes Dash to create an interactive dashboard showcasing entity sentiments.

## Setting Up & Running

### Prerequisites

Ensure you have Python and pip installed.

### Installation

1. Clone the repository:
```
git clone <repository-url>
```

2. Navigate to the project directory:
```
cd ReddiTagger
```

3. Install the required libraries:
```
pip install os requests pandas numpy dash spacy plotly dash-bootstrap-components flair flask flask_caching flask_wtf wtforms
```

4. Download the required spaCy model:
```
python -m spacy download en_core_web_trf
```

5. Set your environment variables for `CLIENT_ID`, `CLIENT_SECRET`, and `REDIRECT_URI`. These will be used for Reddit API access.

### Running the Application

Execute the script:
```
python app.py
```

Then, navigate to `http://localhost:5000/` on your browser to use the ReddiTagger dashboard.

## Usage

1. **Homepage**: Start by authenticating with Reddit. This uses OAuth2 to securely access the Reddit API.
2. **Authenticate**: Select a subreddit and entity type (like Organization, Location, or Country/State) you want to analyze.
3. **Dashboard**: View the interactive charts showing entity sentiments. Adjust the sentiment score slider to filter entities based on their sentiment scores.

## Embedded Video Tutorial
For a comprehensive walkthrough of the ReddiTagger application and to understand its functionalities better, check out the embedded video tutorial available on YouTube: [ReddiTagger Part 1](https://youtu.be/XQZ4CF-KoDc)
[ReddiTagger Part 2](https://youtu.be/gRfhRyPEqWI)

## Contributing

Feel free to submit issues, pull requests, or feature suggestions.

## License

This project is open source, under the MIT license.

---

Enjoy using ReddiTagger and gain insights from the vast world of Reddit data!

