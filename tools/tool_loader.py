import importlib
import pkgutil
import inspect
from typing import List
from langchain.tools import Tool
from tools import __path__ as tools_path

def load_all_tools() -> List[Tool]:
    
    all_tools: List[Tool] = []

    for _, module_name, _ in pkgutil.walk_packages(tools_path, prefix="tools."):
        try:
            module = importlib.import_module(module_name)
        except Exception:
            continue  # skip if import fails

        for _, obj in inspect.getmembers(module):
            if isinstance(obj, Tool):
                print(f"🛠️ Loaded tool: {obj.name} from {module_name}")
                all_tools.append(obj)

    return all_tools
