<div align='center'>
<h1>API Reference</h1>
Identifying Power Infrastructure Through GIS and Machine Learning to Accelerate the Green Transition
</div>

## Table of Contents

* [Deployment](#deployment)
    * [Approach](#approach)
    * [Architecture](#architecture)
    * [API Reference](#api-reference)
    * [Demo](#demo)

This folder contains source code and supporting files for the model deployment as a serverless application that you can deploy with the SAM CLI. It includes the following files and folders.

- images/ - images used in the model deployment testing
- models/ - models used in the model deployment
- labels.txt - A list of labels that the model can recognize.
- Dockerfile - The Dockerfile that you can use to build the application.
- app.py - The application's main file.
- util.py - Utility functions used in the application.
- test.py - Unit tests for the application code.
- samconfig.toml - The SAM configuration file.
- template.yaml - A template that defines the application's AWS resources.

The application uses several AWS resources, including Lambda functions and an API Gateway API. These resources are defined in the `template.yaml` file in this project. You can update the template to add AWS resources through the same deployment process that updates your application code.

## Deploy the sample application

The Serverless Application Model Command Line Interface (SAM CLI) is an extension of the AWS CLI that adds functionality for building and testing Lambda applications. It uses Docker to run your functions in an Amazon Linux environment that matches Lambda. It can also emulate your application's build environment and API.

To use the SAM CLI, you need the following tools.

* SAM CLI - [Install the SAM CLI](https://docs.aws.amazon.com/serverless-application-model/latest/developerguide/serverless-sam-cli-install.html)
* Docker - [Install Docker community edition](https://hub.docker.com/search/?type=edition&offering=community)

You may need the following for local testing.
* [Python 3 installed](https://www.python.org/downloads/)

To build and deploy your application for the first time, run the following in your shell:

```bash
sam sam build --cached --parallel
sam deploy
```

The first command will build a docker image from a Dockerfile and then copy the source of your application inside the Docker image. The second command will package and deploy your application to AWS, with a series of prompts. You can find your API Gateway Endpoint URL in the output values displayed after deployment.

## Use the SAM CLI to build and test locally

Build your application with the `sam build` command.

```bash
api$ sam build --cached --parallel
```

The SAM CLI builds a docker image from a Dockerfile and then installs dependencies defined in `requirements.txt` inside the docker image. The processed template file is saved in the `.aws-sam/build` folder.

The SAM CLI can also emulate your application's API. Use the `sam local start-api` to run the API locally on port 3000.

```bash
api$ sam local start-api
```

## Unit tests

Tests are defined in the `tests` folder in this project. Use PIP to install the [pytest](https://docs.pytest.org/en/latest/) and run unit tests from your local machine.

```bash
api$ python -m pytest test.py -r A
```

## API Endpoint
```bash
https://psrjglc2a8.execute-api.us-east-1.amazonaws.com/prod/detect
```

## Create ECR Repo
```bash
api$ aws ecr create-repository --repository-name omdena-surplusmap --image-tag-mutability IMMUTABLE --image-scanning-configuration scanOnPush=true
```
```bash
{
    "repository": {
        "repositoryArn": "arn:aws:ecr:us-east-1:453934962308:repository/omdena-surplusmap",
        "registryId": "453934962308",
        "repositoryName": "omdena-surplusmap",
        "repositoryUri": "453934962308.dkr.ecr.us-east-1.amazonaws.com/omdena-surplusmap",
        "createdAt": "2022-07-30T20:18:52+01:00",
        "imageTagMutability": "IMMUTABLE",
        "imageScanningConfiguration": {
            "scanOnPush": true
        },
        "encryptionConfiguration": {
            "encryptionType": "AES256"
        }
    }
}
```

## Build
```bash
api$ sam build
```

## Test
```bash
api$ sam local start-api
```

```bash
api$ python -m pytest test_local.py -r A
```

## Deploy
```bash
api$ sam deploy --guided
```