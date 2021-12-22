# This is Pauls' reality
FROM python:3.10-alpine

# This is Paul
RUN adduser -h "/paul" -u 3240 -g "Paul" -D paul

# Paul lives here
WORKDIR /paul

# Copy in Pauls' requirements
COPY --chown=paul  requirements.txt /paul/requirements.txt

# Install Pauls' requirements
RUN pip install -r requirements.txt

# Copy in what makes Paul, Paul
COPY --chown=paul  src /paul

# We are Paul
USER paul

# Wake up Paul!
SHELL ["/usr/local/bin/python", "app.py"]