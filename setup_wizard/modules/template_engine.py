import os

def setup_template(config):


    print(f"Setting up {config.matlab_name}")
    template_path = os.path.join('templates', 'readme.txt')
    with open(template_path, 'r') as file:
        template = file.read()

    completed_template = template.replace("MATLAB_NAME", config.matlab_name)
    return completed_template
