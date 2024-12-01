import datetime as dt
from celery_queue.tasks import get_last_check_notification_time, left_border, send_notification_trip
from celery_queue.create_celery import interval_check
from celery_queue.create_celery import celery_app
from app.schemas.trip import TripRead


def cancel_notification(trip: TripRead):
    i = celery_app.control.inspect()
    cansel = False
    for worker_tasks in i.scheduled.values():
        if cansel:
            break
        for task in worker_tasks:
            task_name = task['request']['name']
            if task_name != 'send_notification_trip':
                continue
            current_trip: TripRead = task['request']['args'][0]
            if current_trip.id == trip.id:
                celery_app.control.revoke(task['request']['id'])
                cansel = True
                break





def check_need_to_create_task_immediately(trip: TripRead):
    notification_time = (trip.travel_date -
                         (trip.notification_before_travel - dt.datetime.fromisoformat('1970-01-01')))
    last_check_time = get_last_check_notification_time()
    if notification_time < (last_check_time + interval_check + left_border):
        return send_notification_trip.apply_async(args=[trip.model_dump_json()], eta=notification_time)
