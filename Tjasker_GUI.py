'''GUI code with dual mode selection, displaying error messages for
invalid directional, speed, or duration inputs v2.0'''
import RPi.GPIO as GPIO
from time import sleep
import tkinter as tk
from tkinter import ttk
from tkinter.messagebox import showinfo
from ttkthemes import ThemedTk
from time import sleep
#Initialize PWM Output
GPIO.setmode(GPIO.BCM)
GPIO.setup(19,GPIO.OUT)
GPIO.setup(13,GPIO.OUT)
cw = GPIO.PWM(19,100)
cc = GPIO.PWM(13,100)
GPIO.setup(24, GPIO.OUT) #Lights
cw.start(0)
cc.start(0)
#Initialize window
root=ThemedTk(theme='black')
root.configure(bg='black')
def light_mode():
    root.configure(theme='adapta')
    root.configure(bg='light blue')
def dark_mode():
    root.configure(theme='black')
    root.configure(bg='black')
def high_contrast_mode():
    root.configure(theme='kroc')
    root.configure(bg='black')
def patriotic_mode():
    root.configure(theme='kroc')
    root.configure(bg='orange')
root.title('Tjasker Control Panel')
#Enable light controls
def lights_on():
    GPIO.output(24, GPIO.HIGH)
def lights_off():
    GPIO.output(24,GPIO.LOW)
#Window dimensions and position
ww = 700
wh = 700
sw = root.winfo_screenwidth()
sh = root.winfo_screenheight()
c_x = int(sw/2 - ww/2)
c_y = int(sh/2 - wh/2)
root.geometry(f'{ww}x{wh}+{c_x}+{c_y}')
#Creates and managaes menubar items
menubar = tk.Menu(root)
lights = tk.Menu(menubar, tearoff=0)
menubar.add_cascade(label='Lights', menu=lights)
lights.add_command(label='On', command=lights_on)
lights.add_command(label='Off', command=lights_off)
view = tk.Menu(menubar, tearoff=0)
menubar.add_cascade(label='View', menu=view)
view.add_command(label='Light Mode',command=light_mode)
view.add_command(label='Dark Mode', command=dark_mode)
view.add_command(label='High Contrast Mode', command=high_contrast_mode)
view.add_command(label='Patriotic Mode', command=patriotic_mode)
esc = tk.Menu(menubar, tearoff=0)
menubar.add_cascade(label='Exit', menu=esc)
esc.add_command(label='Exit',command=lambda: [root.destroy(),GPIO.cleanup()])
root.config(menu=menubar)
#Mode selection, defines modes and creates menu/buttons to toggle modes
welkom = ttk.Label(root,text='Welkom bij de Tjasker Bedieningspaneel',anchor=tk.CENTER,justify=tk.CENTER,
                    font=('Arial',20,'bold'))
welkom.pack(pady=10)
welcome = ttk.Label(root,text='Welcome to the Tjasker Control Panel', anchor=tk.CENTER, justify=tk.CENTER,
                    font=('Arial',16,'bold'))
welcome.pack(pady=5)
mode_lbl=ttk.Label(root,text = 'Select mode:')
mode_lbl.pack(fill='x',padx=5,pady=10)
mode = tk.StringVar()
selected_mode = ttk.Combobox(root,width=27,textvariable=mode)
selected_mode['values'] = ('Set Run', 'Continuous')
selected_mode.pack(padx=5,pady=10)
selected_mode.current()
#Define motion with direction and speed parameters
spinning = False
turn = [0,0]
#Motor running
def scanning():
    global turn
    if spinning:
        if turn[0] == 'True':
            cw.ChangeDutyCycle(turn[1])
            #print(turn)
        elif turn[0]=='False':
            cc.ChangeDutyCycle(turn[1])
            #print(turn)
    root.after(1,scanning)
