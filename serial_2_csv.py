##############
# SERIAL2CSV #
####################################################################################
# This program records .csv rows of numerical data streamed via serial as ASCII
# strings (eg "<float>,<float,<float>") until commanded to stop by the user.
# When recording is stopped the .csv file is created: a plot of the recorded data
# is then displayed and saved as a .png file if the user has selected to do so.
#
# Things that are not checked, ie up to the user to get right, are:
#
# 1) Up to the user to make sure the recorded input is actually rows of numerical
#    .csv data (so make sure your serial source is correctly set up!)
# 2) Serial2CSV does not check that the number of columns entered equals the number
#    of values in the recorded rows.
#
# FLAGS:
# -h, --help    Display (this) help message. NOTE: program does not run when
#               these help flags are included.
# -p, --port    Set port. The following argument should be the name of the
#               serial port.
# -b, --baud    Set baud rate. The following argument should be an int.
####################################################################################
# Author: Daniel Babekuhl.
####################################################################################

import serial
import time
import csv
import pandas as pd
import matplotlib.pyplot as plt
import os
import signal
import sys

#################
# SYSTEM CONFIG #
#################
baud_rate = 9600
serial_port = '/dev/ttyACM0'

#############
# VARIABLES #
#############
ser = 0 # read from serial input
dataset = [] # raw data from serial port
filename = ''
columns = ''
user_input = '_'
printData_realtime = False
save_plot = False
sigint_n = 0
plot_filename = ''
row_count = 0
dir_char = '/'
directory_path = ''

#############
# FUNCTIONS #
#############

# Handle SIGINT (Ctrl-C from user)
def SIGINT_handler(signum, frame):
    global sigint_n
    sigint_n += 1

# Connect to serial stream
def serial_sync():
    global ser, serial_port, baud_rate
    # READ FROM SERIAL PORT
    ser = serial.Serial(serial_port, baud_rate, timeout=1)
    # DISCARD BEGINNING OF SIGNAL
    top = 50
    top_i = 0
    while(top_i < top):
        arduinoData = ser.readline()
        top_i += 1

# Read from serial
def read_serial_in():
    global data
    data = ser.readline()[:-2] # remove '/r/n' bytes from end of serial inputs
    data_str = data.decode('ASCII') + '\n'
    dataset.append(data_str)
    if printData_realtime:
        print('Row %d) %s' % (row_count, data_str), end='')

# save and plot file when user ends recording
def save_plot_data():
    global save_plot, plot_filename, filename
    # save file
    file_object = open(filename, 'a')
    file_object.write(columns)
    for row in dataset:
        file_object.write(row)
    file_object.close()
    # CREATE PLOT
    # import data from saved file
    csv_df = pd.read_csv(filename, error_bad_lines=False)
    title = filename.split('/')[-1]
    # create plot
    fig = plt.figure(figsize=(20,7))
    ax = fig.add_subplot(111)
    fig_title = title[:-3]+'png'
    ax.set_title(fig_title, fontsize=15, fontweight='bold')
    for column in csv_df.columns:
        ax.plot(csv_df[column],label=column)
    ax.legend()
    # save plot
    if save_plot:
        fig.savefig(filename[:-3] + 'png')
        print("\n---------------------------------------------------")
        print("%s created." % (filename[:-3] + '.png'))
    # message user.
    print("---------------------------------------------------")
    print("%s created (%d rows)." % (filename, len(dataset)))
    print("¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯")
    print("\nPress Ctrl-C again to exit.\n")
    plt.show()

###########################
# PRINT TITLE/DESCRIPTION #
###########################

print("\n##################")
print("#  SERIAL 2 CSV  #")
print("##################")

#################
# PROCESS FLAGS #
#################

# -p or --port (set port)
for i, input_element in enumerate(sys.argv):
    if (input_element == '-p') or (input_element == '--port'):
        serial_port = sys.argv[i+1]
        ser = serial.Serial(serial_port, baud_rate, timeout=1)

# -b or --baud (set baud rate)
for i, input_element in enumerate(sys.argv):
    if (input_element == '-b') or (input_element == '--baud'):
        baud_rate = int(sys.argv[i+1])
        ser = serial.Serial(serial_port, baud_rate, timeout=1)

