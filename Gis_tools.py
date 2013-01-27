########################################################################
#
# Gis_Tools
#
# Gis_Tools.py
#
# MAIN
#
# Copyright (C) 1994 Ulrik Hoerlyk Hjort
#
# Gis_Tools is free software; you can redistribute it
# and/or modify it under terms of the GNU General Public License
# as published by the Free Software Foundation; either version 2,
# or (at your option) any later version.
# Gis_Tools is distributed in the hope that it will be
# useful, but WITHOUT ANY WARRANTY; without even the implied warranty
# of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.
# See the GNU General Public License for more details.
# You should have received a copy of the GNU General
# Public License distributed with Yolk. If not, write to the Free
# Software Foundation, 51 Franklin Street, Fifth Floor, Boston,
# MA 02110 - 1301, USA.
######################################################################## 

from math import *


R = 6371.0   # Earth radius

######################################################################
#
# Normalize angle
#
######################################################################
def reduce_angle(x):
    return x - floor(x/360.0) * 360.0



######################################################################
#
# Convert degrees to hour, minutes, seconds
#
######################################################################
def degrees_to_hms(d):
    h = d / 15.0
    m = (h * 60) - int(h) * 60
    s = (m * 60) - int(m) * 60
    return(int(h), int(m), round(s,1))

######################################################################
#
# Convrt degress to degress, minutes, seconds
#
######################################################################
def degrees_to_dms(d):
    deg = int(d)
    m = (d - deg) * 60
    s = (m - int(m)) * 60

    return (deg, int(m), round(s,1))



######################################################################
#
# Convert Degress Minutes Seconds [N/S/E/W] to decimal degrees
#
######################################################################
def dms_with_suffix_to_decimal_degrees(dms):
    deg = dms[0]
    m = dms[1]
    s = dms[2]
    suffix = dms[3]
   
    suffix_sign = 1
    if suffix == 'S' or suffix == 'W':
        suffix_sign = -1

    return (suffix_sign * (deg + (m/60.0) + (s/60.0/60.0)))


######################################################################
#
# Convert Degress Minutes Seconds to decimal degrees
#
######################################################################
def dms_to_degrees(dms):
    deg = dms[0]
    m = dms[1]
    s = dms[2]
    return deg + (m/60.0) + (s/60.0/60.0)


######################################################################
#
# Convert lat, lon degress to hours, minutes, seconds with N/S/W/E suffix
#
######################################################################
def lat_lon_degrees_to_hms_with_suffix(lat_lon_deg):
    lat_suffix = "N"
    lon_suffix = "E"
    lat = degrees_to_dms(abs(lat_lon_deg[0]))
    lon = degrees_to_dms(abs(lat_lon_deg[1]))

    if lat_lon_deg[0] < 0:
        lat_suffix = "S"        

    if lat_lon_deg[1] < 0:
        lon_suffix = "W"        

    return (lat[0],lat[1],lat[2],lat_suffix), (lon[0],lon[1],lon[2],lon_suffix)




######################################################################
#
# Calculate midpoint between two (lat,lon) points
#
######################################################################
def mid_point(from_point, to_point):
    from_lat = dms_with_suffix_to_decimal_degrees(from_point[0]) * pi/180.0
    from_lon = dms_with_suffix_to_decimal_degrees(from_point[1]) * pi/180.0
    to_lat = dms_with_suffix_to_decimal_degrees(to_point[0]) * pi/180.0
    to_lon = dms_with_suffix_to_decimal_degrees(to_point[1]) * pi/180.0

    delta_lat = to_lat - from_lat
    delta_lon = to_lon - from_lon

    Bx = cos(from_lat) * cos(delta_lon)
    By = cos(from_lat) * sin(delta_lon)
    
    mid_lat = reduce_angle((atan2(sin(from_lat) + sin(to_lat), sqrt((cos(from_lat)+Bx) * (cos(from_lat) + Bx)+ (By ** 2)))) * 180.0 / pi)

    mid_lon = reduce_angle((from_lon + atan2(By, cos(from_lat) + Bx)) * 180.0 / pi)

    return (mid_lat, mid_lon)



#########################################################################
#
# Max latitude of a great circle path e.g the closest point to the pole
#
#
#########################################################################
def max_latitude(lat, bearing):

    lat_rad = dms_with_suffix_to_decimal_degrees(lat) * pi/180.0    
    b_rad = bearing * pi/180.0    

    return (acos(abs(sin(b_rad) * cos(lat_rad))) *  180.0 / pi)

