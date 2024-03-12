from typing import Optional, List
from langchain_core.pydantic_v1 import BaseModel, Field

from rich.console import Console
from rich.table import Table
from rich.syntax import Syntax

'''
check_coding_standardsの出力形式を定義, このモデルを元に生成される出力形式の指示文を{format_instruction}に渡す
'''

class CodeSuggestion(BaseModel):
    relevant_file: str = Field(description="a relevant file you want to subject")
    relevant_code: str = Field(description="a relevant code block that the user is going to improve, including original comments")
    relevant_line_start: int = Field(description="the line number that the relevant code block start")
    improved_code: str = Field(description="an improved code block, should be valid code, based on what you propose.")
    description: str = Field(description="an informative and actionable description of your proposal, How user should modify code?")

class ValidationItem(BaseModel):
    title: str = Field(description="A short title for one element of the validation item given in the Coding Rules")
    valid: Optional[bool] = Field(description="whether the validation item is actually followed by the code, or None if its unknown.")
    reason: str = Field(description="The concise and concrete reason for validation")
    suggestion: Optional[CodeSuggestion] = Field(description="required only if the validation is invalid.")

class CodingStandardsReview(BaseModel):
    validation_items: List[ValidationItem]



def visualize_review(review: CodingStandardsReview):
    console = Console()

    def align(code_snippet: str, width: int) -> str:
        """
        引数で受け取った文字列型のコードスニペットを全ての行でwidthの数だけ空白でインデントした文字列を返す
        """
        lines = code_snippet.splitlines()
        indented_lines = [ " "*width + f"{line}\n" for line in lines]
        return "".join(indented_lines)
    
    for item in review.validation_items:
        console.print(f"[bold magenta]Title:[/] {item.title}", justify="left")
        console.print(f"[bold magenta]Valid:[/] {item.valid}", justify="left")
        console.print(f"[bold magenta]Reason:[/] {item.reason}", justify="left")
        

        if item.valid is False or item.suggestion:

            lexer = Syntax.guess_lexer(path=item.suggestion.relevant_file)
            console.print(f"[bold magenta]Suggestion:[/] {item.suggestion.description}", justify="left")
            console.print(f"  in [green][/] {item.suggestion.relevant_file}", justify="left")
            console.print("[bold magenta]From:[/]", justify="left")
            syntax = Syntax(item.suggestion.relevant_code, lexer=lexer, theme="monokai", line_numbers=True, start_line=item.suggestion.relevant_line_start)
            console.print(syntax)
            console.print("[bold magenta]Into:[/]", justify="left")
            improved_code = align(item.suggestion.improved_code, len(str(item.suggestion.relevant_line_start))+3)
            syntax_improved = Syntax(improved_code, lexer=lexer, theme="monokai", line_numbers=False)
            console.print(syntax_improved)

        console.print("")  
