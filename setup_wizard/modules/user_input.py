from setup_wizard.modules.models import ToolConfig
import os


def get_user_input():
    """
    Collects user input with immediate validation and retry loops.
    Provides clear feedback for each input field.
    """
    print("\n" + "="*60)
    print("          MATLAB TOOL SETUP WIZARD")
    print("="*60 + "\n")

    # Step 1: Confirm tool creation
    while True:
        create_tool_s = input("Do you want to create a tool? (Y/N): ").strip().upper()

        if create_tool_s in ['Y', 'YES']:
            create_tool = True
            print("✓ Starting tool creation...\n")
            break
        elif create_tool_s in ['N', 'NO']:
            print("\nℹ Exiting wizard. No tool will be created.")
            return None
        else:
            print("❌ Invalid input. Please enter 'Y' for Yes or 'N' for No.\n")

    # Step 2: Get and validate tool name
    print("-" * 60)
    print("STEP 1: Tool Name")
    print("-" * 60)
    print("Requirements:")
    print("  • Minimum 3 characters")
    print("  • Only letters (spaces allowed)")
    print("  • Example: 'DataAnalyzer' or 'My Tool'\n")

    while True:
        matlab_name = input("Enter tool name: ").strip()

        # Check empty
        if not matlab_name:
            print("❌ Error: Tool name cannot be empty. Please try again.\n")
            continue

        # Check only letters (spaces allowed)
        if not matlab_name.replace(" ", "").isalpha():
            print(f"❌ Error: Tool name '{matlab_name}' contains invalid characters.")
            print("   Only letters and spaces are allowed (no numbers or special characters).")
            print("   Please try again.\n")
            continue

        # Check minimum length
        if len(matlab_name) <= 2:
            print(f"❌ Error: Tool name '{matlab_name}' is too short ({len(matlab_name)} characters).")
            print("   Minimum length is 3 characters. Please try again.\n")
            continue

        # Check maximum length (reasonable limit)
        if len(matlab_name) > 50:
            print(f"❌ Error: Tool name '{matlab_name}' is too long ({len(matlab_name)} characters).")
            print("   Maximum length is 50 characters. Please try again.\n")
            continue

        # Valid name
        print(f"✓ Tool name '{matlab_name}' accepted.\n")
        break

    # Step 3: Get output path
    print("-" * 60)
    print("STEP 2: Output Location")
    print("-" * 60)
    print("Specify where to save the generated tool.")
    print("Press Enter to use default: './generated_tools'\n")

    while True:
        output_path = input("Output path (or press Enter for default): ").strip()

        if not output_path:
            output_path = "./generated_tools"
            print(f"✓ Using default output path: {output_path}\n")
            break

        # Validate path (check if parent directory exists or can be created)
        try:
            # Try to get absolute path
            abs_path = os.path.abspath(output_path)

            # Check if path already exists
            if os.path.exists(abs_path):
                if not os.path.isdir(abs_path):
                    print(f"❌ Error: '{output_path}' exists but is not a directory.")
                    print("   Please provide a valid directory path.\n")
                    continue
                else:
                    print(f"✓ Output path exists: {output_path}\n")
                    break
            else:
                # Path doesn't exist, check if parent exists
                parent = os.path.dirname(abs_path)
                if parent and not os.path.exists(parent):
                    print(f"⚠ Warning: Parent directory '{parent}' does not exist.")
                    create_parent = input("   Create parent directories? (Y/N): ").strip().upper()
                    if create_parent in ['Y', 'YES']:
                        print(f"✓ Will create directory: {output_path}\n")
                        break
                    else:
                        print("   Please provide a different path.\n")
                        continue
                else:
                    print(f"✓ Output path accepted: {output_path}\n")
                    break
        except Exception as e:
            print(f"❌ Error: Invalid path '{output_path}': {str(e)}")
            print("   Please provide a valid directory path.\n")
            continue

    # Step 4: Get and validate input file
    print("-" * 60)
    print("STEP 3: Input File (Optional)")
    print("-" * 60)
    print("Provide a .mat file path if your tool needs input data.")
    print("Press Enter to skip if not applicable.\n")

    while True:
        input_file = input("Input .mat file path (or press Enter to skip): ").strip()

        # If empty, skip validation
        if not input_file:
            print("✓ No input file specified.\n")
            input_file = ""
            break

        # Remove quotes if user wrapped path in quotes
        input_file = input_file.strip('"').strip("'")

        # Validate file exists
        if not os.path.exists(input_file):
            print(f"❌ Error: File not found at '{input_file}'")
            print("   Please check the path and try again, or press Enter to skip.\n")
            continue

        # Validate it's a file, not a directory
        if os.path.isdir(input_file):
            print(f"❌ Error: '{input_file}' is a directory, not a file.")
            print("   Please provide a file path, or press Enter to skip.\n")
            continue

        # Validate .mat extension (case-insensitive)
        if not input_file.lower().endswith('.mat'):
            file_ext = os.path.splitext(input_file)[1]
            print(f"❌ Error: File must have .mat extension (got: {file_ext or 'no extension'})")
            print("   Please provide a .mat file, or press Enter to skip.\n")
            continue

        # Validate file is readable
        try:
            with open(input_file, 'rb') as f:
                # Try to read first byte to ensure file is accessible
                f.read(1)
            print(f"✓ Input file accepted: {input_file}\n")
            break
        except PermissionError:
            print(f"❌ Error: Permission denied to read file '{input_file}'")
            print("   Please check file permissions, or press Enter to skip.\n")
            continue
        except Exception as e:
            print(f"❌ Error: Cannot read file '{input_file}': {str(e)}")
            print("   Please provide a valid file, or press Enter to skip.\n")
            continue

    # Create configuration
    print("=" * 60)
    print("Configuration Summary:")
    print("=" * 60)
    print(f"Tool Name:    {matlab_name}")
    print(f"Output Path:  {output_path}")
    print(f"Input File:   {input_file if input_file else '(none)'}")
    print("=" * 60 + "\n")

    config = ToolConfig(
        create_tool=create_tool,
        matlab_name=matlab_name,
        output_path=output_path,
        input_file=input_file
    )

    return config
