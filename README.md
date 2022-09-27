# DocTR_Indic_OCR_API
API for Handwritten and Printed Texts Recognition for Indian Languages using DocTR model


# Docker Usage Instructions

## Build Docker Image

```docker-compose up```

## Rebuild Docker Image

```docker-compose up --build```

# API Instructions

## Upload Image
### Request

`POST /api/v1/upload`

    file upload with key as 'file'

### Response

    HTTP/1.1 200 OK
    Date: Thu, 24 Feb 9999 12:36:30 GMT
    Status: 200 OK
    Connection: close
    Content-Type: application/json
    Content-Length: 2

    {
    "data": {
        "ids": ["2de49b11-add8-435c-a343-037df78c6ca4"]
        }
    }

## Inference
### Request

`POST /api/v1/inference`

    [{
    "id": "id from first api",
    "modality": "handwritten",
    "level": "word",
    "language": "bengali",
    "model-id": "1",
    "meta": {
        "device": 0
    }}
    ]

### Response

    HTTP/1.1 200 OK
    Date: Thu, 24 Feb 9999 12:36:30 GMT
    Status: 200 OK
    Connection: close
    Content-Type: application/json
    Content-Length: 2

    {
    "data": [
        {
            "file_path": "/../src/uploads/img_2de49b11-add8-435c-a343-037df78c6ca4.43",
            "id": "2de49b11-add8-435c-a343-037df78c6ca4",
            "language": "bengali",
            "level": "word",
            "meta": {
                "device": 0,
            },
            "modality": "handwritten",
            "model-id": "1",
            "text": ""
        }
    ]}


# UI Usage Instructions

The Version 0 is UI based method to use the API

1. Go to ```http://localhost:5000/api/v0/upload```
2. Provide the require arguments, sample image is provided here
3. Submit the Input to fetch the result predictions
