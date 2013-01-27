########################################################################
#
# Gis_test
#
# Gis_test.py
#
# MAIN
#
# Copyright (C) 1994 Ulrik Hoerlyk Hjort
#
# Gis_test is free software; you can redistribute it
# and/or modify it under terms of the GNU General Public License
# as published by the Free Software Foundation; either version 2,
# or (at your option) any later version.
# Gis_test is distributed in the hope that it will be
# useful, but WITHOUT ANY WARRANTY; without even the implied warranty
# of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.
# See the GNU General Public License for more details.
# You should have received a copy of the GNU General
# Public License distributed with Yolk. If not, write to the Free
# Software Foundation, 51 Franklin Street, Fifth Floor, Boston,
# MA 02110 - 1301, USA.
######################################################################## 

from Gis_tools import *



from_p = ((53,01,43,'N'),(007,41,54,'W'))
to_p = ((57,21,18,'N'),(004,01,14,'W'))

print "Distance: ",great_circle_distance(from_p, to_p)
print "Initial: ",degrees_to_dms(initial_bearing(from_p, to_p))
print "Final: ",degrees_to_dms(final_bearing(from_p, to_p))
mp =  mid_point(from_p, to_p)
print mp
print "MP: " , degrees_to_dms(mp[0]),degrees_to_dms(mp[1])

print "================================================================"
p = (54,01,29,'N')
b = 34.1

ml =  max_latitude(p,b)
print "max lat: " , degrees_to_dms(ml)


print "================================================================="
from_p = ((54,14,45,'N'),(2,8,15,'W'))
to_p = ((41,19,01,'N'),(72,5,17,'W'))

dist_bear = loxodrome_distance_and_bearing(from_p, to_p)

print "Dist Bear: ", dist_bear

print "bear: " ,degrees_to_dms(dist_bear[1])

print "================================================================="
from_p = ((53,19,41,'N'),(5,6,21,'W'))
to_p = ((41,24,06,'N'),(72,4,23,'W'))

res = loxodrome_midpoint(from_p, to_p)

print "Loxodrome midpoint: ",lat_lon_degrees_to_hms_with_suffix(res)


print "================================================================="
from_p = ((55,32,54.35,'N'),(12,51,54.05,'E'))
to_p = ((55,32,44.89,'N'),(12,51,32.64,'E'))


print "Distance: ",great_circle_distance(from_p, to_p)
print "Initial: ",degrees_to_dms(initial_bearing(from_p, to_p))
print "Final: ",degrees_to_dms(final_bearing(from_p, to_p))
mp =  mid_point(from_p, to_p)
print mp
print "MP: " , degrees_to_dms(mp[0]),degrees_to_dms(mp[1])

print "================================================================="
start_p = ((51,21,12,'N'), (3,46,43,'W'))
b = (91,04,28)
d = 135.9


lat_lon_deg =  calculate_destination_point(start_p, b, d)
print "LL: ", lat_lon_deg
lat_lon_degrees_to_hms_with_suffix(lat_lon_deg)

print "================================================================="
start_point_1 = ((53, 56, 4,'N'), (0, 12, 4,'E'))
bearing_1 = 110.45

start_point_2 = ((48, 1, 23,'N'), (3, 33, 52, 'E'))
bearing_2 = 33.65

intersect =  path_intersection_point(start_point_1, bearing_1, start_point_2, bearing_2)

print intersect

print lat_lon_degrees_to_hms_with_suffix(intersect)

print "================================================================="
from_point = ((54,6,34,'N'), (2,24,12,'E'))
distance = 51.55
bearing = dms_to_degrees((121,23,14))

res =  loxodrome_destination_point(from_point, distance, bearing)

print res
print lat_lon_degrees_to_hms_with_suffix(res)




