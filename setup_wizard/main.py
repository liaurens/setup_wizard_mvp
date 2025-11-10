from setup_wizard import modules


def intro():
    print("\n" + "🔧 " * 20)
    print("    Welcome to the MATLAB Tool Setup Wizard!")
    print("🔧 " * 20)


def main():
    intro()

    # Get user input (with immediate validation)
    tool_info = modules.get_user_input()

    # Check if user cancelled
    if tool_info is None:
        print("\n👋 Wizard cancelled. Goodbye!")
        return

    # Final validation (safety check)
    is_valid, message = modules.validate_input(tool_info)

    if not is_valid:
        print(f"\n{message}")
        print("❌ Tool creation failed. Please restart the wizard.\n")
        return

    print(f"{message}")

    # Generate files
    try:
        result = modules.generate_files(tool_info)
        print(f"\n{'='*60}")
        print(f"✓ SUCCESS!")
        print(f"{'='*60}")
        print(f"{result}")
        print(f"{'='*60}\n")
    except Exception as e:
        print(f"\n{'='*60}")
        print(f"❌ ERROR during file generation:")
        print(f"{'='*60}")
        print(f"{str(e)}")
        print(f"{'='*60}\n")


if __name__ == "__main__":
    main()
