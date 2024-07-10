from imu_sensor import imu_sensor

import sys
import numpy as np
from PyQt5 import QtWidgets, QtCore, QtGui
from PyQt5.QtWidgets import QVBoxLayout, QHBoxLayout
from PyQt5.QtWidgets import QLabel, QPushButton

import pyqtgraph as pg
import pyqtgraph.opengl as gl

class plotPose(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.isIMUinitialized = False
        self.initUI()

    def initIMU(self, port:str, baudrate:int):
        # Ubuntu: port = '/dev/ttyUSB0'
        # Windows: port = 'COM5'
        # baudrate = 115200
        self.imu = imu_sensor()
        self.imu.connect(port, baudrate)

        self.imu.set_output_gyro_mode(0)
        self.imu.set_output_accelerator_mode(0)
        self.imu.set_output_magnetic(0)
        self.imu.set_output_distance(1)
        self.imu.set_output_temperature(0)
        self.imu.set_output_timestamp(0)

        self.imu.reset_accumulated_pose()

        self.isIMUinitialized = True

    def initUI(self):
        self.setGeometry(100, 100, 800, 600)
        self.view = gl.GLViewWidget()
        self.view.opts['distance'] = 10
        
        self.layout = QVBoxLayout()
        self.layout.addWidget(self.view)
        self.setLayout(self.layout)

        self.color = np.array([[0, 0, 1, 1]])
        for i in range(1, 5000):
            self.color = np.append(self.color, [[i/5000, 0, (5000-i)/5000, 1]], axis=0)
        print(self.color)
        self.poses = np.array([[0, 0, 0]])
        self.points = gl.GLScatterPlotItem(pos=self.poses, color=self.color[0], size=5)
        self.view.addItem(self.points)
        
        self.grid_x = gl.GLGridItem()
        self.grid_y = gl.GLGridItem()
        self.grid_z = gl.GLGridItem()
        self.grid_x.rotate(90, 0, 1, 0)
        self.grid_y.rotate(90, 1, 0, 0)
        

        self.view.addItem(self.grid_x)
        self.view.addItem(self.grid_y)
        self.view.addItem(self.grid_z)

        


        self.timer = QtCore.QTimer()
        self.timer.timeout.connect(self.update)
        self.timer.start(10)

    def update(self):
        if not self.isIMUinitialized:
            return
        
        data = self.imu.get_data()
        if len(data) == 0:
            return
        
        new_pos = np.array([[data['poseX'], data['poseY'], data['poseZ']]])
        self.poses = np.append(self.poses, new_pos, axis=0)
        if self.poses.shape[0] > 5000:
            self.poses = self.poses[-5000:]
        self.points.setData(pos=self.poses, color=self.color[len(self.poses), :], size=5)

        
        print(data)

if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    window = plotPose()
    window.initIMU('/dev/ttyUSB0', 115200)
    window.show()
    sys.exit(app.exec_())