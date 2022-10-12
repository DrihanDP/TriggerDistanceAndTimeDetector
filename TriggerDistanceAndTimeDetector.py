import tkinter
from tkinter import END, filedialog

mainWindow = tkinter.Tk()


# window settings
results = tkinter.Text(mainWindow, height=18, width=40, state='normal')
results.grid(row=1, column=1, sticky='nswe', rowspan=1)
results.config(border=2, relief='sunken')
# get file
input_file = filedialog.askopenfilename(title="Search", filetypes=(("ASC File", "*.asc"), ("all files", "*.*")))
# variables
trigger = False
last_trig_distance = ""
last_trig_time = ""
trig_distances = []
trig_time = []
no_trigger_duplicate_list = []
real_trig_distances = []
results_list = []
speed = 0
speed100 = False
time_trigger = False
#open file
with open(input_file) as file:
    line = file.readlines()

for data in line:
    #split data and remove blank data
    splitLine = [x for x in data.split(" ") if x != ""]
    # check if 'Trigger' has been activated
    if splitLine[2] == "302":
        speed_bit = splitLine[10:12]
        speedJoined = "".join(speed_bit)
        speed = int(speedJoined, 16) * 0.01 * 1.852
        if speed > 100:
            speed100 = True
    # checking ID 303 to see if trigger/event marker has been activated
    if splitLine[2] == "303":
        if splitLine[13].strip("\n") != "01" and splitLine[13].strip("\n") != "03" and splitLine[13].strip("\n") != "33" and splitLine[13].strip("\n") != "35":
            trigger = True
    if trigger == True and speed100 == True:
        if splitLine[2] == "304":
            if last_trig_distance == "":
                last_trig_distance = splitLine[6:10]
            # check if the current distance is equal to the previous distance (indicates trigger stop has finished)
            elif trigger == True and speed < 0.1:
                # TODO change this to convert straight away and then retrain
                if splitLine[6:10] == ['00', '00', '00', '00']:
                    continue
                else:
                    # append to list and 'reset' trigger status
                    trig_distances.append(last_trig_distance)
                    last_trig_distance = ""
                    trigger = False
                    speed100 = False
                    time_trigger = True
            else:
                last_trig_distance = splitLine[6:10]
    if splitLine[2] == "305":
        if time_trigger == True:
            trig_time.append(splitLine[10:12])
            time_trigger = False
    else:
        continue

results_list.append("You may need to press off of the window")
results_list.append("to be able to copy and paste\n")
results_list.append("I would recommend checking the first and last values, and a few in the middle\n")
results_list.append("Trigger distance:")
# gets rid of duplicate data
for i in trig_distances:
    if i not in no_trigger_duplicate_list:
        no_trigger_duplicate_list.append(i)

# converts hex to decimal distance
for j in no_trigger_duplicate_list:
    joined = "".join(j)
    joinedConverted = int(joined, 16)
    distance = joinedConverted * 0.000078125
    rounded_distance = round(distance, 3)
    if rounded_distance < 10:
        continue
    else:
        results_list.append(str(rounded_distance))

results_list.append("\n")
results_list.append("Time")

for m in trig_time:
    joined = "".join(m)
    joinedConverted = int(joined, 16)
    time = joinedConverted * 0.01
    rounded_time = round(time, 3)
    results_list.append(str(rounded_time))

results = tkinter.Text(mainWindow, height=18, width=40, state='normal')
results.grid(row=1, column=1, sticky='nswe', rowspan=1)
results.config(border=2, relief='sunken')

for m in results_list:
    results.insert(END, m + '\n')

mainWindow.mainloop()
# P:\Testing\Projects\VBSS - M9\Test Files\Trigger tests - 1.10.1687\Run 1\Converted_PCAN_USBBUS1_1.trc_08042022-1102.asc
