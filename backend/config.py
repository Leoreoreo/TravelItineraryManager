import os
from dotenv import load_dotenv
from celery.schedules import crontab
from recommend import test_task

# load environment variables from the .env file
load_dotenv()

class Config:
	SECRET_KEY = os.environ.get('SECRET_KEY', 'f3cfe9ed9fae319fe2024dbf')
	DB_USERNAME = os.getenv('DB_USERNAME', 'db_user1') 
	DB_PASSWORD = os.getenv('DB_PASSWORD', 'tim$1234$') 
	DB_HOST = os.getenv('DB_HOST', '3.140.253.15')
	DB_PORT = os.getenv('DB_PORT', '5432')
	DB_NAME = os.getenv('DB_NAME', 'tim_db') 

	#SQLALCHEMY_DATABASE_URI = f"postgresql://{DB_USERNAME}:{DB_PASSWORD}@{DB_HOST}:5432/{DB_NAME}"
	#SQLALCHEMY_TRACK_MODIFICATIONS = False

	#SQLALCHEMY_DATABASE_URI = 'postgresql://db_user1:your_password@your_ec2_ip:5432/tim_db'
	#SQLALCHEMY_TRACK_MODIFICATIONS = False

	
	broker_url = 'redis://3.140.253.15:6379/0'
	result_backend = 'redis://3.140.253.15:6379/0'
	task_serializer = 'json'
	accept_content = ['json']
	result_serializer = 'json'

	broker_connection_retry_on_startup = True

	# Legacy uppercase settings for compatibility
	CELERY_BROKER_URL = broker_url
	CELERY_RESULT_BACKEND = result_backend
	CELERY_TASK_SERIALIZER = task_serializer
	CELERY_ACCEPT_CONTENT = accept_content
	CELERY_RESULT_SERIALIZER = result_serializer
	# CELERYBEAT_SCHEDULE = beat_schedule
	BROKER_CONNECTION_RETRY_ON_STARTUP = broker_connection_retry_on_startup

'''
	CELERY_BROKER_URL = 'redis://3.140.253.15:6379/0'  # Replace with your EC2 instance IP
	CELERY_RESULT_BACKEND = 'redis://3.140.253.15:6379/0'
	CELERY_ACCEPT_CONTENT = ['json']
	CELERY_TASK_SERIALIZER = 'json'
	CELERY_RESULT_SERIALIZER = 'json'
	CELERY_BEAT_SCHEDULE = {

		'run-every-second-for-a-minute': {
			'task': 'test_task_f',  # the name of the task
			'schedule': crontab(minute='*'),  # run every minute
		},
	}'''
	
	
