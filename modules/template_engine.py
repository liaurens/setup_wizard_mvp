import os

def setup_template(matlab_name, valid_input):
    if not valid_input:
        print("cant continue invalid input")
        return

    print(f"Setting up {matlab_name}")
    template_path = os.path.join('templates', 'readme.txt')
    with open(template_path, 'r') as file:
        template = file.read()

    completed_template = template.replace("MATLAB_NAME", matlab_name)
    return completed_template
