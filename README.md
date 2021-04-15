# serial_2_csv

This program records .csv rows of numerical data streamed via serial as ASCII
strings (eg "<float\>,<float\>,<float\>") until commanded to stop by the user.
When recording is stopped the .csv file is created: a plot of the recorded data
is then displayed and saved as a .png file if the user has selected to do so.

Things that are not checked, ie up to the user to get right, are:

1) Up to the user to make sure the recorded input is actually rows of numerical
    .csv data (so make sure your serial source is correctly set up!)
2) Serial2CSV does not check that the number of columns entered equals the number
    of values in the recorded rows.
<br>
FLAGS:

* -h, --help: Display (this) help message. NOTE: program does not run when
               these help flags are included.
* -p, --port: Set port. The following argument should be the name of the
               serial port.
* -b, --baud: Set baud rate. The following argument should be an int.

Designed to run on Windows, Linux and Mac OS.

Demo video available [here](https://drive.google.com/file/d/1pzinTmadcjk-pOsvbEZNIhMFwyMgMltR/view?usp=sharing).
