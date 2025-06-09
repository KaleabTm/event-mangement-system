# Creating image based on the official Python 3 image
FROM python:3.12.4

# Fix Python printing
ENV PYTHONUNBUFFERED=1

# Set the working directory
WORKDIR /usr/src/app

# Installing all python dependencies
ADD requirements/ requirements/
RUN pip install --no-cache-dir -r requirements/local.txt

# Get the django project into the docker container
ADD ../../ .

# Expose the port Django runs on
EXPOSE 8000

# Start the Django development server
CMD ["sh", "-c", "python manage.py migrate && gunicorn config.wsgi:application --bind 0.0.0.0:8000"]