# ui/ui_handler.py

class UIHandler:
    """
    Handles user interface interactions for the Project Time Tracker application.
    """
    def display_welcome_message(self):
        print("Welcome to the Project Time Tracker!")

    def display_project_details(self, project):
        print(f"Project Name: {project.name}")
        print(f"Description: {project.description}")
        print(f"Archived: {project.archived}")
        print(f"Number of Work Sessions: {len(project.work_sessions)}")

    def display_work_session_details(self, work_session):
        print(f"Work Session ID: {work_session.id}")
        print(f"Start Time: {work_session.start_time}")
        print(f"End Time: {work_session.end_time}")
        print(f"Description: {work_session.description}")

    def prompt_for_project_name(self):
        return input("Enter the project name: ")

    def prompt_for_project_description(self):
        return input("Enter the project description: ")

    def prompt_for_work_session_description(self):
        return input("Enter the work session description: ")
