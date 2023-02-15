import json
import util


def handler(event, context):
    """
    lambda handler to execute powergrid detection
    """
    print("[ INFO  ] Reading request...")
    print("[ INFO  ] Event type: {}".format(type(event)))
    body = json.loads(event)
    print(f"[ INFO  ] Event keys: {list(body.keys())}")

    _image = body.get("image", None)
    _model = body.get("model", "m")
    _conf = body.get("conf", 0.5)
    _render = body.get("render", False)

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
                "headers": {
                    "Content-Type": "application/json"
                },
                "body": json.dumps(
                    {
                        "image": image_enc,
                        "bboxes": bboxes,
                        "confs": confs,
                        "labels": labels,
                    }
                )
            }
        else:
            # return the result
            return {
                "statusCode": 200,
                "headers": {
                    "Content-Type": "application/json"
                },
                "body": json.dumps(
                    {
                        "bboxes": bboxes,
                        "confs": confs,
                        "labels": labels,
                    }
                )
            }

    except Exception as e:
        print(f"[ ERROR ] {repr(e)}")

        return {
            "statusCode": 500,
            "headers": {
                "Content-Type": "application/json"
            },
            "body": json.dumps({"error": repr(e)}),
        }
