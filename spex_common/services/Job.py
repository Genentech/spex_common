from spex_common.modules.database import db_instance
from spex_common.models.Job import job, Job
from spex_common.models.Connection import connection
from spex_common.services.Utils import first_or_none, map_or_none
import spex_common.services.Task as TaskService


collection = 'jobs'


def select(id, collection='jobs') -> Job or None:
    value = id
    search = 'FILTER doc._key == @value LIMIT 1'
    items = db_instance().select(collection, search, value=value)
    return first_or_none(items, job)


def select_jobs(collection='jobs', condition=None, **kwargs) -> list[dict] or None:
    search = db_instance().get_search(**kwargs)
    if condition is not None and search:
        search = search.replace('==',  condition)

    items = db_instance().select(collection, search, **kwargs)
    return map_or_none(items, lambda item: job(item).to_json())


def update(id, collection='jobs', data=None, history: dict = {}) -> Job or None:
    search = 'FILTER doc._key == @value LIMIT 1 '
    items = db_instance().update(collection, data, search, value=id, history_content=history)
    return first_or_none(items, job)


def delete(id, collection='jobs') -> Job or None:
    search = 'FILTER doc._key == @value LIMIT 1 '
    items = db_instance().delete(collection, search, value=id, add_to_hist=True)
    return first_or_none(items, job)


def delete_connection(condition=None, collection='jobs_tasks', **kwargs) -> Job or None:
    search = db_instance().get_search(**kwargs)
    if condition is not None and search:
        search = search.replace('==',  condition)
    items = db_instance().delete(collection, search, **kwargs)
    return first_or_none(items, job)


def select_connections(
    condition=None,
    collection="jobs_tasks",
    one=False,
    **kwargs
) -> list[dict] or dict or None:
    search = db_instance().get_search(**kwargs)
    if condition is not None and search:
        search = search.replace('==',  condition)

    items = db_instance().select(collection, search, **kwargs)

    def to_json(item):
        connection(item).to_json()

    if one:
        return first_or_none(items, to_json)

    return map_or_none(items, to_json)


def insert(data, collection='jobs', history: dict = {}) -> Job or None:
    item = db_instance().insert(collection, data, None, history)
    return first_or_none([item['new']], job)


def count(collection='jobs') -> int:
    arr = db_instance().count(collection, '')
    return arr[0]


def update_job(id, data, history: dict = {}) -> dict or None:
    old_job = select(id=id)
    new_job = update(id=id, data=data, history=history)

    if new_job is None:
        return None

    tasks = TaskService.select_tasks_edge(f'jobs/{new_job.id}')

    if set(old_job.omeroIds) != set(new_job.omeroIds):
        for item in tasks:
            delete_connection(_to=item.get('_id'))
            TaskService.delete(item.get('id'))

        tasks = TaskService.create_tasks(data, new_job)
    else:
        for item in tasks:
            TaskService.update(item.get('id'), data)

    new_job.tasks = tasks

    if new_job.status is None or new_job.status == '':
        new_job.status=0

    new_job = new_job.to_json()

    return new_job
