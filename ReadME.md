
# E-Commerce App

This is a E-commerce app in Django.

## Requirements

- Python 3.10+

## Setup Django Project

Clone the project

_using ssh_

```bash
git clone https://github.com/Dhruvik-Kakadiya/video_management.git
```

_or using http_

```bash
git clone 
```

Go to the project directory

```bash
cd ecommerce
```

Create a virtual environment

```bash
python3 -m venv ./venv
```

Activate a virtual environment

```bash
source venv/bin/activate
```

Install dependecies

```bash
pip install -r requirements.txt
```


## Run using runserver


Run the migrations first

```bash
python manage.py migrate
```

To run the python server

```bash
python manage.py runserver
```

To create your admin user

```bash
python manage.py createsuperuser
```
