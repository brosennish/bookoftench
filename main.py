import argparse

from savethewench import SaveTheWenchGame


def load_component(class_name):
    import importlib
    import inspect
    import pkgutil
    package = importlib.import_module('savethewench.component')

    for _, module_name, _ in pkgutil.iter_modules(package.__path__):
        module = importlib.import_module(f"{package.__name__}.{module_name}")

        if hasattr(module, class_name):
            obj = getattr(module, class_name)
            if inspect.isclass(obj):
                return obj

    raise ImportError(
        f"Class '{class_name}' not found in package '{package.__name__}'"
    )


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Save The Wench Game")
    parser.add_argument("-d", "--debug", action="store_true")
    parser.add_argument("-c", "--component", default="ActionMenu")
    parser.add_argument("-s", "--seed", type=int, default=666)

    args = parser.parse_args()

    if args.debug:
        import random

        random.seed(args.seed)
        # noinspection PyTypeChecker
        SaveTheWenchGame.debug_from(load_component(args.component))
    else:
        SaveTheWenchGame.run()
