"""
SIDE-BY-SIDE COMPARISON: Current Approach vs Data Class Approach

Run this to see the practical difference!
"""

from dataclasses import dataclass, field
from typing import List

# ============================================================================
# CURRENT APPROACH (What you have now)
# ============================================================================

print("=" * 70)
print("CURRENT APPROACH - Multiple variables and tuples")
print("=" * 70)

def get_user_input_old():
    """Your current approach"""
    # Simulating user input
    create_tool = "Y"
    matlab_name = "DataProcessor"
    return create_tool, matlab_name

def validate_input_old(create_tool, matlab_name):
    """Your current validator"""
    if create_tool.upper() not in ["Y", "N"]:
        return False, "No Y/N"

    if not matlab_name.replace(" ", "").isalpha():
        return False, "only letters allowed"

    if not matlab_name.strip():
        return False, "empty string"

    return True, "Valid input"

def process_old():
    """Current workflow"""
    print("\n1. Getting user input...")
    create_tool, matlab_name = get_user_input_old()
    print(f"   Got: create_tool='{create_tool}', matlab_name='{matlab_name}'")

    print("\n2. Validating...")
    is_valid, message = validate_input_old(create_tool, matlab_name)
    print(f"   Result: {message}")

    print("\n3. Processing...")
    if is_valid:
        print(f"   Creating tool: {matlab_name}")
        # Passing individual variables around
        print(f"   Parameters being passed: create_tool, matlab_name")
    else:
        print(f"   Cannot proceed!")

    print("\n❌ Problem: What if we need to add more fields?")
    print("   - description, input_type, output_type, category, author, version...")
    print("   - Every function signature needs to change!")
    print("   - Passing 7+ variables around is messy!")

process_old()

# ============================================================================
# DATA CLASS APPROACH (Recommended)
# ============================================================================

print("\n" + "=" * 70)
print("DATA CLASS APPROACH - Clean and scalable")
print("=" * 70)

@dataclass
class ToolConfig:
    """All tool configuration in one clean object"""

    # Required fields
    matlab_name: str
    create_tool: str

    # Optional fields with defaults - easy to add more!
    description: str = ""
    input_type: str = "file_path"
    output_type: str = "data_structure"
    category: str = "general"
    author: str = ""
    version: str = "1.0.0"

    # Validation errors
    errors: List[str] = field(default_factory=list, init=False)

    def __post_init__(self):
        """Auto-clean data"""
        self.matlab_name = self.matlab_name.strip()
        self.create_tool = self.create_tool.upper()

    def validate(self) -> bool:
        """Validate all fields"""
        self.errors.clear()

        if self.create_tool not in ["Y", "N"]:
            self.errors.append("create_tool must be Y or N")

        if not self.matlab_name.replace(" ", "").isalpha():
            self.errors.append("matlab_name must contain only letters")

        if not self.matlab_name.strip():
            self.errors.append("matlab_name cannot be empty")

        return len(self.errors) == 0

    def should_create(self) -> bool:
        """Helper method"""
        return self.create_tool == "Y"


def get_user_input_new() -> ToolConfig:
    """New approach - returns a ToolConfig object"""
    # Simulating user input
    return ToolConfig(
        matlab_name="DataProcessor",
        create_tool="Y",
        description="Processes sensor data",
        category="analysis"
    )

def validate_input_new(config: ToolConfig) -> tuple[bool, str]:
    """New validator - takes ToolConfig object"""
    if config.validate():
        return True, "✓ Valid input"
    else:
        errors = "\n   ".join(config.errors)
        return False, f"✗ Errors:\n   {errors}"

def process_template_new(config: ToolConfig) -> str:
    """New processor - takes ToolConfig object"""
    if not config.should_create():
        return "User cancelled"

    # Look how clean this is - we have access to ALL fields!
    return f"""
    Tool: {config.matlab_name}
    Description: {config.description}
    Category: {config.category}
    Input: {config.input_type}
    Output: {config.output_type}
    Version: {config.version}
    """

