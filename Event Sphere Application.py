import datetime
from tkinter import *
from tkcalendar import *
import sqlite3
from tkinter import messagebox
from tkinter import ttk
import calendar


def showEvent(event):
    y = cal.get_calevents(date=cal.selection_get())
    t.config(state='normal')
    t.delete(1.0, 'end')
    t.insert('end', f"   {cal.selection_get().strftime('%d-%B-%Y')} \n\n")
    t.tag_add("here", "1.0", "2.0")
    t.tag_config("here", background="WHITE", foreground="black",
                 underline=True, justify='center')

    for i in y:
        aux = cal.calevent_cget(i, 'tags')
        if len(aux) > 1:
            t.insert('end', f"{aux[0]}\n")
        else:
            t.insert('end', f"{aux[0]}\n")

    t.config(state='disabled')


def load_task():
    the_cursor.execute(
        'CREATE TABLE IF NOT EXISTS events (tag TEXT, year INTEGER, month INTEGER, day INTEGER, recurring INTEGER)')

    the_cursor.execute('SELECT * FROM events')
    rows = the_cursor.fetchall()

    for row in rows:
        tag = row[0]
        year = row[1]
        month = row[2]
        day = row[3]
        recurrence_type = row[4]

        id = cal.calevent_create(datetime.date(
            year, month, day), 'Task', tags=tag)
        cal.tag_config(tag, background='red', foreground='yellow')

        if recurrence_type == 1:
            create_recurring_events(tag, datetime.date(
                year, month, day), recurrence_type)
        elif recurrence_type == 2:
            create_recurring_events(tag, datetime.date(
                year, month, day), recurrence_type)
        elif recurrence_type == 3:
            create_recurring_events(tag, datetime.date(
                year, month, day), recurrence_type)


def add_task():
    new_task = entry.get()
    if new_task:
        tag = new_task
        recurrence_type = recurrence_var.get()

        the_cursor.execute('INSERT INTO events VALUES (?, ?, ?, ?, ?)', (tag, cal.selection_get(
        ).year, cal.selection_get().month, cal.selection_get().day, recurrence_type))
        the_connection.commit()

        id = cal.calevent_create(cal.selection_get(), 'Task', tags=tag)
        cal.tag_config(tag, background='red', foreground='yellow')

        if recurrence_type == 1:
            create_recurring_events(tag, cal.selection_get(), recurrence_type)
        elif recurrence_type == 2:
            create_recurring_events(tag, cal.selection_get(), recurrence_type)
        elif recurrence_type == 3:
            create_recurring_events(tag, cal.selection_get(), recurrence_type)

        entry.delete(0, 'end')
    else:
        messagebox.showwarning(
            "Validation Error", "Please enter a task before adding.")


def edit_task():
    selected_date = cal.selection_get()
    selected_tags = cal.get_calevents(date=selected_date)

    if not selected_tags:
        messagebox.showwarning(
            "Validation Error", "No task selected for editing.")
        return

    # Assuming there is only one event per date for simplicity
    selected_tag = selected_tags[0]
    old_tag = cal.calevent_cget(selected_tag, 'tags')[0]
    old_date = cal.calevent_cget(selected_tag, 'date')

    new_task = entry.get()
    if new_task:
        new_tag = new_task
        recurrence_type = recurrence_var.get()

        # Delete the old event
        cal.calevent_remove(selected_tag)

        # Delete the old entry in the database
        the_cursor.execute('DELETE FROM events WHERE tag=? AND year=? AND month=? AND day=?',
                           (old_tag, old_date.year, old_date.month, old_date.day))
        the_connection.commit()

        # Add the new event
        the_cursor.execute('INSERT INTO events VALUES (?, ?, ?, ?, ?)', (new_tag, selected_date.year,
                                                                         selected_date.month, selected_date.day, recurrence_type))
        the_connection.commit()

        id = cal.calevent_create(selected_date, 'Task', tags=new_tag)
        cal.tag_config(new_tag, background='red', foreground='yellow')

        if recurrence_type == 1:
            create_recurring_events(new_tag, selected_date, recurrence_type)
        elif recurrence_type == 2:
            create_recurring_events(new_tag, selected_date, recurrence_type)
        elif recurrence_type == 3:
            create_recurring_events(new_tag, selected_date, recurrence_type)

        entry.delete(0, 'end')
    else:
        messagebox.showwarning(
            "Validation Error", "Please enter a new task before editing.")


