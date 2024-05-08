# Ryland Price

import tkinter as tk
import threading
import time
import json

current_page = 0
curr_hour = 0
curr_min = 0
curr_sec = 0
current_section = 0
update_speed = 0.5
total_run_time = 0
total_time_remaining = 0
section_run_time = 0
section_time_remaining = 0
section_time_remaining_min = 0
section_time_remaining_sec = 0
section_run_time_start = 0
section_run_time_min = 0
section_run_time_sec = 0
cycle_start_time = 0
total_run_time_min = 0
total_run_time_sec = 0
total_run_time_hr_start = 0
total_run_time_hr = 0
ramp_dwn_time = 10

section_running = False
cycle_running = False

GPIO_LST = ["GPIO 1", "GPIO 2", "GPIO 3", "GPIO 4", "GPIO 5", "GPIO 6"]


try:
    with open("data_file.txt", "r+") as file:
        temp_obj = file.readlines()
        info = json.loads(temp_obj[0])
except:
    info = {"total_run_time": 0, "total_time_remaining": 0, "curr_section": 0, "section_run_time": 0,
            "section_time_remaining": 0}

section_order = [info["first_section"], info["second_section"], info["third_section"], info["fourth_section"],
                 info["fifth_section"], info["sixth_section"]]
section_time = [info["section_1_time"], info["section_2_time"], info["section_3_time"], info["section_4_time"],
                info["section_5_time"], info["section_6_time"]]


def start_section(n):
    global current_section, section_run_time, section_run_time_start, section_running
    section_run_time = 0
    section_run_time_start = time.time()
    section_running = True
    #GPIO_LST[n-1] turn on
    # print("section " + str(n) + " running")
    current_section = n
    time.sleep(section_time[n-1] * 60)
    #GPIO_LST[n-1] turn off
    section_running = False
    time.sleep(ramp_dwn_time)


def run_cycle():
    global total_run_time_hr_start
    global current_section, cycle_running, cycle_start_time
    cycle_running = True
    cycle_start_time = time.time()
    temp = time.localtime()
    total_run_time_hr_start = temp.tm_hour
    for i in section_order:
        start_section(i)
    current_section = 0
    cycle_running = False


def get_current_time():
    # Get the current time using time.localtime() which returns a time struct
    current_time = time.localtime()

    # Extract hour, minute, and second from the time struct
    if current_time.tm_hour > 12:
        hour = current_time.tm_hour - 12
    else:
        hour = current_time.tm_hour
    minute = current_time.tm_min
    second = current_time.tm_sec

    # Return hour, minute, and second
    return hour, minute, second


def time_thread_func():
    global curr_hour, curr_min, curr_sec, update_speed
    while True:
        curr_hour, curr_min, curr_sec = get_current_time()
        if curr_min < 10:
            curr_min = str(0) + str(curr_min)
        if curr_sec < 10:
            curr_sec = str(0) + str(curr_sec)
        time.sleep(update_speed)
        redraw_status()
        # redraw_screen()


