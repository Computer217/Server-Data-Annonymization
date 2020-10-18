# Server-Data-Annonymization
Scripts request Wireless access data from Cisco Prime Servers and anonymizes the data. PID information and MAC addresses are encoded with airport codes and city names.

## Important Info

The scripts are designed to run via an hourly cron job. Scripts pull information from Cisco Prime Server off a provided template. The request downloads data in JSON format. 
Server storage is maintained at the end of the annonymize.py file by traversing through the local directory and removing csv files older than 7 days. 