def create_recurring_events(tag, start_date, recurrence_type):
    if recurrence_type == 1:  # Yearly
        for year_offset in range(1, 6):
            new_date = start_date.replace(year=start_date.year + year_offset)
            id = cal.calevent_create(new_date, 'Task', tags=tag)
            cal.tag_config(tag, background='red', foreground='yellow')
    elif recurrence_type == 2:  # Monthly
        for month_offset in range(1, 13):
            new_date = add_months(start_date, month_offset)
            id = cal.calevent_create(new_date, 'Task', tags=tag)
            cal.tag_config(tag, background='red', foreground='yellow')
    elif recurrence_type == 3:  # Weekly
        for week_offset in range(1, 53):
            new_date = start_date + datetime.timedelta(weeks=week_offset)
            id = cal.calevent_create(new_date, 'Task', tags=tag)
            cal.tag_config(tag, background='red', foreground='yellow')


def add_months(dt, months):
    month = dt.month - 1 + months
    year = dt.year + month // 12
    month = month % 12 + 1
    day = min(dt.day, calendar.monthrange(year, month)[1])
    return dt.replace(year=year, month=month, day=day)


def delete_task():
    selected_date = cal.selection_get()
    selected_tags = cal.get_calevents(date=selected_date)

    if not selected_tags:
        messagebox.showwarning(
            "Validation Error", "No task selected for deletion.")
        return

    for selected_tag in selected_tags:
        # Get the tag associated with the event
        tag_to_delete = cal.calevent_cget(selected_tag, 'tags')
        if tag_to_delete:
            tag_to_delete = tag_to_delete[0]

            # Delete the event from the calendar
            cal.calevent_remove(selected_tag)

            # Delete the corresponding entry from the database
            the_cursor.execute('DELETE FROM events WHERE tag=? AND year=? AND month=? AND day=?',
                               (tag_to_delete, selected_date.year, selected_date.month, selected_date.day))
            the_connection.commit()

    messagebox.showinfo("Task Deleted", "Task successfully deleted.")


def edit_task():
    selected_date = cal.selection_get()
    selected_tags = cal.get_calevents(date=selected_date)

    if not selected_tags:
        messagebox.showwarning(
            "Validation Error", "No task selected for editing.")
        return

    root_edit = Toplevel(root)
    root_edit.title('Edit Task')
    root_edit.iconbitmap('ga2.ico')

    frame_edit = Frame(root_edit)
    frame_edit.pack(padx=10, pady=10)

    old_tag = cal.calevent_cget(selected_tags[0], 'tags')[0]
    old_date = cal.calevent_cget(selected_tags[0], 'date')

    entry_label_edit = Label(frame_edit, text="Edit Task:",
                             font=('Times New Roman', 12))
    entry_label_edit.grid(row=0, column=0, columnspan=2, pady=(0, 10))

    entry_edit = Entry(frame_edit, width=30, background='white',
                       font=('Times New Roman', 12))
    entry_edit.grid(row=1, column=0, columnspan=2)

    entry_edit.insert(0, old_tag)

    recurrence_var_edit = IntVar()
    yearly_radio_edit = Radiobutton(
        frame_edit, text="Yearly", variable=recurrence_var_edit, value=1, font=('Times New Roman', 12))
    yearly_radio_edit.grid(row=2, column=0)

    monthly_radio_edit = Radiobutton(
        frame_edit, text="Monthly", variable=recurrence_var_edit, value=2,  font=('Times New Roman', 12))
    monthly_radio_edit.grid(row=2, column=1)

    weekly_radio_edit = Radiobutton(
        frame_edit, text="Weekly", variable=recurrence_var_edit, value=3, font=('Times New Roman', 12))
    weekly_radio_edit.grid(row=2, column=2)

    # Set the initial value based on the existing task
    recurrence_var_edit.set(the_cursor.execute(
        'SELECT recurring FROM events WHERE tag=? AND year=? AND month=? AND day=?',
        (old_tag, old_date.year, old_date.month, old_date.day)).fetchone()[0])

    def save_changes():
        new_tag = entry_edit.get()
        recurrence_type = recurrence_var_edit.get()

        # Delete the old event
        cal.calevent_remove(selected_tags[0])

        # Delete the old entry in the database
        the_cursor.execute('DELETE FROM events WHERE tag=? AND year=? AND month=? AND day=?',
                           (old_tag, old_date.year, old_date.month, old_date.day))
        the_connection.commit()

        # Add the new event
        the_cursor.execute('INSERT INTO events VALUES (?, ?, ?, ?, ?)', (new_tag, selected_date.year,
                                                                         selected_date.month, selected_date.day, recurrence_type))
        the_connection.commit()

        id = cal.calevent_create(selected_date, 'Task', tags=new_tag)
        cal.tag_config(new_tag, background='red', foreground='yellow')

        if recurrence_type == 1:
            create_recurring_events(new_tag, selected_date, recurrence_type)
        elif recurrence_type == 2:
            create_recurring_events(new_tag, selected_date, recurrence_type)
        elif recurrence_type == 3:
            create_recurring_events(new_tag, selected_date, recurrence_type)

        entry_edit.delete(0, 'end')
        root_edit.destroy()

    save_button_edit = Button(frame_edit, text='Save Changes',
                              command=save_changes, background='#add8e6', font=('Times New Roman', 12))
    save_button_edit.grid(row=3, column=0, columnspan=3, pady=(10, 0))

    # Close the edit window without saving changes
    cancel_button_edit = Button(frame_edit, text='Cancel',
                                command=root_edit.destroy, background='#add8e6', font=('Times New Roman', 12,))
    cancel_button_edit.grid(row=4, column=0, columnspan=3)


