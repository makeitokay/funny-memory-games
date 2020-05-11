FROM python:3.7
ENV PYTHONUNBUFFERED 1
ENV PYTHONDONTWRITEBYTECODE 1

COPY . funny-memory-games/
WORKDIR funny-memory-games/

RUN pip install -r requirements.txt
CMD ["python", "main.py"]