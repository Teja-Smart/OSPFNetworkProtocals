#https://pythontic.com/modules/socket/udp-client-server-example
#NAME: DRONADULA TEJA
# Roll Number: CS20B026
# Course: CS3205 Jan. 2023 semester
# Lab number: 5
# Date of submission: 29 APR (12 hrs late)
# I confirm that the source file is entirely written by me without
# resorting to any dishonest means.
# Website(s) that I used for basic socket programming code are:
# URL(s): <fill>

import os
for i in range(10):
    os.system("python3 OSPF.py -i {} -f input -o output -h 0.1 -a 0.3 -s 3 &".format(i + 1))
    