echelleMainWindow is a GUI that will determine the orders and 5 wavelengths within each order, evenly spaced from minimum to maximum, based on the supplied information, and write the information to the specified ZEMAX file.  The wavelengths are written to the multi-configuration editor.  The format is

Operand 1: Blank
Operand 2: Order number
Operand 3: Blank
Operand 4: wavelength 1
Operand 5: wavelength 2
Operand 6: wavelength 3
Operand 7: wavelength 4
Operand 8: wavelength 5

If fewer than 8 operands are present, enough operands are inserted to increase it to 8.  If more than 8 operands are present, the above information is written to the first 8 operands.  That means is you have information you do not want overwritten, put it after Operand 8.

The GUI is based on PyQT4 and uses the PyZDDE toolbox.  The specified ZEMAX file MUST be open in ZEMAX for PyZDDE to communicate with the file.  To push the data to ZEMAX, you must setup ZEMAX to accept data from extensions (Setup -> Project Preferences -> Editors -> Check the 'Allow Extensions to Push Lenses' box.)  

***
Be sure to save work before using this program.  If current work is not saved it WILL be overwritten.  This is due to how ZEMAX sets up communication.  A copy of the most current lens file (most current save) is made, altered, and pushed to the ZEMAX GUI.
***

***
Prior to initial use, you must specify  where PyZDDE is saved in echelleMainWindow.pyw.
***

#### License:
[MIT License] (http://opensource.org/licenses/MIT)

