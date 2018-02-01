from celery import Celery
from .models import Readings
from django.conf import settings
from .utils import BunnyApi

app = Celery('tasks', broker='pyamqp://guest@localhost//')



@app.on_after_configure.connect
def setup_periodic_tasks(sender, **kwargs):
    # Calls consult_readings() every 10 minutes.
    sender.add_periodic_task(600.0, consult_readings.s(), name='add every 10 minutes')



@app.task
def consult_readings():
    api_id = settings.BUNNY_API_ID
    api_key = settings.BUNNY_API_KEY
    speed_project = BunnyApi(api_id, api_key)
    readings_set = Readings.objects.filter(status_reads="N", project_id__isnull=False)
    if readings_set:
        for readings in readings_set:
            readings_results = speed_project.check_for_readings(readings.project_id)
            if 'project' in readings_results:
                read_status = ''
                for read in readings_results['project']['reads']:
                    if read['status'] == 'reviewable':
                        read_status = 'reviewable'
                        break

                if read_status != '':
                    readings.status_reads = 'S'
                    readings.reads = readings_results['project']['reads']
                    readings.save()
            elif 'error' in readings_results:
                readings.status_api = 'E'
                readings.project_error = readings_results
                readings.save()
