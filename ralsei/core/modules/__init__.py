import ralsei.core
import os.path
import pkgutil


def fetch_modules():
    return {name: __import__(f"ralsei.core.modules.{name}", fromlist=[name]) for name in
            [name for _, name, _ in pkgutil.iter_modules([os.path.dirname(ralsei.core.modules.__file__)])]}
