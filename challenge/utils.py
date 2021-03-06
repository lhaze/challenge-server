import os
import sys


def import_all_names(_file, _name):
    """
    Trick for dynamic import of all names from all submodules. Use in the
    __init__.py using following idiom:
        import_all_classes(__file__, __name__)

    Provides for __all__ attribute of child modules.
    """
    path = os.path.dirname(os.path.abspath(_file))
    parent_module = sys.modules[_name]

    for py in [filename[:-3] for filename in os.listdir(path)
               if filename.endswith('.py') and filename != '__init__.py']:
        module = __import__('.'.join([_name, py]), fromlist=[py])
        module_names = getattr(module, '__all__', None) or dir(module)
        objects = {
            name: getattr(module, name)
            for name in module_names
            if not name.startswith('_')
        }
        for name, obj in objects.items():
            if hasattr(parent_module, name) and \
               getattr(parent_module, name) is not obj:
                msg = (
                    "Function import_all_names hit upon conflicting "
                    "names. '{}' is already imported to {} module."
                ).format(name, module)
                import warnings
                warnings.warn(msg)
            setattr(parent_module, name, obj)
