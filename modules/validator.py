def validate_input(create_tool, matlab_name):
    if create_tool.upper() not in ["Y", "N"]:
        return False, "No Y/N"

    if not matlab_name.replace(" ", "").isalpha():
        return False, "only letters allowed"

    if not matlab_name.strip():
        return False, "empty string"

    return True, "Valid input"