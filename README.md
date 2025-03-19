# Cahtttty

This project is an AI-powered chatbot built using Django. The Chatttty allows users to send messages and receive responses from a LLM model and interactive conversations.

Note: Now app are using just Mistral model.

## Quick start
Note: To run locally first set `DEBUG=True` in `chatttty/
settings.py` Also provide a Mistral API key as an environment variable `MISTRAL_API_KEY`.
### Linux:
```bash
    python3 -m venv env
    source /env/bin/activate
    ./build.sh
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
- [ ] Dockerize
- [ ] Better showing message like code and others
- [ ] Attaching photos and files
- [ ] Maybe using React!
