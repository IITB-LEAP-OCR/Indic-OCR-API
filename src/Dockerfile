# DockerFile for IITB OCR API
# Run the file

FROM python:3.8

RUN git clone https://github.com/gamingflexer/DocTR_Indic_OCR_API.git
WORKDIR DocTR_Indic_OCR_API
WORKDIR src

RUN pip install -r requirements.txt
RUN pip install python-doctr
RUN pip install "python-doctr[torch]"

RUN apt update && apt install -y curl

ENTRYPOINT ["python"]
CMD ["app.py"]