def redraw_status():
    global status_page_lb, status_page_time_title, status_page_total_running_time_title, \
            status_page_total_time_left_title, status_page_current_section_title, \
            status_page_current_section_runtime_title, status_page_current_section_time_remaining_title, \
            status_page_time_lbl, status_page_total_running_time, status_page_total_time_left, \
            status_page_current_section, status_page_current_section_runtime, \
            status_page_current_section_time_remaining, curr_hour, total_run_time, total_time_remaining, \
            current_section, section_run_time, section_time_remaining, section_run_time_min, section_run_time_sec, \
            total_run_time_sec, total_run_time_min, total_run_time_hr, total_run_time_hr_start, total_time_remaining, \
            section_time_remaining_min, section_time_remaining_sec
    if section_running:
        section_run_time = round(-section_run_time_start + time.time())
        if section_run_time % 60 < 10:
            section_run_time_sec = "0" + str(section_run_time % 60)
        else:
            section_run_time_sec = section_run_time % 60
        if section_run_time // 60 < 10:
            section_run_time_min = "0" + str(section_run_time // 60)
        else:
            section_run_time_min = str(section_run_time // 60)
        if round(((section_time[current_section - 1] * 60) - section_run_time) // 60) < 10:
            section_time_remaining_min = "0" + str(round(((section_time[current_section - 1] * 60) - section_run_time) // 60))
        else:
            section_time_remaining_min = str(round(((section_time[current_section - 1] * 60) - section_run_time) // 60))
        if round(((section_time[current_section - 1] * 60) - section_run_time)) < 10:
            section_time_remaining_sec = "0" + str(round(((section_time[current_section - 1] * 60) - section_run_time) % 60))
        else:
            section_time_remaining_sec = str(round(((section_time[current_section - 1] * 60) - section_run_time) % 60))
    else:
        section_run_time = 0
        section_run_time_min = "00"
        section_run_time_sec = "00"
        section_time_remaining_min = "00"
        section_time_remaining_sec = "00"

    if cycle_running:
        temp = time.localtime()
        total_run_time_hr = "0" + str(temp.tm_hour - total_run_time_hr_start)
        total_run_time = round(time.time() - cycle_start_time)
        total_time_remaining_hr = "0" + str(round(((((section_time[0] + section_time[1] + section_time[2] + section_time[3] +
                                    section_time[4] + section_time[5]) * 60) - total_run_time + (6 * ramp_dwn_time)) // 60) // 60))
        if ((((section_time[0] + section_time[1] + section_time[2] + section_time[3] +
                                    section_time[4] + section_time[5]) * 60) - total_run_time + (6 * ramp_dwn_time)) // 60) < 10:
            total_time_remaining_min ="0" + str(round(((((section_time[0] + section_time[1] + section_time[2] + section_time[3] +
                                    section_time[4] + section_time[5]) * 60) - total_run_time + (6 * ramp_dwn_time)) // 60) % 60))
        else:
            total_time_remaining_min = str(
                round(((((section_time[0] + section_time[1] + section_time[2] + section_time[3] +
                    section_time[4] + section_time[5]) * 60) - total_run_time + (6 * ramp_dwn_time)) // 60) % 60))
        if ((((section_time[0] + section_time[1] + section_time[2] + section_time[3] +
                                    section_time[4] + section_time[5]) * 60) - total_run_time + (6 * ramp_dwn_time)) % 60) < 10:
            total_time_remaining_sec = "0" + str(round((((section_time[0] + section_time[1] + section_time[2] + section_time[3] +
                                    section_time[4] + section_time[5]) * 60) - total_run_time + (6 * ramp_dwn_time)) % 60))
        else:
            total_time_remaining_sec = str(
                round(((section_time[0] + section_time[1] + section_time[2] + section_time[3] +
                   section_time[4] + section_time[5]) * 60) - total_run_time + (6 * ramp_dwn_time)) % 60)
        if total_run_time % 60 < 10:
            total_run_time_sec = "0" + str(total_run_time % 60)
        else:
            total_run_time_sec = total_run_time % 60
        if (total_run_time // 60) % 60 < 10:
            total_run_time_min = "0" + str((total_run_time // 60) % 60)
        else:
            total_run_time_min = str((total_run_time // 60) % 60)
    else:
        total_run_time = 0
        total_run_time_hr = "00"
        total_run_time_min = "00"
        total_run_time_sec = "00"
        total_time_remaining_hr = "00"
        total_time_remaining_min = "00"
        total_time_remaining_sec = "00"
    # setup status page info lables#
    status_page_time_lbl = tk.Label(status_page, text=str(curr_hour) + ":" + str(curr_min) + ":" + str(curr_sec),
                                    font=("", 20), pady=8)
    status_page_time_lbl.grid(row=2, column=0)
    status_page_total_running_time = tk.Label(status_page, text=str(total_run_time_hr) + ":" + str(total_run_time_min) + ":" + str(total_run_time_sec), font=("", 20), pady=8)
    status_page_total_running_time.grid(row=2, column=1)
    status_page_total_time_left = tk.Label(status_page, text=total_time_remaining_hr + ":" + total_time_remaining_min + ":" + total_time_remaining_sec, font=("", 20),
                                                          pady=8)
    status_page_total_time_left.grid(row=2, column=2)
    status_page_current_section = tk.Label(status_page, text=str(current_section), font=("", 20), pady=8)
    status_page_current_section.grid(row=4, column=0)
    status_page_current_section_runtime = tk.Label(status_page, text=str(section_run_time_min) + ":" + str(section_run_time_sec), font=("", 20), pady=8)
    status_page_current_section_runtime.grid(row=4, column=1)
    status_page_current_section_time_remaining = tk.Label(status_page, text=section_time_remaining_min + ":" + section_time_remaining_sec, font=("", 20),
                                                          pady=8)
    status_page_current_section_time_remaining.grid(row=4, column=2)
    ###status page end###


def redraw_screen():
    global current_page
    for i in frame_lst:
        i.pack_forget()
    if not current_page == 0:
        bottom_frame.pack(side=tk.BOTTOM, fill=tk.X)
    else:
        bottom_frame.pack_forget()
    frame_lst[current_page].pack(fill=tk.BOTH, expand=1)


def go_to_home():
    global current_page
    current_page = 0
    redraw_screen()


def go_to_status_screen():
    global current_page
    current_page = 1
    redraw_screen()


def go_to_setup_screen():
    global current_page
    current_page = 2
    redraw_screen()


def go_to_manual_control():
    global current_page
    current_page = 3
    redraw_screen()


time_thread = threading.Thread(target=time_thread_func)
time_thread.start()


button_color = "Gray"
root = tk.Tk()
root.title("")
root.geometry("800x480")
# root.wm_attributes('-toolwindow', 'True')
home_screen = tk.Frame(root)
status_page = tk.Frame(root, height=440, width=800)
setup_page = tk.Frame(root, height=480, width=800)
manual_control = tk.Frame(root, height=480, width=800)
bottom_frame = tk.Frame(root, height=50, width=800)
frame_lst = [home_screen, status_page, setup_page, manual_control]

###bottom frame start###
bottom_frame.pack_propagate(False)
tk.Button(bottom_frame, text="Return Home", font=("", 25), command=go_to_home, bg=button_color).pack(side=tk.RIGHT)

##bottom frame end###

###home screen start###
home_screen.pack(fill=tk.BOTH, expand=1)
home_screen.pack_propagate(False)
tk.Label(home_screen, text="Home Screen", font=("", 40)).pack(side=tk.TOP)
tk.Label(home_screen, text="", width=14, height=1).pack(side=tk.TOP)
tk.Button(home_screen, text="Status Page", font=("", 25), width=14, height=1, bg=button_color, command=go_to_status_screen).pack(side=tk.TOP)
tk.Label(home_screen, text="", width=14, height=1).pack(side=tk.TOP)
tk.Button(home_screen, text="Setup Page", font=("", 25), width=14, height=1, bg=button_color, command=go_to_setup_screen).pack(side=tk.TOP)
tk.Label(home_screen, text="", width=14, height=1).pack(side=tk.TOP)
tk.Button(home_screen, text="Manual Control", font=("", 25), width=14, height=1, bg=button_color, command=go_to_manual_control).pack(side=tk.TOP)

##home screen end###

###status page start###

#configure status page#
status_page.pack_propagate(False)
status_page.grid_columnconfigure([0, 1, 2], weight=1)
status_page.grid_rowconfigure([0], weight=2)
status_page.grid_rowconfigure([1, 2, 3, 4, 5], weight=1)

#setup status page title labels#
status_page_lb = tk.Label(status_page, text="Status Page", font=("", 40))
status_page_lb.grid(row=0, column=0, columnspan=3)
status_page_time_title = tk.Label(status_page, text="Current Time:", font=("", 12), pady=8)
status_page_time_title.grid(row=1, column=0)
status_page_total_running_time_title = tk.Label(status_page, text="Total Running Time:", font=("", 12), pady=8)
status_page_total_running_time_title.grid(row=1, column=1)
status_page_total_time_left_title = tk.Label(status_page, text="Total Time Remaining:", font=("", 12), pady=8)
status_page_total_time_left_title.grid(row=1, column=2)
status_page_current_section_title = tk.Label(status_page, text="Section:", font=("", 12), pady=8)
status_page_current_section_title.grid(row=3, column=0)
status_page_current_section_runtime_title = tk.Label(status_page, text="Section Runtime:", font=("", 12), pady=8)
status_page_current_section_runtime_title.grid(row=3, column=1)
status_page_current_section_time_remaining_title = tk.Label(status_page, text="Section Time Remaining:", font=("", 12), pady=8)
status_page_current_section_time_remaining_title.grid(row=3, column=2)

#setup status page info lables#
status_page_time_lbl = tk.Label(status_page, text=str(curr_hour) + ":" + str(curr_min) + ":" + str(curr_sec), font=("", 20), pady=8)
status_page_time_lbl.grid(row=2, column=0)
status_page_total_running_time = tk.Label(status_page, text=str(total_run_time), font=("", 20), pady=8)
status_page_total_running_time.grid(row=2, column=1)
status_page_total_time_left = tk.Label(status_page, text=str(total_time_remaining), font=("", 20), pady=8)
status_page_total_time_left.grid(row=2, column=2)
status_page_current_section = tk.Label(status_page, text=str(current_section), font=("", 20), pady=8)
status_page_current_section.grid(row=4, column=0)
status_page_current_section_runtime = tk.Label(status_page, text=str(section_run_time), font=("", 20), pady=8)
status_page_current_section_runtime.grid(row=4, column=1)
status_page_current_section_time_remaining = tk.Label(status_page, text=str(section_time_remaining), font=("", 20), pady=8)
status_page_current_section_time_remaining.grid(row=4, column=2)
###status page end###

###setup page start###

setup_page.pack_propagate(False)
tk.Label(setup_page, text="Setup Page", font=("", 40)).pack(side=tk.TOP)


###setup page end###

###manual control start###

manual_control.pack_propagate(False)
tk.Label(manual_control, text="Manual Control", font=("", 40)).pack(side=tk.TOP)


###manual control end###
run_thread = threading.Thread(target=run_cycle)
run_thread.start()
root.mainloop()
