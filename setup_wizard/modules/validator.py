import os

def validate_input(config):
    is_valid = config.validate()


    if len(config.matlab_name)==2:
        config.errors.append("too short")
        is_valid = False

    if config.input_file and config.input_file.strip():  # Only validate if user provided a path
        if not os.path.exists(config.input_file):
            config.errors.append(f"Input file not found: {config.input_file}")
            is_valid = False
        elif not config.input_file.endswith('.mat'):
            config.errors.append("Input file must have .mat extension")
            is_valid = False


    if is_valid:
        return True, "valid input"
    else:
        error_message = ": ".join(config.errors)
        return False, error_message

