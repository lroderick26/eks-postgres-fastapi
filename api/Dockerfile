
FROM python:3.9

COPY ./ /app

RUN pip install -r /app/requirements.txt

WORKDIR /app

EXPOSE 8000

CMD [ "uvicorn", "main:app", "--host", "0.0.0.0"]