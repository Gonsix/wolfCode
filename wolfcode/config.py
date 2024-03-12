from os.path import join
from dynaconf import Dynaconf

from wolfcode.definitions import ROOT_DIR

settings = Dynaconf(
    envvar_prefix="DYNACONF",
    settings_files=[join(ROOT_DIR, f) for f in [
        'wolfcode/settings/check_coding_standards.toml',
    ]]
)
