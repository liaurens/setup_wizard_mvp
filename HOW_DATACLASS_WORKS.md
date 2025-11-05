# How Data Classes Work in Your Wizard

## Quick Answer to Your Questions

### Q1: Does the data class collect user data?
**No.** The data class is just a **container**. Think of it like an empty form.
- `user_input.py` collects the data (asks questions)
- Then creates a `ToolConfig` object to store it

### Q2: Should validation be in the data class or validator module?
**Both!** You have two options:
- **Option A**: Put validation logic IN the data class (recommended for simple validation)
- **Option B**: Keep it in validator.py (better for complex business rules)
- **Best Practice**: Simple checks in data class, complex logic in validator

### Q3: Can template_engine use the data class?
**Yes!** That's the whole point. The template engine receives a ToolConfig object and accesses its fields directly.

---

## How It All Works Together

### The Data Class is Just a Smart Container

```python
# modules/models/tool_config.py
@dataclass
class ToolConfig:
    """This is just a container - like a form with labeled boxes"""
    matlab_name: str
    create_tool: str
    description: str = ""

    def validate(self) -> bool:
        """Built-in validation method"""
        return self.matlab_name.isalpha()
```

Think of it like this:
```
ToolConfig = A Form Template
    ┌─────────────────────┐
    │ matlab_name: [ ]    │  <- Empty boxes
    │ create_tool: [ ]    │
    │ description: [ ]    │
    └─────────────────────┘
```

---

## Step-by-Step Data Flow

### Step 1: user_input.py COLLECTS data and CREATES the object

```python
# modules/user_input.py
from modules.models.tool_config import ToolConfig

def get_user_input() -> ToolConfig:
    """
    This function:
    1. Asks the user questions ✓
    2. Gets their answers ✓
    3. Creates a ToolConfig object with those answers ✓
    4. Returns the filled object ✓
    """

    # COLLECT data (ask questions)
    matlab_name = input("Tool name: ")
    create_tool = input("Create? (Y/N): ")
    description = input("Description: ")

    # CREATE the ToolConfig object with the collected data
    tool_config = ToolConfig(
        matlab_name=matlab_name,
        create_tool=create_tool,
        description=description
    )

    # RETURN the filled object
    return tool_config
```

**After this step:**
```
tool_config = ToolConfig object with data
    ┌─────────────────────────┐
    │ matlab_name: "MyTool"   │  <- Filled with user's answers
    │ create_tool: "Y"        │
    │ description: "Cool app" │
    └─────────────────────────┘
```

---

### Step 2: validator.py (or data class) VALIDATES the data

**Option A: Validation IN the data class**

```python
# modules/models/tool_config.py
@dataclass
class ToolConfig:
    matlab_name: str
    create_tool: str
    description: str = ""
    errors: List[str] = field(default_factory=list, init=False)

    def validate(self) -> bool:
        """Validation logic INSIDE the data class"""
        self.errors.clear()

        # Check matlab_name
        if not self.matlab_name.isalpha():
            self.errors.append("Name must be letters only")

        # Check create_tool
        if self.create_tool.upper() not in ["Y", "N"]:
            self.errors.append("Must be Y or N")

        return len(self.errors) == 0

# Usage in main.py:
tool_config = modules.get_user_input()
if tool_config.validate():  # Call validation method directly on object
    print("Valid!")
else:
    print("Errors:", tool_config.errors)
```

**Option B: Validation in validator.py module**

```python
# modules/validator.py
from modules.models.tool_config import ToolConfig

def validate_tool_config(config: ToolConfig) -> tuple[bool, str]:
    """Validation logic in separate module"""

    # Access the ToolConfig fields
    if not config.matlab_name.isalpha():
        return False, "Name must be letters only"

    if config.create_tool.upper() not in ["Y", "N"]:
        return False, "Must be Y or N"

    return True, "Valid!"

# Usage in main.py:
tool_config = modules.get_user_input()
is_valid, message = modules.validate_tool_config(tool_config)
if is_valid:
    print("Valid!")
```