def process_new():
    """New workflow"""
    print("\n1. Getting user input...")
    tool_config = get_user_input_new()
    print(f"   Got: {tool_config}")

    print("\n2. Validating...")
    is_valid, message = validate_input_new(tool_config)
    print(f"   {message}")

    print("\n3. Processing...")
    if is_valid:
        result = process_template_new(tool_config)
        print(f"   Template generated:{result}")
        print(f"   Parameters being passed: Just ONE ToolConfig object!")
    else:
        print("   Cannot proceed!")

    print("\n✅ Benefits:")
    print("   - Single object to pass around")
    print("   - Add new fields without changing function signatures")
    print("   - Autocomplete works (try: tool_config.)")
    print("   - Type hints help catch errors early")
    print("   - Clean, readable code")

process_new()

# ============================================================================
# PRACTICAL DEMONSTRATION
# ============================================================================

print("\n" + "=" * 70)
print("PRACTICAL DEMONSTRATION")
print("=" * 70)

print("\n📝 Example 1: Adding new fields")
print("-" * 50)

print("\nOLD WAY - Need to update every function:")
print("""
def get_input():
    return name, create, desc, input_type, output_type  # 5 values!

def validate(name, create, desc, input_type, output_type):  # 5 params!
    ...

def process(name, create, desc, input_type, output_type):  # 5 params!
    ...
""")

print("\nNEW WAY - Just add to data class:")
print("""
@dataclass
class ToolConfig:
    name: str
    create: str
    description: str = ""
    input_type: str = "file_path"
    output_type: str = "data_structure"
    # Add new field - DONE! No function changes needed.
    license: str = "MIT"  # <-- Just added this!

# All functions still work - they just pass ToolConfig!
""")

print("\n📝 Example 2: Type safety")
print("-" * 50)

config = ToolConfig(
    matlab_name="MyTool",
    create_tool="Y"
)

print(f"\nAccess with autocomplete:")
print(f"  config.matlab_name = '{config.matlab_name}'  ✓")
print(f"  config.description = '{config.description}'  ✓")
print(f"  config.version = '{config.version}'  ✓")

print(f"\nTry accessing wrong field:")
try:
    # This would fail immediately (if using type checker)
    print(f"  config.matlab_nmae = ???")  # Typo!
    print("  ^ Your IDE would highlight this typo before running!")
except AttributeError:
    print("  ✗ AttributeError - caught at runtime")

print("\n📝 Example 3: Validation")
print("-" * 50)

# Valid config
valid_tool = ToolConfig(
    matlab_name="GoodTool",
    create_tool="Y",
    description="A good tool"
)

print(f"\nValid tool: {valid_tool.matlab_name}")
print(f"Is valid? {valid_tool.validate()}")
print(f"Should create? {valid_tool.should_create()}")

# Invalid config
invalid_tool = ToolConfig(
    matlab_name="123Bad",  # Starts with number
    create_tool="MAYBE"     # Not Y or N
)

print(f"\nInvalid tool: {invalid_tool.matlab_name}")
print(f"Is valid? {invalid_tool.validate()}")
print(f"Errors:")
for error in invalid_tool.errors:
    print(f"  - {error}")

# ============================================================================
# CONCLUSION
# ============================================================================

print("\n" + "=" * 70)
print("CONCLUSION")
print("=" * 70)

print("""
Current Approach (Multiple Variables):
  ✓ Simple for 1-2 fields
  ✗ Doesn't scale to 5+ fields
  ✗ Error-prone (typos, wrong order)
  ✗ Hard to maintain

Data Class Approach:
  ✓ Scales to any number of fields
  ✓ Type-safe (IDE catches errors)
  ✓ Easy to maintain and extend
  ✓ Self-documenting code
  ✓ Less code overall

Recommendation: Switch to data classes! Your future self will thank you.
""")

print("=" * 70)
