# ui/main_menu.py

class MainMenu:
    """
    Main menu interface for the Project Time Tracker application.
    """
    def __init__(self):
        self.header = "=== Project Time Tracker ==="
        self.options = [
            "1. View Projects",
            "2. Create new Project",
            "3. Start Work Session",
            "4. End Active Work Session",
            "5. Export to CSV",
            "6. Exit"
            ]

    def display_menu(self):
        print(self.header)
        print()
        for option in self.options:
            print(option)

    def prompt_for_menu_choice(self):
        return input(f"Select an option (1-{len(self.options)}): ")

    def handle_menu_choice(self, choice):
        match choice:
            case '1':
                print()
            case '2':
                print("Creating new project...")
            case '3':
                print("Starting a work session...")
            case '4':
                print("Ending a work session...")
            case '5':
                print("Exporting data to CSV...")
            case '6':
                print("Exiting the application...")
            case _:
                print("Invalid choice. Please select a valid option.")

    def print_project_list(self, projects):
        if not projects:
            print("No projects available.")
            return
        print("Projects:")
        for project in projects:

            print(f"- {project.name} (ID: {project.proj_id}, Status: {status})")