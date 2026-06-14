
FROM python:3.12
WORKDIR /copy
COPY ./requirements.txt /copy/requirements.txt
RUN pip install --no-cache-dir -r /copy/requirements.txt
COPY . /copy/
CMD ["fastapi","run","main.py","--port","80"]

