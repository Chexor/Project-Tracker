
from datetime import datetime, timedelta
from data.database import Database
from models.project import Project
from models.work_session import WorkSession

def seed_database():
    """Populates the database with sample data for manual testing."""
    db = Database()

    # Create projects
    project1 = Project(name="Project Alpha", description="AI project.")
    project2 = Project(name="Project Beta", description="Project Web Development.")
    project3 = Project(name="Project Gamma", description="Een gearchiveerd project.", archived=True)

    db.add_project_to_db(project1)
    db.add_project_to_db(project2)
    db.add_project_to_db(project3)

    # Create work sessions for Project Alpha
    session1_p1 = WorkSession(
        project_id=project1.proj_id,
        start_time=datetime.now() - timedelta(days=2, hours=3),
        end_time=datetime.now() - timedelta(days=2, hours=1),
        description="Research on machine learning models."
    )
    session2_p1 = WorkSession(
        project_id=project1.proj_id,
        start_time=datetime.now() - timedelta(days=1, hours=5),
        end_time=datetime.now() - timedelta(days=1, hours=2),
        description="Implemented a neural network."
    )
    db.add_work_session_to_db(session1_p1)
    db.add_work_session_to_db(session2_p1)

    # Create work sessions for Project Beta
    session1_p2 = WorkSession(
        project_id=project2.proj_id,
        start_time=datetime.now() - timedelta(hours=4),
        end_time=datetime.now() - timedelta(hours=1),
        description="Developed the front-end components."
    )
    # Active session
    session2_p2 = WorkSession(
        project_id=project2.proj_id,
        start_time=datetime.now() - timedelta(minutes=30),
        description="Testing the API endpoints."
    )
    db.add_work_session_to_db(session1_p2)
    db.add_work_session_to_db(session2_p2)
    
    print("Database seeded with sample data.")
    print("Projects created: 3")
    print("Work sessions created: 4")

if __name__ == "__main__":
    seed_database()
