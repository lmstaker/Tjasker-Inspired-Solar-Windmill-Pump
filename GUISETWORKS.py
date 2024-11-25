import tkinter as tk
from tkinter import ttk
from tkinter.messagebox import showinfo
from time import sleep
import RPi.GPIO as GPIO
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

def mode_selected():
    #Run tjasker
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(19,GPIO.OUT)
    GPIO.setup(13,GPIO.OUT)
    cw = GPIO.PWM(19,100)
    cc = GPIO.PWM(13,100)
    cw.start(0)
    cc.start(0)
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

        '''dir_button =ttk.Button(root,text='Set Direction', command = set_direction)
        dir_button.pack(fill='x',padx=5,pady=5)'''
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
        '''time_button = ttk.Button(settime, text='Set Duration',command=spin)
        time_button.pack(fill='x',pady=10)'''
        #Input speed and direction into Tsajker
        def spin():
            direction = selected_direction.get()
            speed = get_current_speed()
            dur = duration.get()
            #Convert variables
            sf = float(speed)
            df = int(dur)
            if direction==0:
                for i in range(0,df):
                    cw.ChangeDutyCycle(sf)
                    sleep(1)
            else:
                for i in range(0,df):
                    cc.ChangeDutyCycle(sf)
                    sleep(1)
            cw.stop()
            cc.stop()
            msg = direction + ' ' + speed + ' ' + dur
            showinfo(title='spinning', message = msg)
            #Reset widgets
            dir_lbl.destroy()
            ccb.destroy()
            cwb.destroy()
            speed_slider_lbl.destroy()
            speed_control.destroy()
            speed_lbl.destroy()
            speed_now_lbl.destroy()
            settime.destroy()
            duration_lbl.destroy()
            time_entry.destroy()
            spin_button.destroy()
        spin_button = ttk.Button(root,text = 'Run Tsajker',command=spin)
        spin_button.pack(fill='x',pady=10)
    if mode == 'Continuous':
        spinning = False
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
        #Emergency stop
        def stop():
            spinning = False
            msg = 'Stop Performed'
            showinfo(title='Error', message = msg)
            #Reset widgets
            dir_lbl.destroy()
            ccb.destroy()
            cwb.destroy()
            dir_button.destroy()
            speed_slider_lbl.destroy()
            speed_control.destroy()
            speed_lbl.destroy()
            speed_now_lbl.destroy()
            spin_button.destroy()
            stop.destroy()
        #Input speed and direction into Tsajker
        def spin():
            direction = selected_direction.get()
            speed = get_current_speed()
            dur = 'go'
            #Convert variables
            sf = float(speed)
            while stopped == False:
                if direction==0:
                    cw.ChangeDutyCycle(sf)
                else:
                    cc.ChangeDutyCycle(sf)
            cw.stop()
            cc.stop()
            
            msg = direction + ' ' + speed + ' ' + dur
            spinning = True
            showinfo(title='spinning', message = msg)
            while spinning == True:
                print('yes')
                sleep(1)
        stop = ttk.Button(root,text='Stop', command=stop)
        stop.pack(fill='x',pady=10)  
        spin_button = ttk.Button(root,text = 'Run Tsajker',command=spin)
        spin_button.pack(fill='x',pady=10)
        root.mainloop()
        GPIO.cleanup()
mode_button = ttk.Button(root,text='Set Mode',command = mode_selected)
mode_button.pack(fill='x')

