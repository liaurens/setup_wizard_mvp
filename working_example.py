"""
WORKING EXAMPLE: How Data Class Works With All Modules

Run this file to see how data flows through your wizard!
"""

from dataclasses import dataclass, field
from typing import List

# ============================================================================
# 1. THE DATA CLASS (Container)
# ============================================================================

@dataclass
class ToolConfig:
    """
    This is just a CONTAINER - like a form with labeled boxes
    It STORES data, it doesn't COLLECT data
    """

    # Required fields
    matlab_name: str
    create_tool: str

    # Optional fields with defaults
    description: str = ""
    input_type: str = "file_path"
    output_type: str = "data_structure"
    category: str = "general"

    # Validation errors (internal)
    errors: List[str] = field(default_factory=list, init=False)

    def validate(self) -> bool:
        """
        VALIDATION can be in the data class
        This is convenient for simple checks
        """
        self.errors.clear()

        if not self.matlab_name.replace(" ", "").isalpha():
            self.errors.append("Name must contain only letters")

        if self.create_tool.upper() not in ["Y", "N"]:
            self.errors.append("create_tool must be Y or N")

        if len(self.matlab_name) < 3:
            self.errors.append("Name must be at least 3 characters")

        return len(self.errors) == 0

    def should_create(self) -> bool:
        """Helper method"""
        return self.create_tool.upper() == "Y"

    def get_summary(self) -> str:
        """Display a summary of the config"""
        return f"""
    Tool Name: {self.matlab_name}
    Create: {self.create_tool}
    Description: {self.description}
    Category: {self.category}
    Input: {self.input_type}
    Output: {self.output_type}
        """


# ============================================================================
# 2. USER INPUT MODULE (Collector)
# ============================================================================

def get_user_input_interactive() -> ToolConfig:
    """
    COLLECTS data from user and CREATES a ToolConfig object
    The data class does NOT collect - this function does!
    """
    print("\n" + "="*60)
    print("  MATLAB TOOL WIZARD")
    print("="*60)

    # COLLECT data by asking questions
    matlab_name = input("\n1. Tool name: ")
    create_tool = input("2. Create tool? (Y/N): ")
    description = input("3. Description: ")
    category = input("4. Category (optional, press Enter for 'general'): ") or "general"

    # CREATE the ToolConfig object with collected data
    tool_config = ToolConfig(
        matlab_name=matlab_name,
        create_tool=create_tool,
        description=description,
        category=category
    )

    # RETURN the filled object
    return tool_config


def get_user_input_simulated() -> ToolConfig:
    """
    Same as above, but with simulated input for demo purposes
    """
    print("\n" + "="*60)
    print("  SIMULATED USER INPUT")
    print("="*60)

    # Simulate user input
    matlab_name = "DataProcessor"
    create_tool = "Y"
    description = "Processes sensor data"
    category = "analysis"

    print(f"\n1. Tool name: {matlab_name}")
    print(f"2. Create tool? (Y/N): {create_tool}")
    print(f"3. Description: {description}")
    print(f"4. Category: {category}")

    # CREATE ToolConfig object
    return ToolConfig(
        matlab_name=matlab_name,
        create_tool=create_tool,
        description=description,
        category=category
    )


# ============================================================================
# 3. VALIDATOR MODULE (Checker)
# ============================================================================

# Reserved MATLAB keywords
RESERVED_MATLAB_WORDS = ['function', 'end', 'if', 'else', 'for', 'while', 'return']

def validate_tool_config(config: ToolConfig) -> tuple[bool, str]:
    """
    VALIDATES a ToolConfig object
    Can use BOTH the object's validation AND add custom business rules
    """

    print("\n" + "-"*60)
    print("  VALIDATION")
    print("-"*60)

    # First: Use the data class's built-in validation
    if not config.validate():
        errors = "\n  ".join(config.errors)
        return False, f"❌ Format errors:\n  {errors}"

    # Second: Add complex business rules here
    if config.matlab_name.lower() in RESERVED_MATLAB_WORDS:
        return False, f"❌ '{config.matlab_name}' is a reserved MATLAB keyword"

    if config.should_create() and not config.description.strip():
        return False, "❌ Description required when creating a tool"

    # All checks passed
    return True, "✅ Configuration is valid!"


# ============================================================================
# 4. TEMPLATE ENGINE MODULE (User of data)
# ============================================================================

def setup_template(config: ToolConfig) -> str:
    """
    USES the ToolConfig object to fill in a template
    Accesses the object's fields directly
    """

    print("\n" + "-"*60)
    print("  TEMPLATE PROCESSING")
    print("-"*60)

    if not config.should_create():
        return "❌ Tool creation cancelled by user"

    print(f"Creating template for: {config.matlab_name}")

    # Simulate reading a template file
    template = """
# MATLAB Tool: {{TOOL_NAME}}

## Description
{{DESCRIPTION}}

## Details
- **Category**: {{CATEGORY}}
- **Input Type**: {{INPUT_TYPE}}
- **Output Type**: {{OUTPUT_TYPE}}

## Usage
```matlab
result = {{TOOL_NAME}}(input_data);
```

## Author
Generated by MATLAB Tool Wizard
"""

    # REPLACE placeholders with data from ToolConfig object
    filled_template = template.replace("{{TOOL_NAME}}", config.matlab_name)
    filled_template = filled_template.replace("{{DESCRIPTION}}", config.description)
    filled_template = filled_template.replace("{{CATEGORY}}", config.category)
    filled_template = filled_template.replace("{{INPUT_TYPE}}", config.input_type)
    filled_template = filled_template.replace("{{OUTPUT_TYPE}}", config.output_type)

    return filled_template


