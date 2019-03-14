# API ########
FROM python:3.7
LABEL maintainer="tnurkkala@cse.taylor.edu"

WORKDIR /api
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

CMD ["flask", "run", "--host=0.0.0.0"]
