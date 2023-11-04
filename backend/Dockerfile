# Container image 
FROM python:3.8-alpine

# Set the working directory to app/
WORKDIR /app

# Set env
ENV VIRTUAL_ENV=/opt/venv
RUN python3 -m venv $VIRTUAL_ENV
ENV PATH="$VIRTUAL_ENV/bin:$PATH"

# install c++ compiler
RUN apk add --no-cache gcc libc-dev linux-headers

# Copy current directory to /app
ADD . /app

# Install dependencies:
RUN pip install --upgrade pip
RUN pip install -r requirements.txt


# Start UWSGi
CMD ["uwsgi", "app.ini"]