FROM python:3-slim-bullseye
WORKDIR /app
COPY ./src/requirements.txt /app/requirements.txt
RUN pip install --no-cache-dir --upgrade pip
RUN pip install --no-cache-dir --upgrade -r /app/requirements.txt
VOLUME ["/app/data"]
COPY ./src /app
EXPOSE 8080
ENV FLASK_APP=app
CMD [ "python", "-m" , "flask", "run", "--host=0.0.0.0", "--port=8080" ]
