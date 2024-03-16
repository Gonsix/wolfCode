import sys
import os

from typing import Optional, List
from pydantic import BaseModel, Field
from pathlib import Path
import typer
from typing_extensions import Annotated
from wolfcode.definitions import ROOT_DIR
from wolfcode.agents import CodeAuditAgent, CodingStandardsChecker

app = typer.Typer()




@app.command(
    help="Audit code and Suggest improvement to help you fix source code in specified files.  For mode info. -> $ wolfcode audit --help"
)
def audit( 
    files: Annotated[List[Path], typer.Argument(help="files to input")] = None,
    show_config_path: Annotated[bool, typer.Option(help="Show default config path in your system")] = False,
    config_file: Annotated[Optional[Path], typer.Option(help="config file path to alternate the default")] = None,
    ):

    if not files and not show_config_path and not config_file:
        typer.echo('wolfCode Error: You missed input files or options')
        typer.echo('  See help: $ wolfcode audit --help')
        sys.exit(3)

    elif show_config_path and (files or config_file):
        typer.echo("wolfCode: Cannot use '--show-config-path' with any other option or args")
        sys.exit(3)


    elif show_config_path:
        #TODO:  設定パスを表示するロジックを実装
        print(os.path.join(ROOT_DIR, CodeAuditAgent.DEFAULT_CONFIG_PATH))
        sys.exit(0)

    elif files is None or len(files) == 0 or files == []:
        print("wolfCode:  Missing argument 'FILES...'.   ")
        print("See help: $ wolfcode audit --help")
        sys.exit(3)

    else:
        # Execute the agent
        CodeAuditAgent(files, config_file).run()


@app.command(
    help="check whether the code follows wolfSSL coding standards.  For mode info. -> $ wolfcode check --help"
)
def check( 
    files: Annotated[List[Path], typer.Argument(help="files to input")] = None,
    show_config_path: Annotated[bool, typer.Option(help="Show default config path in your system")] = False,
    config_file: Annotated[Optional[Path], typer.Option(help="config file path to alternate the default")] = None,
    ):

    if not files and not show_config_path and not config_file:
        typer.echo('wolfCode Error: You missed input files or options')
        typer.echo('  See help: $ wolfcode check --help')
        sys.exit(3)

    elif show_config_path and (files or config_file):
        typer.echo("wolfCode: Cannot use '--show-config-path' with any other option or args")
        sys.exit(3)


    elif show_config_path:
        #TODO:  設定パスを表示するロジックを実装
        print(os.path.join(ROOT_DIR, CodingStandardsChecker.DEFAULT_CONFIG_PATH))
        sys.exit(0)

    elif files is None or len(files) == 0 or files == []:
        print("wolfCode:  Missing argument 'FILES...'.   ")
        print("See help: $ wolfcode audit --help")
        sys.exit(3)

    else:
        # Execute the agent
        CodingStandardsChecker(files, config_file).run()



def main():
    app()
    
if __name__ == '__main__':
    main()

