FROM python:3.10.2

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

WORKDIR /company_lunch

RUN apt-get update \
  && apt-get -y install netcat gcc postgresql \
  && apt-get clean

COPY requirements.txt /company_lunch/
RUN pip install --upgrade pip
RUN pip install -r requirements.txt


# Add the rest of the code
COPY ./company_lunch/ /company_lunch/

# Run the application
CMD ["gunicorn", "--bind", ":8000", "--workers", "3", "company_lunch_inforce.wsgi:application"]

