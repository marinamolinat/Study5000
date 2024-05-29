import tkinter
from tkinter import *
import time
from tkinter import ttk
import json
from tkinter import messagebox
import spotipy
from spotipy.oauth2 import SpotifyOAuth
import webbrowser
import matplotlib

#from tkinter.ttk import Frame
import json
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk





#window
root = Tk()
root.geometry('500x500')
root.title("Self Management App")
Title = Label(root, text=" Study 5000 ", font=("Consolas", 40, "bold"), fg="white", relief="groove")
root.attributes('-fullscreen',True)

#Style for the window
root.tk_setPalette(background='#000000', foreground='white',
               activeBackground='black', activeForeground="black")

root.option_add("*Font","Consolas")



#Graph class
class App(Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.pack()

        # Initial setup
        self.create_widgets()
        self.create_figure()

        # Initial data
        self.update_graph()

    def create_widgets(self):
        # Create refresh button
        self.refresh_button = Button(self, text="Refresh Graph", command=self.update_graph, fg="black")
        self.refresh_button.pack(side=TOP, pady=10)

    def create_figure(self):
        # Create a figure
        self.figure = Figure(figsize=(6, 4), dpi=100)
        self.axes = self.figure.add_subplot()

        # Create FigureCanvasTkAgg object
        self.figure_canvas = FigureCanvasTkAgg(self.figure, self)

        # Create the toolbar
        self.toolbar = NavigationToolbar2Tk(self.figure_canvas, self)
        self.toolbar.update()
        self.figure_canvas.get_tk_widget().pack(side=TOP, fill=BOTH, expand=1)

    def update_graph(self):
        # Read data
        data = ""
        with open("activities.json", "r") as file:
            data = json.load(file)

        data = data["Activities"]
        languages = list(data.keys())
        popularity = list(data.values())

        # Clear current plot
        self.axes.clear()

        # Create the bar chart

        self.axes.bar(languages, popularity, color='black', edgecolor='blue', linewidth=2)
        self.axes.set_title('Time spent in activities')
        self.axes.set_ylabel('Seconds')


        # Redraw the canvas
        self.figure_canvas.draw()


graph = App(master=root)
graph.place(relx=0.5, rely=0.70, anchor=CENTER)

#Create stopwtach class
class Stopwatch:
    def __init__(self):
        self.start_time = None
        self.elapsed_time = 0
        self.running = False
    def start(self):
        if not self.running:
            self.start_time = time.time() - self.elapsed_time
            self.running = True
            print("Stopwatch started.")

    def stop(self):
        if self.running:
            self.elapsed_time = time.time() - self.start_time
            self.running = False
            print("Stopwatch stopped.")

    def get_elapsed_time(self):
        if self.running:
            return time.time() - self.start_time
        return self.elapsed_time

    def __str__(self):
        return f"Elapsed time: {self.get_elapsed_time():.2f} seconds"


#Frame para medir el tiempo
timetracker = Frame(root, width=150, height=200, bg="black")





#Funciones para el cronometro
clock = Stopwatch()

#Convertir segundos a minutos:segundos
def redable_time(time):
    time = int(time)
    seconds = 0
    minutes = 0
    seconds = int(time % 60)
    minutes = int(time / 60)

    if seconds < 10:
        seconds = "0" + str(seconds)
    if minutes < 10:
        minutes = "0" + str(minutes)



    return fr"{minutes}:{seconds}"


#Update clock, cada 100 ms
def update_clock(label):
    label.config(text=redable_time(clock.get_elapsed_time()))

    root.after(100, update_clock, label)



def startt(label, start, combobox):

   var = combobox.get()
   if not clock.running:
        if var in combobox["values"]:
            start.config(text="Pause")
            clock.start()

            combobox.config(state="disabled")

        else:
            messagebox.showinfo("Alert", "Please select an activity")

   else:
        clock.stop()
        start.config(text="Start")



   update_clock(timee)


def reset(label, start, combobox):


    clock.stop()
    label.config(text="00:00")
    start.config(text="Start")
    var = combobox.get()
    combobox.config(state="enabled")


    with open("activities.json", "r+") as file:
        data = json.load(file)
        if var in data["Activities"]:
            data["Activities"][var] += clock.get_elapsed_time()
            file.seek(0)
            file.truncate()
            json.dump(data, file)

    clock.elapsed_time = 0
    update_clock(label)





#Settings button window

def delete_activity(valueslist):
    var = valueslist.get()
    current_values = list(valueslist["values"])

    with open("activities.json", 'r+') as file:

        data = json.load(file)
        if var in data["Activities"]:

            result = messagebox.askyesnocancel("Alert", "Are you sure you would like to delete " + var)
            if result:
                del data["Activities"][var]
                current_values.remove(var)
                valueslist["values"] = current_values



                file.seek(0)
                file.truncate()
                json.dump(data, file)





def add_activity(valueslist):
    var = valueslist.get()
    current_values = list(valueslist["values"])
    if var not in current_values and var:
        current_values.append(var)
        valueslist["values"] = current_values
        with open("activities.json", 'r+') as file:
            data = json.load(file)
            data["Activities"][var] = 0
            file.seek(0)
            file.truncate()
            json.dump(data, file)





#Display activities.json using matplotlib
matplotlib.use('TkAgg')




#Elementos en el frame y funciones
activities = ttk.Combobox(timetracker, width = 27, background="black", foreground="white")
timee = Label(timetracker, text="00:00", font=("Consolas", 40, "bold"), fg="white")
start = Button(timetracker, text="Start", font=("Consolas", 10, "bold"), command=lambda: startt(timee, start, activities), fg="black")
reset_button = Button(timetracker, text="Reset", font=("Consolas", 10, "bold"), command=lambda: reset(timee, start, activities), fg="black")
delete_button = Button(timetracker, text="Delete Activity", command=lambda: delete_activity(activities), font=("Consolas", 10, "bold"), fg="black")


add_activity_button = Button(timetracker, text="Add activity", command=lambda: add_activity(activities), font=("Consolas", 10, "bold"), fg="black")

#Spotify, youtube, and webrowser
#Spotify OAuth
sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id="CLIENT ID",
                                                   client_secret="CLIENT SECRET",
                                                   redirect_uri="https://genius.com/Death-flesh-and-the-power-it-holds-lyrics",
                                                   scope="user-modify-playback-state user-read-playback-state"))

