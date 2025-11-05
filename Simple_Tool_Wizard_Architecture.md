# Simple Tool Wizard Architecture Guide
## A Beginner-Friendly Python Implementation

---

## Overview
This guide explains how to build a MATLAB Tool Wizard using Python with a simple command-line interface. Think of it as a program that asks you questions and then creates a complete MATLAB tool based on your answers.

---

## 1. What Does This Tool Do?

The Tool Wizard is like a recipe generator for MATLAB tools:
1. It asks you questions (tool name, what it does, etc.)
2. It fills in templates with your answers
3. It creates all the necessary files and folders
4. You get a working MATLAB tool ready to use!

---

## 2. Simple Project Structure

Here's how we organize our Python project:

```
tool-wizard/
│
├── main.py                  # The starting point - runs the wizard
├── config.py               # Settings and constants
│
├── modules/                # Different parts of our program
│   ├── __init__.py        # Makes this a Python package
│   ├── user_input.py      # Asks questions to the user
│   ├── validator.py       # Checks if answers are valid
│   ├── template_engine.py # Fills in the templates
│   └── file_generator.py  # Creates files and folders
│
├── templates/              # MATLAB templates with placeholders
│   ├── main_function.txt   # Main MATLAB function template
│   ├── test_template.txt   # Test file template
│   └── readme_template.txt # Documentation template
│
└── requirements.txt        # List of Python packages needed (minimal!)
```

---

## 3. How Do These Files Work Together?

Think of it like an assembly line:

```
main.py starts everything
    ↓
user_input.py asks questions
    ↓
validator.py checks the answers
    ↓
template_engine.py fills templates
    ↓
file_generator.py creates files
    ↓
Your MATLAB tool is ready!
```

### Here's what each file does:

**main.py** - The boss that coordinates everything
```python
# This is the file you run to start the wizard
from modules import user_input, template_engine, file_generator

def main():
    # Step 1: Get information from user
    tool_info = user_input.collect_tool_information()
    
    # Step 2: Process templates
    files_to_create = template_engine.process_templates(tool_info)
    
    # Step 3: Generate the tool
    output_path = file_generator.create_tool_structure(tool_info, files_to_create)
    
    print(f"Tool created successfully at: {output_path}")

if __name__ == "__main__":
    main()
```

**config.py** - Stores settings
```python
# All our configuration in one place
TEMPLATES_DIR = "templates"
OUTPUT_DIR = "generated_tools"
MAX_TOOL_NAME_LENGTH = 30

# Input and output types the user can choose
INPUT_TYPES = ["file_path", "direct_data", "config_file"]
OUTPUT_TYPES = ["file", "data_structure", "visualization", "report"]
```

---

## 4. The Core Modules Explained

### 4.1 User Input Module (user_input.py)

This module is like a questionnaire - it asks the user for information:

```python
# modules/user_input.py
from modules.validator import validate_tool_name, validate_description

def collect_tool_information():
    """Ask the user questions about their tool"""
    
    print("=== MATLAB Tool Wizard ===")
    print("I'll help you create a MATLAB tool. Please answer a few questions:\n")
    
    # Get tool name
    while True:
        tool_name = input("1. What do you want to name your tool? ")
        if validate_tool_name(tool_name):
            break
        print("   Tool name must start with a letter and contain only letters/numbers/underscores")
    
    # Get input type
    print("\n2. How will your tool receive data?")
    print("   1) File path")
    print("   2) Direct data input")
    print("   3) Configuration file")
    input_choice = input("   Choose (1-3): ")
    input_type = ["file_path", "direct_data", "config_file"][int(input_choice)-1]
    
    # Get output type
    print("\n3. What will your tool produce?")
    print("   1) A file")
    print("   2) A data structure")
    print("   3) A visualization")
    print("   4) A report")
    output_choice = input("   Choose (1-4): ")
    output_type = ["file", "data_structure", "visualization", "report"][int(output_choice)-1]
    
    # Get description
    description = input("\n4. Brief description of what your tool does: ")
    
    # Optional category
    category = input("\n5. Category (optional, press Enter to skip): ") or "general"
    
    # Return all information as a dictionary
    return {
        "tool_name": tool_name,
        "input_type": input_type,
        "output_type": output_type,
        "description": description,
        "category": category
    }
```

### 4.2 Validator Module (validator.py)

This checks if the user's answers are valid:

