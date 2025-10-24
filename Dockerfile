# download the base images
FROM python:3.9

# update the system
RUN  apt-get update

#create the working directory
WORKDIR /app

#copy everthing from the from local host machine
COPY . .

# TO DOWNLOAD TEH PACKAGES
RUN pip install -r requirement.txt

# give the port 
EXPOSE 5000

#to run the system 
CMD ["python" , "app.py"]
