"""API Deplyment Tests"""
import json
import os
import sys

import pytest
import requests
from PIL import Image

# Add `api` to the path
current = os.path.dirname(os.path.realpath(__file__))
parent = os.path.dirname(current)
sys.path.append(parent)

# Import `util` from `api`
import util  # noqa: E402


@pytest.fixture()
def api_event():
    """ Generates API GW Event"""

    return {
        "image": util.encode_image(Image.open('images/img1.png')),
        "model": "m",
        "conf": 0.5,
        "render": True
    }


@pytest.fixture()
def api_url():
    """ Generates API GW URL"""

    return {
        "method": "POST",
        "url":
        "https://u3ipqrwr25.execute-api.us-east-1.amazonaws.com/Prod/map/"
    }


# Test the handler deployed
def test_handler_deploy(api_event, api_url):
    """Test the handler deployed"""

    method = api_url["method"]
    url = api_url["url"]

    req = requests.Request(method, url, json=json.dumps(api_event)).prepare()
    resp = requests.Session().send(req)
    data = json.loads(resp.json().get("body"))

    assert resp.status_code == 200

    assert "image" in data
    assert "bboxes" in data
    assert "confs" in data
    assert "labels" in data
    assert "error" not in data

    image = util.decode_image(data["image"])
    image.save("images/test1_out.png")

    print("[ INFO  ] Detection:")
    util.print_detection(data["bboxes"], data["confs"], data["labels"])


# Test the handler deployed with no render
def test_handler_deploy_no_render(api_event, api_url):
    """Test the handler deployed with no render"""

    api_event["render"] = False
    method = api_url["method"]
    url = api_url["url"]

    req = requests.Request(method, url, json=json.dumps(api_event)).prepare()
    resp = requests.Session().send(req)
    data = json.loads(resp.json().get("body"))

    print("[ INFO ] ", data)

    assert resp.status_code == 200

    assert "image" not in data
    assert "bboxes" in data
    assert "confs" in data
    assert "labels" in data
    assert "error" not in data

    print("[ INFO  ] Detection:")
    util.print_detection(data["bboxes"], data["confs"], data["labels"])


# Test the handler deployed with a empty request
def test_handler_deploy_null_reqest(api_event, api_url):
    """Test the handler deployed with a empty request"""

    api_event = {}
    method = api_url["method"]
    url = api_url["url"]

    req = requests.Request(method, url, json=json.dumps(api_event)).prepare()
    resp = requests.Session().send(req)
    data = json.loads(resp.json().get("body"))

    print("[ INFO ] ", data)

    assert resp.status_code == 200
    assert "error" in data

    print("[ ERROR ] ", data["error"])


# Test the handler with a bad request value
def test_handler_deploy_bad_value(api_event, api_url):
    """Test the handler with a bad request value"""

    api_event["image"] = "Image"
    api_event["model"] = "Model"
    api_event["conf"] = "Conf"
    api_event["render"] = "Render"
    method = api_url["method"]
    url = api_url["url"]

    req = requests.Request(method, url, json=json.dumps(api_event)).prepare()
    resp = requests.Session().send(req)
    data = json.loads(resp.json().get("body"))

    print("[ INFO ] ", data)

    assert resp.status_code == 200
    assert "error" in data

    print("[ ERROR ] ", data["error"])
