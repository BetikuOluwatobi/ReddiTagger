# ReddiTagger: Named Entity Recognition and Sentiment Analysis with spaCy and Flair

ReddiTagger is a comprehensive project built to analyze Reddit data, extracting named entities using the `en_core_web_trf` spaCy model, and performing sentiment classification using the Flair library. The tool can be visualized using Dash.

## Features

- **Entity Extraction**: Uses spaCy's Transformer model (`en_core_web_trf`) for high-accuracy named entity recognition.
- **Sentiment Classification**: Applies the Flair library to assign sentiment scores.
- **Data Visualization**: Utilizes Dash to create an interactive dashboard showcasing entity sentiments.
- **Authentication**: Seamless Reddit OAuth authentication to access data.

## Setting Up & Running

### Prerequisites

Make sure you have Python 3.x installed.


### Installation

1. Clone the repository:
```
git clone https://github.com/BetikuOluwatobi/ReddiTagger.git
```

2. Create and Activate a Virtual Environment:
 ```bash
 python3 -m venv myenv
 source venv/bin/activate
 ```

3. Navigate to the project directory:
```
cd ReddiTagger
```

4. Install the required libraries:
```
pip install -r requirements.txt
```

5. Download the required spaCy model:
```
python -m spacy download en_core_web_trf
```

6. Set your environment variables for `CLIENT_ID`, `CLIENT_SECRET`, and `REDIRECT_URI`. These will be used for Reddit API access.
   
7. Also, set the `redirect_url=http://localhost:5000/callback` in your Reddit app.

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

### Docker Installation

**Note**: The Docker image is around 7GB, so it might take a while to build.

1. **Build the Docker Image**

    ```bash
    docker build -t redditagger .
    ```

2. **Run the Docker Container**

    Make sure to replace `<YOUR_CLIENT_ID>` and `<YOUR_CLIENT_SECRET>` with your Reddit application credentials.

    ```bash
    docker run -d -p 5000:5000 -e CLIENT_ID=<YOUR_CLIENT_ID> -e CLIENT_SECRET=<YOUR_CLIENT_SECRET> redditagger
    ```

**Tip**: You can obtain `CLIENT_ID` and `CLIENT_SECRET` from the Reddit App Preferences: `reddit.com/prefs/apps`. If you haven't created a Reddit App yet, you'll need to do so. The `CLIENT_ID` and `CLIENT_SECRET` are found under the newly created app's details.

## Embedded Video Tutorial
For a comprehensive walkthrough of the ReddiTagger application and to understand its functionalities better, check out the embedded video tutorial available on YouTube: [ReddiTagger Part 1](https://youtu.be/XQZ4CF-KoDc)
[ReddiTagger Part 2](https://youtu.be/gRfhRyPEqWI)

## Contributing

Feel free to fork this repository, make your changes, and submit a pull request. Feedback, issues, and contributions are highly appreciated!

## License

This project is open source, under the MIT license.

---

Enjoy using ReddiTagger and gain insights from the vast world of Reddit data!