# ============================================================================
# 5. MAIN WORKFLOW
# ============================================================================

def demo_valid_flow():
    """Demo with VALID input"""
    print("\n" + "="*70)
    print("  DEMO 1: VALID INPUT FLOW")
    print("="*70)

    # Step 1: COLLECT data (returns ToolConfig object)
    tool_config = get_user_input_simulated()

    # Show what we collected
    print("\n📦 Created ToolConfig object:")
    print(tool_config.get_summary())

    # Step 2: VALIDATE data (using ToolConfig object)
    is_valid, message = validate_tool_config(tool_config)
    print(f"\n{message}")

    if not is_valid:
        print("\n❌ Cannot proceed - fix errors first")
        return

    # Step 3: PROCESS template (using ToolConfig object)
    result = setup_template(tool_config)

    print("\n" + "="*70)
    print("  GENERATED TEMPLATE")
    print("="*70)
    print(result)


def demo_invalid_flow():
    """Demo with INVALID input"""
    print("\n\n" + "="*70)
    print("  DEMO 2: INVALID INPUT FLOW")
    print("="*70)

    # Create ToolConfig with INVALID data
    print("\nCreating ToolConfig with invalid data...")
    tool_config = ToolConfig(
        matlab_name="123Bad",  # Invalid: starts with number
        create_tool="MAYBE",    # Invalid: not Y or N
        description=""
    )

    print(f"\n1. Tool name: {tool_config.matlab_name}")
    print(f"2. Create tool? (Y/N): {tool_config.create_tool}")
    print(f"3. Description: {tool_config.description}")

    # Step 2: VALIDATE (will fail)
    is_valid, message = validate_tool_config(tool_config)
    print(f"\n{message}")

    if not is_valid:
        print("\n❌ Validation failed - cannot proceed")
        print("\nThis shows how the data class catches errors!")


def demo_validation_in_dataclass():
    """Demo showing validation inside the data class"""
    print("\n\n" + "="*70)
    print("  DEMO 3: DATA CLASS VALIDATION METHODS")
    print("="*70)

    tool_config = ToolConfig(
        matlab_name="GoodTool",
        create_tool="Y",
        description="A good tool"
    )

    print("\nDemonstrating data class methods:")
    print(f"\n1. tool_config.validate() = {tool_config.validate()}")
    print(f"2. tool_config.should_create() = {tool_config.should_create()}")
    print(f"3. tool_config.matlab_name = '{tool_config.matlab_name}'")
    print(f"4. tool_config.category = '{tool_config.category}' (default value)")

    print("\n✨ The data class provides convenient methods!")
    print("   You can call validation directly on the object!")


def demo_data_access():
    """Demo showing how easy it is to access data"""
    print("\n\n" + "="*70)
    print("  DEMO 4: ACCESSING DATA FROM THE OBJECT")
    print("="*70)

    tool_config = ToolConfig(
        matlab_name="MyTool",
        create_tool="Y",
        description="Cool tool"
    )

    print("\nAccessing data with dot notation:")
    print(f"  tool_config.matlab_name = '{tool_config.matlab_name}'")
    print(f"  tool_config.description = '{tool_config.description}'")
    print(f"  tool_config.input_type = '{tool_config.input_type}' (default)")

    print("\nCompare to dictionary:")
    tool_dict = {
        "matlab_name": "MyTool",
        "create_tool": "Y",
        "description": "Cool tool"
    }
    print(f"  tool_dict['matlab_name'] = '{tool_dict['matlab_name']}'")
    print(f"  tool_dict.get('matlab_name') = '{tool_dict.get('matlab_name')}'")

    print("\n✨ Data class syntax is cleaner and has autocomplete!")


# ============================================================================
# RUN ALL DEMOS
# ============================================================================

if __name__ == "__main__":
    print("\n" + "█"*70)
    print("█  DATA CLASS WORKING EXAMPLE")
    print("█  See how data flows through all modules!")
    print("█"*70)

    # Run demonstrations
    demo_valid_flow()
    demo_invalid_flow()
    demo_validation_in_dataclass()
    demo_data_access()

    print("\n\n" + "="*70)
    print("  SUMMARY")
    print("="*70)
    print("""
1. ToolConfig = CONTAINER (holds data)
   - Created by: user_input.py
   - Used by: validator, template_engine

2. get_user_input() = COLLECTOR (fills the container)
   - Asks questions
   - Creates ToolConfig object
   - Returns filled object

3. validate_tool_config() = CHECKER (validates the container)
   - Receives ToolConfig object
   - Can use object's validate() method
   - Can add extra business rules
   - Returns (is_valid, message)

4. setup_template() = USER (uses the container)
   - Receives ToolConfig object
   - Accesses fields: config.matlab_name, config.description, etc.
   - Fills template with data
   - Returns result

KEY INSIGHT: One object passes through ALL modules!
    """)

    print("\n" + "█"*70)
    print("█  Want to try with real input?")
    print("█  Uncomment the line below and run again!")
    print("█"*70)

    # Uncomment to try with real user input:
    # tool_config = get_user_input_interactive()
    # is_valid, msg = validate_tool_config(tool_config)
    # print(msg)
    # if is_valid:
    #     print(setup_template(tool_config))
