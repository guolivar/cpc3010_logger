# CPC3010 logger
Python utility to read the output from a TSI CPC3010 and optionally control the voltage of a compatible differential mobility analizer (DMA) and upload data to a PostgreSQL database.
## Modules required
* **pyserial**
* **psycopg2**
* **time**
## Usage
The runtime settings are specified in the [settings.txt] file which should look like:
/dev/ttyUSB0
./
local,0
user=datauses password=l3tme1n host=penap-data.dyndns.org dbname=didactic port=5432
408,409,1
SMPS,10
## Only the first lines are processed.
1 <SERIAL PORT ADDRESS>
2 <DATA SAVE PATH>
3 <local/db selector>,<compress data? 1=='yes'>
4 <DATABASE CONNECTION STRING>
5 <DATABASE INSERT IDs>



For details contact Gustavo Olivares
