def validate_input(config):
    is_valid = config.validate()

    if len(config.matlab_name)==2:
        config.errors.append("too short")
        is_valid = False

    if is_valid:
        return True, "valid input"
    else:
        error_message = ": ".join(config.errors)
        return False, error_message

