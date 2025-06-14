FROM python:3.9-slim

RUN apt update && apt install -y git ffmpeg libsm6 libxext6 libgl1 && \
    pip install realesrgan flask opencv-python

WORKDIR /app
COPY . .

EXPOSE 5000
CMD ["python", "server.py"]
