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

