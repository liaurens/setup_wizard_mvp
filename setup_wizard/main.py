from setup_wizard import modules

def intro():
    print("Welcome to the setup wizard!")

def main():
    intro()
    tool_info = modules.get_user_input()
    is_valid, message = modules.validate_input(tool_info)
    if not is_valid:
        print(message)
        return

    print(message)
    result = modules.generate_files(tool_info)
    print(result)
if __name__ == "__main__":
    main()


