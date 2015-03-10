# CPC3010 logger
Python utility to read the output from a TSI CPC3010 and optionally control the voltage of a compatible differential mobility analizer (DMA) and upload data to a PostgreSQL database.

The script requests the 1 second buffer from the CPC, timestamps it and saves it to a file. Optionally, it can send the control command to sweep the voltage on the DMA and upload the data to a database.

## Modules required
* **pyserial**
* **psycopg2**
* **time**

## Usage
The settings are specified in the ```settings.txt``` file which should look like:
```
/dev/ttyUSB0
./
local,0
user=datauses password=l3tme1n host=penap-data.dyndns.org dbname=didactic port=5432
408,409,1
SMPS,10
## Only the first lines are processed.
1 <SERIAL PORT ADDRESS>
2 <DATA SAVE PATH>
3 <local/database selector>,<compress data? 1=='yes'>
4 <DATABASE CONNECTION STRING>
5 <DATABASE INSERT IDs>
```
There are two scripts to run:
* ```logger_mail.py```. This is the main logging script and the one that interacts directly with the CPC. It must be run manually and it will continue to run until stopped by ```^C```. The outputs from this script are one datafile named ```YYYYMMDD.txt``` with the 1 second data and a ```SQL/inserts.sql```with the SQL statements to update the database with the **1 minute average** data.
* ```upload_batch_sql.py```. This is the database updater and it it recommended to be run as a cron job every 5 to 10 minutes

For further details contact Gustavo Olivares
