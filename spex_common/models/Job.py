from spex_common.models.Status import TaskStatus


class Job:
    def __init__(self, **kwargs):
        self.id = kwargs.get('_key', None)
        self._id = kwargs.get('_id', '')
        self.name = kwargs.get('name', '')
        self.content = kwargs.get('content', '')
        self.omeroIds = kwargs.get('omeroIds', [])
        self.file_names = kwargs.get('file_names', [])
        self.author = kwargs.get('author', '')
        self.status = kwargs.get('status', 0)

    def to_json(self) -> dict:
        return {
            'id': self.id,
            'name': self.name,
            'content': self.content,
            'author': self.author,
            'omeroIds': self.omeroIds,
            '_id': self._id,
            'status': self.status,
            'status_name': TaskStatus.from_status(self.status),
            'file_names': self.file_names
         }


def job(data):
    return Job(**data)
