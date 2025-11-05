# How to Integrate Data Classes into Your Setup Wizard

## Step-by-Step Integration Guide

### Step 1: Create a Models Module

Create a new directory for your data models:
```bash
mkdir modules/models
touch modules/models/__init__.py
```

### Step 2: Define Your ToolConfig Data Class

Create `modules/models/tool_config.py`:
```python
from dataclasses import dataclass, field
from typing import List

@dataclass
class ToolConfig:
    """Configuration for a MATLAB tool to be generated"""

    # Required fields
    matlab_name: str
    create_tool: str

    # Optional fields with defaults
    input_type: str = "file_path"
    output_type: str = "data_structure"
    description: str = ""
    category: str = "general"
    author: str = ""
    version: str = "1.0.0"

    # Validation errors (not set in __init__)
    errors: List[str] = field(default_factory=list, init=False)

    def __post_init__(self):
        """Clean and normalize data after initialization"""
        self.matlab_name = self.matlab_name.strip()
        self.create_tool = self.create_tool.upper()
        self.category = self.category.lower()

    def validate(self) -> bool:
        """Validate all fields"""
        self.errors.clear()

        # Validate matlab_name
        if not self.matlab_name.replace(" ", "").isalpha():
            self.errors.append("Tool name must contain only letters")

        if len(self.matlab_name) < 3:
            self.errors.append("Tool name must be at least 3 characters")

        # Validate create_tool
        if self.create_tool not in ["Y", "N"]:
            self.errors.append("create_tool must be Y or N")

        # Validate description
        if not self.description.strip():
            self.errors.append("Description cannot be empty")

        return len(self.errors) == 0

    def should_create(self) -> bool:
        """Helper method to check if tool should be created"""
        return self.create_tool == "Y"
```

### Step 3: Update Your Modules

**BEFORE (current approach):**

**user_input.py:**
```python
def get_user_input():
    create_tool = input("Do you want to create a tool? (Y/N): ")
    matlab_name = input("What is the name of your tool?: ")
    return create_tool, matlab_name
```

**validator.py:**
```python
def validate_input(create_tool, matlab_name):
    if create_tool.upper() not in ["Y", "N"]:
        return False, "No Y/N"
    if not matlab_name.replace(" ", "").isalpha():
        return False, "only letters allowed"
    return True, "Valid input"
```

**AFTER (with data classes):**

**user_input.py:**
```python
from modules.models.tool_config import ToolConfig

def get_user_input() -> ToolConfig:
    """Collect user input and return a ToolConfig object"""

    print("\n=== MATLAB Tool Wizard ===\n")

    # Collect basic info
    create_tool = input("Do you want to create a tool? (Y/N): ")
    matlab_name = input("What is the name of your tool?: ")

    # Collect additional info
    description = input("Brief description of your tool: ")
    category = input("Category (optional, press Enter for 'general'): ") or "general"

    # Create and return ToolConfig object
    return ToolConfig(
        matlab_name=matlab_name,
        create_tool=create_tool,
        description=description,
        category=category
    )
```

**validator.py:**
```python
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
        return True, "✓ Valid input"
    else:
        error_message = "\n".join(f"  • {error}" for error in config.errors)
        return False, f"✗ Validation errors:\n{error_message}"
```

**template_engine.py:**
```python
import os
from modules.models.tool_config import ToolConfig

def setup_template(config: ToolConfig) -> str:
    """
    Process template with ToolConfig data

    Args:
        config: ToolConfig object with tool information

    Returns:
        Processed template string
    """

    if not config.should_create():
        return "Tool creation cancelled by user"

    print(f"Setting up {config.matlab_name}")

    template_path = os.path.join('templates', 'readme.txt')
    with open(template_path, 'r') as file:
        template = file.read()

    # Replace all placeholders
    completed_template = template.replace("MATLAB_NAME", config.matlab_name)
    completed_template = completed_template.replace("DESCRIPTION", config.description)
    completed_template = completed_template.replace("CATEGORY", config.category)

    return completed_template
```

### Step 4: Update main.py

