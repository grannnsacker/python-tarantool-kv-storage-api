FROM python:3.9

WORKDIR /

RUN mkdir app

COPY requirements.txt /app

RUN pip install -r /app/requirements.txt

COPY app /app

EXPOSE 8000

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
