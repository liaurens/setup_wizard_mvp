"""
DATA CLASSES TUTORIAL
=====================
Complete examples showing different approaches to data management
"""

# ============================================================================
# APPROACH 1: Multiple Variables (What you have now)
# ============================================================================

def approach_1_multiple_variables():
    """Passing individual variables - gets messy quickly"""

    print("\n=== APPROACH 1: Multiple Variables ===")

    # Collecting data
    matlab_name = "DataProcessor"
    create_tool = "Y"
    input_type = "file_path"
    output_type = "data_structure"
    description = "Processes sensor data"

    # Passing to functions
    process_tool(matlab_name, create_tool, input_type, output_type, description)

    # Problem: Function signature gets huge!
    # If you add more fields, you need to update EVERY function

def process_tool(name, create, input_t, output_t, desc):
    """Notice: 5 parameters already! This grows fast."""
    print(f"Processing: {name}")
    print(f"Create: {create}, Input: {input_t}, Output: {output_t}")


# ============================================================================
# APPROACH 2: Dictionary (Simple but limited)
# ============================================================================

def approach_2_dictionary():
    """Using a dictionary - better, but still has issues"""

    print("\n=== APPROACH 2: Dictionary ===")

    # Store everything in a dict
    tool_info = {
        "matlab_name": "DataProcessor",
        "create_tool": "Y",
        "input_type": "file_path",
        "output_type": "data_structure",
        "description": "Processes sensor data"
    }

    # Easier to pass around
    process_tool_dict(tool_info)

    # But... problems:
    print("\nProblems with dictionaries:")
    # 1. Typos are not caught
    print(f"Name: {tool_info.get('matlab_nmae', 'TYPO NOT FOUND!')}")  # Silent failure!

    # 2. No autocomplete in your IDE
    # 3. No type hints
    # 4. Can't tell what keys are required

def process_tool_dict(tool_info):
    """Better: Only one parameter!"""
    print(f"Processing: {tool_info['matlab_name']}")
    print(f"Description: {tool_info['description']}")


# ============================================================================
# APPROACH 3: Traditional Class (Object-Oriented)
# ============================================================================

class ToolConfigTraditional:
    """Traditional Python class for storing tool configuration"""

    def __init__(self, matlab_name, create_tool, input_type="file_path",
                 output_type="data_structure", description=""):
        """
        Initialize tool configuration

        Args:
            matlab_name: Name of the MATLAB tool
            create_tool: Whether to create the tool (Y/N)
            input_type: Type of input (default: "file_path")
            output_type: Type of output (default: "data_structure")
            description: Tool description (default: "")
        """
        self.matlab_name = matlab_name
        self.create_tool = create_tool
        self.input_type = input_type
        self.output_type = output_type
        self.description = description

    def __repr__(self):
        """String representation for debugging"""
        return (f"ToolConfigTraditional(matlab_name={self.matlab_name}, "
                f"create_tool={self.create_tool})")

    def __eq__(self, other):
        """Check if two configs are equal"""
        if not isinstance(other, ToolConfigTraditional):
            return False
        return (self.matlab_name == other.matlab_name and
                self.create_tool == other.create_tool)

    def is_valid_name(self):
        """Custom validation method"""
        return self.matlab_name.replace(" ", "").isalpha()

def approach_3_traditional_class():
    """Using a traditional class"""

    print("\n=== APPROACH 3: Traditional Class ===")

    # Create an instance
    tool = ToolConfigTraditional(
        matlab_name="DataProcessor",
        create_tool="Y",
        description="Processes sensor data"
    )

    # Access with dot notation (autocomplete works!)
    print(f"Tool name: {tool.matlab_name}")
    print(f"Input type: {tool.input_type}")  # Uses default value
    print(f"Is valid: {tool.is_valid_name()}")

    # Better, but requires lots of boilerplate code
    # Notice all the __init__, __repr__, __eq__ methods we had to write


# ============================================================================
# APPROACH 4: Data Class (Modern Python 3.7+)
# ============================================================================

from dataclasses import dataclass, field
from typing import Optional

