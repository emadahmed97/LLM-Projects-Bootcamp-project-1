#
FROM python:3.10

#


COPY requirements.txt ./

#
RUN pip install -r requirements.txt

#
WORKDIR /app
COPY . .

#
#CMD ["uvicorn", "main:app", "--proxy-headers", "--host", "0.0.0.0", "--port", "80"]
