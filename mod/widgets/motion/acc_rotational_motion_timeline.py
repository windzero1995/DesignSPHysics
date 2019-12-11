#!/usr/bin/env python3.7
# -*- coding: utf-8 -*-
"""DesignSPHysics Accelerated Rotation Motion widget"""

from PySide import QtCore, QtGui

from mod.translation_tools import __
from mod.gui_tools import get_icon
from mod.stdout_tools import debug

from mod.dataobjects.motion.acc_rot_motion import AccRotMotion


class AccRotationalMotionTimeline(QtGui.QWidget):
    """ An accelerated rotational motion graphical representation for a table-based timeline """

    changed = QtCore.Signal(int, AccRotMotion)
    deleted = QtCore.Signal(int, AccRotMotion)
    order_up = QtCore.Signal(int)
    order_down = QtCore.Signal(int)

    def __init__(self, index, acc_rot_motion, parent=None):
        if not isinstance(acc_rot_motion, AccRotMotion):
            raise TypeError("You tried to spawn an accelerated rotational "
                            "motion widget in the timeline with a wrong object")
        if acc_rot_motion is None:
            raise TypeError("You tried to spawn an accelerated rotational "
                            "motion widget in the timeline without a motion object")
        super().__init__(parent=parent)

        self.index = index
        self.main_layout = QtGui.QHBoxLayout()
        self.main_layout.setContentsMargins(10, 0, 10, 0)
        self.label = QtGui.QLabel("Accelerated \nRotational \nMotion ")
        self.label.setMinimumWidth(75)
        self.vel_and_acc_layout = QtGui.QVBoxLayout()
        self.vel_layout = QtGui.QHBoxLayout()
        self.acc_layout = QtGui.QHBoxLayout()
        self.velocity_label = QtGui.QLabel("Vel: ")
        self.velocity_input = QtGui.QLineEdit()
        self.velocity_input.setStyleSheet("width: 5px;")
        self.acceleration_label = QtGui.QLabel("Acc: ")
        self.acceleration_input = QtGui.QLineEdit()
        self.acceleration_input.setStyleSheet("width: 5px;")
        self.axis_label = QtGui.QLabel(
            "Axis 1 (X, Y, Z): \n\nAxis 2 (X, Y, Z): ")
        self.axis_layout = QtGui.QVBoxLayout()
        self.axis_first_row_layout = QtGui.QHBoxLayout()
        self.axis_second_row_layout = QtGui.QHBoxLayout()
        self.x1_input = QtGui.QLineEdit()
        self.x1_input.setStyleSheet("width: 5px;")
        self.y1_input = QtGui.QLineEdit()
        self.y1_input.setStyleSheet("width: 5px;")
        self.z1_input = QtGui.QLineEdit()
        self.z1_input.setStyleSheet("width: 5px;")
        self.x2_input = QtGui.QLineEdit()
        self.x2_input.setStyleSheet("width: 5px;")
        self.y2_input = QtGui.QLineEdit()
        self.y2_input.setStyleSheet("width: 5px;")
        self.z2_input = QtGui.QLineEdit()
        self.z2_input.setStyleSheet("width: 5px;")
        self.time_label = QtGui.QLabel(__("Duration (s): "))
        self.time_input = QtGui.QLineEdit()
        self.time_input.setStyleSheet("width: 5px;")
        self.delete_button = QtGui.QPushButton(
            get_icon("trash.png"), None)
        self.order_button_layout = QtGui.QVBoxLayout()
        self.order_button_layout.setContentsMargins(0, 0, 0, 0)
        self.order_button_layout.setSpacing(0)
        self.order_up_button = QtGui.QPushButton(
            get_icon("up_arrow.png"), None)
        self.order_down_button = QtGui.QPushButton(
            get_icon("down_arrow.png"), None)

        self.vel_layout.addWidget(self.velocity_label)
        self.vel_layout.addWidget(self.velocity_input)
        self.acc_layout.addWidget(self.acceleration_label)
        self.acc_layout.addWidget(self.acceleration_input)
        self.vel_and_acc_layout.addLayout(self.vel_layout)
        self.vel_and_acc_layout.addLayout(self.acc_layout)
        self.order_button_layout.addWidget(self.order_up_button)
        self.order_button_layout.addWidget(self.order_down_button)
        self.main_layout.addWidget(self.label)
        self.main_layout.addLayout(self.vel_and_acc_layout)
        self.main_layout.addWidget(self.axis_label)
        self.axis_first_row_layout.addWidget(self.x1_input)
        self.axis_first_row_layout.addWidget(self.y1_input)
        self.axis_first_row_layout.addWidget(self.z1_input)
        self.axis_second_row_layout.addWidget(self.x2_input)
        self.axis_second_row_layout.addWidget(self.y2_input)
        self.axis_second_row_layout.addWidget(self.z2_input)
        self.axis_layout.addLayout(self.axis_first_row_layout)
        self.axis_layout.addLayout(self.axis_second_row_layout)
        self.main_layout.addLayout(self.axis_layout)
        self.main_layout.addStretch(1)
        self.main_layout.addWidget(self.time_label)
        self.main_layout.addWidget(self.time_input)
        self.main_layout.addWidget(self.delete_button)
        self.main_layout.addLayout(self.order_button_layout)

        self.setLayout(self.main_layout)
        self.fill_values(acc_rot_motion)
        self._init_connections()

    def fill_values(self, acc_rot_motion):
        """ Fills the values from the data structure to the widget. """
        self.x1_input.setText(str(acc_rot_motion.axis1[0]))
        self.y1_input.setText(str(acc_rot_motion.axis1[1]))
        self.z1_input.setText(str(acc_rot_motion.axis1[2]))
        self.x2_input.setText(str(acc_rot_motion.axis2[0]))
        self.y2_input.setText(str(acc_rot_motion.axis2[1]))
        self.z2_input.setText(str(acc_rot_motion.axis2[2]))
        self.velocity_input.setText(str(acc_rot_motion.ang_vel))
        self.acceleration_input.setText(str(acc_rot_motion.ang_acc))
        self.time_input.setText(str(acc_rot_motion.duration))

    def _init_connections(self):
        self.x1_input.textChanged.connect(self.on_change)
        self.y1_input.textChanged.connect(self.on_change)
        self.z1_input.textChanged.connect(self.on_change)
        self.x2_input.textChanged.connect(self.on_change)
        self.y2_input.textChanged.connect(self.on_change)
        self.z2_input.textChanged.connect(self.on_change)
        self.velocity_input.textChanged.connect(self.on_change)
        self.acceleration_input.textChanged.connect(self.on_change)
        self.time_input.textChanged.connect(self.on_change)
        self.delete_button.clicked.connect(self.on_delete)
        self.order_up_button.clicked.connect(self.on_order_up)
        self.order_down_button.clicked.connect(self.on_order_down)

    def disable_order_up_button(self):
        """ Disables the order up button. """
        self.order_up_button.setEnabled(False)

    def disable_order_down_button(self):
        """ Disables the order down button. """
        self.order_down_button.setEnabled(False)

    def on_order_up(self):
        """ Reacts to the order up button being pressed. """
        self.order_up.emit(self.index)

    def on_order_down(self):
        """ Reacts to the order down button being pressed. """
        self.order_down.emit(self.index)

    def on_change(self):
        """ Reacts to any input change sanitizing it and firing a signal with the appropriate data object. """
        self._sanitize_input()
        try:
            self.changed.emit(self.index, self.construct_motion_object())
        except ValueError:
            debug("Introduced an invalid value for a float number.")

    def construct_motion_object(self):
        """ Constructs an AccRotMotion from the data on the widget. """
        return AccRotMotion(
            ang_vel=float(self.velocity_input.text()),
            ang_acc=float(self.acceleration_input.text()),
            axis1=[float(self.x1_input.text()),
                   float(self.y1_input.text()),
                   float(self.z1_input.text())],
            axis2=[float(self.x2_input.text()),
                   float(self.y2_input.text()),
                   float(self.z2_input.text())],
            duration=float(self.time_input.text()))

    def on_delete(self):
        """ Deletes the currently represented motion object. """
        self.deleted.emit(self.index, self.construct_motion_object())

    def _sanitize_input(self):
        if not self.x1_input.text():
            self.x1_input.setText("0")
        if not self.y1_input.text():
            self.y1_input.setText("0")
        if not self.z1_input.text():
            self.z1_input.setText("0")
        if not self.x2_input.text():
            self.x2_input.setText("0")
        if not self.y2_input.text():
            self.y2_input.setText("0")
        if not self.z2_input.text():
            self.z2_input.setText("0")
        if not self.velocity_input.text():
            self.velocity_input.setText("0")
        if not self.acceleration_input.text():
            self.acceleration_input.setText("0")
        if not self.time_input.text():
            self.time_input.setText("0")

        self.x1_input.setText(self.x1_input.text().replace(",", "."))
        self.y1_input.setText(self.y1_input.text().replace(",", "."))
        self.z1_input.setText(self.z1_input.text().replace(",", "."))
        self.x2_input.setText(self.x2_input.text().replace(",", "."))
        self.y2_input.setText(self.y2_input.text().replace(",", "."))
        self.z2_input.setText(self.z2_input.text().replace(",", "."))
        self.velocity_input.setText(
            self.velocity_input.text().replace(",", "."))
        self.acceleration_input.setText(
            self.acceleration_input.text().replace(",", "."))
        self.time_input.setText(self.time_input.text().replace(",", "."))
