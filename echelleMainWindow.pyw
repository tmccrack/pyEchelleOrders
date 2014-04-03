#-------------------------------------------------------------------------------
# Name:     echelleMainWindow.py
# Purpose:  Python based DDE link with ZEMAX server, similar to Matlab based
#           MZDDE toolbox.
# Purpose:  Python GUI to write wavelengths of all orders in a specified range
#           to the multiconfiguration editor in Zemax using the PyZDDE 
# Author:   Tyler McCracken
#
# Created:     4/03/2014
# Copyright:   (c) Tyler McCracken, Yale University, 2014
# Licence:     MIT License
#              This file is subject to the terms and conditions of the MIT License.
#              For further details, please refer to LICENSE.txt
# Revision:    0.1
#-------------------------------------------------------------------------------

import sys
import traceback
import numpy as np
# from PyQt4 import QtGui, uic ### not using pyuic4
from PyQt4 import QtGui
from echelleDesignerWindow import *  # Made from pyuic4

PyZDDEPath = 'NULL'  # Path to PyZDDE

RAD = np.pi / 180.  # degrees to radians

'''
###
# Does not use pyuic4
# Must load .ui file manually
###

class MyWindow(QtGui.QMainWindow):
    def __init__(self):
        super(MyWindow, self).__init__()
        uic.loadUi('echelleDesigner.ui', self)
        self.show()
    
if __name__ == '__main__':
    app = QtGui.QApplication(sys.argv)
    window = MyWindow()
    sys.exit(app.exec_())
    
   
'''
class mainWindow(QtGui.QMainWindow):
    def __init__(self, parent = None):
        QtGui.QWidget.__init__(self, parent)
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        
    def updateClicked(self):
        self.computeAngles()
        self.computeOrders()
        self.ui.textOrderMax.setText(str(self.orderMax))
        self.ui.textOrderMin.setText(str(self.orderMin))
        self.ui.textOrders.setText(str(self.numOrders))
        self.pushToZemax()
        
        
    def selectFileClicked(self):
        self.filename = str(QtGui.QFileDialog.getOpenFileName(self, 'Select ZEMAX file'))
        self.ui.labelFileName.setText(self.filename)       
        
        
    def computeAngles(self):
        """
        Compute angle of incidence (alpha) and angle of diffraction (beta) in radians
        """
        self.alpha = np.double(self.ui.textBlaze.text()) + np.double(self.ui.textInAngle.text())  # angle of incidence
        self.alpha *= RAD
        self.beta = np.double(self.ui.textBlaze.text()) + np.double(self.ui.textInAngle.text())  # angle of diffraction
        self.beta *= RAD
        
        
    def computeOrders(self):
        """
        Compute min and max order, number of orders
        """
        c0 = (1000. / np.double(self.ui.textGroovesMm.text())) * np.cos(np.double(self.ui.textOutAngle.text()) * RAD)
        c1 = c0 * (np.sin(self.alpha) + np.sin(self.beta))
        self.orderMin = np.floor(c1 / np.double(self.ui.textLambdaMax.text()))
        self.orderMax = np.floor(c1 / np.double(self.ui.textLambdaMin.text()))
        self.numOrders = self.orderMax - self.orderMin + 1
        
        m = np.arange(self.orderMin, self.orderMax+1, 1, dtype=np.double)
        lambda_center = c1 / m
        d_lambda = lambda_center / m
        spacing = np.array([-0.5, -0.25, 0.0, 0.25, 0.5])
        self.wavs = lambda_center.reshape(lambda_center.size, 1) * np.ones([1, spacing.size]) + d_lambda.reshape(d_lambda.size, 1) * spacing.reshape(1, spacing.size)
            
            
    def pushToZemax(self):
        # Create a PyZDDE object
        link0 = pyz.PyZDDE()
        
        try:
            # Initiate the DDE link
            status = link0.zDDEInit()   # if status == -1, then zDDEInit failed!
            
            if ~status:
                link0.zLoadFile(self.filename)
                # Size the number of configurations in MCE                
                configInfo = link0.zGetConfig()
            
                # Number configs = number of orders
                if configInfo[1] > self.numOrders:
                    for n in range(int(configInfo[1] - self.numOrders)):
                        link0.zDeleteConfig(configInfo[1]-n)
                elif configInfo[1] < self.numOrders:
                    for n in range(int(self.numOrders - configInfo[1])):
                        link0.zInsertConfig(configInfo[1]+1+n)
                        
                # Check for at least 8 operands
                if configInfo[2] < 8:
                    for n in range(int(8 - configInfo[2])):
                        link0.zInsertMCO(1)
                                       
                # Write wavelengths to Zemax                       
                (m, n) = self.wavs.shape
                for configs in range(m):
                    data = link0.zSetMulticon(m-configs, 2, np.int(self.orderMin+configs), 0, 0, 0, 0, 0)  # Write order number to MCE
        
                    for rows in range(n):
                        data = link0.zSetMulticon(m-configs, rows+4, self.wavs[configs, rows], 0, 0, 0, 0, 0)
                
            else:
                print("DDE link could not be established.")
        
        except Exception, err:
            traceback.print_exc()
        finally:
            link0.zPushLens(0)  # Push updates to Zemax
            link0.zDDEClose()  # Close Zemax link
    

if __name__ == '__main__':
    app = QtGui.QApplication(sys.argv)
    if (PyZDDEPath == 'NULL'):
        window = QtGui.QLabel('Specify PyZDDE path!!')
    else:
        if (PyZDDEPath not in sys.path):
            sys.path.append(PyZDDEPath)
        
        import pyzdde.zdde as pyz
        import pyzdde.zcodes.zemaxoperands as zo # if required. (use pyz.zo to access module functions)
        import pyzdde.zcodes.zemaxbuttons  as zb # if required. (use pyz.zb to access module functions)
        window = mainWindow()
        
    window.show()
    sys.exit(app.exec_())
    
