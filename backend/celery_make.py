from celery import Celery
from celery.schedules import crontab

def make_celery(app):
	# initialize the celery object
	celery = Celery(
		app.import_name,
		broker=app.config['CELERY_BROKER_URL'],
		backend=app.config['CELERY_RESULT_BACKEND']
	)
	# make sure flask app uses same as celery
	celery.conf.update(app.config)
	return celery
'''
	# configure periodic tasks via beat
	celery.conf.CELERYBEAT_SCHEDULE = {
		'init-models-minite': {
			'task': 'server.test_task_f',  # This is the task you want to run
			'schedule': crontab(minute='*'),  # Every Sunday at midnight
		},
	}'''
