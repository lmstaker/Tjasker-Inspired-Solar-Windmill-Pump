import tkinter as tk
from tkinter import ttk
from tkinter.messagebox import showinfo
from time import sleep
#Initialize window
root=tk.Tk()
root.title('Tjasker Control Panel')
#Window dimensions and position
ww = 600
wh = 600
sw = root.winfo_screenwidth()
sh = root.winfo_screenheight()
c_x = int(sw/2 - ww/2)
c_y = int(sh/2 - wh/2)
root.geometry(f'{ww}x{wh}+{c_x}+{c_y}')
#Mode selection
mode_lbl=ttk.Label(root,text = 'Select mode:')
mode_lbl.pack(fill='x',padx=5,pady=10)
mode = tk.StringVar()
selected_mode = ttk.Combobox(root,width=27,textvariable=mode)
selected_mode['values'] = ('Set Run', 'Continuous')
selected_mode.pack(fill='x',padx=5,pady=10)
selected_mode.current()
#Define motion
spinning = False
def scanning():
    if spinning:
        print('yes')
    root.after(1000,scanning)
def mode_selected():
    #Stop
    def stop():
        global spinning
        spinning = False
        msg = 'Stop Performed'
        showinfo(title='Stopped', message = msg)
        #Resets widgets
        dir_lbl.destroy()
        ccb.destroy()
        cwb.destroy()
        speed_slider_lbl.destroy()
        speed_control.destroy()
        speed_lbl.destroy()
        speed_now_lbl.destroy()
        spin_button.destroy()
        if mode == 'Set Run':
            settime.destroy()
            duration_lbl.destroy()
            time_entry.destroy()
            estop.destroy()
        elif mode == 'Continuous':
            dir_button.destroy()
            cstop.destroy()
    mode = selected_mode.get()
    #Set window to mode
    if mode == 'Set Run':
        #Input to select direction
        def set_direction():
            showinfo(title='Direction Changed', message=selected_direction.get())
        selected_direction = tk.StringVar()
        directions = (('Clockwise','True'), ('Counterclockwise','False'))
        dir_lbl = ttk.Label(text='Direction')
        dir_lbl.pack(fill='x', padx=5,pady=5)
        cwb = ttk.Radiobutton(root, text=directions[0][0],value=directions[0][1],
                        variable=selected_direction)
        cwb.pack(fill='x',padx=5,pady=5)
        ccb = ttk.Radiobutton(root, text=directions[1][0],value=directions[1][1],
                        variable=selected_direction)
        ccb.pack(fill='x',padx=5,pady=5)
        #Input to select speed
        current_speed = tk.DoubleVar()
        def get_current_speed():
            return '{: .2f}'.format(current_speed.get())
        def speed_changed(event):
            speed_now_lbl.configure(text=get_current_speed())
        speed_slider_lbl = ttk.Label(root, text='Speed')
        speed_slider_lbl.pack(fill='x',padx=5,pady=20)
        speed_control = ttk.Scale(root, from_=0, to=100,orient='horizontal',
                          command=speed_changed,variable=current_speed)
        speed_control.pack(fill='x',padx=5,pady=5)
        speed_lbl = ttk.Label(root,text='Speed:')
        speed_lbl.pack(fill='x',padx=5,pady=5)
        speed_now_lbl = ttk.Label(root, text = current_speed)
        speed_now_lbl.pack(fill='x',padx=5,pady=5)
        #Input time
        duration = tk.StringVar()
        settime = ttk.Frame(root)
        settime.pack(fill='x',padx=5,pady=20)
        duration_lbl = ttk.Label(settime,text='Duration:')
        duration_lbl.pack(fill='x',)
        time_entry = ttk.Entry(settime,textvariable = duration)
        time_entry.pack(fill='x')
        time_entry.focus()
        #Input speed and direction into Tsajker
        def spin():
            direction = selected_direction.get()
            speed = float(get_current_speed())
            dur = duration.get()
            print(direction, speed, dur.isdigit())
            #Validate input settings
            if (direction != 'True') and (direction != 'False'):
                msg = 'Please select a direction'
                showinfo(title='Error',message = msg)
            elif 10 > speed:
                msg = 'Please select a valid speed'
                showinfo(title='Error',message=msg)
            elif not dur.isdigit():
                msg = 'Please input a valid duration'
                showinfo(title='Error',message=msg)
            else:
                #Run Tjasker
                spin_button.destroy()
                global spinning
                spinning = True
                root.after(int(1000*float(dur)),stop)
                msg = direction + ' ' + str(speed) + ' ' + dur
                #showinfo(title='spinning', message = msg)  
        spin_button = ttk.Button(root,text = 'Run Tsajker',command=spin)
        spin_button.pack(fill='x',pady=10)
        estop = ttk.Button(root,text='Emergency Stop', command=stop)
        estop.pack(fill='x',pady=10)
    if mode == 'Continuous':
        #Input to select direction
        def set_direction():
            showinfo(title='Direction Changed', message=selected_direction.get())
        selected_direction = tk.StringVar()
        directions = (('Clockwise','True'), ('Counterclockwise','False'))
        dir_lbl = ttk.Label(text='Direction')
        dir_lbl.pack(fill='x', padx=5,pady=5)
        cwb = ttk.Radiobutton(root, text=directions[0][0],value=directions[0][1],
                        variable=selected_direction)
        cwb.pack(fill='x',padx=5,pady=5)
        ccb = ttk.Radiobutton(root, text=directions[1][0],value=directions[1][1],
                        variable=selected_direction)
        ccb.pack(fill='x',padx=5,pady=5)

        dir_button =ttk.Button(root,text='Change Direction', command = set_direction)
        dir_button.pack(fill='x',padx=5,pady=5)
        #Input to select speed
        current_speed = tk.DoubleVar()
        def get_current_speed():
            return '{: .2f}'.format(current_speed.get())
        def speed_changed(event):
            speed_now_lbl.configure(text=get_current_speed())
        speed_slider_lbl = ttk.Label(root, text='Speed')
        speed_slider_lbl.pack(fill='x',padx=5,pady=20)
        speed_control = ttk.Scale(root, from_=0, to=100,orient='horizontal',
                          command=speed_changed,variable=current_speed)
        speed_control.pack(fill='x',padx=5,pady=5)
        speed_lbl = ttk.Label(root,text='Speed:')
        speed_lbl.pack(fill='x',padx=5,pady=5)
        speed_now_lbl = ttk.Label(root, text = current_speed)
        speed_now_lbl.pack(fill='x',padx=5,pady=5)
        #Input speed and direction into Tsajker
        def spin():
            global spinning
            direction = selected_direction.get()
            speed = float(get_current_speed())
            dur = 'go'
            #Validate input settings
            if (direction != 'True') and (direction != 'False'):
                msg = 'Please select a direction'
                showinfo(title='Error',message = msg)
            elif 10 > speed:
                msg = 'Please select a valid speed'
                showinfo(title='Error',message=msg)
            else:
                msg = direction + ' ' + str(speed) + ' ' + dur
                spinning = True
                #showinfo(title='spinning', message = msg)
        spin_button = ttk.Button(root,text = 'Run Tsajker',command=spin)
        spin_button.pack(fill='x',pady=10)
        cstop = ttk.Button(root,text='Stop', command=stop)
        cstop.pack(fill='x',pady=10)
        root.mainloop()
root.after(1000,scanning)
mode_button = ttk.Button(root,text='Set Mode',command = mode_selected)
mode_button.pack(fill='x')

