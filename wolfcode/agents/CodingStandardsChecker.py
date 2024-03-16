import sys, os
from typing import List, Optional
from pathlib import Path
from langchain.output_parsers import PydanticOutputParser, OutputFixingParser, RetryOutputParser
from langchain.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI
from rich.console import Console
from rich.syntax import Syntax
from rich.panel import Panel
from rich.text import Text

from wolfcode.output_schemas import CodingStandardsReview
from wolfcode.config import load_config, coding_rules
from wolfcode.definitions import ROOT_DIR
from wolfcode.utils import get_file_contents
from wolfcode.config import load_config, load_default

# format coding rules
coding_rules: list[str] = coding_rules.rules
coding_rules = "".join([f"- {rule}\n" for rule in coding_rules])

class CodingStandardsChecker(object):
    # a relative path to the config file
    DEFAULT_CONFIG_PATH = "wolfcode/settings/check_coding_standards_config.toml"

    def __init__(self, files: List[Path], config_path: Optional[Path]) -> None:
        self.target_files = files
        self.config_path = config_path
        
        if config_path:
            self.settings = load_config(config_path=config_path)
        else:
            self.settings = load_default(CodingStandardsChecker.DEFAULT_CONFIG_PATH)

    def run(self):

        # Loading source code from multiple files.
        code_chunks = get_file_contents([str(path) for path in self.target_files])

        # TODO: settingファイルからOPENAI_API_KEYを読み込み
        llm = ChatOpenAI(model="gpt-4-1106-preview", temperature=0.0)

        prompt = ChatPromptTemplate.from_messages(messages=[
            ("system", self.settings.templates.SYSTEM_TEMPLATE),
            ("user", self.settings.templates.USER_TEMPLATE)
        ])

        pydantic_parser = PydanticOutputParser(pydantic_object=CodingStandardsReview)
        # This second parser calls out to another LLM to fix any errors when the first parser fails.
        parser = OutputFixingParser.from_llm(llm=ChatOpenAI(model="gpt-4-1106-preview", temperature=0.0), parser=pydantic_parser)

        chain = prompt | llm | parser

        result: CodingStandardsReview = chain.invoke({
            "language": self.settings.variables.language, 
            "coding_rules": coding_rules,
            "extra_instruction": self.settings.variables.extra_instruction,
            "format_instruction": parser.get_format_instructions(),
            "code_chunks": code_chunks
        
        })
        self.displayCodingStandardsReview(result)

    def displayCodingStandardsReview(self, review: CodingStandardsReview):
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
        
        summary = Panel.fit(Text(f"{review.summary}", style="yellow"), title="Summary", title_align="left", style="bold", border_style="green")
        console.print(summary)

        


