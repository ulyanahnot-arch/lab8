import unittest
from datetime import datetime
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from database import Base
from models import TaskDB
from repository import TaskRepository
from todo_model import TaskModel, TaskStatus

TEST_DATABASE_URL = "postgresql+psycopg2://test_user:password@localhost:5443/test_db"

class TestTaskModelIntegration(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.engine = create_engine(TEST_DATABASE_URL)
        cls.SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=cls.engine)
        Base.metadata.create_all(bind=cls.engine)

    @classmethod
    def tearDownClass(cls):
        Base.metadata.drop_all(bind=cls.engine)
        cls.engine.dispose()

    def setUp(self):
        self.session = self.SessionLocal()
        
        self.session.query(TaskDB).delete()
        self.session.commit()

        self.repo = TaskRepository(self.session)
        self.model = TaskModel(self.repo)
        self.schedule_time = datetime(2025, 12, 31, 12, 0)

        self.task = self.model.add_task("Test task", self.schedule_time)

    def tearDown(self):
        self.session.close()

    def test_add_task(self):
        self.assertEqual(len(self.model.get_all_tasks()), 1)
        fetched = self.model.get_all_tasks()[0]
        self.assertEqual(fetched.description, "Test task")
        self.assertEqual(fetched.status, TaskStatus.TODO)

    def test_get_task_by_id_success(self):
        fetched = self.model.get_task_by_id(str(self.task.id))
        self.assertIsNotNone(fetched)

        fetched_short = self.model.get_task_by_id(str(self.task.id)[:5])
        self.assertIsNotNone(fetched_short)

    def test_get_task_by_id_fail(self):
        fetched = self.model.get_task_by_id("invalid-id")
        self.assertIsNone(fetched)

    def test_update_task_status(self):
        res = self.model.update_task_status(str(self.task.id), TaskStatus.IN_PROGRESS)
        self.assertTrue(res)
        
        updated_task = self.model.get_task_by_id(str(self.task.id))
        self.assertEqual(updated_task.status, TaskStatus.IN_PROGRESS)

        res_fail = self.model.update_task_status("123", TaskStatus.DONE)
        self.assertFalse(res_fail)

    def test_update_task_description(self):
        res = self.model.update_task_description(str(self.task.id), "New description")
        self.assertTrue(res)
        
        updated_task = self.model.get_task_by_id(str(self.task.id))
        self.assertEqual(updated_task.description, "New description")

    def test_delete_task(self):
        res = self.model.delete_task(str(self.task.id))
        self.assertTrue(res)
        self.assertEqual(len(self.model.get_all_tasks()), 0)

    def test_filter_by_status(self):
        task2 = self.model.add_task("Done task", self.schedule_time)
        self.model.update_task_status(str(task2.id), TaskStatus.DONE)
        
        todos = self.model.filter_by_status(TaskStatus.TODO)
        dones = self.model.filter_by_status(TaskStatus.DONE)
        
        self.assertEqual(len(todos), 1)
        self.assertEqual(len(dones), 1)
        self.assertEqual(dones[0].description, "Done task")

if __name__ == '__main__':
    unittest.main()