# -h or --help
for input_element in sys.argv:
    if (input_element == '-h') or (input_element == '--help'):
        print('\n' +\
                'This program records .csv rows of numerical data streamed via serial as ASCII\n' + \
                'strings (eg "<float>,<float,<float>") until commanded to stop by the user.\n' + \
                'When recording is stopped the .csv file is created: a plot of the recorded data\n' + \
                'is then displayed and saved as a .png file if the user has selected to do so.\n' + \
                '\n' +\
                'Things that are not checked, ie up to the user to get right, are:\n' + \
                '\n' + \
                '1) Up to the user to make sure the recorded input is actually rows of numerical\n' +\
                '   .csv data (so make sure your serial source is correctly set up!)\n' + \
                '2) Serial2CSV does not check that the number of columns entered equals the number\n' +\
                '   of values in the recorded rows.\n' + \
                '\n' +\
                'FLAGS:\n'+\
                '-h, --help    Display (this) help message. NOTE: program does not run when\n' +\
                '              these help flags are included,\n' +\
                '-p, --port    Set port. The following argument should be the name of the\n' +\
                '              serial port.\n' +\
                '-b, --baud    Set baud rate. The following argument should be an int.\n' +\
                '\n' +\
                'Author: Daniel Babekuhl.\n'

                 )

        quit()
else:
    print("\nFor help run: `$ python3 serial_2_csv.py -h` or `$ python3 serial_2_csv.py --help`" )
print('\nCURRENT SETTINGS:')
print('* Serial port: %s' % serial_port)
print('* Baud rate: %d' % baud_rate)

##############
# INITIALISE #
##############

# detect Windows operating system and adjust for different command line
if sys.platform in ['Win32', 'Win64']:
    dir_char = '\\'

########################
# GET CONFIG FROM USER #
########################

# FILENAMES
filename = input("\nEnter name/path of csv, eg, '~/data/my_file.csv': ")
#check if user input is a directory
if filename.find(dir_char) != -1:
    # check if directory exists/create directory
    path_dirs = filename.split(dir_char)[:-1]
    directory_path = dir_char.join(path_dirs)
    if not os.path.exists(directory_path):
        if input('\nDirectory does not exist - create it? y/n: ')[0].lower() == 'y':
            os.mkdir(directory_path)
            print('Directory %s created.' % (directory_path + dir_char))
        else:
            print('\nPlease try again with an existing directory. Goodbye.\n')
            quit()
# check if file exists/create file
if not os.path.exists(filename):
    print("\n---- Using filename: %s ----\n" % filename)
else:
    user_input = input("That file already exists - replace? y/n: ")
    if user_input.lower()[0] == 'y':
        os.remove(filename)
        print("\n---- Using filename: %s ----\n" % filename)
    else:
        print("\nPlease try again with a different filename. Goodbye.\n")
        time.sleep(1)
        quit()

# get column names from user
user_input = input('Enter column names or enter if done: ')
while user_input != '':
    columns = columns + user_input + ','
    user_input = input('Enter column names or enter if done: ')
if columns == '':
    print("No columns named added.")
else:
    columns = columns[:-1] + '\n'
    print("\n---- Column names: %s ----" % columns[:-1].replace(',', ', '))

# get print status from user
user_input = input("\nPrint serial values to terminal in real-time? y/n: ")
if user_input.lower()[0] == 'y':
    printData_realtime = True
    print("Serial input will be printed.\n")
else:
    printData_realtime = False
    print("Serial values will not be printed.\n")

# ask user about saving plot
user_input = input("Save data plot as a .png file? y/n: ")
if user_input.lower()[0] == 'y':
    plot_filename = filename[:-3]+'png'
    if not os.path.exists(plot_filename):
        save_plot = True
    else:
        user_input = input("The .png for your chosen filename already exists - replace it? y/n: ")
        if user_input.lower()[0] == 'y':
            os.remove(plot_filename)
            print("\n---- %s will be replaced. ----" % plot_filename)
            save_plot = True
        else:
            print(".png of plot will not be saved.")
            save_plot = False
else:
    save_plot = False
    print("Plot will not be saved.")
print("\nThe following files will be created:\n")
print("---- %s ----" % filename)
if save_plot:
    print("---- %s ----" % plot_filename)

# message user
time.sleep(1)
print("\nStarting . . . ")

# setup SIGINT_handler
signal.signal(signal.SIGINT, SIGINT_handler)

#######
# RUN #
#######

# record streaming data
serial_sync()
print("\nRunning.\n\nPress Ctrl-C to finish recording data, save file(s) and view plot.")

print("\nRows recorded:")
while(True):
    read_serial_in()
    row_count += 1
    if not printData_realtime:
        print("%d                " % row_count, end='\r')
    # monitor for keyboard Ctrl-C from user
    if sigint_n == 1:
        break

# save files, display plot
save_plot_data()
