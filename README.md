# ReddiTagger: Advanced NER and Sentiment Analysis with spaCy & Flair

Dive deep into Reddit's data with ReddiTagger. Harnessing the prowess of spaCy's `en_core_web_trf` and the sentiment analysis capabilities of Flair, this project is designed to efficiently extract named entities and analyze sentiments. Visual insights are made available via a user-friendly Dash interface.

## Features

- **Entity Extraction**: Lean on the precision of spaCy's Transformer model, `en_core_web_trf`, for top-tier NER.
- **Sentiment Determination**: Exploit Flair's sentiment analysis capabilities to ascertain sentiments.
- **Interactive Data Visualization**: Present the gathered insights through a vibrant Dash dashboard.
- **Secure Authentication**: Leverage Reddit's OAuth for seamless and secure data access.

## Installation & Setup

### Prerequisites

Ensure Python 3.x is installed on your machine.

### Step-by-step Installation

1. **Clone the Repository**:
   ```bash
   git clone https://github.com/BetikuOluwatobi/ReddiTagger.git
   ```

2. **Navigate to the Project Directory**:
   ```bash
   cd ReddiTagger
   ```

3. **Set up a Virtual Environment and Activate It**:
   ```bash
   python3 -m venv myenv
   source myenv/bin/activate
   ```

4. **Install Required Libraries**:
   ```bash
   pip install -r requirements.txt
   ```

5. **Fetch the Essential spaCy Model**:
   ```bash
   python -m spacy download en_core_web_trf
   ```

6. **Environment Variables**: Update your environment with `CLIENT_ID`, `CLIENT_SECRET`, and `REDIRECT_URI` for Reddit API interactions.
   
7. **Reddit App Configuration**: Ensure you've set `redirect_url` to `http://localhost:5000/callback` within your Reddit app.

### Launching the Application

1. Run the following command:
   ```bash
   python app.py
   ```

2. Open a browser and visit `http://localhost:5000/` to experience the ReddiTagger dashboard.

## How to Use

1. **Homepage**: Initiate by authenticating through Reddit using the secure OAuth2 protocol.
2. **Authenticate**: Pick your desired subreddit and specify the entity type (e.g., Organization, Location, Country/State) for analysis.
3. **Dashboard**: Explore interactive visualizations, shedding light on entity sentiments. Fine-tune your view by adjusting the sentiment score slider.

### Docker Setup

> **Heads-up**: The Docker image is sizable (~7GB). Patience is the key during the build.

1. **Craft the Docker Image**:
   ```bash
   docker build -t redditagger .
   ```

2. **Deploy the Docker Container**: Remember to slot in your specific `CLIENT_ID` and `CLIENT_SECRET`.
   ```bash
   docker run -d -p 5000:5000 -e CLIENT_ID=<YOUR_CLIENT_ID> -e CLIENT_SECRET=<YOUR_CLIENT_SECRET> redditagger
   ```

> **Tip**: Procure your `CLIENT_ID` and `CLIENT_SECRET` from the Reddit App Preferences at `reddit.com/prefs/apps`. If you're a first-timer, initiate by creating a Reddit App. Your credentials will be listed under the app's details section.

## Comprehensive Video Walkthrough

For an extensive tutorial on ReddiTagger, we've curated a video series to assist you:
- [ReddiTagger - Introduction & Overview](https://youtu.be/XQZ4CF-KoDc)
- [ReddiTagger - Deep Dive & Features](https://youtu.be/gRfhRyPEqWI)

## Contribution

Your insights can shape ReddiTagger's future! Feel free to fork, tweak, and submit pull requests. We eagerly await your feedback, queries, and contributions.

## Licensing

ReddiTagger is open-sourced under the MIT license.

---

Dive into the ocean of Reddit data with ReddiTagger and unearth exciting insights! 🚀
