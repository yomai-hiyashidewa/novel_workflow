
import os
import shutil

class Director:
    def __init__(self, work_folder):
        self.work_folder = work_folder
        self.steps = [
            {"id": "A", "name": "record", "prompt": "recorder.md", "output_folder": "01_record"},
            {"id": "B", "name": "research", "prompt": "researcher.md", "output_folder": "02_research"},
            {"id": "C", "name": "plan", "prompt": "planner.md", "output_folder": "03_plan"},
            {"id": "D", "name": "plot", "prompt": "plotter.md", "output_folder": "04_plot"},
            {"id": "E", "name": "write", "prompt": "writer.md", "output_folder": "05_manuscript"},
            {"id": "F", "name": "illustrate", "prompt": "illustrator.md", "output_folder": "06_illustration"},
        ]
        self._create_project_structure()

    def _create_project_structure(self):
        """Creates the necessary folder structure for the project."""
        if not os.path.exists(self.work_folder):
            os.makedirs(self.work_folder)
            print(f"Created working folder: {self.work_folder}")

        for step in self.steps:
            folder_path = os.path.join(self.work_folder, step["output_folder"])
            if not os.path.exists(folder_path):
                os.makedirs(folder_path)
                print(f"Created folder: {folder_path}")

    def _client_check(self, step_name):
        """Simulates the client check process."""
        while True:
            response = input(f"Proceed to the next step after '{step_name}'? (yes/no): ").lower()
            if response in ["yes", "y"]:
                return True
            elif response in ["no", "n"]:
                print("Project halted by user.")
                return False
            else:
                print("Invalid input. Please enter 'yes' or 'no'.")

    def run_workflow(self):
        """Runs the entire novel writing workflow."""
        print("Starting novel writing workflow...")
        for step in self.steps:
            print(f"--- Running Step {step['id']}: {step['name']} ---")
            # Here you would typically run the prompt associated with the step
            # For now, we'll just print a message
            print(f"Executing prompt: {step['prompt']}")
            print(f"Output will be saved in: {step['output_folder']}")

            if not self._client_check(step['name']):
                break
        print("--- Workflow finished ---")

if __name__ == '__main__':
    # The user should specify the working folder.
    # For demonstration, we'll use a folder named 'novel_project' in the current directory.
    project_path = os.path.join(os.getcwd(), "novel_project")
    
    director = Director(project_path)
    director.run_workflow()
