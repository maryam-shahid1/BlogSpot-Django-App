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
cd BlogSpot/
pip install -r requirements.txt
```  

### 4. Install requirements  
```sh
git clone "https://github.com/maryam-shahid1/Django-Blog-App.git"
```  

### 5. Edit project settings  
```
AUTH_USER_MODEL = 'user.User'

AUTHENTICATION_BACKENDS = [
    'django.contrib.auth.backends.ModelBackend',
]

MESSAGE_STORAGE = 'django.contrib.messages.storage.fallback.FallbackStorage'

STATIC_URL = '/static/'
STATICFILES_DIRS = [os.path.join(BASE_DIR, 'static')]

INSTALLED_APPS = [
    "blog.apps.BlogConfig",
    "user.apps.UserConfig",
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
]
```  

### 6. Run the server  
```sh
python manage.py makemigrations user
python manage.py sqlmigrate user 0001
python manage.py migrate
python manage.py runserver
```  
# BlogSpot-Django-App
