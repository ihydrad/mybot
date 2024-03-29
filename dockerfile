FROM python:3.10
WORKDIR /code
COPY . /code
RUN mkdir -p /code/downloads; pip install --no-cache-dir --upgrade -r /code/requirements.txt
ENTRYPOINT [ "python" ] 
CMD [ "rest_api.py"]