def mode_selected():
    #Resets widgets according to last mode
    def reset_widgets():
        changemode_button.destroy()
        if mode == 'Set Run' or mode == 'Continuous':
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
    #Stop
    def stop():
        global spinning
        if spinning:
            cw.ChangeDutyCycle(0)
            cc.ChangeDutyCycle(0)
            spinning = False
            msg = 'Stop Performed'
            reset_widgets()
            mode_button = ttk.Button(root,text='Set Mode',command =lambda: [mode_button.destroy(), mode_selected()])
            mode_button.pack()
    changemode_button = ttk.Button(root,text='Change Mode',command = lambda:[reset_widgets(),mode_selected()])
    changemode_button.pack()
    mode = selected_mode.get()
    #Set window to mode
    if mode == 'Set Run':
        #Input to select direction
        def set_direction():
            showinfo(title='Direction Changed', message='Direction Changed')
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
        speed_control = ttk.Scale(root, from_=10, to=100,orient='horizontal',
                          command=speed_changed,variable=current_speed)
        speed_control.pack(fill='x',padx=5,pady=5)
        speed_lbl = ttk.Label(root,text='Set Speed:')
        speed_lbl.pack(fill='x',padx=5,pady=5)
        speed_now_lbl = ttk.Label(root, text = str(float(get_current_speed())))
        speed_now_lbl.pack(fill='x',padx=5,pady=5)
        #Input duration of run
        duration = tk.StringVar()
        settime = ttk.Frame(root)
        settime.pack(fill='x',padx=5,pady=20)
        duration_lbl = ttk.Label(settime,text='Duration:')
        duration_lbl.pack(fill='x')
        #Creates entry box to type duration
        time_entry = ttk.Entry(settime,textvariable = duration)
        time_entry.pack(fill='x')
        time_entry.focus()
        #Input speed and direction into Tsajker
        def spin():
            direction = selected_direction.get()
            speed = float(get_current_speed())
            dur = duration.get()
            #Validate input settings
            if (direction != 'True') and (direction != 'False'):
                msg = 'Please select a direction'
                showinfo(title='Error',message = msg)
            elif 10 > speed: #Reject speeds too low for motor movement
                msg = 'Please select a valid speed'
                showinfo(title='Error',message=msg)
            elif not dur.isdigit(): #Reject entries that are not a valid duration
                msg = 'Please input a valid duration'
                showinfo(title='Error',message=msg)
            else:
                #Run Tjasker if all inputs are valid
                changemode_button.destroy()
                spin_button.destroy()
                global spinning
                global turn
                spinning = True
                turn = [direction, speed]
                root.after(int(1000*float(dur)),stop)
                msg = direction + ' ' + str(speed) + ' ' + dur
        #Creates button to start run
        spin_button = ttk.Button(root,text = 'Run Tsajker',command=spin)
        spin_button.pack(fill='x',pady=10)
        #Emergency stop to force stop during run
        estop = ttk.Button(root,text='Emergency Stop', command=lambda: [stop()])
        estop.pack(fill='x',pady=10)
        '''Scans for whether motor is "spinning" every millisecond,
        runs "scanning" if true'''
        root.after(1,scanning)
    elif mode == 'Continuous':
        '''Same input definitions as set mode, but excludes duration input'''
        #Input to select direction
        selected_direction = tk.StringVar()
        directions = (('Clockwise','True'), ('Counterclockwise','False'))
        def set_direction():
            showinfo(title='Direction Changed', message='Direction Changed')
            turn[0]= selected_direction.get()
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
            turn[1] = float(get_current_speed())
        speed_slider_lbl = ttk.Label(root, text='Speed')
        speed_slider_lbl.pack(fill='x',padx=5,pady=20)
        speed_control = ttk.Scale(root, from_=10, to=100,orient='horizontal',
                          command=speed_changed,variable=current_speed)
        speed_control.pack(fill='x',padx=5,pady=5)
        speed_lbl = ttk.Label(root,text='Current Speed:')
        speed_lbl.pack(fill='x',padx=5,pady=5)
        speed_now_lbl = ttk.Label(root, text = str(float(get_current_speed())))
        speed_now_lbl.pack(fill='x',padx=5,pady=5)
        #Input speed and direction into Tsajker
        def spin():
            global spinning
            global turn
            direction = selected_direction.get()
            speed = float(get_current_speed())
            #Validate input settings
            if (direction != 'True') and (direction != 'False'):
                msg = 'Please select a direction'
                showinfo(title='Error',message = msg)
            elif 10 > speed:
                msg = 'Please select a valid speed'
                showinfo(title='Error',message=msg)
            else:
                turn  = [direction,speed]
                changemode_button.destroy()
                spin_button.destroy()
                print('yes')
                spinning = True
        #Button for spin command
        spin_button = ttk.Button(root,text = 'Run Tsajker',command=spin)
        spin_button.pack(fill='x',pady=10)
        cstop = ttk.Button(root,text='Stop', command=lambda: [stop()])
        cstop.pack(fill='x',pady=10)
        root.after(1,scanning)
        root.mainloop()
    else:
        msg = 'Please select a mode'
        showinfo(title='Error', message=msg)
#Creates mode menu selection button
mode_button = ttk.Button(root,text='Set Mode',command =lambda: [mode_button.destroy(), mode_selected()])
mode_button.pack()
