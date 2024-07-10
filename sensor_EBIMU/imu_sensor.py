import serial
import time

MODE_EULER = 0
MODE_QUATERNION = 1
MODE_GYROSCOPE_OFF = 0
MODE_GYROSCOPE_ON = 1
MODE_ACCELERATOR_OFF = 0
MODE_ACCELERATOR_ON = 1
MODE_ACCELERATOR_LOCAL_WITHOUT_GRAVITY = 2
MODE_ACCELERATOR_GLOBAL_WITHOUT_GRAVITY = 3
MODE_ACCELERATOR_LOCAL_VELOCITY = 4
MODE_ACCELERATOR_GLOBAL_VELOCITY = 5
MODE_MAGNETIC_OFF = 0
MODE_MAGNETIC_ON = 1
MODE_DISTANCE_OFF = 0
MODE_DISTANCE_LOCAL = 1
MODE_DISTANCE_GLOBAL = 2
MODE_TEMPERATURE_OFF = 0
MODE_TEMPERATURE_ON = 1
MODE_TIMESTAMP_OFF = 0
MODE_TIMESTAMP_ON = 1



class imu_sensor:
    def connect(self, port, baudrate):
        self.ser = serial.Serial(port, baudrate, timeout=1)
        self.reset_imu_default()
       
    def disconnect(self):
        self.reset_imu_default()
        self.ser.close()

    def get_data(self):
        if self.ser.in_waiting > 0:
            data = {}
            string = self.ser.readline().decode('utf-8')[1:-2].split(',')
            
            count = 0
                
            try:
                if self.mode_sof == MODE_EULER:
                    data['Rx'] = float(string[count])
                    data['Ry'] = float(string[count+1])
                    data['Rz'] = float(string[count+2])
                    count += 3
                elif self.mode_sof == MODE_QUATERNION:
                    data['Qw'] = float(string[count])
                    data['Qx'] = float(string[count+1])
                    data['Qy'] = float(string[count+2])
                    data['Qz'] = float(string[count+3])
                    count += 4
            except Exception as e:
                print(e)

            try:
                if self.mode_sog == MODE_GYROSCOPE_ON:
                    data['gyroX'] = float(string[count])
                    data['gyroY'] = float(string[count+1])
                    data['gyroZ'] = float(string[count+2])
                    count += 3
            except Exception as e:
                print(e)

            try:
                if self.mode_soa == MODE_ACCELERATOR_ON or self.mode_soa == MODE_ACCELERATOR_LOCAL_WITHOUT_GRAVITY or self.mode_soa == MODE_ACCELERATOR_GLOBAL_WITHOUT_GRAVITY:
                    data['accelX'] = float(string[count])
                    data['accelY'] = float(string[count+1])
                    data['accelZ'] = float(string[count+2])
                    count += 3
                elif self.mode_soa == MODE_ACCELERATOR_LOCAL_VELOCITY or self.mode_soa == MODE_ACCELERATOR_GLOBAL_VELOCITY:
                    data['veloX'] = float(string[count])
                    data['veloY'] = float(string[count+1])
                    data['veloZ'] = float(string[count+2])
                    count += 3
            except Exception as e:
                print(e)

            try:
                if self.mode_som == MODE_MAGNETIC_ON:
                    data['magX'] = float(string[count])
                    data['magY'] = float(string[count+1])
                    data['magZ'] = float(string[count+2])
                    count += 3
            except Exception as e:
                print(e)

            try:
                if self.mode_sod == MODE_DISTANCE_LOCAL or self.mode_sod == MODE_DISTANCE_GLOBAL:
                    data['poseX'] = float(string[count])
                    data['poseY'] = float(string[count+1])
                    data['poseZ'] = float(string[count+2])
                    count += 3
            except Exception as e:
                print(e)

            try:
                if self.mode_sot == MODE_TEMPERATURE_ON:
                    data['temperature'] = float(string[count])
                    count += 1
            except Exception as e:
                print(e)

            try:
                if self.mode_sots == MODE_TIMESTAMP_ON:
                    data['timestamp'] = float(string[count])
                    count += 1
            except Exception as e:
                print(e)

            return data
        else:
            return {}
        

    def reset_imu_default(self):
        self.send_command("<lf>")
        time.sleep(1)

        self.mode_sof = MODE_EULER
        self.mode_sog = MODE_GYROSCOPE_OFF
        self.mode_soa = MODE_ACCELERATOR_OFF
        self.mode_som = MODE_MAGNETIC_OFF
        self.mode_sod = MODE_DISTANCE_OFF
        self.mode_sot = MODE_TEMPERATURE_OFF
        self.mode_sots = MODE_TIMESTAMP_OFF
        
        print("IMU Reset to Default")

    def send_command(self, command:str):
        self.ser.write(command.encode('utf-8'))
        time.sleep(0.5) # wait for setting to be applied

    def set_baudrate(self, baudrate):
        if baudrate == 9600:
            self.send_command("<sb1>")
        elif baudrate == 19200:
            self.send_command("<sb2>")
        elif baudrate == 38400:
            self.send_command("<sb3>")
        elif baudrate == 57600:
            self.send_command("<sb4>")
        elif baudrate == 115200:
            self.send_command("<sb5>")
        else:
            print("Invalid Baudrate")
            return
        
    def set_output_rate(self, output_rate:int):
        command = f"<sor{output_rate}>"
        self.send_command(command)
    
    def set_output_code(self, output_code:str):
        if output_code.lower() == "ascii":
            self.send_command("<soc1>")
        elif output_code.lower() == "hex" or output_code.lower() == "binary":
            self.send_command("<soc2>")
        else:
            print("Invalid Output Code")
            return
        
    def set_output_format(self, output_format:str):
        if output_format.lower() == "euler":
            self.send_command("<sof1>")
            self.mode_sof = MODE_EULER
            print("Output Format: Euler")
        elif output_format.lower() == "quaternion":
            self.send_command("<sof2>")
            self.mode_sof = MODE_QUATERNION
            print("Output Format: Quaternion")
        else:
            print("Invalid Output Format")
            return
        
    def set_output_gyro_mode(self, mode:int):
        self.send_command(f"<sog{mode}>")

        if mode == 0:
            self.mode_sog = MODE_GYROSCOPE_OFF
            print("Gyro Mode: Off")
        elif mode == 1:
            self.mode_sog = MODE_GYROSCOPE_ON
            print("Gyro Mode: On")

    def set_output_accelerator_mode(self, mode:int):
        self.send_command(f"<soa{mode}>")

        if mode == 0:
            self.mode_soa = MODE_ACCELERATOR_OFF
            print("Accelerator Mode: Off")
        elif mode == 1:
            self.mode_soa = MODE_ACCELERATOR_ON
            print("Accelerator Mode: On")
        elif mode == 2:
            self.mode_soa = MODE_ACCELERATOR_LOCAL_WITHOUT_GRAVITY
            print("Accelerator Mode: local without gravity")
        elif mode == 3:
            self.mode_soa = MODE_ACCELERATOR_GLOBAL_WITHOUT_GRAVITY
            print("Accelerator Mode: global without gravity")
        elif mode == 4:
            self.mode_soa = MODE_ACCELERATOR_LOCAL_VELOCITY
            print("Accelerator Mode: local velocity")
        elif mode == 5:
            self.mode_soa = MODE_ACCELERATOR_GLOBAL_VELOCITY
            print("Accelerator Mode: global velocity")
        else:
            print("Invalid Accelerator Mode")

    def set_output_magnetic(self, mode:int):
        self.send_command(f"<som{mode}>")

        if mode == 0:
            self.mode_som = MODE_MAGNETIC_OFF
            print("Magnetic Mode: Off")
        elif mode == 1:
            self.mode_som = MODE_MAGNETIC_ON
            print("Magnetic Mode: On")
        else:
            print("Invalid Magnetic Mode")

    def set_output_distance(self, mode:int):
        self.send_command(f"<sod{mode}>")

        if mode == 0:
            self.mode_sod = MODE_DISTANCE_OFF
            print("Distance Mode: Off")
        elif mode == 1:
            self.mode_sod = MODE_DISTANCE_LOCAL
            print("Distance Mode: On (local)")
        elif mode == 2:
            self.mode_sod = MODE_DISTANCE_GLOBAL
            print("Distance Mode: On (global)")
        else:
            print("Invalid Distance Mode")
        
    def set_output_temperature(self, mode:int):
        self.send_command(f"<sot{mode}>")

        if mode == 0:
            self.mode_sot = MODE_TEMPERATURE_OFF
            print("Temperature Mode: Off")
        elif mode == 1:
            self.mode_sot = MODE_TEMPERATURE_ON
            print("Temperature Mode: On")
        else:
            print("Invalid Temperature Mode")

    def set_output_timestamp(self, mode:int):
        self.send_command(f"<sots{mode}>")

        if mode == 0:
            self.mode_sots = MODE_TIMESTAMP_OFF
            print("Timestamp Mode: Off")
        elif mode == 1:
            self.mode_sots = MODE_TIMESTAMP_ON
            print("Timestamp Mode: On")
        else:
            print("Invalid Timestamp Mode")

    def set_enable_magneto(self, mode:int):
        self.send_command(f"<sem{mode}>")

        if mode == 0:
            print("Magneto: Off")
        elif mode == 1:
            print("Magneto: On")
        elif mode == 2:
            print("Magneto: On (2)") # what is this????
        else:
            print("Invalid Magneto Mode")

    def set_gyro_sensitivity(self, mode:int):
        self.send_command(f"<ssg{mode}>")

        if mode == 1:
            print("Gyro Sensitivity: 125 dps")
        elif mode == 2:
            print("Gyro Sensitivity: 250 dps")
        elif mode == 3:
            print("Gyro Sensitivity: 500 dps")
        elif mode == 4:
            print("Gyro Sensitivity: 1000 dps")
        elif mode == 5:
            print("Gyro Sensitivity: 2000 dps")
        else:
            print("Invalid Gyro Sensitivity")

    def set_accelerator_sensitivity(self, mode:int):
        self.send_command(f"<ssa{mode}>")

        if mode == 1:
            print("Accelerator Sensitivity: 2 g")
        elif mode == 2:
            print("Accelerator Sensitivity: 4 g")
        elif mode == 3:
            print("Accelerator Sensitivity: 8 g")
        elif mode == 4:
            print("Accelerator Sensitivity: 16 g")
        else:
            print("Invalid Accelerator Sensitivity")

    def set_low_pass_filter_gyroscope(self, mode:int):
        self.send_command(f"<lpfg{mode}>")

        if mode == 0:
            print("Low Pass Filter Gyroscope: 21Hz")
        elif mode == 1:
            print("Low Pass Filter Gyroscope: 48Hz")
        elif mode == 2:
            print("Low Pass Filter Gyroscope: 59Hz")
        elif mode == 3:
            print("Low Pass Filter Gyroscope: 97Hz")
        elif mode == 4:
            print("Low Pass Filter Gyroscope: 117Hz")
        elif mode == 5:
            print("Low Pass Filter Gyroscope: 191Hz")
        elif mode == 6:
            print("Low Pass Filter Gyroscope: 230Hz")
        elif mode == 7:
            print("Low Pass Filter Gyroscope: 262Hz")
        elif mode == 8:
            print("Low Pass Filter Gyroscope: 493Hz")
        elif mode == 9:
            print("Low Pass Filter Gyroscope: None")
        else:
            print("Invalid Low Pass Filter Gyroscope")

    def set_low_pass_filter_accelerator(self, mode:int):
        self.send_command(f"<lpfa{mode}>")

        if mode == 0:
            print("Low Pass Filter Accelerator: 21Hz")
        elif mode == 1:
            print("Low Pass Filter Accelerator: 44Hz")
        elif mode == 2:
            print("Low Pass Filter Accelerator: 59Hz")
        elif mode == 3:
            print("Low Pass Filter Accelerator: 97Hz")
        elif mode == 4:
            print("Low Pass Filter Accelerator: 117Hz")
        elif mode == 5:
            print("Low Pass Filter Accelerator: 191Hz")
        elif mode == 6:
            print("Low Pass Filter Accelerator: 230Hz")
        elif mode == 7:
            print("Low Pass Filter Accelerator: 262Hz")
        elif mode == 8:
            print("Low Pass Filter Accelerator: 493Hz")
        elif mode == 9:
            print("Low Pass Filter Accelerator: None")
        else:
            print("Invalid Low Pass Filter Accelerator")

    def set_filter_factor_accelerator_magnetic(self, mode:int):
        if mode < 1 or mode > 50:
            print("Invalid Filter Factor. should be between 1 and 50")
            return
        
        self.send_command(f"<sff{mode}>")

    def set_filter_factor_accelerator(self, mode:int):
        if mode < 1 or mode > 50:
            print("Invalid Filter Factor. should be between 1 and 50")
            return
        
        self.send_command(f"<sffa{mode}>")

    def set_filter_factor_magnetic(self, mode:int):
        if mode < 1 or mode > 50:
            print("Invalid Filter Factor. should be between 1 and 50")
            return
        
        self.send_command(f"<sffg{mode}>")

    def set_robust_attitude_level(self, mode:float):
        if mode < 0 or mode > 100:
            print("Invalid Robust Attitude Level. should be between 0.0 and 100.0")
            return
        
        self.send_command(f"<raa_l{mode}>")

    def set_robust_attitude_timeout(self, mode:int):
        if mode < 0 or mode > 2000000000:
            print("Invalid Robust Attitude Timeout. should be between 0 and 2000000000")
            return
        
        self.send_command(f"<raa_t{mode}>")
        
    def set_robust_heading_level(self, mode:float):
        if mode < 0 or mode > 100:
            print("Invalid Robust Heading Level. should be between 0.0 and 100.0")
            return
        
        self.send_command(f"<rha_l{mode}>")

    def set_robust_heading_timeout(self, mode:int):
        if mode < 0 or mode > 2000000000:
            print("Invalid Robust Heading Timeout. should be between 0 and 2000000000")
            return
        
        self.send_command(f"<rha_t{mode}>")

    def set_auto_gyroscope_calibration_enable(self, mode:int):
        self.send_command(f"<agc_e{mode}>")

        if mode == 0:
            print("Auto Gyroscope Calibration: Off")
        elif mode == 1:
            print("Auto Gyroscope Calibration: On")
        else:
            print("Invalid Auto Gyroscope Calibration")

    def set_auto_gyroscope_calibration_threshold(self, mode:float):
        if mode < 0 or mode > 100:
            print("Invalid Auto Gyroscope Calibration Threshold. should be between 0.0 and 100.0")
            return
        
        self.send_command(f"<agc_t{mode}>")

    def set_auto_gyroscope_calibration_drift(self, mode:float):
        if mode < 0 or mode > 10:
            print("Invalid Auto Gyroscope Calibration Drift. should be between 0.0 and 10.0")
            return
        
        self.send_command(f"<agc_d{mode}>")

    def set_active_vibration_cancellation_gyro(self, mode:int):
        self.send_command(f"<avcg_e{mode}>")

        if mode == 0: # 0 is On????
            print("Active Vibration Cancellation Gyro: On")
        elif mode == 1:
            print("Active Vibration Cancellation Gyro: Off")
        else:
            print("Invalid Active Vibration Cancellation Gyro")

    def set_active_vibration_cancellation_accelerator(self, mode:int):
        self.send_command(f"<avca_e{mode}>")

        if mode == 0:
            print("Active Vibration Cancellation Accelerator: On")
        elif mode == 1:
            print("Active Vibration Cancellation Accelerator: Off")
        else:
            print("Invalid Active Vibration Cancellation Accelerator")

    def set_position_filter_parameters(self, posf_sl:float, posf_st:int, posf_sr:float, posf_ar:float):
        if posf_sl < 0 or posf_sl > 1:
            print("Invalid Position Filter Slope. should be between 0.0 and 1.0")
            return

        if posf_st < 0 or posf_st > 1000:
            print("Invalid Position Filter Time. should be between 0 and 1000")
            return

        if posf_sr < 0 or posf_sr > 1:
            print("Invalid Position Filter Rate. should be between 0.0 and 1.0")
            return

        if posf_ar < 0 or posf_ar > 1:
            print("Invalid Position Filter Acceleration. should be between 0.0 and 1.0")
            return
        
        self.send_command(f"<posf_sl{posf_sl}>")
        self.send_command(f"<posf_st{posf_st}>")
        self.send_command(f"<posf_sr{posf_sr}>")
        self.send_command(f"<posf_ar{posf_ar}>")

    def reset_accumulated_pose(self):
        self.send_command("<posz>")
        print("Pose Reset")