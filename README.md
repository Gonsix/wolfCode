# wolfCode
Use `wolfcode`command to verify your code follows the wolfSSL coding standards.

## Getting Started

1. **Clone the repository**: Clone this repository to your local machine to start working with the scripts.

2. **Install dependencies**: Run `pip3 install .` in the root of this project to install the necessary Python packages listed in `pyproject.toml`.

    NOTE: If you are using newer pip, you need to add option: `pip3 install --break-system-packages .`


3. **Export OPENAI_API_KEY ⚙️**:

You must exoport an `OPENAI_API_KEY` in your environment.
Also, you must have an access to the GPT-4 model to call OpenAI API. I recommend to export the key in .zshrc. 

### Amazing! 

Now you can use the `wolfcode` command. 

4. **Usage**:
    See help:
   `$ wolfcode --help`

5. **Configulation**
You can pass your config file with `--config-file` option.
Also, Run `check <subcommand> --show-config-path` to see where the default config file are located and you can change value to the variables like 'lanugage' in the config file.
