from database import engine, Base, SessionLocal
from repository import TaskRepository
from todo_model import TaskModel
from todo_view import TaskView
from todo_controller import TaskController

def main():
    Base.metadata.create_all(bind=engine)
    
    session = SessionLocal()
    repository = TaskRepository(session)
    model = TaskModel(repository)
    view = TaskView()
    controller = TaskController(model, view)

    try:
        controller.run()
    finally:
        session.close()

if __name__ == "__main__":
    main()