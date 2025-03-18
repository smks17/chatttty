from enum import Enum
import importlib
import pkgutil

import sys
from typing import List
sys.path.append(".")


from lib.llm.base_llm import BaseLLM
from lib.llm import models


def import_submodules(package):
    package_name = package.__name__
    for _, module_name, _ in pkgutil.iter_modules(package.__path__):
        full_module_name = f"{package_name}.{module_name}"
        importlib.import_module(full_module_name)


def get_all_subclasses(cls) -> List[BaseLLM]:
    subclasses = set(cls.__subclasses__())
    for subclass in list(subclasses):
        subclasses.update(get_all_subclasses(subclass))
    return subclasses


import_submodules(models)
ModelsEnum = Enum("Models", {cls.LLM_NAME: cls for cls in get_all_subclasses(BaseLLM)})

assert len(ModelsEnum) == 2, "You add/remove any models and you should use `makemigrations`"
