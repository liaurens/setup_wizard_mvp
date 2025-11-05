import modules

def intro():
    print("Welcome to the setup wizard!")

def main():
    intro()
    create_tool, matlab_name = modules.get_user_input()
    valid_input, message = modules.validate_input(create_tool, matlab_name)
    print(message)
    created_template = modules.setup_template(matlab_name, valid_input)
    print(created_template)
if __name__ == "__main__":
    main()


