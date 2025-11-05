def get_user_input():
    create_tool = input("Do you want to create a tool? (Y/N): ")
    matlab_name = input("What is the name of your tool?: ")
    return create_tool, matlab_name

def greet():
    print("HI")