######################################################################
#
# Great circle distance (e.g shortest distance over earth surface) - 
# between to points based on  the haversine fomular
#
######################################################################
def great_circle_distance(from_point, to_point):

    from_lat = dms_with_suffix_to_decimal_degrees(from_point[0]) * pi/180.0
    from_lon = dms_with_suffix_to_decimal_degrees(from_point[1]) * pi/180.0
    to_lat = dms_with_suffix_to_decimal_degrees(to_point[0]) * pi/180.0
    to_lon = dms_with_suffix_to_decimal_degrees(to_point[1]) * pi/180.0


    delta_lat = (to_lat - from_lat)  
    delta_lon = (to_lon - from_lon)  


    a = (sin(delta_lat / 2.0) ** 2) + (sin(delta_lon / 2.0) ** 2) * cos(from_lat) * cos(to_lat)
    c = 2.0 * atan2(sqrt(a), sqrt(1-a))
    d = R * c

    return d
######################################################################
#
# Calculate initial bering from "from_point" to "to_point"
#
######################################################################
def initial_bearing(from_point, to_point):
    from_lat = dms_with_suffix_to_decimal_degrees(from_point[0]) * pi/180.0
    from_lon = dms_with_suffix_to_decimal_degrees(from_point[1]) * pi/180.0
    to_lat = dms_with_suffix_to_decimal_degrees(to_point[0]) * pi/180.0
    to_lon = dms_with_suffix_to_decimal_degrees(to_point[1]) * pi/180.0
    
    delta_lat = to_lat - from_lat
    delta_lon = to_lon - from_lon

    x = cos(from_lat) * sin(to_lat) - sin(from_lat) * cos(to_lat)* cos(delta_lon)
    y = sin(delta_lon) * cos(to_lat)

    brg = atan2(y,x) * 180.0 / pi

    return reduce_angle(brg) 

######################################################################
#
# Final bearing = reversed initial bearing from end to start point
#
#
######################################################################
def final_bearing(from_point, to_point):
    return reduce_angle(initial_bearing(to_point,from_point) + 180.0)



######################################################################
#
# Calculate loxodrome distance and bearing between two points
#
#
######################################################################
def loxodrome_distance_and_bearing(from_point, to_point):
    from_lat = dms_with_suffix_to_decimal_degrees(from_point[0]) * pi/180.0
    from_lon = dms_with_suffix_to_decimal_degrees(from_point[1]) * pi/180.0
    to_lat = dms_with_suffix_to_decimal_degrees(to_point[0]) * pi/180.0
    to_lon = dms_with_suffix_to_decimal_degrees(to_point[1]) * pi/180.0

    delta_lat = to_lat - from_lat
    delta_lon = to_lon - from_lon

    delta_phi = log(tan(pi/4.0+ to_lat/2.0)/tan(pi/4.0 + from_lat/2.0))
    q = 0

    if delta_phi != 0:
        q = delta_lat/delta_phi
    else:
        q = cos(from_lat)

    if abs(delta_lon) > pi:
        if delta_lon > 0:
            delta_lon = -1 * (2*pi - delta_lon)
        else:
            delta_lon = (2*pi + delta_lon)

    dist = sqrt((delta_lat ** 2) + (q ** 2) * (delta_lon ** 2)) * R

    bearing = reduce_angle(atan2(delta_lon, delta_phi) * (180.0/pi))

    return (dist, bearing)


######################################################################
#
# Calculate loxodrome midpoint between two (lat,lon) points
#
######################################################################
def loxodrome_midpoint(from_point, to_point):
    from_lat = dms_with_suffix_to_decimal_degrees(from_point[0]) * pi/180.0
    from_lon = dms_with_suffix_to_decimal_degrees(from_point[1]) * pi/180.0
    to_lat = dms_with_suffix_to_decimal_degrees(to_point[0]) * pi/180.0
    to_lon = dms_with_suffix_to_decimal_degrees(to_point[1]) * pi/180.0

    mid_lat = (from_lat + to_lat) /2.0

    e1 = tan(pi/4.0 + from_lat/2.0)
    e2 = tan(pi/4.0 + to_lat/2.0)
    e3 = tan(pi/4.0  + mid_lat/2.0)

    mid_lon = 0

    if log(e2/e1) != 0:
            mid_lon = ((to_lon - from_lon) * log (e3) + from_lon * log (e2) - to_lon*log(e1))/ log(e2/e1)
        
    else: 
        mid_lon = (from_lon + to_lon) /2.0

    # Normalize -180 .. + 180 
    mid_lon = (mid_lon + 3*pi)%(2*pi) - pi

    return (mid_lat * 180.0 /pi, mid_lon * 180.0 /pi)

