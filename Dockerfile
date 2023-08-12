from python:3.10

# Create a non-root user and switch to it
RUN useradd -m reddit
USER reddit

RUN apt-get update && \
    apt-get install -y pip

# Copy just the requirements file and install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt && \
    python -m spacy download en_core_web_trf


# Copy the rest of the application
COPY app.py templates ./

# Environment variables for Flask to run (consider using environment variables for CLIENT_ID and CLIENT_SECRET)
ENV FLASK_APP=app.py \
    FLASK_RUN_HOST=0.0.0.0 

# CLIENT_ID=VfcL89ypgv4EnA4yyZmt3Q \
# CLIENT_SECRET=NigUGHSeQesXowLNtvXabg_wAfyJFQ

# Expose the Flask port
EXPOSE 5000

# Use Flask command to run the app
ENTRYPOINT ["flask", "run"]


