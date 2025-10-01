FROM python:3.11

# set a directory for the app
WORKDIR /usr/src/main

# copy all the files to the container
COPY . .

# install dependencies
RUN pip3 install --no-cache-dir -r requirements.txt

# tell the port number the container should expose
EXPOSE 6000

# run the command
CMD ["python3", "./app.py"]
