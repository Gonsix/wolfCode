from os.path import join
from dynaconf import Dynaconf

from wolfcode.definitions import ROOT_DIR



coding_rules = Dynaconf(
    envvar_prefix="DYNACONF",
    settings_files=[join(ROOT_DIR, f) for f in [
        'wolfcode/settings/wolfssl_coding_standards.toml',
    ]]
)

def load_default(relative_path: str)->Dynaconf:
    """
    This function returns Dynaconf settings from relative path from the project root.
    """
    settings = Dynaconf(
        envvar_prefix="DYNACONF",
        settings_files=[join(ROOT_DIR, f) for f in [
           relative_path,
        ]]
    )

    return settings


def load_config(config_path: str)-> Dynaconf:
    """
    This function returns Dynaconf settings from config_path    
    """
    settings = Dynaconf(
        envvar_prefix="DYNACONF",
        settings_files=[
            config_path
        ]
    )
    return settings