```python
# modules/validator.py
import re

def validate_tool_name(name):
    """Check if the tool name is valid"""
    
    # Must start with letter, contain only letters/numbers/underscores
    pattern = r'^[a-zA-Z][a-zA-Z0-9_]*$'
    
    # Check length
    if len(name) < 3 or len(name) > 30:
        return False
    
    # Check pattern
    if not re.match(pattern, name):
        return False
    
    # Check if it's a MATLAB reserved word
    reserved_words = ['function', 'end', 'if', 'else', 'for', 'while']
    if name.lower() in reserved_words:
        return False
    
    return True

def validate_description(description):
    """Check if description is valid"""
    return len(description) > 0 and len(description) < 500
```

### 4.3 Template Engine Module (template_engine.py)

This fills in the templates with the user's information:

```python
# modules/template_engine.py
import os
from config import TEMPLATES_DIR

def process_templates(tool_info):
    """Fill in templates with user information"""
    
    processed_files = {}
    
    # Read and process main function template
    main_template = read_template("main_function.txt")
    main_content = fill_template(main_template, tool_info)
    processed_files[f"{tool_info['tool_name']}.m"] = main_content
    
    # Read and process test template
    test_template = read_template("test_template.txt")
    test_content = fill_template(test_template, tool_info)
    processed_files[f"{tool_info['tool_name']}_Test.m"] = test_content
    
    # Read and process README template
    readme_template = read_template("readme_template.txt")
    readme_content = fill_template(readme_template, tool_info)
    processed_files["README.md"] = readme_content
    
    return processed_files

def read_template(template_name):
    """Read a template file"""
    template_path = os.path.join(TEMPLATES_DIR, template_name)
    with open(template_path, 'r') as file:
        return file.read()

def fill_template(template, tool_info):
    """Replace placeholders in template with actual values"""
    
    # Simple placeholder replacement
    # We use {{PLACEHOLDER}} format in templates
    content = template
    content = content.replace("{{TOOL_NAME}}", tool_info["tool_name"])
    content = content.replace("{{TOOL_NAME_UPPER}}", tool_info["tool_name"].upper())
    content = content.replace("{{DESCRIPTION}}", tool_info["description"])
    content = content.replace("{{INPUT_TYPE}}", tool_info["input_type"])
    content = content.replace("{{OUTPUT_TYPE}}", tool_info["output_type"])
    
    # Add input/output specific code based on type
    content = add_input_handling(content, tool_info["input_type"])
    content = add_output_handling(content, tool_info["output_type"])
    
    return content

def add_input_handling(content, input_type):
    """Add specific code based on input type"""
    
    if input_type == "file_path":
        input_code = """
    % Check if file exists
    if ~exist(input, 'file')
        error('{{TOOL_NAME}}:FileNotFound', 'Input file not found');
    end
    data = readmatrix(input);"""
    
    elif input_type == "direct_data":
        input_code = """
    % Validate input data
    if isempty(input)
        error('{{TOOL_NAME}}:EmptyInput', 'Input cannot be empty');
    end
    data = input;"""
    
    else:  # config_file
        input_code = """
    % Load configuration
    config = jsondecode(fileread(input));
    data = config.data;"""
    
    return content.replace("{{INPUT_HANDLING}}", input_code)

def add_output_handling(content, output_type):
    """Add specific code based on output type"""
    
    if output_type == "file":
        output_code = "writematrix(result, 'output.csv');"
    elif output_type == "data_structure":
        output_code = "output = result;"
    elif output_type == "visualization":
        output_code = "figure; plot(result); title('Results');"
    else:  # report
        output_code = "generateReport(result);"
    
    return content.replace("{{OUTPUT_HANDLING}}", output_code)
```

### 4.4 File Generator Module (file_generator.py)

This creates the actual files and folders:

