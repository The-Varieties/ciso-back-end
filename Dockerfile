FROM python:3.10
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
WORKDIR /code

RUN pip install pipenv 
COPY Pipfile* /code/

# RUN pipenv shell --python 3.10
# RUN pipenv install

RUN pipenv lock --keep-outdated --requirements > /code/requirements.txt
RUN set -ex && pip install --no-cache-dir -r /code/requirements.txt

COPY . /code/

WORKDIR /code/
