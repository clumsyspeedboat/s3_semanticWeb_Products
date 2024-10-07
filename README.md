# s3_semanticWeb_Products
Mini projects, using MinIO S3 and Python, for Course- Advanced Big Data Concepts WS24 (THI)


## Steps:

#### 1. Clone repository (once) and cd into project
```bash
git clone https://github.com/clumsyspeedboat/s3_semanticWeb_Products.git
```
```bash
cd s3_semanticWeb_Products
```

#### 2. Create virtual environment called "env" (once)
```bash
python -m venv env
```

#### 3. Activate "env"
```bash
source env/bin/activate  # In Linux/Mac
```
```bash
env\Scripts\activate  # In Windows
```

#### 4. Install required packages (once, if not new packages added to "requirements.txt" file)
```bash
pip install -r requirements.txt
```

#### 5. Run Django server
```bash
python manage.py runserver
```
```bash
python manage.py migrate # Run this before the "python manage.py runserver" if error = "no such table: django_session"
```


### After initial setup, you will need to only run steps 3 and 5 everytime you would want to start your web application