from .models import ToolConfig


def get_user_input():

    create_tool_s = input("Do you want to create a tool? (Y/N): ")
    create_tool = create_tool_s.upper() == "Y"

    matlab_name = input("What is the name of your tool?: ")
    config = ToolConfig(create_tool=create_tool, matlab_name=matlab_name)
    return config

