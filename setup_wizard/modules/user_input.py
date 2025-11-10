from setup_wizard.modules.models import ToolConfig


def get_user_input():

    create_tool_s = input("Do you want to create a tool? (Y/N): ")
    create_tool = create_tool_s.upper() == "Y"

    matlab_name = input("What is the name of your tool?: ")
    output_path = input("Where do you want to save the tool? Press enter for default: ")
    input_file = input("What is the path of your inputfile? (pres enter if not applicable):").strip()
    if not output_path:
        output_path = "./generated_tools"
    config = ToolConfig(create_tool=create_tool,
                        matlab_name=matlab_name,
                        output_path=output_path,
                        input_file= input_file)
    return config

