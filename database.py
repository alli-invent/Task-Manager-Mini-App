import sqlite3


class Database():
    def __init__(self):
        self.connection = sqlite3.connect("tasks_diary.db")
        self.cursor = self.connection.cursor()
        self.create_task_table()

    # creating the tasks table
    def create_task_table(self):
        # with fields id, task, completed
        self.cursor.execute("CREATE TABLE IF NOT EXISTS tasks (id integer PRIMARY KEY AUTOINCREMENT, task varchar(50) NOT NULL, due_date varchar(50), completed BOOLEAN NOT NULL CHECK (completed IN (0,1)))")
        self.connection.commit()

    # create individual task
    def create_task(self, task, due_date="None"):
        self.cursor.execute("INSERT INTO tasks(task, due_date, completed) VALUES(?,?,?)", (task, due_date, 0) )
        self.connection.commit()


        # get last entered list item and add it to the task list
        created_task = self.cursor.execute("SELECT id, task, due_date FROM tasks WHERE task = ? and completed = 0", (task,)).fetchall()
        # return last one
        return created_task[-1]

    # Getting all records in the table
    def get_tasks(self):
        '''Getting all tasks: completed and incompleted'''
        incompleted_tasks = self.cursor.execute("SELECT id, task, due_date FROM tasks WHERE completed = 0").fetchall()
        completed_tasks = self.cursor.execute("SELECT id, task, due_date FROM tasks WHERE completed = 1").fetchall()
        return completed_tasks, incompleted_tasks

    # Updating the tasks and removing strike through
    def mark_task_as_completed(self, taskid):
        '''Mark tasks as completed'''
        self.cursor.execute("UPDATE tasks SET completed = 1 WHERE id = ?", (taskid,))
        self.connection.commit()

    def mark_task_as_incompleted(self, taskid):
        '''Mark tasks as completed'''
        self.cursor.execute("UPDATE tasks SET completed = 0 WHERE id = ?", (taskid,))
        self.connection.commit()

        # return the task text
        task_text = self.cursor.execute("SELECT task FROM tasks WERE id = ?", (taskid,)).fetchall()
        return task_text[0][0]

    # Deleting task
    def delete_task(self, taskid):
        '''Delete a task'''
        self.cursor.execute("DELETE FROM tasks WHERE id = ?", (taskid,))
        self.connection.commit()

    # close connection
    def close_db_connection(self):
        self.connection.close()