if __name__ == '__main__':
    tag_list = []
    date_list = []

    root = Tk()
    root.title('Event Sphere')
    root.iconbitmap('ga2.ico')

    the_connection = sqlite3.connect('new1.db')
    the_cursor = the_connection.cursor()

    style = ttk.Style()
    style.theme_use('clam')

    cal = Calendar(root, year=datetime.datetime.now().year)
    cal.config(background='green', foreground='white', font=('Times New Roman', 12), bordercolor='#add8e6',
               borderwidth=0,
               headersbackground='#add8e6', headersforeground='black',
               normalbackground='white', normalforeground='black', weekendbackground='white',
               weekendforeground='black',
               othermonthforeground='#464646', othermonthbackground='#C5C5C5', othermonthweforeground='#464646',
               othermonthwebackground='#C5C5C5')

    cal.bind('<<CalendarSelected>>', showEvent)
    cal.pack(fill='both', expand=1)

    load_task()

    t = Text(root, height=5, width=50, font=('Times New Roman', 12))
    t.config(relief='solid', borderwidth=2, state='disabled')
    t.pack(fill='both', expand=1)

    entry_label = Label(root, text="New Task:",
                        background='white', font=('Times New Roman', 12))
    entry_label.pack()

    entry = Entry(root, width=30, background='white',
                  font=('Times New Roman', 12))
    entry.pack()

    recurrence_var = IntVar()
    yearly_radio = Radiobutton(
        root, text="Yearly", variable=recurrence_var, value=1, background='white', font=('Times New Roman', 12))
    yearly_radio.pack()
    monthly_radio = Radiobutton(
        root, text="Monthly", variable=recurrence_var, value=2, background='white', font=('Times New Roman', 12))
    monthly_radio.pack()
    weekly_radio = Radiobutton(
        root, text="Weekly", variable=recurrence_var, value=3, background='white', font=('Times New Roman', 12))
    weekly_radio.pack()

    add_button = Button(root, text='Add Task',
                        command=add_task, font=('Times New Roman', 12))
    add_button.pack(fill='both', expand=1)
    add_button.config(relief='solid', borderwidth=1, cursor='hand2', background='#add8e6',
                      font=('Pristina 15 bold'))

    edit_button = Button(root, text='Edit Task',
                         command=edit_task, font=('Times New Roman', 12))
    edit_button.pack(fill='both', expand=1)
    edit_button.config(relief='solid', borderwidth=1, cursor='hand2', background='#add8e6',
                       font=('Pristina 15 bold'))

    delete_button = Button(root, text='Delete Task',
                           command=delete_task, font=('Times New Roman', 12))
    delete_button.pack(fill='both', expand=1)
    delete_button.config(relief='solid', borderwidth=1, cursor='hand2', background='#add8e6',
                         font=('Pristina 15 bold'))

    root.configure(background='white')

    root.mainloop()
