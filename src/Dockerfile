# DockerFile for IITB OCR API
# Run the file

FROM python:3.8

# Install Indic Doctr
RUN git clone https://github.com/kasuba-badri-vishal/doctr-iitb.git /doctr_indic
WORKDIR /doctr_indic
RUN pip install python-doctr
RUN pip install "python-doctr[torch]"
RUN pip install -e .

RUN git clone https://github.com/document-analysis-tools/Indic-OCR-API /data/app

WORKDIR /data/app/src/

RUN pip install -r requirements.txt

RUN apt update && apt install -y curl
RUN apt-get install ffmpeg libsm6 libxext6  -y
RUN pip3 install torch torchvision

RUN mkdir models
RUN mkdir uploads

RUN pip3 install wget
RUN python3 setup.py
RUN mv *.pt /data/app/src/models/

EXPOSE 5000
CMD ["python3","app.py"]