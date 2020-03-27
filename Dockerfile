FROM python:3.7-slim
COPY . /
RUN pip install -r ./requirements.txt

# CMD ["python", "app.py"]

# CMD ["gunicorn", "-c", "gunicorn.conf.py", "app:app"]
CMD [\
"gunicorn", \
"-b", "0.0.0.0:5000", \
"app:app", \
"--workers", "5", \
"--threads", "2", \
"--worker-connections", "1000", \
"--worker-class", "gevent", \
"--log-level", "info", \
"--capture-output", \
"--error-logfile", "-", \
"--timeout", "300" \
]