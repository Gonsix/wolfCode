import sys
import os
from langchain.output_parsers import PydanticOutputParser
from langchain.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI

from wolfcode.definitions import ROOT_DIR
from wolfcode.config import settings, coding_rules
from wolfcode.output_schemas import CodingStandardsReview, visualize_review
from wolfcode.utils import get_file_contents

# get coding rules from config files.
coding_rules: list[str] = coding_rules.rules
coding_rules = "".join([f"- {rule}\n" for rule in coding_rules])




def main():
    if len(sys.argv) < 2:
        print('Usage: $ python wolfcode/check_coding_standards.py <File...>')
        print('  ex)  $ python wolfcode/check_coding_standards.py file1.txt file2.txt')
        sys.exit(2)
    # settingファイルに行ってlanguageなど設定を変更できる。
    if sys.argv[1] == '--show-config-path':
        print(os.path.join(ROOT_DIR, "wolfcode/settings/check_coding_standards.toml"))
        sys.exit(0)


        # ファイル(複数)のソースコードをロードする.
    code_chunks = get_file_contents(sys.argv[1:])

    # TODO: settingファイルからOPENAI_API_KEYを読み込み
    llm = ChatOpenAI(model="gpt-4-1106-preview", temperature=0.0)

    prompt = ChatPromptTemplate.from_messages(messages=[
        ("system", settings.templates.SYSTEM_TEMPLATE),
        ("user", settings.templates.USER_TEMPLATE)
    ])

    parser = PydanticOutputParser(pydantic_object=CodingStandardsReview)

    chain = prompt | llm | parser

    # CodingStandardReview型のオブジェクトで受け取る
    # TODO: ユーザーが設定ファイルのテンプレートに変数を新しく追加したときに、このプログラムを触らなくてよくする
    result: CodingStandardsReview = chain.invoke({
        "language": settings.variables.language, 
        "coding_rules": coding_rules,
        "extra_instruction": settings.variables.extra_instruction,
        "format_instruction": parser.get_format_instructions(),
        "code_chunks": code_chunks
    
    })
    print(result)
    visualize_review(result)


if __name__ == '__main__':
    main()
