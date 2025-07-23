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
import tifffile as tf

progress_bar = "####\n"
    

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
    
    cam_obj.exposure_time_us = 150000  # set exposure to 11 ms
    cam_obj.frames_per_trigger_zero_for_unlimited = 0  # start camera in continuous mode
    cam_obj.image_poll_timeout_ms = 1000  # 1 second polling timeout
    if cam_obj.gain_range.max > 0:
        db_gain = 2.0
        gain_index = cam_obj.convert_decibels_to_gain(db_gain)
        cam_obj.gain = gain_index
        print(f"Set camera gain to {cam_obj.convert_gain_to_decibels(cam_obj.gain)}")



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
    start_pos = 2.8                                     # Input start wavelength (nm) for sweep
    end_pos = 7.2                                       # Input end wavelength (nm)

    translation = np.arange(start_pos,end_pos,0.05)
    N = np.size(translation)                              # Number of stage positions
    # np.savetxt("pos-01.csv", translation,delimiter = ",")
    # Initialize the stage and camera

    with TLCameraSDK() as sdk:

        with Connection.open_serial_port("COM6") as connection:

            # connection = Connection.open_serial_port("COM4")        # For the stage
            axis = initalize_stage(connection)
            axis.move_absolute(start_pos, Units.LENGTH_MILLIMETRES)       # Move stage to safe position

            # Initialize the camera

            # sdk = TLCameraSDK()                                     # For Thorcam
            available_cameras = sdk.discover_available_cameras()
            if len(available_cameras) < 1:
                print("no cameras detected")
            
            with sdk.open_camera(available_cameras[0]) as camera:
                
                initialize_camera(camera)

                # Get ready
                nd_image_array = np.full((camera.image_height_pixels, camera.image_width_pixels, N), 0, dtype=np.uint8)
                    

                
                frames_counted = 0

                # Begin acquisition
                
                for i in range(N):        

                    axis.move_absolute(translation[i], Units.LENGTH_MILLIMETRES)
                    for l in progress_bar:
                        sys.stdout.write(l)
                        sys.stdout.flush()
                        time.sleep(0.5)                                                # Wait for user to get ready

                    camera.arm(2)
                    camera.issue_software_trigger()
                    print("Position :", translation[i], '\n')


                    
                    frame = camera.get_pending_frame_or_null()
                    if frame is None:
                        raise TimeoutError("Timeout was reached while polling for a frame, program will now exit")
                                       
                    image_buffer_copy = np.copy(frame.image_buffer)
                    numpy_shaped_image = image_buffer_copy.reshape(camera.image_height_pixels, camera.image_width_pixels)
                    nd_image_array[:,:,i] = numpy_shaped_image
                    
                    # tf.imwrite('temp'+str(i)+'.tif', numpy_shaped_image, photometric='minisblack')

                    frames_counted += 1

                    camera.disarm()

                    time.sleep(0.2)
                    print('Measured ! \n')

                np.save('air-07-21-2025-hwp-48.npy', nd_image_array)
        
        
        # connection.close()