@dataclass
class ToolConfig:
    """
    Modern data class for tool configuration

    Automatically generates:
    - __init__ method
    - __repr__ method
    - __eq__ method
    - And more!
    """

    # Required fields (no default)
    matlab_name: str
    create_tool: str

    # Optional fields with defaults
    input_type: str = "file_path"
    output_type: str = "data_structure"
    description: str = ""
    category: str = "general"
    verbose: bool = False

    # Computed field (not included in __init__)
    errors: list = field(default_factory=list, init=False)

    def is_valid_name(self) -> bool:
        """Custom validation method"""
        return self.matlab_name.replace(" ", "").isalpha()

    def add_error(self, error: str):
        """Add validation error"""
        self.errors.append(error)

    def validate(self) -> bool:
        """Complete validation"""
        self.errors.clear()

        if not self.is_valid_name():
            self.add_error("Name must contain only letters")

        if self.create_tool.upper() not in ["Y", "N"]:
            self.add_error("create_tool must be Y or N")

        if not self.description.strip():
            self.add_error("Description cannot be empty")

        return len(self.errors) == 0

def approach_4_dataclass():
    """Using modern data classes - The best approach!"""

    print("\n=== APPROACH 4: Data Class (RECOMMENDED) ===")

    # Create an instance - clean and simple
    tool = ToolConfig(
        matlab_name="DataProcessor",
        create_tool="Y",
        description="Processes sensor data"
    )

    # Autocomplete works perfectly
    print(f"Tool name: {tool.matlab_name}")
    print(f"Input type: {tool.input_type}")  # Default value
    print(f"Category: {tool.category}")  # Default value

    # Validation is built into the class
    if tool.validate():
        print("✓ Tool configuration is valid")
    else:
        print("✗ Errors:", tool.errors)

    # Beautiful string representation (automatically generated)
    print(f"\nObject representation:\n{tool}")

    # Equality comparison works automatically
    tool2 = ToolConfig(matlab_name="DataProcessor", create_tool="Y")
    print(f"\ntools are equal: {tool == tool2}")


# ============================================================================
# APPROACH 5: Data Class with Validation (Advanced)
# ============================================================================

from dataclasses import dataclass
from typing import List, Optional

@dataclass
class AdvancedToolConfig:
    """Data class with built-in validation using __post_init__"""

    matlab_name: str
    create_tool: str
    input_type: str = "file_path"
    output_type: str = "data_structure"
    description: str = ""

    def __post_init__(self):
        """Called automatically after __init__ - perfect for validation!"""

        # Auto-clean the name
        self.matlab_name = self.matlab_name.strip()

        # Auto-uppercase the create_tool
        self.create_tool = self.create_tool.upper()

        # Validate immediately
        if not self.matlab_name.replace(" ", "").isalpha():
            raise ValueError(f"Invalid tool name: {self.matlab_name}")

        if self.create_tool not in ["Y", "N"]:
            raise ValueError(f"create_tool must be Y or N, got: {self.create_tool}")

def approach_5_dataclass_validation():
    """Data class with automatic validation"""

    print("\n=== APPROACH 5: Data Class with Auto-Validation ===")

    # Valid creation
    try:
        tool = AdvancedToolConfig(
            matlab_name="DataProcessor",
            create_tool="y",  # Will be auto-converted to "Y"
            description="Processes data"
        )
        print(f"✓ Created tool: {tool.matlab_name}")
        print(f"✓ Create tool (auto-uppercased): {tool.create_tool}")
    except ValueError as e:
        print(f"✗ Error: {e}")

    # Invalid creation - will raise error immediately
    print("\nTrying to create invalid tool:")
    try:
        bad_tool = AdvancedToolConfig(
            matlab_name="123Invalid",  # Starts with number
            create_tool="Y"
        )
    except ValueError as e:
        print(f"✓ Caught error: {e}")


# ============================================================================
# MAIN DEMONSTRATION
# ============================================================================

def main():
    """Run all examples"""

    print("=" * 70)
    print("DATA CLASSES TUTORIAL")
    print("=" * 70)

    approach_1_multiple_variables()
    approach_2_dictionary()
    approach_3_traditional_class()
    approach_4_dataclass()
    approach_5_dataclass_validation()

    print("\n" + "=" * 70)
    print("SUMMARY:")
    print("=" * 70)
    print("1. Multiple Variables: Simple but doesn't scale")
    print("2. Dictionary: Better but no type safety")
    print("3. Traditional Class: Good but lots of boilerplate")
    print("4. Data Class: ⭐ BEST - Clean, type-safe, less code")
    print("5. Data Class + Validation: ⭐⭐ BEST - Everything above + auto-validation")
    print("=" * 70)

if __name__ == "__main__":
    main()
