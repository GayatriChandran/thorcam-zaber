#!/usr/bin/env python

"""
To control Zaber + Thorcam and get stage position-vs-BFP image data. From this we can estimate the incident angle corresponding to each position of the stage. 

Gayatri 09/2024

"""

from zaber_motion import Units
from zaber_motion.ascii import Connection
import numpy as np
from thorlabs_tsi_sdk.tl_camera import TLCameraSDK, OPERATION_MODE
import matplotlib.pyplot as plt
import time
import sys

progress_bar = "###\n"
    

def initalize_stage(stage):
    stage.enable_alerts()
    device_list = stage.detect_devices()
    print("Found {} devices".format(len(device_list)))
    device = device_list[1]
    stage_axis = device.get_axis(1)
    # if not axis.is_homed():
    #   axis.home()
    return stage_axis

def initialize_camera(cam_obj):
    cam_obj = sdk.open_camera(available_cameras[0])
    cam_obj.exposure_time_us = 10000  # set exposure to 11 ms
    cam_obj.frames_per_trigger_zero_for_unlimited = 0  # start camera in continuous mode
    cam_obj.image_poll_timeout_ms = 1000  # 1 second polling timeout


def get_frame(cam):
    cam.issue_software_trigger()
    frame = cam.get_pending_frame_or_null()


try:
    # if on Windows, use the provided setup script to add the DLLs folder to the PATH
    from windows_setup import configure_path
    configure_path()
except ImportError:
    configure_path = None

if __name__ == "__main__":
    
    # Stage positions to sweep through
    start_pos = 2.300                                     # Input start wavelength (nm) for sweep
    end_pos = 2.800                                       # Input end wavelength (nm)

    translation = np.arange(start_pos,end_pos,0.1)
    
    # Initialize the stage and camera

    with [TLCameraSDK(), Connection.open_serial_port("COM4")] as [sdk,connection]:

        # connection = Connection.open_serial_port("COM4")        # For the stage
        axis = initalize_stage(connection)
        axis.move_absolute(2.3, Units.LENGTH_MILLIMETRES)       # Move stage to safe position

        # Initialize the camera

        # sdk = TLCameraSDK()                                     # For Thorcam
        available_cameras = sdk.discover_available_cameras()
        if len(available_cameras) < 1:
            print("no cameras detected")

        with sdk.open_camera(available_cameras[0]) as camera:
            
            initialize_camera(camera)

            # Get ready

            
            frames_counted = 0

            # Begin acquisition
            
            for i in range(np.size(translation)):        

                axis.move_absolute(i, Units.LENGTH_MILLIMETRES)
                for l in progress_bar:
                    sys.stdout.write(l)
                    sys.stdout.flush()
                    time.sleep(0.5)                                                # Wait for user to get ready

                camera.arm(2)
                camera.issue_software_trigger()
                print("Position :", i, '\n')


                
                frame = camera.get_pending_frame_or_null()
                if frame is None:
                    raise TimeoutError("Timeout was reached while polling for a frame, program will now exit")
                image_data = frame.image_buffer
                print(len(image_data))

                frames_counted += 1

                camera.disarm()

                time.sleep(0.2)
                print('Measured ! \n')


        
        
        # connection.close()

