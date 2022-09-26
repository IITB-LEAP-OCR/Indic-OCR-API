import time
import os

import multiprocessing as mp
import pandas as pd

import torch
from torch.utils.data import DataLoader, SequentialSampler
from torchvision.transforms import Normalize
from tqdm import tqdm

from doctr import datasets
from doctr import transforms as T
from doctr.datasets import VOCABS
from doctr.models import recognition
from doctr.utils.metrics import TextMatch
from config import ALLOWED_EXTENSIONS

os.environ["USE_TORCH"] = "1"


def get_test_results(predictions, language):
    df = pd.DataFrame(predictions)
    df[['pred','score']] =  pd.DataFrame(df.pred.tolist(), index= df.index)
    df = df.drop_duplicates()
    df['id']= df['name'].str.split("_")
    df[['temp','id']] =  pd.DataFrame(df.id.tolist(), index= df.index)
    df['name'] = df['name'].str.replace('_','/')
    df = df.sort_values('id')
    df = df[['name','pred']]
    data = dict(zip(df.name, df.pred))
    filename = 'results.txt'
    df.to_csv(filename, mode='a',sep='\t', index=False)
    return data


@torch.no_grad()
def evaluate(model, val_loader, batch_transforms, val_metric, amp=False):
    # Model in eval mode
    model.eval()
    # Reset val metric
    val_metric.reset()
    # Validation loop
    val_loss, batch_cnt = 0, 0
    predictions = []
    for images, targets, names in tqdm(val_loader):
        try:
            if torch.cuda.is_available():
                images = images.cuda()
            images = batch_transforms(images)
            if amp:
                with torch.cuda.amp.autocast():
                    out = model(images, targets, return_preds=True)
            else:
                out = model(images, targets, return_preds=True)
            # Compute metric
            
            d = {}
            d['pred'] = out['preds'][0]
            d['actual'] = targets[0]
            d['name'] = names[0]
            predictions.append(d)
            if len(out["preds"]):
                words, _ = zip(*out["preds"])
            else:
                words = []
            val_metric.update(targets, words)

            val_loss += out["loss"].item()
            batch_cnt += 1
        except ValueError:
            print(f"unexpected symbol/s in targets:\n{targets} \n--> skip batch")
            continue
            
    val_loss /= batch_cnt
    result = val_metric.summary()
    return val_loss, result["raw"], result["unicase"], predictions


def infer_model(language, modality, model_path, img_path, device):

    arch = "crnn_vgg16_bn_" + "handwritten_" + language + ".pt" 
    workers = None
    torch.backends.cudnn.benchmark = True

    if not isinstance(workers, int):
        workers = min(16, mp.cpu_count())

    # Load doctr model
    model = recognition.__dict__["crnn_vgg16_bn"](
        pretrained=True,
        input_shape=(3, 32, 4 * 32),
        vocab=VOCABS[language],
    ).eval()

    checkpoint = torch.load(model_path + arch , map_location="cpu")
    model.load_state_dict(checkpoint)

        

    st = time.time()
    ds = datasets.__dict__["IndicData"](
        train=True,
        download=True,
        recognition_task=True,
        language=language,
        inp_path=img_path,
        sets="test",
        use_polygons=True,
        img_transforms=T.Resize((32, 4 * 32), preserve_aspect_ratio=True),
    )


    test_loader = DataLoader(
        ds,
        batch_size=1,
        drop_last=False,
        num_workers=workers,
        sampler=SequentialSampler(ds),
        pin_memory=torch.cuda.is_available(),
        collate_fn=ds.collate_fn,
    )
    print(f"Test set loaded in {time.time() - st:.4}s ({len(ds)} samples in " f"{len(test_loader)} batches)")

    mean, std = model.cfg["mean"], model.cfg["std"]
    batch_transforms = Normalize(mean=mean, std=std)

    # Metrics
    val_metric = TextMatch()

    # GPU
    # Silent default switch to GPU if available
    if torch.cuda.is_available():
        device = 0
    else:
        print("No accessible GPU, targe device set to CPU.")
    
    if torch.cuda.is_available():
        torch.cuda.set_device(device)
        model = model.cuda()

    print("Running evaluation")
    val_loss, exact_match, partial_match, predictions = evaluate(model, test_loader, batch_transforms, val_metric, amp=True)
    return get_test_results(predictions, language)


def log(s):
	"""
	replacing the print function with log that also gives a sense of time
	"""
	s = f'[{int(time.time()*100)%10000}]\t{s}'
	print(s)

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS