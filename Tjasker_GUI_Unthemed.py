import RPi.GPIO as GPIO
from time import sleep
import tkinter as tk
from tkinter import ttk
from tkinter.messagebox import showinfo
#from ttkthemes import ThemedTk
from time import sleep
#Initialize window
root = tk.Tk()
#root=ThemedTk(theme='adapta')
#root.configure(bg='light blue')
#root=ThemedTk(theme='black')
#root.configure(bg='black')
root.title('Tjasker Control Panel')
#Window dimensions and position
ww = 700
wh = 700
sw = root.winfo_screenwidth()
sh = root.winfo_screenheight()
c_x = int(sw/2 - ww/2)
c_y = int(sh/2 - wh/2)
#background_image=tk.PhotoImage(file=r"C:\Users\meh\Downloads\holland.png")
#background_label = tk.Label(root, image=background_image)
#background_label.place(x=0, y=0, relwidth=1, relheight=1)
root.geometry(f'{ww}x{wh}+{c_x}+{c_y}')
#Run Motor
#Mode selection
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
#Define motion
spinning = False
turn = [0,0]
def scanning():
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(19,GPIO.OUT)
    GPIO.setup(13,GPIO.OUT)
    cw = GPIO.PWM(19,100)
    cc = GPIO.PWM(13,100)
    cw.start(0)
    cc.start(0)
    if spinning:
        if turn[0] == 'True':
            cw.ChangeDutyCycle(turn[1])
            print(turn)
        elif turn[0]=='False':
            cc.ChangeDutyCycle(turn[1])
            print(turn)
    elif not spinning:
        GPIO.cleanup()
    root.after(1,scanning)
def mode_selected():
    def reset_widgets():
        changemode_button.destroy()
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
    #Stop
    def stop():
        global spinning
        if spinning:
            spinning = False
            msg = 'Stop Performed'
            #showinfo(title='Stopped', message = msg)
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
                changemode_button.destroy()
                spin_button.destroy()
                global spinning
                global turn
                spinning = True
                turn = [direction, speed]
                root.after(int(1000*float(dur)),stop)
                msg = direction + ' ' + str(speed) + ' ' + dur
                #showinfo(title='spinning', message = msg)  
        spin_button = ttk.Button(root,text = 'Run Tsajker',command=spin)
        spin_button.pack(fill='x',pady=10)
        estop = ttk.Button(root,text='Emergency Stop', command=lambda: [stop()])
        estop.pack(fill='x',pady=10)
    elif mode == 'Continuous':
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
        speed_now_lbl = ttk.Label(root, text = current_speed)
        speed_now_lbl.pack(fill='x',padx=5,pady=5)
        #Input speed and direction into Tsajker
        def spin():
            global spinning
            global turn
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
                turn  = [direction,speed]
                changemode_button.destroy()
                spin_button.destroy()
                cstop = ttk.Button(root,text='Stop', command=lambda: [cstop.destroy(),stop()])
                cstop.pack(fill='x',pady=10)
                #showinfo(title='spinning', message = msg)
        spin_button = ttk.Button(root,text = 'Run Tsajker',command=spin)
        spin_button.pack(fill='x',pady=10)
        root.mainloop()
    else:
        msg = 'Please select a mode'
        showinfo(title='Error', message=msg)
root.after(1,scanning)
mode_button = ttk.Button(root,text='Set Mode',command =lambda: [mode_button.destroy(), mode_selected()])
mode_button.pack()
