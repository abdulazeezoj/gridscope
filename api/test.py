import json

import pytest
from PIL import Image
from requests import request

import app
import util


@pytest.fixture()
def apigw_event():
    """ Generates API GW Event"""

    return {
        "image": util.encode_image(Image.open('images/img1.png')),
        "model": "m",
        "conf": 0.5,
        "render": True
    }


@pytest.fixture()
def apigw_url():
    """ Generates API GW URL"""

    return {
        "url": "http://127.0.0.1:3000/detect",
        "method": "POST"
    }


# Test the handler with a full request
def test_handler(apigw_event, apigw_url):
    ret = request(apigw_url["method"], apigw_url["url"], json=apigw_event)
    data = ret.json()

    assert ret.status_code == 200
    assert "image" in data
    assert "bboxes" in data
    assert "confs" in data
    assert "labels" in data
    assert "error" not in data

    image = util.decode_image(data["image"])
    image.save("images/test1_out.png")

    print("[ INFO  ] Detection...")
    util.print_detection(data["bboxes"], data["confs"], data["labels"])


# Test the handler with a empty request
def test_handler_null_reqest(apigw_event, apigw_url):
    apigw_event = {}
    ret = request(apigw_url["method"], apigw_url["url"], json=apigw_event)
    data = ret.json()

    assert ret.status_code == 500
    assert "error" in data


# Test the handler with a bad image
def test_handler_bad_image(apigw_event, apigw_url):
    apigw_event["image"] = "bad image"
    ret = request(apigw_url["method"], apigw_url["url"], json=apigw_event)
    data = ret.json()

    assert ret.status_code == 500
    assert "error" in data


# Test the handler with a bad model
def test_handler_bad_model(apigw_event, apigw_url):
    apigw_event["model"] = "bad model"
    ret = request(apigw_url["method"], apigw_url["url"], json=apigw_event)
    data = ret.json()

    assert ret.status_code == 500
    assert "error" in data


# Test the handler with no render
def test_handler_no_render(apigw_event, apigw_url):
    apigw_event["render"] = False
    ret = request(apigw_url["method"], apigw_url["url"], json=apigw_event)
    data = ret.json()

    assert ret.status_code == 200
    assert "image" not in data
    assert "bboxes" in data
    assert "confs" in data
    assert "labels" in data
    assert "error" not in data

    print("[ INFO  ] Detection...")
    util.print_detection(data["bboxes"], data["confs"], data["labels"])


# Test the handler locally
def test_handler_locally(apigw_event):
    apigw_event = {"body": json.dumps(apigw_event)}
    ret = app.handler(apigw_event, "")
    data = json.loads(ret["body"])

    assert ret["statusCode"] == 200
    assert "image" in data
    assert "bboxes" in data
    assert "confs" in data
    assert "labels" in data
    assert "error" not in data

    image = util.decode_image(data["image"])
    image.save("images/test2_out.png")

    print("[ INFO  ] Detection...")
    util.print_detection(data["bboxes"], data["confs"], data["labels"])
