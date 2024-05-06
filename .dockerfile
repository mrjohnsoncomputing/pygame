FROM python:3.11
COPY requirements.txt .
RUN pip install -r requirements.txt
RUN cd ./apple_catch/apple_catch/
CMD ["python", "-m", "server"]

