from spex_common.models.Status import TaskStatus


class Task:
    def __init__(self, **kwargs):
        self.name = kwargs.get('name', '')
        self.content = kwargs.get('content', '')
        self.omeroId = kwargs.get('omeroId', '')
        self.author = kwargs.get('author', '')
        self.parent = kwargs.get('parent', '')
        self.params = kwargs.get('params', {})
        self.status = kwargs.get('status', 0)
        self.file_names = kwargs.get('file_names', [])
        self.id = kwargs.get('_key', '')
        self._id = kwargs.get('_id', '')
        self.csvdata = kwargs.get('csvdata', [])
        self.impath = kwargs.get('impath', '')
        self.result = kwargs.get('result', '')
        self.error = kwargs.get('error')

    def to_json(self) -> dict:

        return {
            'omeroId': self.omeroId,
            'name': self.name,
            'content': self.content,
            'author': self.author,
            'parent': self.parent,
            'params': self.params,
            'status': self.status,
            'csvdata': self.csvdata,
            'file_names': self.file_names,
            'id': self.id,
            '_id': self._id,
            'impath': self.impath,
            'result': self.result,
            'status_name': TaskStatus.from_status(self.status),
            'error': self.error
        }


def task(data):
    return Task(**data)
