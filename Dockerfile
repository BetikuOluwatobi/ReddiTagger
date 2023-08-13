from python:3.10

# System update and package installation
RUN apt-get update && \
    apt-get install -y pip

# Create a non-root user and switch to it
RUN useradd -m reddit
USER reddit

# Copy just the requirements file and install Python dependencies
COPY requirements.txt .
RUN pip install --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt && \
    python -m spacy download en_core_web_trf

WORKDIR /usr/src/app/

RUN mkdir templates

# Copy the rest of the application

COPY templates ./templates/
COPY app.py ./


# Environment variables for Flask to run (consider using environment variables for CLIENT_ID and CLIENT_SECRET)
ENV FLASK_APP=app.py \
    FLASK_RUN_HOST=0.0.0.0 

ENV PATH="/home/reddit/.local/bin:${PATH}"

# Expose the Flask port
EXPOSE 5000

# Use Flask command to run the app
ENTRYPOINT ["flask", "run"]

