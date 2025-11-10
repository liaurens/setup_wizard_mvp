import os

def process_template(template_name, config):
    # Get the directory of the package (setup_wizard_MVP/)
    package_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    templates_path = os.path.join(package_dir, 'templates', template_name)
    with open(templates_path, 'r') as file:
        template = file.read()
    completed_template = template.replace("MATLAB_NAME", config.matlab_name)
    completed_template = completed_template.replace("INPUT_FILE", config.input_file)
    return completed_template


def generate_files(config):
    base_path = os.path.join(config.output_path, config.matlab_name)
    src_folder = os.path.join(base_path, "src")
    docs_folder = os.path.join(base_path, "docs")
    os.makedirs(src_folder, exist_ok=True)
    os.makedirs(docs_folder, exist_ok=True)

    # Generate MATLAB file
    if config.input_file:
        template_name = "matlab_input_tool.m"
    else:
        template_name = "matlab_tool.m"
    matlab_template = process_template(template_name, config)
    matlab_file_path = os.path.join(src_folder, f"{config.matlab_name}.m")
    with open(matlab_file_path, 'w') as file:
        file.write(matlab_template)

    # Generate README file
    readme_template = process_template("readme.md", config)
    readme_file_path = os.path.join(docs_folder, "README.md")
    with open(readme_file_path, 'w') as file:
        file.write(readme_template)

    # Return success message
    return f"Tool '{config.matlab_name}' created successfully at {base_path}"