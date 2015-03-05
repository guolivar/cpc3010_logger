#!/usr/bin/env python

# Load the libraries
import serial # Serial communications
import time # Timing utilities
import subprocess # Shell utilities ... compressing data files

# Set the time constants
rec_time=time.gmtime()
timestamp = time.strftime("%Y/%m/%d %H:%M:%S GMT",rec_time)
prev_minute=rec_time[4]
# Set the minute averaging variable
min_concentration=0
n_concentration = 0
# Set the pre/post SQL statement values
insert_statement = """INSERT INTO data.fixedmeasurements 
(parameterid,value,siteid,recordtime) 
VALUES (%s,%s,%s,timestamptz %s);"""
insert_statement_file = """INSERT INTO data.fixedmeasurements 
(parameterid,value,siteid,recordtime) 
VALUES (%s,'%s',%s,timestamptz '%s');\n"""
# Read the settings from the settings file
settings_file = open("./settings.txt")
# e.g. "/dev/ttyUSB0"
port = settings_file.readline().rstrip('\n')
print(port)
# path for data files
# e.g. "/home/logger/datacpc3010/"
datapath = settings_file.readline().rstrip('\n')
print(datapath)
prev_file_name = datapath+time.strftime("%Y%m%d.txt",rec_time)
# psql connection string
# e.g "user=datauser password=l33t host=penap-data.dyndns.org dbname=didactic port=5432"
db_conn = settings_file.readline().rstrip('\n')
print(db_conn)
# ID values for the parameters and site (DATA, ERROR, SITE)
# e.g. "408,409,2" == CPCdata,CPCerror,QueenStreet
params = settings_file.readline().rstrip('\n').split(",")
print(params)
# SMPS operation settings
# e.g. "SMPS,60" == mode,nbins
smps_settings=settings_file.readline().rstrip('\n').split(",")
print(smps_settings)
is_smps = (smps_settings[0] == "SMPS")
print(is_smps)
nbins = eval(smps_settings[1])
print(nbins)
# Close the settings file
settings_file.close()
# Setup the SMPS scan information
# Logarithmic scale for the voltages
# 3 seconds on each step ... nbins == 
Vset = [0 for i in range(nbins*3)]
for i in range(nbins):
	print(i)
	Vset[i*3] = 11**((i+1.0)/(nbins)) - 1
	Vset[i*3+1]=Vset[i*3]
	Vset[i*3+2]=Vset[i*3]
Vset = Vset + list(reversed(Vset))
print(Vset)
# Hacks to work with custom end of line
eol = b'\r'
leneol = len(eol)
bline = bytearray()
# Open the serial port and clean the I/O buffer
ser = serial.Serial(port,9600,parity = serial.PARITY_EVEN,bytesize = serial.SEVENBITS)
ser.flushInput()
ser.flushOutput()
# Start the logging
dma_loop=0
volt_command=''
while True:
	## Request counts for the last second
	ser.write('RB\r')
	# Get the line of data from the instrument
	while True:
		c = ser.read(1)
		bline += c
		if bline[-leneol:] == eol:
			break
	# Parse the data line
	line = bline.decode("utf-8")
	if is_smps:
		# Convert number voltage to text
		volt_command = 'V' + str(int(1000*Vset[dma_loop%(nbins*6)])) + '\r'
		print(volt_command)
		# Send the command to the CPC
		#ser.write(volt_command)
		dma_loop+=1
	# Set the time for the record
	rec_time_s = int(time.time())
	rec_time=time.gmtime()
	timestamp = time.strftime("%Y/%m/%d %H:%M:%S GMT",rec_time)
	# SAMPLE LINE ONLY
	line = '2500\r'
	line = line.rstrip()
	concentration = eval(line)
	# Make the line pretty for the file
	file_line = timestamp+','+line+','+volt_command[1:-1]
	print(file_line)
	# Save it to the appropriate file
	current_file_name = datapath+time.strftime("%Y%m%d.txt",rec_time)
	current_file = open(current_file_name,"a")
	current_file.write(file_line+"\n")
	current_file.flush()
	current_file.close()
	line = ""
	bline = bytearray()
	## Is it the top of the minute?
	#if rec_time[4] != prev_minute:
		#prev_minute = rec_time[4]
		## YES! --> generate the psql statement
		## Average for the minute with what we have
		#min_concentration = min_concentration / n_concentration
		## Print the missing insert statements to a file
		## to be processed by another programme
		#sql_buffer = open(datapath + "SQL/inserts.sql","a")
		## Insert the DATA record
		#sql_buffer.write(insert_statement_file%
		#(params[0],min_concentration,params[2],timestamp))
		## Insert the ERROR record
		#sql_buffer.write(insert_statement_file%
		#(params[0],line[split_indx+1:],params[2],timestamp))
		#sql_buffer.flush()
		#sql_buffer.close()
	#min_concentration = 0
	#n_concentration = 0
	# Is it the last minute of the day?
	if current_file_name != prev_file_name:
		subprocess.call(["gzip",prev_file_name])
		prev_file_name = current_file_name
	# Wait until the next second
	while int(time.time())<=rec_time_s:
		#wait a few miliseconds
		time.sleep(0.05)	
print('I\'m done')
