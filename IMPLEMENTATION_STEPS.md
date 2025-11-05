# Data Class Implementation Steps for Your Project

## Quick Summary

**What are data classes?**
Data classes are Python objects that store data with automatic features like initialization, string representation, and comparison. Think of them as "smart containers" for related information.

**Why use them?**
- Your IDE will autocomplete field names (prevents typos)
- Pass ONE object instead of multiple variables
- Easy to add new fields without breaking existing code
- Built-in validation and data cleaning

## Step-by-Step Implementation

### Step 1: Create the models directory (30 seconds)

```bash
cd /home/user/setup_wizard_mvp
mkdir -p modules/models
touch modules/models/__init__.py
touch modules/models/tool_config.py
```

### Step 2: Create your ToolConfig data class (2 minutes)

**File: `modules/models/tool_config.py`**

```python
"""Data model for tool configuration"""

from dataclasses import dataclass, field
from typing import List

@dataclass
class ToolConfig:
    """
    Configuration for a MATLAB tool to be generated.

    This class stores all information needed to create a tool.
    It replaces passing around multiple variables or dictionaries.
    """

    # =========================================
    # REQUIRED FIELDS (user must provide)
    # =========================================
    matlab_name: str
    create_tool: str

    # =========================================
    # OPTIONAL FIELDS (have defaults)
    # =========================================
    description: str = ""
    input_type: str = "file_path"
    output_type: str = "data_structure"
    category: str = "general"
    author: str = ""
    version: str = "1.0.0"

    # =========================================
    # INTERNAL FIELDS (not set by user)
    # =========================================
    errors: List[str] = field(default_factory=list, init=False)

    def __post_init__(self):
        """
        Called automatically after __init__
        Use this to clean/normalize data
        """
        self.matlab_name = self.matlab_name.strip()
        self.create_tool = self.create_tool.upper()
        self.category = self.category.lower()

    def validate(self) -> bool:
        """
        Validate all fields and populate self.errors

        Returns:
            True if valid, False otherwise
        """
        self.errors.clear()

        # Validate create_tool
        if self.create_tool not in ["Y", "N"]:
            self.errors.append("create_tool must be Y or N")

        # Validate matlab_name
        if not self.matlab_name.replace(" ", "").isalpha():
            self.errors.append("Tool name must contain only letters")

        if len(self.matlab_name) < 3:
            self.errors.append("Tool name must be at least 3 characters")

        if not self.matlab_name.strip():
            self.errors.append("Tool name cannot be empty")

        # Validate description (optional check)
        if not self.description.strip():
            self.errors.append("Description cannot be empty")

        return len(self.errors) == 0

    def should_create(self) -> bool:
        """Helper method to check if tool should be created"""
        return self.create_tool == "Y"

    def get_error_message(self) -> str:
        """Get formatted error message"""
        if not self.errors:
            return "No errors"
        return "\n".join(f"  • {error}" for error in self.errors)
```

### Step 3: Update user_input.py (1 minute)

**REPLACE your current `modules/user_input.py` with:**

```python
"""User input module - collects information from the user"""

from modules.models.tool_config import ToolConfig

def get_user_input() -> ToolConfig:
    """
    Collect user input and return a ToolConfig object

    Returns:
        ToolConfig object with user's input
    """
    print("\n=== MATLAB Tool Setup Wizard ===\n")

    # Collect input
    create_tool = input("Do you want to create a tool? (Y/N): ")
    matlab_name = input("What is the name of your tool?: ")
    description = input("Brief description (optional): ") or "A MATLAB tool"
    category = input("Category (optional, default 'general'): ") or "general"

    # Create and return ToolConfig object
    return ToolConfig(
        matlab_name=matlab_name,
        create_tool=create_tool,
        description=description,
        category=category
    )

def greet():
    """Greeting function"""
    print("Welcome to the MATLAB Tool Wizard!")
```

### Step 4: Update validator.py (1 minute)

**REPLACE your current `modules/validator.py` with:**

```python
"""Validation module - validates tool configuration"""

from modules.models.tool_config import ToolConfig

def validate_tool_config(config: ToolConfig) -> tuple[bool, str]:
    """
    Validate a ToolConfig object

    Args:
        config: ToolConfig object to validate

    Returns:
        (is_valid, message): Tuple of bool and error/success message
    """
    if config.validate():
        return True, "✓ Valid input - ready to proceed"
    else:
        error_msg = f"✗ Validation failed:\n{config.get_error_message()}"
        return False, error_msg

# Keep old function for backward compatibility (if needed)
def validate_input(create_tool: str, matlab_name: str) -> tuple[bool, str]:
    """
    DEPRECATED: Use validate_tool_config instead

    Legacy function for backward compatibility
    """
    if create_tool.upper() not in ["Y", "N"]:
        return False, "No Y/N"

    if not matlab_name.replace(" ", "").isalpha():
        return False, "only letters allowed"

    if not matlab_name.strip():
        return False, "empty string"

    return True, "Valid input"
```

### Step 5: Update template_engine.py (1 minute)

**REPLACE your current `modules/template_engine.py` with:**

