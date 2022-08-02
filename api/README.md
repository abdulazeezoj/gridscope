<div align='center'>
<h1>Power Grid Mapper Deployment</h1>
Identifying Power Infrastructure Through GIS and Machine Learning to Accelerate the Green Transition
</div>

---

## Table of Contents

* [Deployment](#deployment)
    * [Approach](#approach)
    * [Architecture](#architecture)
    * [API Reference](#api-reference)
    * [Demo](#demo)

---

Now that we have a trained model available, our goal is to make this model available for use. To achieve this, we decided to find somewhere to host your models and expose them via REST APIs. This can make it easy for end users to integrate the model outputs directly into their applications and business processes.
Moreover, Serverless computing is a new approach to building applications that allows users to create and run their code without first having to manage the underlying physical resources. In serverless computing, an application's code is hosted in a centralized location and accessed through APIs, which are then used by the application. This model allows for the creation of more complex applications, as well as those that need to scale easily.

#### Approach
Building a custom training and serving workflow is hard. It's also incredibly important because it determines how you're going to handle the operational aspects of your product. The goal here is to produce a simple deploy workflow that works in any CI/CD tool. In addition, we want to:
- Use a docker container, to serve anywhere containers can run
- Expose a REST API so that others can consume it
- Minimize the complexity and attack surface of the operational container

We will create a serverless application that is capable of serializing a model inside of a Docker container, and then packaging the service with Docker and AWS ECR. We will then use AWS Lambda to serve the model with an API (serverless API) that is built on top of it. Finally, we will build, test, and deploy our project in a CI/CD workflow using GitHub Actions.

In addition, we also use the SAM (Serverless Application Model) framework to set up resources on AWS in an infrastructure-as-code (IaC) style. This makes it easier to manage resources over time and helps us keep track of changes made to them.

![Deployment Architecture](../docs/assets/aws-architecture.png)


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

![Deployment Demo](../docs/assets/deployment_demo.gif)
