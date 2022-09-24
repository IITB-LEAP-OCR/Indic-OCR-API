import wget,os
from config import modelpath

links = ['https://github.com/kasuba-badri-vishal/doctr-iitb/releases/download/Indic_Models/crnn_vgg16_bn_bengali.pt','https://github.com/kasuba-badri-vishal/doctr-iitb/releases/download/Indic_Models/crnn_vgg16_bn_devanagari.pt','https://github.com/kasuba-badri-vishal/doctr-iitb/releases/download/Indic_Models/crnn_vgg16_bn_gujarati.pt','https://github.com/kasuba-badri-vishal/doctr-iitb/releases/download/Indic_Models/crnn_vgg16_bn_gurumukhi.pt','https://github.com/kasuba-badri-vishal/doctr-iitb/releases/download/Indic_Models/crnn_vgg16_bn_kannada.pt','https://github.com/kasuba-badri-vishal/doctr-iitb/releases/download/Indic_Models/crnn_vgg16_bn_odia.pt','https://github.com/kasuba-badri-vishal/doctr-iitb/releases/download/Indic_Models/crnn_vgg16_bn_tamil.pt','https://github.com/kasuba-badri-vishal/doctr-iitb/releases/download/Indic_Models/crnn_vgg16_bn_telugu.pt','https://github.com/kasuba-badri-vishal/doctr-iitb/releases/download/Indic_Models/crnn_vgg16_bn_urdu.pt']

download_folder = os.path.join(modelpath, 'recognition', 'handwritten')

for link in links:
    wget.download(link, download_folder)
    
print("Downloaded all models")
