#sez_to_ecef.py
#
# Usage: python3 sez_to_ecef.py o_lat_deg o_lon_deg o_hae_km s_km e_km z_km
#  Text explaining script usage
# Parameters:
#  o_lat_deg: Latitude in degrees
#  o_lon_deg: Longitude in degrees
#  o_hae_km: Height Above the Elipsoid in km
#  s_km: South
#  e_km: East
#  z_km: Zenith
#  
# Output:
#  Transforms SEZ cords into ECEF
#
# Written by Nicola Demarinis
# Other contributors: None
#
# Optional license statement, e.g., See the LICENSE file for the license.

# write script below this line

# import Python modules
import math # math module
import sys  # argv
import numpy # matrix math

# "constants"
R_E_KM = 6378.1363
E_E    = 0.081819221456

# initialize script arguments
o_lat_deg = float('nan') # ECEF x-component in km
o_lon_deg = float('nan') # ECEF y-component in km
o_hae_km = float('nan') # ECEF z-component in km
s_km = float('nan') # SEZ s-component in km
e_km = float('nan') # SEZ e-component in km
z_km = float('nan') # SEZ z-component in km

# parse script arguments
if len(sys.argv)==7:
  o_lat_deg = float(sys.argv[1])
  o_lon_deg = float(sys.argv[2])
  o_hae_km = float(sys.argv[3])
  s_km = float(sys.argv[4])
  e_km = float(sys.argv[5])
  z_km = float(sys.argv[6])
else:
  print(\
   'Usage: '\
   'python3 sez_to_ecef.py o_lat_deg o_lon_deg o_hae_km s_km e_km z_km'\
  )
  exit()

## First: Convert LLH to ECEF

## calculated denominator
def calc_denom(ecc, lat_rad):
  return math.sqrt(1.0-(ecc**2)*(math.sin(lat_rad)**2))

lat_rad = o_lat_deg*math.pi/180
lon_rad = o_lon_deg*math.pi/180

c_E = R_E_KM/calc_denom(E_E,lat_rad)
s_E = (R_E_KM*(1-E_E**2))/calc_denom(E_E,lat_rad)

r_x_km = (c_E+o_hae_km)*math.cos(lat_rad)*math.cos(lon_rad)
r_y_km = (c_E+o_hae_km)*math.cos(lat_rad)*math.sin(lon_rad)
r_z_km = (s_E+o_hae_km)*math.sin(lat_rad)
#r_km = math.sqrt(r_x_km**2 + r_y_km**2 + r_z_km**2)

# Second: Now ECEF to SEZ (Rotation Matracies)

ecef_observer_x = math.cos(lon_rad)*math.sin(lat_rad)*s_km + math.cos(lon_rad)*math.cos(lat_rad)*z_km - math.sin(lon_rad)*e_km
ecef_observer_y = math.sin(lon_rad)*math.sin(lat_rad)*s_km + math.sin(lon_rad)*math.cos(lat_rad)*z_km + math.cos(lon_rad)*e_km
ecef_observer_z = -math.cos(lat_rad)*s_km + math.sin(lat_rad)*z_km

# Adding them together
ecef_x_km = ecef_observer_x + r_x_km
ecef_y_km = ecef_observer_y + r_y_km
ecef_z_km = ecef_observer_z + r_z_km

# Last Thing
print(ecef_x_km)
print(ecef_y_km)
print(ecef_z_km)