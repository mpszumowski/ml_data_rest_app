# base image
FROM python:3.6.4

# set working directory
RUN mkdir -p /usr/src/webfetch
WORKDIR /usr/src/webfetch

# add requirements
COPY requirements.txt requirements.txt

# install requirements
RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt

# add app
COPY . .

# run command
CMD [ "python", "-m", "serve" ]
