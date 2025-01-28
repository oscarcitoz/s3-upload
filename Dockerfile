FROM public.ecr.aws/lambda/python:3.8

COPY app.py /var/task/

COPY requirements.txt ./
RUN pip install -r requirements.txt

CMD [ "app.lambda_handler" ]
