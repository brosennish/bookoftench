from savethewench import SaveTheWenchGame
from savethewench.component.menu import ActionMenu

DEBUG = True

if __name__ == '__main__':
    if DEBUG:
        component = ActionMenu
        SaveTheWenchGame.debug_from(component)
    else:
        SaveTheWenchGame.run()
