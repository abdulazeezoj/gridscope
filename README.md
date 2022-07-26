<div align='center'>
<h1>SurplusMap</h1>
Identifying Power Infrastructure Through GIS and Machine Learning to Accelerate the Green Transition
</div>

## Table of Contents

* [The problem](#the-problem)
* [The Approach](#the-approach)
    * [Data](#data)
        * [Data Collection](#data-collection)
        * [Data Processing](#data-processing)
    * [Model](#model)
        * [Model Training](#model-training)
        * [Model Evaluation](#model-evaluation)
    * [Deployment](#deployment)
        * [Approach](#approach)
        * [Architecture](#architecture)
        * [API Reference](#api-reference)
        * [Demo](#demo)
* [The Results](#the-results)
* [Conclusion](#conclusion)


## The Problem
The main problem that surplusMap is trying to solve is to identify and map the power grid lines using EOT (Electro-Optics Technology) data products in India. This will be achieved by identifying and locating features associated with grid lines such as electric pylons, landscape corridors, and connected transformation stations, through data-driven approaches using machine learning (ML) algorithms to automatically extract this information from satellite images. To achieve this goal, Omdena is kindly requested to derive needed resources.



## The Approach
The approach to solving the problem is to collect satellite images containing features associated with powergrid grid such as electric pylons, power station, and substation. These satellite images are then used to train an AI model to identify and locate the power grid lines. The model is then deployed on a cloud platform to identify and locate the power grid lines. The model can queried through an API to identify and locate the power grid lines in satellite images.

### Data
The data used to train the model is satellite images containing features associated with powergrid grid such as electric pylons, power station, and substation. The data is collected from the following sources:

* OpenStreetMap (OSM) data of the India
* Wikipedia data of the India
* Google Maps data of the India
* Google Earth data of the India
* SASPlanet data of the India

#### Data Collection
Wikipedia and OpenStreetMap data are scraped from the web. The data contains information about the location of power grid lines in India. The coordinate provieded by the data is used in downloading the satellite images. The satellite images are collected at zoom level 16, 17, 18, 19 ad 20. The satellite images are collected from the following sources:

* Google Maps data of the India
* Google Earth data of the India
* SASPlanet data of the India

#### Data Processing
The satellite images are processed using the following steps:

* The satellite images are split into individual tiles of size 768x768 and 1024x1024 pixels
* The tiles georeference tags are removed
* The tiles are annotated and labeled using the following labels:
    * pylon
    * power-station
    * sub-station

This preprocessing is done to make the model detect the features more accurately on the satellite images. The preprocessed data is contain images and labels, which are then used to train the model. The preprocessed data is zipped and structured as follows:

    * powergrid.zip
        * images/
            * train/
                * 0a1ac112d5fb4f28a9841df345eeefd8.png
                * ...
            * test/
                * 0a1ac112d5fb4f28a9841df345eeefd8.png
                * ...
            * val/
                * 0a1ac112d5fb4f28a9841df345eeefd8.png
                * ...
        * labels/
            * train/
                * 0a1ac112d5fb4f28a9841df345eeefd8.txt
                * ...
            * test/
                * 0a1ac112d5fb4f28a9841df345eeefd8.txt
                * ...
            * val/
                * 0a1ac112d5fb4f28a9841df345eeefd8.txt
                * ...
        powergrid.names
        README.md
        LICENSE
        data.yaml

powergrid.zip is a zip file containing the preprocessed data. The data.yaml file contains paths to the images and labels. The powergrid.names file contains the names of the labels. The README.md file contains the table of contents. The LICENSE file contains the license information.

### Model
The model is trained on the preprocessed data. The model is trained using YOLOv5 as the neural network architecture. YOLOv5 🚀 is a family of object detection architectures and models pretrained on the COCO dataset, and represents Ultralytics open-source research into future vision AI methods, incorporating lessons learned and best practices evolved over thousands of hours of research and development.

#### Model Training
The model is trained on two pretrained YOLOv5 models:

|Model |size<br><sup>(pixels) |mAP<sup>val<br>0.5:0.95 |mAP<sup>val<br>0.5 |Speed<br><sup>CPU b1<br>(ms) |Speed<br><sup>V100 b1<br>(ms) |Speed<br><sup>V100 b32<br>(ms)
|---                    |---  |---    |---    |---    |---    |---
|YOLOv5l                |640  |49.0   |67.3   |430    |10.1   |2.7
|YOLOv5x                |640  |50.7   |68.9   |766    |12.1   |4.8
|                       |     |       |       |       |       |

#### Model Evaluation
The model is evaluated on the test set. The model is evaluated using the Mean Average Precision (mAP) at 0.5:0.95. The Mean Average Precision (mAP) is a metric used to evaluate the performance of a model on new data. The mAP is calculated by averaging the precision of all ground truth objects over all images.

|Model |size<br><sup>(pixels) |mAP<sup>val<br>0.5 |Precision |Recall 
|---                    |---  |---    |---    |---    
|YOLOv5l                |640  |73.0   |       |   
|YOLOv5x                |640  |74     |73.1   |72.6   
|                       |     |       |       |    


### Deployment
[![](https://img.shields.io/badge/Github-omdena--surplusmap-blue)](https://github.com/OmdenaAI/omdena-surplusmap)  

Now that we have a trained model available, our goal is to make this model available for use. To achieve this, we decided to find somewhere to host your models and expose them via REST APIs. This can make it easy for end users to integrate the model outputs directly into their applications and business processes.
Moreover, Serverless computing is a new approach to building applications that allows users to create and run their code without first having to manage the underlying physical resources. In serverless computing, an application's code is hosted in a centralized location and accessed through APIs, which are then used by the application. This model allows for the creation of more complex applications, as well as those that need to scale easily.

#### Approach
Building a custom training and serving workflow is hard. It's also incredibly important because it determines how you're going to handle the operational aspects of your product. The goal here is to produce a simple deploy workflow that works in any CI/CD tool. In addition, we want to:
- Use a docker container, to serve anywhere containers can run
- Expose a REST API so that others can consume it
- Minimize the complexity and attack surface of the operational container

We will create a serverless application that is capable of serializing a model inside of a Docker container, and then packaging the service with Docker and AWS ECR. We will then use AWS Lambda to serve the model with an API (serverless API) that is built on top of it. Finally, we will build, test, and deploy our project in a CI/CD workflow using GitHub Actions.

In addition, we also use the SAM (Serverless Application Model) framework to set up resources on AWS in an infrastructure-as-code (IaC) style. This makes it easier to manage resources over time and helps us keep track of changes made to them.

![](docs/assets/aws-architecture.png)


#### API Reference
The API is organized around REST. Our API has predictable resource-oriented URLs, accepts form-encoded request bodies, returns JSON-encoded responses, and uses standard HTTP response codes.

**Base URL**

`https://ppp1mtcq9k.execute-api.us-east-1.amazonaws.com/demo/detect`

**Parameters**  

`image` - satellite image in base64 string  
`model` - model to be used [oyela_1, oyela_2, oyela_3]  
`conf`  - confidence score to filter detection [0.1 to 1]

**Response**

`statusCode`  - value is  200  or  500  
`detection`   - dictionary containing the following;  
- `image`   - rendered image in  base64 string  
- `bboxes`  - bounding boxes of the detection [0.1 to 1]  
- `confs`   - confidence of the detection [0.1 to 1]  
- `labels`  - labels of the detection  [pylon, substation, power-station]   
- `error`   - return details of the error if statusCode is  500  

**Sample Request**

``` python
from pprint import pprint
import time, requests, _src
from PIL import Image
 
print("[INFO] Preparing request...")
data = {
    "image": _src.encode_image(Image.open('images/img2.png')),
    "model": oyela_1,
    "score": 0.5
}
url = "https://ppp1mtcq9k.execute-api.us-east-1.amazonaws.com/demo/detect"
 
print("[INFO] Sending request...")
t0 = time.time()
response = requests.post(url, json=data).json()
delta = time.time() - t0
print(f"[INFO] Request took {delta:.3} seconds")
print("[INFO] Processing response...")
if response.get("statusCode") == 200:
    response = response["detection"]
    image = _src.decode_image(response["image"])
    response.pop("image")
    pprint(response)
    image.save('images/api_out2.png')
elif response.get("statusCode") == 500:
    response = response['detection']
    print(f"[ERROR] {response['error']}")
 
========== [OUTPUT] ==========
 
{
    'bboxes': [[853, 169, 41, 53], [197, 567, 56, 49]],
    'confs': [0.8610458374023438, 0.8063827157020569],
    'labels': ['pylon', 'pylon']
}

```

#### Demo  
[![Open in Streamlit](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://abdulazeezoj-powergrid-mapper-demo-app-deploy-s1zigm.streamlitapp.com)  

The demo is a simple web application that allows users to upload an image and then use the API to detect pylons, substations and power stations.

![Deployment Demo](docs/assets/deployment_demo.gif)

