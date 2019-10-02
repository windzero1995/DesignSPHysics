#!/usr/bin/env python3.7
# -*- coding: utf-8 -*-
'''DesignSPHysics Run Dialog'''

from PySide import QtCore, QtGui

from mod.translation_tools import __


class RunDialog(QtGui.QDialog):
    ''' Defines run window dialog '''

    WINDOW_TITLE_TEMPLATE = __("DualSPHysics Simulation: {}%")
    PARTICLES_OUT_TEMPLATE = __("Total particles out: {}")
    ETA_TEMPLATE = __("Estimated time to complete simulation: {}")

    cancelled = QtCore.Signal()

    def __init__(self, case_name: str, processor: str, number_of_particles: int):
        super(RunDialog, self).__init__()

        self.run_watcher = QtCore.QFileSystemWatcher()
        # Title and size
        self.setModal(False)
        self.setWindowTitle(__("DualSPHysics Simulation: {}%").format("0"))
        self.run_dialog_layout = QtGui.QVBoxLayout()

        # Information GroupBox
        self.run_group = QtGui.QGroupBox(__("Simulation Data"))
        self.run_group_layout = QtGui.QVBoxLayout()

        self.run_group_label_case = QtGui.QLabel(__("Case name: {}").format(case_name))
        self.run_group_label_proc = QtGui.QLabel(__("Simulation processor: {}").format(processor))
        self.run_group_label_part = QtGui.QLabel(__("Number of particles: ").format(number_of_particles))
        self.run_group_label_partsout = QtGui.QLabel(self.PARTICLES_OUT_TEMPLATE.format(0))
        self.run_group_label_eta = QtGui.QLabel(self)
        self.run_group_label_eta.setText(self.ETA_TEMPLATE.format("Calculating..."))
        self.run_group_label_completed = QtGui.QLabel("<b>{}</b>".format(__("Simulation is complete.")))
        self.run_group_label_completed.setVisible(False)

        self.run_group_layout.addWidget(self.run_group_label_case)
        self.run_group_layout.addWidget(self.run_group_label_proc)
        self.run_group_layout.addWidget(self.run_group_label_part)
        self.run_group_layout.addWidget(self.run_group_label_partsout)
        self.run_group_layout.addWidget(self.run_group_label_eta)
        self.run_group_layout.addWidget(self.run_group_label_completed)
        self.run_group_layout.addStretch(1)

        self.run_group.setLayout(self.run_group_layout)

        # Progress Bar
        self.run_progbar_layout = QtGui.QHBoxLayout()
        self.run_progbar_bar = QtGui.QProgressBar()
        self.run_progbar_bar.setRange(0, 100)
        self.run_progbar_bar.setTextVisible(False)
        self.run_progbar_layout.addWidget(self.run_progbar_bar)

        # Buttons
        self.run_button_layout = QtGui.QHBoxLayout()
        self.run_button_details = QtGui.QPushButton(__("Details"))
        self.run_button_cancel = QtGui.QPushButton(__("Cancel Simulation"))
        self.run_button_layout.addStretch(1)
        self.run_button_layout.addWidget(self.run_button_details)
        self.run_button_layout.addWidget(self.run_button_cancel)

        self.run_dialog_layout.addWidget(self.run_group)
        self.run_dialog_layout.addLayout(self.run_progbar_layout)
        self.run_dialog_layout.addLayout(self.run_button_layout)

        self.setLayout(self.run_dialog_layout)

        # Defines run details
        self.run_details = QtGui.QDialog()
        self.run_details.setMinimumWidth(650)
        self.run_details.setModal(False)
        self.run_details.setWindowTitle(__("Simulation details"))
        self.run_details_layout = QtGui.QVBoxLayout()

        self.run_details_text = QtGui.QTextEdit()
        self.run_details_text.setReadOnly(True)
        self.run_details_layout.addWidget(self.run_details_text)

        self.run_button_cancel.clicked.connect(self.cancelled.emit)

        self.run_details.setLayout(self.run_details_layout)

    def hide_all(self) -> None:
        ''' Hides both the run details and this dialog. '''
        self.run_details.hide()
        self.hide()

    def set_value(self, value: int) -> None:
        ''' Sets the value for the run dialog progress bar. '''
        self.run_progbar_bar.setvalue(value)

    def run_update(self, percentage: float, particles_out: int, estimated_time: str) -> None:
        ''' Updates the run dialog with information about the execution. '''
        self.setWindowTitle(self.WINDOW_TITLE_TEMPLATE.format(percentage))
        self.set_value(percentage)
        self.run_group_label_partsout.setText(self.PARTICLES_OUT_TEMPLATE.format(str(particles_out)))
        if estimated_time:
            self.run_group_label_eta.setText(self.ETA_TEMPLATE.format(estimated_time))

    def run_complete(self) -> None:
        ''' Modifies the dialog accordingly with a complete simulation. '''
        self.setWindowTitle(__("DualSPHysics Simulation: Complete"))
        self.run_progbar_bar.setValue(100)
        self.run_button_cancel.setText(__("Close"))
        self.run_group_label_completed.setVisible(True)

    def toggle_run_details(self) -> None:
        ''' Toggles the run details dialog panel. '''
        self.run_details.setHidden(not self.run_details.isVisible())
        self.run_details.move(self.x() - self.run_details.width() - 15, self.y())

    def set_detail_text(self, details: str) -> None:
        ''' Sets the details text contents and scrolls it to the bottom. '''
        self.run_details_text.setText(details)
        self.run_details_text.moveCursor(QtGui.QTextCursor.End)
