import os
# ".env\Scripts\activate"

virtual_env = os.environ.get('VIRTUAL_ENV')

if virtual_env:
    print('Virtual environment detected')
    print('Virtual environment path: ' + virtual_env)
else:
    print('No virtual environment detected')