**Option C: BOTH (Best Practice)**

```python
# Simple validation IN the data class
@dataclass
class ToolConfig:
    matlab_name: str
    create_tool: str

    def is_valid_format(self) -> bool:
        """Simple format checks"""
        return (self.matlab_name.isalpha() and
                self.create_tool.upper() in ["Y", "N"])

# Complex validation in validator.py
def validate_tool_config(config: ToolConfig) -> tuple[bool, str]:
    """Complex business rules"""

    # First check basic format
    if not config.is_valid_format():
        return False, "Invalid format"

    # Then check complex rules
    if config.matlab_name in RESERVED_MATLAB_WORDS:
        return False, "Name conflicts with MATLAB keyword"

    if config.create_tool == "Y" and not config.description:
        return False, "Description required when creating tool"

    return True, "Valid!"
```

---

### Step 3: template_engine.py USES the data class

```python
# modules/template_engine.py
from modules.models.tool_config import ToolConfig

def setup_template(config: ToolConfig) -> str:
    """
    This function:
    1. Receives the ToolConfig object ✓
    2. Accesses its fields directly ✓
    3. Uses them to fill the template ✓
    """

    # ACCESS the data from the ToolConfig object
    tool_name = config.matlab_name
    description = config.description
    category = config.category

    # Or access directly in the template
    template_content = f"""
    # Project: {config.matlab_name}

    Description: {config.description}
    Category: {config.category}
    Input Type: {config.input_type}
    Output Type: {config.output_type}
    """

    # Read template file
    with open('templates/readme.txt', 'r') as f:
        template = f.read()

    # Replace placeholders with ToolConfig data
    template = template.replace("MATLAB_NAME", config.matlab_name)
    template = template.replace("DESCRIPTION", config.description)
    template = template.replace("CATEGORY", config.category)

    return template
```

---

## Complete Example: All Three Working Together

