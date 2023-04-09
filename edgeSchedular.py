import tkinter as tk
import webbrowser
import datetime
import threading
from tkcalendar import DateEntry
import tkinter.messagebox as messagebox
import time


def open_browser(link):
    webbrowser.open(link, new=2)

def schedule_browser_opening():
    year = date_entry.get_date().year
    month = date_entry.get_date().month
    day = date_entry.get_date().day
    hour = hour_var.get()
    minute = minute_var.get()
    link = link_entry.get()
    try:
        time_obj = datetime.datetime.strptime("{}:{}:00".format(hour, minute), "%H:%M:%S")
        scheduled_time = datetime.datetime(year, month, day, time_obj.hour, time_obj.minute, 0)
        now = datetime.datetime.now()
        time_diff = (scheduled_time - now).total_seconds()
        if time_diff <= 0:
            messagebox.showerror("Error", "The scheduled time has already passed.")
        else:
            threading.Timer(time_diff, open_browser, args=[link]).start()
            scheduled_items.append((scheduled_time, link))
            scheduled_items.sort(key=lambda x: x[0])
            update_listbox()
            messagebox.showinfo("Scheduled", "The browser page will open on {}-{}-{} at {}:{}".format(year, month, day, hour, minute))
    except ValueError:
        messagebox.showerror("Error", "Invalid time format. Please enter a time in the format HH:MM.")

def update_listbox():
    listbox.delete(0, tk.END)
    for item in scheduled_items:
        listbox.insert(tk.END, "{} - {}".format(item[0].strftime("%Y-%m-%d %H:%M:%S"), item[1]))

root = tk.Tk()
root.title("Browser Scheduler")

scheduled_items = []

date_label = tk.Label(root, text="Select the date:")
date_entry = DateEntry(root, width=12, background='darkblue', foreground='white', borderwidth=2)

hour_label = tk.Label(root, text="Select the hour:")
hour_var = tk.StringVar(value="00")
hour_choices = [str(i).zfill(2) for i in range(0, 24)]
hour_menu = tk.OptionMenu(root, hour_var, *hour_choices)

minute_label = tk.Label(root, text="Select the minute:")
minute_var = tk.StringVar(value="00")
minute_choices = [str(i).zfill(2) for i in range(0, 60)]
minute_menu = tk.OptionMenu(root, minute_var, *minute_choices)

link_label = tk.Label(root, text="Enter the link:")
link_entry = tk.Entry(root)

button = tk.Button(root, text="Schedule", command=schedule_browser_opening)

listbox_label = tk.Label(root, text="Scheduled Items:")
listbox = tk.Listbox(root, width=50, height=10)

date_label.pack()
date_entry.pack()
hour_label.pack()
hour_menu.pack()
minute_label.pack()
minute_menu.pack()
link_label.pack()
link_entry.pack()
button.pack()

listbox_label.pack()
listbox.pack()

def on_closing():
    if messagebox.askokcancel("Quit", "Do you want to quit?"):
        root.destroy()

root.protocol("WM_DELETE_WINDOW", on_closing)


def update_schedule():
    while True:
        now = datetime.datetime.now()
        for item in scheduled_items:
            if now >= item[0]:
                threading.Thread(target=open_browser, args=[item[1]]).start()
                scheduled_items.remove(item)
                update_listbox()
        time.sleep(1)

threading.Thread(target=update_schedule, daemon=True).start()

def update_listbox():
    listbox.delete(0, tk.END)
    for item in scheduled_items:
        listbox.insert(tk.END, "{} - {}".format(item[0].strftime("%Y-%m-%d %H:%M:%S"), item[1]))

def sort_by_time():
    scheduled_items.sort(key=lambda x: x[0])
    update_listbox()

def sort_by_link():
    scheduled_items.sort(key=lambda x: x[1])
    update_listbox()

sort_time_button = tk.Button(root, text="Sort by Time", command=sort_by_time)
sort_link_button = tk.Button(root, text="Sort by Link", command=sort_by_link)

sort_time_button.pack(side=tk.RIGHT, anchor=tk.N)
sort_link_button.pack(side=tk.RIGHT, anchor=tk.N)

listbox_label.pack(side=tk.TOP, anchor=tk.W)
listbox.pack(side=tk.TOP, anchor=tk.W)


root.mainloop()