```python
# modules/file_generator.py
import os
from config import OUTPUT_DIR

def create_tool_structure(tool_info, files_content):
    """Create the folder structure and files for the tool"""
    
    tool_name = tool_info["tool_name"]
    
    # Create main tool directory
    tool_path = os.path.join(OUTPUT_DIR, tool_name)
    os.makedirs(tool_path, exist_ok=True)
    
    # Create subdirectories
    subdirs = [
        f"+{tool_name.lower()}",  # MATLAB package for private functions
        "+tests",                  # Tests folder
        "Templates",               # Config templates
        "docs"                     # Documentation
    ]
    
    for subdir in subdirs:
        os.makedirs(os.path.join(tool_path, subdir), exist_ok=True)
    
    # Write main files
    for filename, content in files_content.items():
        if filename.endswith("_Test.m"):
            # Put test files in the tests folder
            filepath = os.path.join(tool_path, "+tests", filename)
        elif filename == "README.md":
            # Put README in docs folder
            filepath = os.path.join(tool_path, "docs", filename)
        else:
            # Put main file in root
            filepath = os.path.join(tool_path, filename)
        
        with open(filepath, 'w') as file:
            file.write(content)
    
    # Create additional required files
    create_changelog(tool_path, tool_info)
    
    print(f"\n✅ Tool structure created at: {tool_path}")
    print_directory_tree(tool_path)
    
    return tool_path

def create_changelog(tool_path, tool_info):
    """Create a changelog file"""
    
    changelog_content = f"""# Changelog for {tool_info['tool_name']}

## [1.0.0] - {get_current_date()}
### Added
- Initial version of {tool_info['tool_name']}
- Basic functionality: {tool_info['description']}
- Input type: {tool_info['input_type']}
- Output type: {tool_info['output_type']}
"""
    
    with open(os.path.join(tool_path, "changelog.yml"), 'w') as file:
        file.write(changelog_content)

def get_current_date():
    """Get today's date"""
    from datetime import date
    return date.today().strftime("%Y-%m-%d")

def print_directory_tree(path):
    """Print the created directory structure"""
    print("\nCreated structure:")
    for root, dirs, files in os.walk(path):
        level = root.replace(path, '').count(os.sep)
        indent = ' ' * 2 * level
        print(f'{indent}{os.path.basename(root)}/')
        subindent = ' ' * 2 * (level + 1)
        for file in files:
            print(f'{subindent}{file}')
```

---

## 5. Template Examples

### 5.1 Main Function Template (templates/main_function.txt)

```matlab
function [output] = {{TOOL_NAME}}(input, options)
% {{TOOL_NAME_UPPER}} - {{DESCRIPTION}}
%
% Syntax:
%   output = {{TOOL_NAME}}(input)
%   output = {{TOOL_NAME}}(input, options)
%
% Inputs:
%   input - Input data ({{INPUT_TYPE}})
%   options - Optional parameters structure
%
% Outputs:
%   output - {{OUTPUT_TYPE}}
%
% Example:
%   result = {{TOOL_NAME}}(myData);

% Input validation
arguments
    input
    options.verbose (1,1) logical = false
end

% Main processing
try
    {{INPUT_HANDLING}}
    
    % Process data (TODO: Add your processing logic here)
    result = processData(data);
    
    {{OUTPUT_HANDLING}}
    
catch ME
    fprintf('Error in {{TOOL_NAME}}: %s\n', ME.message);
    rethrow(ME);
end

end

% Helper function
function result = processData(data)
    % TODO: Implement your data processing here
    result = data; % Placeholder
end
```

### 5.2 Test Template (templates/test_template.txt)

```matlab
classdef {{TOOL_NAME}}_Test < matlab.unittest.TestCase
    
    methods(Test)
        function testBasicExecution(testCase)
            % Test that the tool runs without errors
            
            % Create sample input
            sampleInput = [1, 2, 3, 4, 5];
            
            % Run the tool
            output = {{TOOL_NAME}}(sampleInput);
            
            % Verify it produces output
            testCase.verifyNotEmpty(output);
        end
        
        function testEmptyInput(testCase)
            % Test that empty input is handled properly
            
            emptyInput = [];
            
            % This should produce an error
            testCase.verifyError(@() {{TOOL_NAME}}(emptyInput), ...
                                '{{TOOL_NAME}}:EmptyInput');
        end
    end
end
```

---

## 6. How Components Communicate

### Communication Flow Diagram

```
User runs: python main.py
            │
            ▼
    ┌──────────────┐
    │   main.py    │ ←── Orchestrator (controls the flow)
    └──────┬───────┘
           │
           │ calls collect_tool_information()
           ▼
    ┌──────────────┐
    │ user_input.py│ ←── Collects data from user
    └──────┬───────┘
           │ 
           │ returns dictionary: {"tool_name": "MyTool", ...}
           ▼
    ┌──────────────┐
    │ validator.py │ ←── Validates the data
    └──────┬───────┘
           │
           │ data passes validation
           ▼
    ┌──────────────────┐
    │template_engine.py│ ←── Processes templates
    └──────┬───────────┘
           │
           │ returns dict: {"MyTool.m": "content...", ...}
           ▼
    ┌──────────────────┐
    │file_generator.py │ ←── Creates files
    └──────────────────┘
           │
           ▼
    Tool created in generated_tools/MyTool/
```

### Data Flow Between Modules

The modules communicate by passing Python dictionaries (like a package of information):

