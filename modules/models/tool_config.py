from dataclasses import dataclass, field
from typing import List

@dataclass
class ToolConfig:
    matlab_name: str
    create_tool: bool

    description: str = ""
    input_type: str = ""
    output_type: str = ""
    category: str = ""

    errors: List[str] = field(default_factory=list, init=False)

    def validate(self)->bool:
        self.errors.clear()
        if not self.matlab_name.replace(" ", "").isalpha():
            self.errors.append("only letters allowed")
        if not self.matlab_name.strip():
            self.errors.append("empty string")
        return len(self.errors) == 0


    def get_summary(self):
        return f"MATLAB Name: {self.matlab_name}\n" \
               f"Create Tool: {self.create_tool}\n" \
               f"Description: {self.description}\n" \
               f"Input Type: {self.input_type}\n" \
               f"Output Type: {self.output_type}\n" \
               f"Category: {self.category}"
