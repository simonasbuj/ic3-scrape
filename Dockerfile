FROM python:3.11-slim

WORKDIR /app
COPY . /app

# install dependencies using poetry
RUN pip install poetry 
RUN poetry install --no-root --no-dev

CMD ["poetry", "run", "python", "main.py"]