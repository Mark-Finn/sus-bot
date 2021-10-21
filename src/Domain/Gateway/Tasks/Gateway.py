from typing import List

from Dtos.Task import Task
from Gateway.BaseJson.Gateway import BaseJsonGateway
from Domain.Gateway.Tasks.Decoder import Decoder
from Domain.Gateway.Tasks.Encoder import Encoder


class Gateway(BaseJsonGateway):

    def fetch(self) -> List[Task]:
        test = super().fetch()
        return list(test.values())

    def update(self, task: Task):
        tasks = self.fetch()
        tasks[task.name] = task
        self.save(tasks)

    def add(self, task: Task):
        tasks = super().fetch()
        tasks[task.name] = task
        super().save(tasks)

    def _filename(self):
        return 'tasks'

    def _get_decoder(self):
        return Decoder

    def _get_encoder(self):
        return Encoder