# pip install kivi
# pip install kivymd

from kivymd.app import MDApp
from kivymd.uix.dialog import MDDialog
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.pickers import MDDatePicker, MDTimePicker
from datetime import datetime

from kivymd.uix.list import  TwoLineAvatarIconListItem, ILeftBody
from kivymd.uix.selectioncontrol import MDCheckbox

from database import Database
db = Database()


class DialogContent(MDBoxLayout):
    # the init function for class constructor
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.ids.date_text.text = datetime.now().strftime("%A %d %B %Y")

    # # this function will show the date picker
    def show_date_picker(selfs):
        date_dialog = MDDatePicker()
        date_dialog.bind(on_save=selfs.on_save)
        date_dialog.open()

    # this function will get the date and saves in a friendly form
    def on_save(self, instance, value, date_range):
        date = value.strftime("%A %d %B %Y")
        self.ids.date_text.text = str(date)


# Class for marking and deleting list item
class ListItemWithCheckbox(TwoLineAvatarIconListItem):
    def __init__(self, pk=None, **kwargs):
        super().__init__(**kwargs)
        self.pk = pk

    # marking the item as complete or imcomplete
    def mark(self, check, the_list_item):
        if check.active:
            the_list_item.text = '[s]' + the_list_item.text + '[/s]'
            db.mark_task_as_completed(the_list_item.pk)
        else:
            the_list_item.text = str(db.mark_task_as_incompleted(the_list_item.pk))

    # deleting list item
    def delete_item(self, the_list_item):
        self.parent.remove_widget(the_list_item)
        db.delete_task(the_list_item.pk)


class LeftCheckbox(ILeftBody, MDCheckbox):
    '''custom list'''


# This is the main class
class MainApp(MDApp):
    task_list_dialog = None

    # This is the build function for setting the theme
    def build(self):
        self.theme_cls.primary_palette = "Teal"

    # this is the show task function
    def show_task_dialog(self):
        if not self.task_list_dialog:
            self.task_list_dialog = MDDialog(
                title="Create Task",
                type="custom",
                content_cls=DialogContent()
            )
            self.task_list_dialog.open()

    # to add task
    def add_task(self, task, task_date):
        # print(task.text, task_date)
        created_task = db.create_task(task.text, task_date)
        self.root.ids['container'].add_widget(ListItemWithCheckbox(pk = created_task[0], text='[b]' + created_task[1] + '[/b]', secondary_text=created_task[2]))
        task.text = ""

    # this is to close
    def close_dialog(self, *args):
        self.task_list_dialog.dismiss()
        self.task_list_dialog = None  # Reset the reference to None


    def on_start(self):
        '''This is to load saved tasks and add them to the MDList widget'''
        completed_tasks, incompleted_tasks = db.get_tasks()

        if incompleted_tasks != []:
            for task in incompleted_tasks:
                add_task = ListItemWithCheckbox(pk=task[0], text=task[1], secondary_text=task[2])
                self.root.ids.container.add_widget(add_task)

        if completed_tasks != []:
            for task in completed_tasks:
                add_task = ListItemWithCheckbox(pk=task[0], text="[s]" + task[1] + "[/s]", secondary_text=task[2])
                add_task.ids.check.active = True
                self.root.ids.container.add_widget(add_task)


if __name__ == '__main__':
    app = MainApp()
    app.run()