1. **user_input.py** creates a dictionary:
```python
tool_info = {
    "tool_name": "DataAnalyzer",
    "input_type": "file_path",
    "output_type": "report",
    "description": "Analyzes data files"
}
```

2. **template_engine.py** receives this dictionary and creates another:
```python
files_content = {
    "DataAnalyzer.m": "function code here...",
    "DataAnalyzer_Test.m": "test code here...",
    "README.md": "documentation here..."
}
```

3. **file_generator.py** receives both dictionaries and creates the files

---

## 7. Minimal Python Dependencies

For the MVP, we only need Python's built-in libraries:

**requirements.txt** (almost empty!):
```
# No external dependencies required for MVP!
# Using only Python standard library
```

If you want to add features later:
```
# Optional enhancements (not needed for MVP):
# pyyaml==6.0  # For YAML configuration files
# colorama==0.4.6  # For colored terminal output
```

---

## 8. How to Run the Wizard

### Step 1: Set up the project
```bash
# Create project directory
mkdir tool-wizard
cd tool-wizard

# Create the folder structure
mkdir modules templates generated_tools

# Create the Python files
touch main.py config.py
touch modules/__init__.py modules/user_input.py modules/validator.py
touch modules/template_engine.py modules/file_generator.py
```

### Step 2: Add the templates
Create your template files in the `templates/` folder with placeholders like `{{TOOL_NAME}}`

### Step 3: Run the wizard
```bash
python main.py
```

### Step 4: Answer the questions
```
=== MATLAB Tool Wizard ===
1. What do you want to name your tool? DataProcessor
2. How will your tool receive data? 1
3. What will your tool produce? 2
4. Brief description: Processes sensor data
5. Category: analysis

✅ Tool created at: generated_tools/DataProcessor/
```

---

## 9. Testing Your Wizard

Create a simple test file to make sure everything works:

**test_wizard.py**:
```python
import os
import sys
sys.path.append('.')  # Add current directory to path

from modules import user_input, validator, template_engine, file_generator

def test_validator():
    """Test the validator module"""
    print("Testing validator...")
    
    # Should pass
    assert validator.validate_tool_name("MyTool") == True
    assert validator.validate_tool_name("Tool123") == True
    
    # Should fail
    assert validator.validate_tool_name("123Tool") == False
    assert validator.validate_tool_name("my-tool") == False
    assert validator.validate_tool_name("if") == False
    
    print("✓ Validator tests passed")

def test_template_engine():
    """Test template processing"""
    print("Testing template engine...")
    
    test_info = {
        "tool_name": "TestTool",
        "input_type": "file_path",
        "output_type": "data_structure",
        "description": "A test tool"
    }
    
    # Test placeholder replacement
    template = "Tool name is {{TOOL_NAME}}"
    result = template.replace("{{TOOL_NAME}}", test_info["tool_name"])
    assert result == "Tool name is TestTool"
    
    print("✓ Template engine tests passed")

if __name__ == "__main__":
    test_validator()
    test_template_engine()
    print("\nAll tests passed! ✅")
```

---

## 10. Common Issues and Solutions

### Issue 1: "Module not found"
**Solution**: Make sure you have `__init__.py` in the modules folder (it can be empty)

### Issue 2: "Template not found"
**Solution**: Check that your template files are in the `templates/` folder

### Issue 3: "Permission denied when creating files"
**Solution**: Make sure the `generated_tools/` folder exists and you have write permissions

---

## 11. Next Steps After MVP

Once your basic wizard works, you can enhance it:

1. **Add more templates**: Create templates for different tool types
2. **Add configuration file**: Store settings in a JSON/YAML file
3. **Add colors**: Use the `colorama` library for colored output
4. **Add progress bar**: Show progress for long operations
5. **Add more validation**: Check for existing tools, validate file paths
6. **Add logging**: Keep a record of generated tools

---

## Summary

This Tool Wizard is built like a simple assembly line:
1. **Collect** information from the user (command line questions)
2. **Validate** the information (check it's correct)
3. **Process** templates (fill in the blanks)
4. **Generate** files (create the tool structure)

The beauty of this design is that each part does one job well, and they work together by passing dictionaries of information. No complex frameworks needed - just plain Python!

**Key Points for Beginners:**
- Each module is a separate file that does one specific job
- Modules communicate by passing dictionaries (Python's way of grouping data)
- Templates use simple placeholder replacement ({{TOOL_NAME}} becomes "MyTool")
- Everything runs from the command line - no complex UI needed
- The whole thing uses only Python's built-in features - no extra libraries required!
