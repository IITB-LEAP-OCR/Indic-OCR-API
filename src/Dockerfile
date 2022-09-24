# DockerFile for IITB OCR API
# Run the file

FROM python:3.8

# Install Indic Doctr
RUN git clone https://github.com/kasuba-badri-vishal/doctr-iitb.git /doctr_indic
WORKDIR /doctr_indic
RUN git reset --hard 8b41efc1863bd76657617a40d2c277e156db0803
RUN pip install -e .

RUN git clone https://github.com/gamingflexer/DocTR_Indic_OCR_API.git /data/app

WORKDIR /data
WORKDIR /data/app/src/

RUN pip install -r requirements.txt

RUN apt update && apt install -y curl
RUN apt-get install ffmpeg libsm6 libxext6  -y
RUN pip3 install torch torchvision

RUN python3 init_db.py
RUN python3 setup.py

EXPOSE 5000


CMD ["python3","app.py"]