**BEFORE:**
```python
def main():
    intro()
    create_tool, matlab_name = modules.get_user_input()
    valid_input, message = modules.validate_input(create_tool, matlab_name)
    print(message)
    created_template = modules.setup_template(matlab_name, valid_input)
    print(created_template)
```

**AFTER:**
```python
from modules.models.tool_config import ToolConfig

def main():
    intro()

    # Get user input as ToolConfig object
    tool_config = modules.get_user_input()

    # Validate the configuration
    is_valid, message = modules.validate_tool_config(tool_config)
    print(message)

    if not is_valid:
        print("\n❌ Cannot proceed with invalid configuration")
        return

    # Process template
    created_template = modules.setup_template(tool_config)
    print(created_template)
```

## Key Benefits You'll Get

### 1. **Type Safety**
```python
# Your IDE will autocomplete these fields:
tool_config.matlab_name  # ✓ Autocomplete works!
tool_config.matlab_nmae  # ✗ IDE will highlight this error

# Dictionary version - no autocomplete:
tool_info["matlab_name"]  # No autocomplete
tool_info["matlab_nmae"]  # Typo goes undetected until runtime
```

### 2. **Default Values**
```python
# No need to pass everything
tool = ToolConfig(
    matlab_name="MyTool",
    create_tool="Y"
    # category defaults to "general"
    # version defaults to "1.0.0"
)
```

### 3. **Built-in Validation**
```python
tool = ToolConfig(matlab_name="Test", create_tool="Y")

if tool.validate():
    print("Ready to proceed!")
else:
    print("Errors:", tool.errors)
```

### 4. **Single Source of Truth**
All tool configuration lives in ONE place - the ToolConfig class.
No more passing around multiple variables or dictionaries.

### 5. **Easy to Extend**
Need to add a new field? Just add it to the data class:
```python
@dataclass
class ToolConfig:
    # ... existing fields ...
    license: str = "MIT"  # New field - that's it!
```

## Testing Your Data Classes

Create `tests/test_tool_config.py`:
```python
from modules.models.tool_config import ToolConfig

def test_valid_config():
    """Test valid configuration"""
    tool = ToolConfig(
        matlab_name="TestTool",
        create_tool="Y",
        description="Test description"
    )

    assert tool.validate() == True
    assert tool.should_create() == True
    assert len(tool.errors) == 0

def test_invalid_name():
    """Test invalid tool name"""
    tool = ToolConfig(
        matlab_name="123Invalid",  # Starts with number
        create_tool="Y"
    )

    assert tool.validate() == False
    assert "only letters" in tool.errors[0].lower()

def test_auto_normalization():
    """Test __post_init__ normalization"""
    tool = ToolConfig(
        matlab_name="  TestTool  ",  # Extra spaces
        create_tool="y",  # Lowercase
        category="GENERAL"  # Uppercase
    )

    assert tool.matlab_name == "TestTool"  # Stripped
    assert tool.create_tool == "Y"  # Uppercased
    assert tool.category == "general"  # Lowercased

if __name__ == "__main__":
    test_valid_config()
    test_invalid_name()
    test_auto_normalization()
    print("✓ All tests passed!")
```

## File Structure After Integration

```
setup_wizard_mvp/
├── main.py
├── config.py
├── modules/
│   ├── __init__.py
│   ├── user_input.py       # Returns ToolConfig
│   ├── validator.py        # Validates ToolConfig
│   ├── template_engine.py  # Accepts ToolConfig
│   └── models/
│       ├── __init__.py
│       └── tool_config.py  # ⭐ Your data class
├── templates/
│   └── readme.txt
└── tests/
    └── test_tool_config.py
```

## Quick Reference: When to Use What

| Use Case | Best Choice |
|----------|-------------|
| 1-2 simple values | Individual variables |
| 3+ related values | Data class |
| Configuration objects | Data class |
| API responses | Data class |
| Database models | Data class |
| Passing data between modules | Data class |

## Summary

Data classes make your code:
- ✅ **Cleaner** - Less boilerplate
- ✅ **Safer** - Type hints and validation
- ✅ **Easier** - Autocomplete and better IDE support
- ✅ **More maintainable** - Single source of truth
- ✅ **More testable** - Easy to create test objects

Start with the `ToolConfig` data class and gradually migrate your code to use it!
