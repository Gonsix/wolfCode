from enum import Enum
from typing import List
from langchain_core.pydantic_v1 import BaseModel, Field


class CodeSuggestion(BaseModel):
    relevant_file: str = Field(description="a relevant file you want to subject")
    relevant_code: str = Field(description="a relevant code block that the user is going to improve.")
    relevant_line_start: int = Field(description="the line number that the relevant code block start")
    improved_code: str = Field(description="an improved code block for the part to be changed based on your suggestion.")
    description: str = Field(description="an informative and actionable description of your proposal, How user should modify code?")

class BugType(str, Enum):
    memory_bug = "Memory Bug"
    logic_bug = "Logic Bug"
    syntax_bug = "Syntax Bug"
    exception_handling_bug = "Improper exception handling Bug"
    race_condition_bug = "Race Condition Bug"
    io_bug = "I/O Bug"
    resource_leak_bug = "Resource leak Bug"
    other = "Other Bug"

class Bug(BaseModel):
    title: str = Field(description="a short concise title of the bug that you found.")
    type: BugType = Field(description="Type of the bug")
    suggestion: CodeSuggestion

class AuditReport(BaseModel):
    bugs: List[Bug]
    summary: str = Field(description="comprehensive and informative summary of bugs you found in the code chunks")
