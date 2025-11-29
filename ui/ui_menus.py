# ui/ui_menus.py

class MainMenu:
    """
    Main menu interface for the Project Time Tracker application.
    """
    def display_menu(self):
        print("=== Project Time Tracker ===")
        print("1. Create New Project")
        print("2. View Projects")
        print("3. Start Work Session")
        print("4. End Work Session")
        print("5. View Reports")
        print("6. Exit")

    def prompt_for_menu_choice(self):
        return input("Select an option (1-6): ")

class ProjectMenu:
    """
    Project menu interface for managing project.
    """
    def display_project_menu(self):
        print("=== Project Menu ===")
        print("1. Rename Project")
        print("2. Archive Project")
        print("3. Set Project Description")
        print("4. Back to Main Menu")

    def prompt_for_project_menu_choice(self):
        return input("Select an option (1-4): ")

