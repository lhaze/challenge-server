import os
import sys


def import_all_classes(_file, _name):
    """
    Trick for dynamic import of all classes from all submodules. Use in the
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
        classes = {
            classname: getattr(module, classname)
            for classname in module_names
            if isinstance(getattr(module, classname), type)
        }
        for classname, cls in classes.items():
            if hasattr(parent_module, classname) and \
               getattr(parent_module, classname) is not cls:
                msg = (
                    "Function import_all_classes hit upon conflicting "
                    "class names. '{}' is already imported to {} module."
                ).format(classname, module)
                import warnings
                warnings.warn(msg)
            setattr(parent_module, classname, cls)
