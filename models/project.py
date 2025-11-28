# models\project.py

class Project:
    def __init__(self, name:str, description:str, proj_id:int=None, archived:bool=False ):
        self.name = name
        self.description = description
        self.work_sessions = []
        self.proj_id = proj_id
        self.archived = archived

    def archive(self):
        self.archived = True

    def set_description(self, description:str):
        self.description = description

    def add_work_session(self, work_session):
        self.work_sessions.append(work_session)

    def __repr__(self):
        return f"Project(id={self.proj_id}, name={self.name}, description={self.description}, archived={self.archived})"

    def __str__(self):
        return f"Project: {self.name} (ID: {self.proj_id})\nDescription: {self.description}\nArchived: {self.archived}\nWork Sessions: {len(self.work_sessions)}"



