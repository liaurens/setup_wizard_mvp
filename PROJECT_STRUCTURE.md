# Project Structure with Data Classes

## Current Structure (Before)
```
setup_wizard_mvp/
├── .git/
├── .idea/
├── main.py
├── config.py
├── modules/
│   ├── __init__.py
│   ├── user_input.py
│   ├── validator.py
│   └── template_engine.py
└── templates/
    └── readme.txt
```

## New Structure (After Adding Data Classes)
```
setup_wizard_mvp/
├── .git/
├── .idea/
├── main.py                          # Orchestrator
├── config.py                        # Configuration constants
│
├── modules/                         # Main modules
│   ├── __init__.py                 # Exports: get_user_input, validate_tool_config, setup_template, ToolConfig
│   ├── user_input.py               # Returns ToolConfig object
│   ├── validator.py                # Validates ToolConfig object
│   ├── template_engine.py          # Accepts ToolConfig object
│   │
│   └── models/                     # ⭐ NEW: Data models directory
│       ├── __init__.py             # Exports: ToolConfig
│       └── tool_config.py          # ⭐ NEW: ToolConfig data class
│
├── templates/                       # Template files
│   └── readme.txt
│
├── tests/                          # (Optional) Test directory
│   ├── __init__.py
│   └── test_tool_config.py         # Tests for ToolConfig
│
└── docs/                           # (Optional) Documentation
    ├── DATA_CLASSES_EXPLAINED.md
    ├── IMPLEMENTATION_STEPS.md
    └── INTEGRATION_GUIDE.md
```

## Key Files Explained

### modules/models/tool_config.py (THE DATA CLASS)
```python
from dataclasses import dataclass, field
from typing import List

@dataclass
class ToolConfig:
    """Configuration for a MATLAB tool"""

    # Required fields
    matlab_name: str
    create_tool: str

    # Optional fields with defaults
    description: str = ""
    input_type: str = "file_path"
    output_type: str = "data_structure"
    category: str = "general"

    # Validation errors
    errors: List[str] = field(default_factory=list, init=False)

    def validate(self) -> bool:
        """Validate the configuration"""
        # Validation logic here
        pass
```

### modules/models/__init__.py
```python
"""Data models for the setup wizard"""

from .tool_config import ToolConfig

__all__ = ['ToolConfig']
```

### modules/__init__.py (Updated)
```python
"""Module exports"""

from .user_input import greet, get_user_input
from .validator import validate_tool_config
from .template_engine import setup_template
from .models.tool_config import ToolConfig

__all__ = [
    'greet',
    'get_user_input',
    'validate_tool_config',
    'setup_template',
    'ToolConfig'
]
```

## Data Flow with Data Classes

```
┌─────────────┐
│   main.py   │  Entry point
└──────┬──────┘
       │
       ├─→ modules.get_user_input()
       │   └─→ Returns: ToolConfig object
       │
       ├─→ modules.validate_tool_config(tool_config)
       │   └─→ Accepts: ToolConfig object
       │   └─→ Returns: (bool, str)
       │
       └─→ modules.setup_template(tool_config)
           └─→ Accepts: ToolConfig object
           └─→ Returns: str
```

## MVC Pattern Alignment

```
Model (Data Layer)
  └── modules/models/
      └── tool_config.py          # ⭐ Data structure + validation

View (User Interface Layer)
  └── modules/user_input.py       # CLI interaction with user

Controller (Business Logic Layer)
  ├── main.py                     # Orchestrates flow
  ├── modules/validator.py        # Validation logic
  └── modules/template_engine.py  # Template processing

Configuration
  └── config.py                   # Constants and settings

Templates
  └── templates/                  # MATLAB templates
```

## How to Create This Structure

```bash
# From the project root
cd /home/user/setup_wizard_mvp

# Create the models directory
mkdir -p modules/models

# Create the __init__.py files
touch modules/models/__init__.py

# Create the data class file
touch modules/models/tool_config.py

# (Optional) Create tests directory
mkdir -p tests
touch tests/__init__.py
touch tests/test_tool_config.py
```

## File Sizes (Approximate)

```
modules/models/tool_config.py     ~80 lines   # The data class
modules/models/__init__.py        ~5 lines    # Exports
modules/__init__.py (updated)     ~10 lines   # Updated exports
modules/user_input.py (updated)   ~25 lines   # Returns ToolConfig
modules/validator.py (updated)    ~20 lines   # Validates ToolConfig
modules/template_engine.py (upd)  ~30 lines   # Accepts ToolConfig
main.py (updated)                 ~25 lines   # Uses ToolConfig
```

## Benefits of This Structure

✅ **Clear Separation**
  - Data models in their own directory
  - Easy to find and maintain

✅ **Scalable**
  - Add more data classes easily (e.g., `template_config.py`)
  - No need to change existing structure

✅ **MVC Compliant**
  - Model: `modules/models/`
  - View: `modules/user_input.py`
  - Controller: `main.py`, validators, processors

✅ **Testable**
  - Data classes are easy to test
  - Separate test directory for unit tests

✅ **Professional**
  - Industry-standard structure
  - Clear naming conventions
  - Self-documenting organization
