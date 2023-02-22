from spex_common.models.Status import TaskStatus
from spex_common.modules.database import db_instance
from spex_common.models.Task import task, Task
from spex_common.services.Utils import first_or_none, map_or_none


_collectionName = 'tasks'


def select(_id, collection=_collectionName, search='FILTER doc._key == @value LIMIT 1') -> Task:
    items = db_instance().select(collection, search, value=_id)
    return first_or_none(items, task)


def select_tasks(condition=None, collection=_collectionName, search=None, **kwargs) -> list[dict]:
    search = search or db_instance().get_search(**kwargs)
    if condition is not None and search:
        search = search.replace('==', condition)
    items = db_instance().select(collection, search, **kwargs)
    return map_or_none(items, lambda item: task(item).to_json())


def select_tasks_edge(_key) -> list[dict]:
    items = db_instance().select_edge(collection='jobs_tasks', inbound=False, _key=_key)

    if len(items) < 1:
        return []

    items = list(filter(None.__ne__, items))

    if len(items) < 1:
        return []

    return map_or_none(items, lambda item: task(item).to_json())


def update(_id, data=None, collection='tasks') -> Task:
    search = 'FILTER doc._key == @value LIMIT 1 '
    items = db_instance().update(collection, data, search, value=_id)
    return first_or_none(items, task)


def update_tasks(condition=None, data=None, collection=_collectionName, **kwargs) -> list[dict]:
    search = db_instance().get_search(**kwargs)
    if condition is not None and search:
        search = search.replace('==',  condition)
    items = db_instance().update(collection, data, search, **kwargs)
    return map_or_none(items, lambda item: task(item).to_json())


def delete(_id) -> Task:
    search = 'FILTER doc._key == @value LIMIT 1 '
    items = db_instance().delete(_collectionName, search, value=_id)
    return first_or_none(items, task)


def insert(data) -> Task:
    item = db_instance().insert(_collectionName, data)
    return task(item['new']) if item['new'] is not None else None


def count() -> int:
    arr = db_instance().count(_collectionName, '')
    return int(arr[0])


def create_tasks(body, job) -> list[dict]:
    parent = job.id
    result = []

    body = dict(body)

    if 'omeroIds' in body and len(body['omeroIds']) > 0:
        for omeroId in body['omeroIds']:
            data = dict(body)
            data['omeroId'] = omeroId
            data['parent'] = parent
            data['status'] = body.get('status', TaskStatus.pending_approval.value)
            del data['omeroIds']

            new_task = insert(data)
            if new_task:
                result.append(new_task.to_json())
    else:
        data = dict(body)
        data['parent'] = parent
        data['status'] = body.get('status', TaskStatus.pending_approval.value)
        new_task = insert(data)
        if new_task:
            result.append(new_task.to_json())

    for item in result:
        db_instance().insert_edge(
            'jobs_tasks',
            _from=job._id,
            _to=item.get('_id')
        )

    return result
