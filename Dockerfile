FROM python:3.10-slim

# install requirements
COPY requirements.txt /
WORKDIR /
RUN pip install --no-cache-dir -r requirements.txt

# Install OpenJDK 11
RUN apt-get update && apt-get install -y openjdk-17-jdk


# copy the pipe source code
COPY pipe /
COPY LICENSE.txt README.md pipe.yml /

ENTRYPOINT ["python3", "/pipe.py"]