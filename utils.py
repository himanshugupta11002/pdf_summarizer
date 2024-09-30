import os

def save_data(data, file_name):
    """Save data to a file on the user's system."""
    data_dir = os.path.join(os.path.expanduser("~"), ".your_app_data")  
    os.makedirs(data_dir, exist_ok=True)  
    file_path = os.path.join(data_dir, file_name)
    with open(file_path, "w") as file:
        file.write(data)

def load_data(file_name):
    """Load data from a file on the user's system."""
    data_dir = os.path.join(os.path.expanduser("~"), ".your_app_data")
    file_path = os.path.join(data_dir, file_name)
    if os.path.exists(file_path):
        with open(file_path, "r") as file:
            data = file.read()
        return data
    else:
        return None
