# lmsunsw

This app has been configured to run on AWS Elastic Beanstalk.

To setup the app, you will need to create a virtualenv to run the app

when you have run the git clone command, run 'virtualenv env' to create an env folder alongside the lmsunsw repo

type 'source env/bin/activate' to set the env into PATH.

cd into lmsunsw and run 'pip install -r requirements.txt' to configure the env with packages

run 'python manage.py runserver to start the webserver locally'
