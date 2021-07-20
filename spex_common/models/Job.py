class Job:
    def __init__(self, **kwargs):
        self.id = kwargs.get('_key', None)
        self._id = kwargs.get('_id', '')
        self.name = kwargs.get('name', '')
        self.content = kwargs.get('content', '')
        self.omeroIds = kwargs.get('omeroIds', [])
        self.author = kwargs.get('author', '')

    def to_json(self):
        return {
            'id': self.id,
            'name': self.name,
            'content': self.content,
            'author': self.author,
            'omeroIds': self.omeroIds,
            '_id': self._id
         }


def job(data):
    return Job(**data)
