from spex_common.models.Status import PipelineStatus


class Pipeline:
    def __init__(self, **kwargs):
        self.name = kwargs.get('name', '')
        self.author = kwargs.get('author', '')
        self._from = kwargs.get('_from', '')
        self._to = kwargs.get('_to', '')
        self.status = kwargs.get('complete', 0)
        self.project = kwargs.get('project', '')
        self.id = kwargs.get('_key', '')
        self._id = kwargs.get('_id', '')
        self.shared = kwargs.get('shared', False)

    def to_json(self):
        return {
            'name': self.name,
            'author': self.author,
            '_from': self._from,
            '_to': self._to,
            'status': self.status,
            'id': self.id,
            '_id': self._id,
            'project': self.project,
            'status_name': PipelineStatus.from_status(self.status),
            'shared': self.shared,
        }


def pipeline(data):
    return Pipeline(**data)
