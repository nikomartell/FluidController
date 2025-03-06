################################################################################
# Copyright © 2019 TRINAMIC Motion Control GmbH & Co. KG
# (now owned by Analog Devices Inc.),
#
# Copyright © 2023 Analog Devices Inc. All Rights Reserved.
# This software is proprietary to Analog Devices, Inc. and its licensors.
################################################################################

import pytrinamic
from pytrinamic.connections import ConnectionManager
from pytrinamic.modules import TMCM3110
import time

pytrinamic.show_info()
connection_manager = ConnectionManager()  # using USB

with connection_manager.connect() as my_interface:
    module = TMCM3110(my_interface)
    motor_0 = module.motors[0]
    motor_1 = module.motors[1]
    motor_2 = module.motors[2]

    # Please be sure not to use a too high current setting for your motor.

    print("Preparing parameters")
    # preparing drive settings
    motor_0.drive_settings.max_current = 4
    motor_0.drive_settings.standby_current = 0
    motor_0.drive_settings.boost_current = 0
    motor_0.drive_settings.microstep_resolution = motor_0.ENUM.microstep_resolution_256_microsteps
    print(motor_0.drive_settings)
    motor_1.drive_settings.max_current = 4
    motor_1.drive_settings.standby_current = 0
    motor_1.drive_settings.boost_current = 0
    motor_1.drive_settings.microstep_resolution = motor_0.ENUM.microstep_resolution_256_microsteps
    print(motor_1.drive_settings)
    motor_2.drive_settings.max_current = 4
    motor_2.drive_settings.standby_current = 0
    motor_2.drive_settings.boost_current = 0
    motor_2.drive_settings.microstep_resolution = motor_0.ENUM.microstep_resolution_256_microsteps
    print(motor_2.drive_settings)

    # preparing linear ramp settings
    motor_0.max_acceleration = 1000
    motor_0.max_velocity = 1000
    motor_1.max_acceleration = 1000
    motor_1.max_velocity = 1000
    motor_2.max_acceleration = 1000
    motor_2.max_velocity = 1000

    motor_0.rotate(1000)
    motor_1.rotate(1000)
    time.sleep(5)
    motor_0.stop()
    motor_1.stop()

    print(motor_0.linear_ramp)    
    print(motor_1.linear_ramp)
    print(motor_2.linear_ramp)
    