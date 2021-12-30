"""define vehicle parameters:
    - horsepower vs rpm
    - torque vs rpm
    - coefficients of friction in x and y
    - mass of vehicle
    - drag coefficient
    - lift coefficient
    - gear ratios
    - final drive ratios
"""

import csv
import json
import sys, getopt
import math

class Vehicle:
    
    def __init__(self,vehicle_file):
        self.vehicle = self.parseVehicleJSON(vehicle_file)
        self.name = self.vehicle["name"]
        self.mass = self.vehicle["mass"]
        self.final_drive = self.vehicle["final_drive"]
        self.gears= self.vehicle["gears"]
        self.torque_curve = self.readCSVData(self.vehicle["torque_data"])
        self.power_curve = self.readCSVData(self.vehicle["power_data"])
        self.frontal_area = self.vehicle["frontal_area"]
        self.cd = self.vehicle["Cd"]
        self.cl = self.vehicle["Cl"]
        self.mux = self.vehicle["mux"]
        self.muy = self.vehicle["muy"]
        self.tire_diameter = self.vehicle["tire_diameter"]
        self.tire_circumfrence = math.pi*self.tire_diameter
        
    def parseVehicleJSON(self,vehicle_file):
        with open(vehicle_file) as json_file:
            return json.load(json_file)
    
    def readCSVData(self,csv_file):
        with open(csv_file, mode='r') as inp:
            reader = csv.reader(inp)
            next(reader)
            return {rows[0]:rows[1] for rows in reader}
    
    def max_acceleration(self,v0,gear,d):
        forward_force = self.getTorquefromVehicleSpeed(v0,gear)*self.tire_diameter/2
        """reverse_force = self.getAirForce(v0,self.cd)
        down_force = self.getAirForce(v0,self.cl)
        g = 9.81
        normal_force = self.mass*g + down_force
        friction_force = normal_force*self.mu""" #out of scope
        
        vf = (v0**2)+2*(forward_force/self.mass)*d
        
        return vf
    
    def getAirForce(self,v,coeff):
        rho_air = 1.225 #kg/m^3
        return 0.5*rho_air*(v**2)*coeff*self.frontal_area
    
    def getTorquefromVehicleSpeed(self,speed,gear):
        engine_rpm = self.getEngineRpmFromSpeed(self,speed,gear)

        if self.torque_curve.get(engine_rpm) is None:
            rpms = self.torque_curve.keys()
            nearest_index,nearest_rpm = self.findNearestVal(rpms,engine_rpm)
            if nearest_index == len(rpms)-1:
                previous_rpm = rpms[nearest_index-1]
                next_rpm = nearest_rpm
                previous_torque = self.torque_curve.get(previous_rpm)
                next_torque = self.torque_curve.get(next_rpm)
                torque = self.linearInterpolate(previous_rpm,previous_torque,engine_rpm,next_rpm,next_torque)
            elif nearest_index == 0:
                previous_rpm = nearest_rpm
                next_rpm = rpms[nearest_index+1]
                previous_torque = self.torque_curve.get(previous_rpm)
                next_torque = self.torque_curve.get(next_rpm)
                torque = self.linearInterpolate(previous_rpm,previous_torque,engine_rpm,next_rpm,next_torque)
            else:
                previous_rpm = rpms[nearest_index-1]
                next_rpm = rpms[nearest_index+1]
                previous_torque = self.torque_curve.get(previous_rpm)
                next_torque = self.torque_curve.get(next_rpm)
                torque = self.linearInterpolate(previous_rpm,previous_torque,engine_rpm,next_rpm,next_torque)
        return torque
    
    def getEngineRpmFromSpeed(self, speed, gear):
        wheel_rpm = (speed*60)/(self.tire_diameter*math.pi)
        return wheel_rpm/(self.final_drive*self.gears[gear-1])

    def findNearestVal(self,list,val):
        diffs = [abs(list_val - val) for list_val in list]
        min_diff = min(diffs)
        min_index = diffs.index(min_diff)
        return (min_index,list[min_index])
        
    def linearInterpolate(self,x1,y1,x2,x3,y3):
        y2 = y1 + ((x2 - x1)/(x3-x1)) * (y3-y1)
        return y2

def main():
    argv = sys.argv[1:]
    vehicle_file = ""
    try:
        opts, args = getopt.getopt(argv,"f:")
    except getopt.GetoptError:
        print("vehicle.py -f <vehicle_json>")
        sys.exit(2)
    for opt, arg in opts:
        if opt in ["-f"]:
            vehicle_file = arg
    v = Vehicle(vehicle_file)
    print(v.vehicle)

if __name__ == '__main__':
    main()
    