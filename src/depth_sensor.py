import ms5837


# Print readings
def read_depth(sensor):        
        if sensor.read():
                print(("P: %0.1f mbar  %0.3f psi\tDepth: %0.3f\tT: %0.2f C  %0.2f F") % (
                sensor.pressure(), # Default is mbar (no arguments)
                sensor.pressure(ms5837.UNITS_psi), # Request psi
                sensor.depth(),
                sensor.temperature(), # Default is degrees C (no arguments)
                sensor.temperature(ms5837.UNITS_Farenheit))) # Request Farenheit
                return sensor.depth(), sensor.pressure(ms5837.UNITS_psi)
        else:
                print("Sensor read failed!")
                exit(1)