import pytermgui as ptg
from localstore import LocalStore

CONFIG = """
config:
    InputField:
        styles:
            prompt: dim italic
            cursor: '@72'
    Label:
        styles:
            value: dim bold

    Window:
        styles:
            border: '60'
            corner: '60'

    Container:
        styles:
            border: '96'
            corner: '96'
"""

with ptg.YamlLoader() as loader:
    pass
    #loader.load(CONFIG)

store = LocalStore('db.json')

def submit(button):
    #print(f'{btn=}')
    project_name = button.label
    #print(f'{project_name}')
    store.switch_to(project_name)

def show_summary(button):
    summary = store.get_total_spent_per_project()
    summary = dict(summary)
    print(summary)

def active_project(fmt):
    return store.get_current_project()


ptg.tim.define('!current', active_project)

projects = [
    'reading a book',
    'sleeping',
    'go for walk',
    'meeting with friends'
]

with ptg.WindowManager() as manager:
    #manager.layout.add_slot('body')
    #manager.add(
    #    ptg.Window(
    #        'Current project: [!current].'
    #    )
    #)

    btns = [ptg.Button(name, submit) for name in projects ]

    window = (
        ptg.Window(
            *btns,
            ptg.Button('show summary', show_summary),
            #ptg.Button('btn', submit, projname='pystem'),
            # ["btn", lambda *_: submit(manager, window, _), ],
            # ["btn", lambda *_: submit(manager, window, _)],
            # ["btn", lambda *_: submit(manager, window, _)],
            # ["btn", lambda *_: submit(manager, window, _)],
            width=60,
            box="DOUBLE",
        )
        .set_title("[210 bold]New contact")
        #.center()
    )

    manager.add(window)
