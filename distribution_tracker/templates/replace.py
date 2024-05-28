import os
import re

def replace_static_paths(file_path):
    # Define the pattern to match src and href attributes with local paths
    pattern = r'(src|href)="([^"]+)"'
    
    with open(file_path, 'r', encoding='utf-8') as file:
        content = file.read()

    # Function to replace the matched pattern with the {% static %} template tag
    def replacement(match):
        attribute = match.group(1)
        path = match.group(2)
        if not path.startswith("{% static"):
            return f'{attribute}="{{% static \'{path}\' %}}"'
        return match.group(0)
    
    # Use re.sub with the replacement function to modify the content
    new_content = re.sub(pattern, replacement, content)

    if new_content != content:
        print(f"Updated: {file_path}")
    else:
        print(f"No changes made: {file_path}")

    # Write the new content back to the same file
    with open(file_path, 'w', encoding='utf-8') as file:
        file.write(new_content)

def process_html_files_in_directory(root_directory):
    for dirpath, dirnames, filenames in os.walk(root_directory):
        for filename in filenames:
            if filename.endswith('.html'):
                file_path = os.path.join(dirpath, filename)
                print(f'Processing file: {file_path}')
                replace_static_paths(file_path)

# Example usage
root_directory = ''
process_html_files_in_directory(root_directory)
