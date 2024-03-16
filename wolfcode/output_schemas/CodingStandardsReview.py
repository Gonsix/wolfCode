from typing import Optional, List
from langchain_core.pydantic_v1 import BaseModel, Field


'''
check_coding_standardsの出力形式を定義, このモデルを元に生成される出力形式の指示文を{format_instruction}に渡す
'''

class CodeSuggestion(BaseModel):
    relevant_file: str = Field(description="a relevant file you want to subject")
    relevant_code: str = Field(description="a relevant code block that the user is going to improve, including original comments")
    relevant_line_start: int = Field(description="the line number that the relevant code block start")
    improved_code: str = Field(description="an accurately improved code block for the part to be changed based on your suggestion.")
    description: str = Field(description="an informative and actionable description of your proposal, How user should modify code?")

class ValidationItem(BaseModel):
    title: str = Field(description="A short title for one element of the validation item given in the Coding Rules")
    valid: Optional[bool] = Field(description="whether the validation item is actually followed by the code, or None if its unknown.")
    reason: str = Field(description="The concise and concrete reason for validation")
    suggestion: Optional[CodeSuggestion] = Field(description="required only if the validation is invalid.")

class CodingStandardsReview(BaseModel):
    validation_items: List[ValidationItem]
    summary: str = Field(description="comprehensive and informative summary of coding standards review.")


