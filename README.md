# thorcam-zaber
To control a Thorlabs Zelux camera and Zaber linear stage

Step 1 : Run `angle_capture`  
Step 2 : Run `save_pos` to generate translation array  
Step 3 : Run `visualize_frames.py` with custom frame numbers (like 1,1,0,20,...80,90) to observe frames. Edit the pixel range in line 34 to capture just the path of the reflected beam. 
Step 3 : Do `extract_intensity` with sliding window to get 
         sum of normalized pixel values. This rejects stray reflections.
         (Check with `visualize` first)  
         - in line 131 - select the x-range of window.
Step 4 : Step through `fresnel_calibration.ipynb` to find middle spot, then fit fresnel.  
         - Pay attention to np.flip()  
Step 5 : To get precise angles vs stage positions - run `angle-calibration.ipynb` 