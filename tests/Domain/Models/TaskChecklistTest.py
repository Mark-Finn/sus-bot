import unittest

from Domain.Models.TaskChecklist import TaskChecklist
from Dtos.Task import Task


class TaskChecklistTest(unittest.TestCase):

    def testGetUncompletedTasks_whenAllTasksIncomplete_returnAllTaskNames(self):
        #arrange
        expected = []
        task_checklist = TaskChecklist()
        for task in self.__get_fake_tasks():
            expected.append(task.name)
            task_checklist.add_task(task.name)

        #act
        actual = task_checklist.get_uncompleted_tasks()

        #assert
        self.assertEqual(set(expected), set(actual))

    def testGetUncompletedTasks_whenSomeTasksIncomplete_returnNotAllTaskNames(self):
        #arrange
        more_than_expected = []
        task_checklist = TaskChecklist()
        for task in self.__get_fake_tasks():
            more_than_expected.append(task.name)
            task_checklist.add_task(task.name)

        #act
        task_checklist.complete_task('wires')
        actual = task_checklist.get_uncompleted_tasks()

        #assert
        self.assertGreater(set(more_than_expected), set(actual))

    def testGetUncompletedTasks_whenAllTasksIncomplete_returnNoTaskNames(self):
        #arrange
        task_checklist = TaskChecklist()
        for task in self.__get_fake_tasks():
            task_checklist.add_task(task.name)
            task_checklist.complete_task(task.name)

        #act
        actual = task_checklist.get_uncompleted_tasks()

        #assert
        self.assertFalse(actual)

    def testGetCompletedCount_whenOneTaskCompleted_returnOne(self):
        #arrange
        task_checklist = TaskChecklist()
        for task in self.__get_fake_tasks():
            task_checklist.add_task(task.name)

        #act
        task_checklist.complete_task('wires')
        actual = task_checklist.get_completed_count()

        #assert
        expected = 1
        self.assertEqual(expected, actual)

    def __get_fake_tasks(self):
        return [
            Task('admin swipe', 'admin', 'swipe card', 'common'),
            Task('wires', 'everywhere', 'connect wires', 'common'),
            Task('scan', 'medbay', 'scans body', 'short'),
            Task('chart course', 'navigation', 'char course', 'short'),
            Task('clean vent', 'anywhere', 'clean vent', 'short'),
            Task('asteroids', 'weapons', 'destroy asteroids', 'long'),
            Task('simon says', 'nuclear', 'play simon says', 'long'),
        ]


if __name__ == '__main__':
    unittest.main()