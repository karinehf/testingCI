FROM python:3.8
COPY . /app
WORKDIR /app
RUN pip install -r requirements.txt
#ENTRYPOINT ["python"]
#CMD ["app.py"]
CMD ["gunicorn","-b", "0.0.0.0:4000", "app:app", "--log-level", "debug"]