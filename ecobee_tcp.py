#!/usr/bin/env python3.6

from time import sleep
from datetime import datetime

#create connection list and current proc file list
connection_list = []
proc_file = []

#re-run the script
while True:

    #open /proc/net/tcp for reading
    f = open("/proc/net/tcp", "r")
    #skip the header line
    next(f)
    
    #create our custom timestamp
    time = datetime.now()
    timestamp = time.strftime("%Y-%m-%d %H:%M:%S")

    #iterate through the lines, grabbing only the remote address and port
    for lines in f:

        #pull out remote address
        result = lines.split()[2]

        #convert remote address to standard ip format
        addr = (result.split(':')[0])
        #split address into each individual octet
        addr_long = ["".join(addr) for addr in zip(*[iter(addr)]*2)]
        #convert each octet into int
        addr_long = [int(x, 16) for x in addr_long]
        #rewrite into standard ip format
        ip = (".".join(str(x) for x in reversed(addr_long)))

        #convert remote port to standard format
        sock = (result.split(':')[1])
        port = int(sock, 16)

        #save the connection as a string
        connection = str(ip) + ":" + str(port)

        #add the connection to the current proc file list
        proc_file.append(connection)


        #check if connection is new
        #if the connection is in the proc file, but isnt in the connection list, add it to the connection list and print its new
        if connection not in connection_list:
            
            connection_list.append(connection)
            print(f"{timestamp}: New Connection: {connection}")

        #if the connection is in the proc file and in the connection list, do nothing


    #check if connection is removed
    #if a connection(x) that is in the connection list isnt in the completed proc file, remove the connection from the connection list and print that
    for x in connection_list:
        
        if x not in proc_file:
            
            connection_list.remove(x)
            print(f"{timestamp}: Removed Connection: {x}")


    #clear the proc_file list for the next run
    proc_file.clear()


    #wait 10 seconds before re-run
    sleep(10)
    

