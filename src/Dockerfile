# DockerFile for IITB OCR API
# Run the file

FROM python:3.8

RUN git clone https://github.com/gamingflexer/DocTR_Indic_OCR_API.git /data/app

WORKDIR /data
WORKDIR /data/app/src/
RUN git clone https://github.com/kasuba-badri-vishal/doctr-iitb.git

RUN pip install -r requirements.txt
RUN pip install python-doctr
RUN pip install "python-doctr[torch]"

RUN apt update && apt install -y curl
RUN apt-get install ffmpeg libsm6 libxext6  -y

EXPOSE 5000

# intialize the db
CMD ["python3","init_db.py"]
#download the models
CMD ["python3","download.py"]
CMD ["python3","app.py"]