# DockerFile for IITB OCR API
# Run the file

FROM python:3.8

RUN git clone https://github.com/gamingflexer/DocTR_Indic_OCR_API.git /data/app

WORKDIR /data
WORKDIR /data/app/src/
RUN pwd

RUN pip install -r requirements.txt
RUN pip install python-doctr
RUN pip install "python-doctr[torch]"

RUN apt update && apt install -y curl

EXPOSE 5000

ENTRYPOINT ["python3"]
CMD "init_db.py"
CMD "app.py"