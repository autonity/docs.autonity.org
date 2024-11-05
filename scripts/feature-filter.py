import yaml
from pathlib import Path
import re

css_directory = Path("docs/_assets/css")
feature_config = Path("_features.yml")

def load_features_config(filepath):
    """Load the feature configuration file."""
    with open(filepath, 'r') as file:
        try:
            config = yaml.safe_load(file)
            return config
        except yaml.YAMLError as e:
            print(f"Error loading YAML file: {e}")
            return None

def remove_css_classes(content, classes_to_remove):
    """Remove specified CSS classes."""
    for css_class in classes_to_remove:
        pattern = rf'\.{css_class}\s*\{{[^}}]*\}}'
        content = re.sub(pattern, '', content, flags=re.MULTILINE)
    return content

def modify_css_files(css_directory, classes_to_remove):
    """Find and modify CSS files in the specified directory."""
    for css_file in css_directory.glob("*.scss"):
        with open(css_file, 'r+') as file:
            content = file.read()
            updated_content = remove_css_classes(content, classes_to_remove)
            file.seek(0)
            file.write(updated_content)
            file.truncate()

if __name__ == "__main__":
    print("Feature filter script started.")
    config = load_features_config(feature_config.resolve())
    if config and 'css' in config:
        classes_to_remove = config['css_classes']
        print(f"Removing: {classes_to_remove}")
        modify_css_files(css_directory, classes_to_remove)
    else:
        print("No CSS classes found to remove.")