######################################################################
#
# Calculate loxodrome destination point given start point, distance and
# bearing
#
######################################################################
def loxodrome_destination_point(from_point, distance, bearing):

    from_lat = dms_with_suffix_to_decimal_degrees(from_point[0]) * pi/180.0
    from_lon = dms_with_suffix_to_decimal_degrees(from_point[1]) * pi/180.0


    b_rad = bearing * pi/180
    
    delta_lat = (distance/R) * cos(b_rad)

    to_lat = from_lat + delta_lat 

    delta_phi = log(tan(to_lat/2.0 + pi/4.0)/tan(from_lat/2.0 + pi/4.0))

    q = 0

    if delta_phi != 0:
        q = delta_lat/delta_phi
    else:
        q = cos(from_lat)

    delta_lon = (distance/R) * sin(b_rad) / q

    if abs(to_lat) > pi/2.0:
        if to_lat > 0:
            to_lat = pi - to_lat
        else:
            to_lat = -1 * (pi - to_lat)

    # Normalize -180 .. + 180 
    to_lon = (from_lon+ delta_lon + 3.0*pi) % (2.0*pi) - pi

    return (to_lat * 180.0 /pi, to_lon * 180.0 /pi)
    


######################################################################
#
# Calculate destination point given start point, distance and
# bearing
#
#
######################################################################
def calculate_destination_point(start_point, bearing, distance):

    start_lat = dms_with_suffix_to_decimal_degrees(start_point[0]) * pi/180.0
    start_lon = dms_with_suffix_to_decimal_degrees(start_point[1]) * pi/180.0
    bearing_rad = dms_to_degrees(bearing) * pi/180.0

    dest_lat = (asin(sin(start_lat) * cos(distance/R) + cos(start_lat)*sin(distance/R) * cos(bearing_rad)))
    dest_lon = ((start_lon + atan2(sin(bearing_rad) * sin(distance/R) * cos(start_lat), cos(distance/R) - sin(start_lat)*sin(dest_lat))) * 180.0 /pi)
    dest_lat *= (180.0/pi)


    return (dest_lat, dest_lon)




######################################################################
#
# Calculate intersection point between two paths given by:
# path1 = (start_point_1, bearing 1)
# path2 = (start_point_2, bearing 2)
#
######################################################################
def path_intersection_point(start_point_1, bearing_1, start_point_2, bearing_2):
    sp1_lat =  dms_with_suffix_to_decimal_degrees(start_point_1[0]) * pi/180.0
    sp1_lon =  dms_with_suffix_to_decimal_degrees(start_point_1[1]) * pi/180.0

    sp2_lat =  dms_with_suffix_to_decimal_degrees(start_point_2[0]) * pi/180.0
    sp2_lon =  dms_with_suffix_to_decimal_degrees(start_point_2[1]) * pi/180.0

    b1_rad = bearing_1 * pi/180.0
    b2_rad = bearing_2 * pi/180.0

    delta_lat = sp2_lat - sp1_lat
    delta_lon = sp2_lon - sp1_lon

    d = 2 * asin(sqrt( (sin(delta_lat / 2.0) ** 2.0) + cos(sp1_lat) * cos(sp2_lat) * (sin(delta_lon/2.0) ** 2)))


    b1 = acos( (sin(sp2_lat) - sin(sp1_lat) * cos (d)) / (sin(d) * cos(sp1_lat)))
    b2 = acos( (sin(sp1_lat) - sin(sp2_lat) * cos(d)) / (sin(d) * cos (sp2_lat)))


    if sin(sp2_lon - sp1_lon) > 0:
        b2 = (2*pi) - b2
    else:
        b1 = (2*pi) -b1

    a1 = (b1_rad -b1 + pi) % (2*pi) - pi
    a2 = (b2 - b2_rad +pi) % (2*pi) - pi


    if ( (sin(a1) == 0 and sin(a2) == 0) or (sin(a1) * sin(a2) < 0)):
        return null

    a3 = acos(-cos(a1) * cos(a2) + sin(a1) * sin(a2) * cos(d))
    d1 = atan2(sin(d) * sin(a1)* sin(a2), cos(a2)+cos(a1)*cos(a3))
    lat = asin(sin(sp1_lat) * cos(d1) + cos(sp1_lat) * sin(d1) * cos(b1_rad))
    
    d_lon = atan2(sin(b1_rad) * sin(d1) * cos (sp1_lat), cos(d1)-sin(sp1_lat)*sin(lat)) + sp1_lon

    lon = (d_lon + 3* pi) % (2*pi) - pi

    return (lat * (180.0/pi),lon * (180.0/pi))
    