```python
"""Template engine - processes templates with tool configuration"""

import os
from modules.models.tool_config import ToolConfig

def setup_template(config: ToolConfig) -> str:
    """
    Process template with ToolConfig data

    Args:
        config: ToolConfig object with tool information

    Returns:
        Processed template string or error message
    """
    if not config.should_create():
        return "❌ Tool creation cancelled by user"

    print(f"\n📝 Setting up template for: {config.matlab_name}")
    print(f"   Description: {config.description}")
    print(f"   Category: {config.category}\n")

    # Read template
    template_path = os.path.join('templates', 'readme.txt')
    try:
        with open(template_path, 'r') as file:
            template = file.read()
    except FileNotFoundError:
        return f"❌ Error: Template not found at {template_path}"

    # Replace placeholders
    completed_template = template.replace("MATLAB_NAME", config.matlab_name)
    completed_template = completed_template.replace("DESCRIPTION", config.description)
    completed_template = completed_template.replace("CATEGORY", config.category)
    completed_template = completed_template.replace("VERSION", config.version)

    return completed_template
```

### Step 6: Update modules/__init__.py (30 seconds)

**REPLACE your current `modules/__init__.py` with:**

```python
"""Module exports"""

from .user_input import greet, get_user_input
from .validator import validate_tool_config, validate_input  # Keep old for compatibility
from .template_engine import setup_template
from .models.tool_config import ToolConfig

# Make ToolConfig easily accessible
__all__ = ['greet', 'get_user_input', 'validate_tool_config', 'validate_input', 'setup_template', 'ToolConfig']
```

### Step 7: Update main.py (1 minute)

**REPLACE your current `main.py` with:**

```python
"""Main entry point for the setup wizard"""

import modules

def intro():
    """Welcome message"""
    print("\n" + "=" * 60)
    print("  MATLAB Tool Setup Wizard")
    print("=" * 60)
    print("\nThis wizard will help you create a new MATLAB tool.")

def main():
    """Main workflow"""
    intro()

    # Step 1: Get user input (returns ToolConfig object)
    tool_config = modules.get_user_input()

    # Step 2: Validate the configuration
    is_valid, message = modules.validate_tool_config(tool_config)
    print(f"\n{message}")

    if not is_valid:
        print("\n❌ Cannot proceed with invalid configuration")
        print("Please run the wizard again with correct inputs.\n")
        return

    # Step 3: Process template
    print("\n" + "-" * 60)
    print("Processing template...")
    print("-" * 60)

    created_template = modules.setup_template(tool_config)

    print("\n" + "=" * 60)
    print("GENERATED TEMPLATE:")
    print("=" * 60)
    print(created_template)
    print("=" * 60 + "\n")

if __name__ == "__main__":
    main()
```

### Step 8: Test your implementation (1 minute)

```bash
cd /home/user/setup_wizard_mvp
python main.py
```

**Expected output:**
```
============================================================
  MATLAB Tool Setup Wizard
============================================================

This wizard will help you create a new MATLAB tool.

=== MATLAB Tool Setup Wizard ===

Do you want to create a tool? (Y/N): Y
What is the name of your tool?: TestTool
Brief description (optional): My test tool
Category (optional, default 'general'): analysis

✓ Valid input - ready to proceed

------------------------------------------------------------
Processing template...
------------------------------------------------------------

📝 Setting up template for: TestTool
   Description: My test tool
   Category: analysis

============================================================
GENERATED TEMPLATE:
============================================================
# Project Title "TestTool"

readme for a matlab tool

# FKjff
============================================================
```

## What You've Gained

### Before (Multiple Variables):
```python
create_tool, matlab_name = get_user_input()
validate_input(create_tool, matlab_name)
setup_template(matlab_name, valid_input)
```

### After (Data Class):
```python
tool_config = get_user_input()
validate_tool_config(tool_config)
setup_template(tool_config)
```

**Benefits:**
1. ✅ **Cleaner code** - Pass one object instead of many variables
2. ✅ **Autocomplete** - Your IDE knows all the fields
3. ✅ **Type safety** - Catch typos before running
4. ✅ **Easy to extend** - Add fields without changing function signatures
5. ✅ **Self-documenting** - The class definition shows all available fields

## Next Steps

### Add More Fields (Example)

Want to add an "author" field? Just update `tool_config.py`:

```python
@dataclass
class ToolConfig:
    matlab_name: str
    create_tool: str
    author: str = "Unknown"  # <-- Just add this!
    # ... rest of fields
```

Then in `user_input.py`:
```python
author = input("Author name (optional): ") or "Unknown"

return ToolConfig(
    matlab_name=matlab_name,
    create_tool=create_tool,
    author=author  # <-- Use it!
)
```

**That's it!** No need to change validator.py or template_engine.py - they still just accept `ToolConfig`.

### Create Tests (Optional)

```python
# test_tool_config.py
from modules.models.tool_config import ToolConfig

def test_valid_config():
    tool = ToolConfig(
        matlab_name="TestTool",
        create_tool="Y",
        description="Test"
    )
    assert tool.validate() == True

def test_invalid_name():
    tool = ToolConfig(
        matlab_name="123Bad",
        create_tool="Y"
    )
    assert tool.validate() == False
    assert len(tool.errors) > 0
```

## Summary

Data classes are **containers for related data** that make your code:
- **Cleaner** - Less boilerplate
- **Safer** - Type hints catch errors
- **Easier** - Autocomplete works
- **Scalable** - Add fields without breaking things

You've now upgraded from passing around loose variables to using a proper data model - this is a key step toward professional Python code!
