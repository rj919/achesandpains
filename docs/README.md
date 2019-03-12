# Aches & Pains
_A Health Journaling Bot for HealthHacks 2017 Hackathon_  
**by Jeff & Rich**

## Benefits
- Creates more prevalent and more accurate user health reporting
- Acknowledges and affirms user's desire for their symptoms to be heard

## Project Materials
[GitHub Repo](https://github.com/rj919/achesandpains)

## Features
- Collects user reported conditions through messaging platform
- Extracts snowmed CT codes from user messages
- Saves user reports to EHR platform
- Uses AB testing and cluster analysis to select responses that maximize user compliance

## Requirements
- Python dependencies listed in Dockerfile
- Valid credentials for Telegram & IBM Bluemix

## Components
- Alpine Edge (OS)
- Python 3.5.2 (Environment)
- Gunicorn 19.4.5 (Server)
- Flask 0.11.1 (Framework)
- Gevent 1.1.2 (Thread Manager)
- APScheduler 1.5.0 (Job Scheduler)
- SQLAlchemy 1.1.1 (Database ORM)
- Telegram Bot API (Messaging)
- IBM Watson Speech2Text API (Transcription)

## Dev Env
- Docker (Provisioning)
- Bitbucket (Version Control)
- PyCharm (IDE)
- Dropbox (Sync, Backup)

## Languages
- Python 3.5

Flask Bot References
--------------------
[README-UPSTREAM.md](https://bitbucket.org/collectiveacuity/flaskbotfork/src/master/README-UPSTREAM.md)  
[DOCUMENTATION.md](https://bitbucket.org/collectiveacuity/flaskbotfork/src/master/DOCUMENTATION.md)  
[RESOURCES.md](https://bitbucket.org/collectiveacuity/flaskbotfork/src/master/REFERENCES.md)