```python
# ============================================
# modules/models/tool_config.py
# ============================================
from dataclasses import dataclass, field
from typing import List

@dataclass
class ToolConfig:
    """The container for tool data"""

    matlab_name: str
    create_tool: str
    description: str = ""
    input_type: str = "file_path"
    output_type: str = "data_structure"
    category: str = "general"

    errors: List[str] = field(default_factory=list, init=False)

    def validate(self) -> bool:
        """Simple validation - checks basic format"""
        self.errors.clear()

        if not self.matlab_name.replace(" ", "").isalpha():
            self.errors.append("Name must contain only letters")

        if self.create_tool.upper() not in ["Y", "N"]:
            self.errors.append("create_tool must be Y or N")

        return len(self.errors) == 0

    def should_create(self) -> bool:
        """Helper method"""
        return self.create_tool.upper() == "Y"


# ============================================
# modules/user_input.py
# ============================================
from modules.models.tool_config import ToolConfig

def get_user_input() -> ToolConfig:
    """COLLECTS data and CREATES ToolConfig object"""

    print("\n=== Tool Setup Wizard ===\n")

    # COLLECT the data
    matlab_name = input("Tool name: ")
    create_tool = input("Create tool? (Y/N): ")
    description = input("Description: ")
    category = input("Category (optional): ") or "general"

    # CREATE and RETURN the ToolConfig object
    return ToolConfig(
        matlab_name=matlab_name,
        create_tool=create_tool,
        description=description,
        category=category
    )


# ============================================
# modules/validator.py
# ============================================
from modules.models.tool_config import ToolConfig

# List of reserved MATLAB words
RESERVED_WORDS = ['function', 'end', 'if', 'else', 'for', 'while']

def validate_tool_config(config: ToolConfig) -> tuple[bool, str]:
    """
    VALIDATES ToolConfig object
    Uses both the object's built-in validation AND custom business rules
    """

    # First: Use the built-in validation from ToolConfig
    if not config.validate():
        errors = "\n".join(config.errors)
        return False, f"Validation failed:\n{errors}"

    # Second: Apply complex business rules
    if config.matlab_name.lower() in RESERVED_WORDS:
        return False, f"'{config.matlab_name}' is a reserved MATLAB word"

    if len(config.matlab_name) < 3:
        return False, "Tool name must be at least 3 characters"

    if config.should_create() and not config.description.strip():
        return False, "Description required when creating a tool"

    # All checks passed
    return True, "✓ Valid configuration"


# ============================================
# modules/template_engine.py
# ============================================
import os
from modules.models.tool_config import ToolConfig

def setup_template(config: ToolConfig) -> str:
    """USES ToolConfig object to fill template"""

    if not config.should_create():
        return "Tool creation cancelled by user"

    print(f"\n📝 Creating template for: {config.matlab_name}")

    # Read the template
    template_path = os.path.join('templates', 'readme.txt')
    with open(template_path, 'r') as f:
        template = f.read()

    # REPLACE placeholders with data from ToolConfig
    template = template.replace("MATLAB_NAME", config.matlab_name)
    template = template.replace("DESCRIPTION", config.description)
    template = template.replace("CATEGORY", config.category)
    template = template.replace("INPUT_TYPE", config.input_type)
    template = template.replace("OUTPUT_TYPE", config.output_type)

    return template


# ============================================
# main.py
# ============================================
import modules

def main():
    print("Welcome to the MATLAB Tool Wizard!\n")

    # Step 1: COLLECT data (returns ToolConfig object)
    tool_config = modules.get_user_input()

    print(f"\nReceived configuration:")
    print(f"  Name: {tool_config.matlab_name}")
    print(f"  Create: {tool_config.create_tool}")
    print(f"  Description: {tool_config.description}")

    # Step 2: VALIDATE data (using ToolConfig object)
    is_valid, message = modules.validate_tool_config(tool_config)
    print(f"\nValidation: {message}")

    if not is_valid:
        print("❌ Cannot proceed - please fix errors")
        return

    # Step 3: PROCESS template (using ToolConfig object)
    result = modules.setup_template(tool_config)

    print("\n" + "="*60)
    print("GENERATED TEMPLATE:")
    print("="*60)
    print(result)

if __name__ == "__main__":
    main()
```

---

## Visual Summary

```
┌─────────────────────┐
│  user_input.py      │
│                     │
│  1. Asks questions  │
│  2. Collects data   │
│  3. Creates         │
│     ToolConfig      │
└──────────┬──────────┘
           │
           ▼
    ┌──────────────┐
    │  ToolConfig  │  <- THE OBJECT (contains all data)
    │  Object      │
    └──┬───────┬───┘
       │       │
       │       └──────────────┐
       │                      │
       ▼                      ▼
┌──────────────┐      ┌──────────────────┐
│ validator.py │      │ template_engine  │
│              │      │                  │
│ Uses object  │      │ Uses object      │
│ to validate  │      │ to fill template │
└──────────────┘      └──────────────────┘
```

---

## Recommendations

### For Simple Projects (Like Yours Now):
✅ **Put validation IN the data class**
- Easier to maintain
- Everything in one place
- Less files to manage

```python
@dataclass
class ToolConfig:
    # ... fields ...

    def validate(self) -> bool:
        # All validation here
        pass

# Usage
tool_config = get_user_input()
if tool_config.validate():  # Direct call
    process(tool_config)
```

### For Larger Projects:
✅ **Use BOTH**
- Simple format checks in data class
- Complex business rules in validator.py

```python
# In data class
def is_valid_format(self) -> bool:
    return self.name.isalpha()

# In validator.py
def validate_tool_config(config):
    if not config.is_valid_format():
        return False
    # Complex checks here...
```

---

## Key Takeaways

1. **Data class = Container** (stores data)
2. **user_input.py = Collector** (fills the container)
3. **Validator = Checker** (checks the container contents)
4. **template_engine = User** (uses the container data)

**The beauty:** One object passes through all modules instead of multiple loose variables!
