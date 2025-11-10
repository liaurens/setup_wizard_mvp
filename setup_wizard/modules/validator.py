import os


def validate_input(config):
    """
    Final validation safety check.
    Most validation happens during input collection in user_input.py.
    This provides a safety net for programmatically created configs.
    """
    if config is None:
        return False, "❌ Error: No configuration provided (user cancelled)"

    config.errors.clear()

    # Re-validate critical fields (safety check)
    is_valid = config.validate()

    # Check minimum length
    if len(config.matlab_name) <= 2:
        config.errors.append("Tool name too short (minimum 3 characters)")
        is_valid = False

    # Check maximum length
    if len(config.matlab_name) > 50:
        config.errors.append("Tool name too long (maximum 50 characters)")
        is_valid = False

    # Validate input file if provided (safety check)
    if config.input_file and config.input_file.strip():
        if not os.path.exists(config.input_file):
            config.errors.append(f"Input file not found: {config.input_file}")
            is_valid = False
        elif not config.input_file.lower().endswith('.mat'):
            config.errors.append("Input file must have .mat extension")
            is_valid = False

    if is_valid:
        return True, "✓ Configuration validated successfully"
    else:
        error_message = " | ".join(config.errors)
        return False, f"❌ Validation failed: {error_message}"
