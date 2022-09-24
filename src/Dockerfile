# DockerFile for IITB OCR API
# Run the file

FROM python:3.8

RUN git clone https://github.com/gamingflexer/DocTR_Indic_OCR_API.git
WORKDIR /app/src
COPY requirements.txt /app/src/
COPY . /DocTR_Indic_OCR_API/src/

RUN dir -s  
RUN pip install -r requirements.txt
RUN pip install python-doctr
RUN pip install "python-doctr[torch]"

RUN apt update && apt install -y curl

ENTRYPOINT ["python"]
CMD ["app.py"]