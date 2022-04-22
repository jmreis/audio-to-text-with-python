FROM python:3.9.12-slim-buster
LABEL author="Jair Reis"
LABEL description="For run the audiototxt.py"
WORKDIR /app
COPY . /app
RUN apt update -y && apt upgrade -y
RUN apt install -y ffmpeg
RUN pip install -r /app/requirements.txt
CMD ["python3"]