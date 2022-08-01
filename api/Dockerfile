FROM public.ecr.aws/lambda/python:3.8

COPY models/ ./models/
COPY app.py util.py  ./
COPY labels.txt requirements.txt ./

RUN python3.8 -m pip install --upgrade pip
RUN python3.8 -m pip install -r requirements.txt --no-cache-dir

# Command can be overwritten by providing a different command in the template directly.
CMD ["app.handler"]
