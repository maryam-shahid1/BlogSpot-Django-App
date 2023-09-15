# Blogging App in Django  

## Installation:  

### 1. Install python-3.7.2 and python-pip.  

### 2. Setup Virtual Environment  
```sh
# Install virtual environment
sudo pip install virtualenv

# Make a directory
mkdir envs

# Create virtual environment
virtualenv ./envs/

# Activate virtual environment
source envs/bin/activate

```  

### 3. Clone git repository    
```sh
git clone "https://github.com/maryam-shahid1/BlogSpot-Django-App.git"
```  

### 4. Install requirements  
```sh
cd BlogSpot/
pip install -r requirements.txt
```  

### 5. Add your secret key in settings.py
```
SECRET_KEY = "your_key"
```  

### 6. Run the server  
```sh
python manage.py makemigrations
python manage.py migrate
python manage.py runserver
```  
