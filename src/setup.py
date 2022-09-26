import wget,os
from config import MODEL_PATH

links = ['https://github.com/kasuba-badri-vishal/doctr-iitb/releases/download/Indic_Models/crnn_vgg16_bn_handwritten_bengali.pt',
'https://github.com/kasuba-badri-vishal/doctr-iitb/releases/download/Indic_Models/crnn_vgg16_bn_handwritten_hindi.pt',
'https://github.com/kasuba-badri-vishal/doctr-iitb/releases/download/Indic_Models/crnn_vgg16_bn_handwritten_gujarati.pt',
'https://github.com/kasuba-badri-vishal/doctr-iitb/releases/download/Indic_Models/crnn_vgg16_bn_handwritten_gurumukhi.pt',
'https://github.com/kasuba-badri-vishal/doctr-iitb/releases/download/Indic_Models/crnn_vgg16_bn_handwritten_kannada.pt',
'https://github.com/kasuba-badri-vishal/doctr-iitb/releases/download/Indic_Models/crnn_vgg16_bn_handwritten_odia.pt',
'https://github.com/kasuba-badri-vishal/doctr-iitb/releases/download/Indic_Models/crnn_vgg16_bn_handwritten_tamil.pt',
'https://github.com/kasuba-badri-vishal/doctr-iitb/releases/download/Indic_Models/crnn_vgg16_bn_handwritten_telugu.pt',
'https://github.com/kasuba-badri-vishal/doctr-iitb/releases/download/Indic_Models/crnn_vgg16_bn_handwritten_urdu.pt']




for link in links:
    try:
        os.system('wget -nc {} {}'.format(MODEL_PATH,link))
    except:
        wget.download(link, MODEL_PATH)
    
print("\nDownloaded all models")
