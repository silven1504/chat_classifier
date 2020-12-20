FROM jupyter/datascience-notebook:python-3.7.6

RUN pip3 install pipenv

ENV PROJECT_DIR /usr/src/classifier

WORKDIR ${PROJECT_DIR}

COPY Pipfile .
COPY Pipfile.lock .
COPY *.py ./
COPY tf_model.h5 .
COPY tokens.json .


RUN pipenv install --deploy --ignore-pipfile

EXPOSE 8080

CMD ["pipenv", "run", "uvicorn", "api:app", "--host", "0.0.0.0", "--port", "8080"]
