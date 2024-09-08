import os
import json

def load_questions_from_file(arc_name: str):
    # Mapping arc names to JSON file names
    arc_file_mapping = {
        "Arlong Park": "arlong_park.json",
        "Syrup Village": "syrup_village.json"
    }

    # Get the correct directory of the script (absolute path)
    script_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "data")

    # Log the arc name to ensure we're using the correct one
    logger.info(f"Selected arc: {arc_name}")

    # Construct the full file path
    file_path = os.path.join(script_dir, arc_file_mapping[arc_name])
    
    # Debugging: Show the file path and check if it exists
    st.write(f"Attempting to load questions from file: {file_path}")
    file_exists = os.path.exists(file_path)
    st.write(f"File exists: {file_exists}")

    # If the file doesn't exist, return an empty list
    if not file_exists:
        st.error(f"No questions found for the arc: {arc_name}")
        logger.error(f"File not found for arc: {arc_name}")
        return []

    # Try loading the file, catch any issues
    try:
        with open(file_path, 'r') as f:
            data = json.load(f)
            logging.info(f"Loaded data from {arc_name}: {data}")  # Log loaded data
    except Exception as e:
        st.error(f"Error reading file: {e}")
        logger.error(f"Error reading file for {arc_name}: {e}")
        return []

    # Check if 'questions' exists in the data, print questions and return them
    questions = data.get("questions", [])
    st.write(f"Questions loaded for {arc_name}: {questions}")
    return questions