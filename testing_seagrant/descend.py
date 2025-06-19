from bouyancy_control import BouyancyFloatController
import time
bfc = BouyancyFloatController()
time.sleep(6)
bfc.start_descending()