#Play song from name
def spotiplay(entrybox):
    song_name = entrybox.get()
    devices = sp.devices()
    device_id = devices['devices'][0]['id'] if devices['devices'] else None
    result = sp.search(q=song_name, type='track', limit=1)
    tracks = result['tracks']['items']
    if tracks:
        sp.start_playback(device_id=device_id, uris=["spotify:track:" + tracks[0]['id']])

def playyoutube(entrybox):
    var = entrybox.get()
    if var == "":
       pass
    else:
        var = var.replace(" ", "+")
        webbrowser.open("https://www.youtube.com/results?search_query=" + var)





#Frame
web_frame = Frame(root)
web_frame_title = Label(web_frame, text="Search Songs or Youtube", font=("Helvetica", 20, "bold"))
entry_box = Entry(web_frame, highlightcolor="white", highlightbackground="white", highlightthickness=1)
spotify_button = Button(web_frame, text="Play Song", font=("Consolas", 10), command=lambda: spotiplay(entry_box), fg="black")
youtube_button = Button(web_frame, text="Search Youtube", font=("Consolas", 10), command=lambda: playyoutube(entry_box), fg="black")

web_frame.pack()
web_frame_title.grid(row=0, column=0, columnspan=2, padx=20, pady=20, sticky="ew")
entry_box.grid(row=1, column=0, columnspan=2, padx=10, pady=10)
spotify_button.grid(row=2, column=0)
youtube_button.grid(row=2, column=1)
web_frame.place(relx=0.70, rely=0.10)



#Cuando la ventana cargue, añadir actividades al combobox del json
with open("activities.json", "r") as file:
    data = json.load(file)
    data = list(data["Activities"])
    activities["values"] = data

Title.pack()
timee.grid(row=0, column=0, columnspan=2)
start.grid(row=1, column=0, columnspan=1)
reset_button.grid(row=1, column=1, columnspan=1)
activities.grid(row=2, column=0, columnspan=2)
add_activity_button.grid(row=3, column=0, columnspan=1)
delete_button.grid(row=3, column=1, columnspan=1)



timetracker.place(relx=0.15, rely=0.1)

root.mainloop()


