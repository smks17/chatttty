# Cahtttty

# Chatttty - AI-powered Chatbot

Chatttty is a web-based chatbot application built with Django. It leverages Django's robust web framework to create a simple and efficient API for interacting with users through a chat interface.

## Features
- AI-powered responses via Mistral model
- Local development setup with Docker support
- Easy setup and deployment using Django
- Support for expanding with additional models in the future

## Requirements
- Python 3.x
- Django
- Mistral API key

Note: Now app are using just Mistral model.

## Installation

### Clone the repository:
```bash
git clone https://github.com/smks17/chatttty.git
cd chatttty
```

### Set up the environment:
1 - Copy `.env.example` to `.env` and provide necessary values.

2 - Install dependencies:
```bash
pip install -r requirements.txt
```

3 - Apply migrations:
```bash
python manage.py migrate
```


### Running the app:
### Linux:
```bash
    python3 -m venv env
    source /env/bin/activate
    ./build.sh
    python3 manage.py migrate
    python3 manage.py runserver
```

### Windows
```powershell
    python3 -m venv env
    source /env/bin/Activate.ps1
    pip install -r requirements.txt
    python manage.py collectstatic --no-input
    python manage.py migrate
    python3 manage.py runserver
```


## TODO
- [ ] Adding more models
- [ ] Adding model settings
- [x] Sending stream https response
- [ ] Temporarily chat
- [ ] Adding fine tuning
- [x] Dockerize
- [ ] Better showing message like code and others
- [ ] Attaching photos and files
- [ ] Maybe using React!
