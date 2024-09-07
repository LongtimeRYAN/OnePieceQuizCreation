import json
import os

def load_questions_from_file(arc_name):
    # Mapping arc names to JSON file names
    arc_file_mapping = {
        "Arlong Park": "arlong_park.json",
        "Syrup Village": "syrup_village.json"
    }

    # Get the correct directory of the script (absolute path)
    script_dir = os.path.dirname(os.path.abspath(__file__))  # This gets the current directory of the script

    # Construct the full file path
    file_path = os.path.join(script_dir, arc_file_mapping.get(arc_name, None))

    # Check if the file exists
    if not os.path.exists(file_path):
        print(f"File not found: {file_path}")
        return

    # Try loading the file
    try:
        with open(file_path, 'r') as f:
            data = json.load(f)
            print(f"Loaded data from {arc_name}:")
            print(json.dumps(data, indent=4))  # Print the loaded JSON data in a readable format
    except Exception as e:
        print(f"Error reading file: {e}")

if __name__ == "__main__":
    # Prompt the user to choose which arc to load
    arc_choice = input("Enter the arc to load (Arlong Park or Syrup Village): ")
    
    # Load and print the questions from the chosen arc
    load_questions_from_file(arc_choice)
