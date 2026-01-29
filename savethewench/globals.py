_DEBUG_MODE = False


def is_debug_mode():
    return _DEBUG_MODE


def enable_debug_mode():
    global _DEBUG_MODE
    _DEBUG_MODE = True
