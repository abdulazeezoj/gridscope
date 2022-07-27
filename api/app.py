import json
import util


def handler(event, context):
    """
    lambda handler to execute powergrid detection
    """
    print(f"[ INFO  ] Reading request...")
    event = json.loads(event["body"])
    print(f"[ INFO  ] Event keys: {list(event.keys())}")

    _image = event.get("image", None)
    _model = event.get("model", "m")
    _conf = event.get("conf", 0.5)
    _render = event.get("render", False)

    try:
        print("[ INFO  ] Reading image...")
        image = util.decode_image(_image)

        print("[ INFO  ] Loading model...")
        net = util.load_model(_model)

        print("[ INFO  ] Detecting...")
        bboxes, confs, labels = util.detect(image, net, _conf)
        print(f"[ INFO  ] Inference: {util.check_speed(net):.2f} ms")

        if _render:
            print("[ INFO  ] Rendering...")
            image = util.render(image, bboxes, confs, labels)

            print("[ INFO  ] Encoding image...")
            image_enc = util.encode_image(image)

            # return the result
            return {
                "statusCode": 200,
                "body": json.dumps(
                    {
                        "image": image_enc,
                        "bboxes": bboxes,
                        "confs": confs,
                        "labels": labels,
                    }
                ),
                "contentType": "application/json"
            }
        else:
            # return the result
            return {
                "statusCode": 200,
                "body": json.dumps(
                    {
                        "bboxes": bboxes,
                        "confs": confs,
                        "labels": labels,
                    }
                ),
                "contentType": "application/json"
            }

    except Exception as e:
        print(f"[ ERROR ] {repr(e)}")

        return {
            "statusCode": 500,
            "body": json.dumps({"error": repr(e)}),
            "contentType": "application/json"
        }
