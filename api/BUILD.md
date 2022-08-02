## Deploying the Power Grid Mapper

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

The Serverless Application Model Command Line Interface (SAM CLI) is an extension of the AWS CLI that adds functionality for building and testing Lambda applications. It uses Docker to run your functions in an Amazon Linux environment that matches Lambda. It can also emulate your application's build environment and API.

To use the SAM CLI, you need the following tools.

* SAM CLI - [Install the SAM CLI](https://docs.aws.amazon.com/serverless-application-model/latest/developerguide/serverless-sam-cli-install.html)
* Docker - [Install Docker community edition](https://hub.docker.com/search/?type=edition&offering=community)

You may need the following for local testing.
* [Python 3 installed](https://www.python.org/downloads/)

To build and deploy your application for the first time, run the following in your shell:

## 1. Create ECR Repo
```bash
api$ aws ecr create-repository --repository-name omdena-surplusmap --image-tag-mutability IMMUTABLE --image-scanning-configuration scanOnPush=true
```

## 2. Build
```bash
api$ sam build
```

## 3. Test
```bash
api$ sam local start-api
```

```bash
api$ python -m pytest tests/test_local.py -r A
```

## 4. Deploy
```bash
api$ sam deploy --no-confirm-changeset --no-fail-on-empty-changeset
```

### 4.1 API Endpoint
```bash
https://u3ipqrwr25.execute-api.us-east-1.amazonaws.com/Prod/map
```

### 4.2 Test
```bash
api$ python -m pytest tests/test_deploy.py -r A
```