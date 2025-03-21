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

    motor_1.move_by()
    time.sleep(1)
    motor_1.stop()
    