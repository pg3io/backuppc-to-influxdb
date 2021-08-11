#!/usr/bin/python3

import sys
from datetime import datetime
from pytz import timezone
from influxdb import InfluxDBClient
import time
from config import *
import argparse

def preBackup(fields, tags, date):
    now_utc = datetime.now(timezone('UTC'))
    now_paris = now_utc.astimezone(timezone('Europe/Paris'))
    json_data = [ 
	{
	    "measurement": "preBackup",
	    "tags": tags,
            "time": now_paris,
	    "fields": fields 
	}
    ]
    return json_data

def postBackup(fields, tags, date, client, db, strdate):	   
    client.switch_database(db)
    s = "SELECT * FROM preBackup WHERE hostIP = '{}' AND backupServer = '{}' GROUP BY * ORDER BY DESC LIMIT 1".format(fields['host'], fields['backupServer'])
    try:
        query = client.query(s)
        points = query.get_points()
        for point in points:
    	    begin = point['time']
        beginSeconds = convertToSeconds(begin, "%Y-%m-%dT%H:%M:%S.%fZ")
        b = datetime.strptime(begin, "%Y-%m-%dT%H:%M:%S.%fZ")
        endSeconds = convertToSeconds(strdate, "%Y-%m-%dT%H:%M:%S.%fZ")
        diff = float(endSeconds) - float(beginSeconds)
        d = ((date - b).total_seconds()) - 3600
        fields['duration'] = round(d, 0)
        now_utc = datetime.now(timezone('UTC'))
        now_paris = now_utc.astimezone(timezone('Europe/Paris'))
        json_data = [ 
	    {
	        "measurement": "postBackup",
	        "tags": tags,
                "time": now_paris,
	        "fields": fields
	    }
        ]
    except:
        fields['duration'] = 0
        now_utc = datetime.now(timezone('UTC'))
        now_paris = now_utc.astimezone(timezone('Europe/Paris'))
        json_data = [ 
	    {
	        "measurement": "postBackup",
	        "tags": tags,
                "time": now_paris,
	        "fields": fields
	    }
        ]
    return json_data

def convertToSeconds(date, format):
    s = date
    secondsTimestamp = time.mktime(datetime.strptime(s, "%Y-%m-%dT%H:%M:%S.%fZ").timetuple())
    return secondsTimestamp

def insert_logs(db, user, passwd, host, port, fields, tags):
    err = {}
    err['status_code'] = 2
    msg_connect = "Unable to connect to the database"
    msg_list = "Unable to list databases"
    msg_create = "Unable to create database"
    msg_write = "Unable to write to the database"
    try:
        client = InfluxDBClient(host=host, port=port, username=user, password=passwd, database=db, ssl=True, verify_ssl=True)
    except:
        err['message'] = msg_connect
        print(err)
        return 1
    try:
        dbs = client.get_list_database()
    except:
        err['message'] = msg_list
        print(err)
        return 1
    if db not in dbs:
        try:
            client.create_database(db)
        except:
            err['message'] = msg_create
            print(err)
            return 1
    now_utc = datetime.now(timezone('UTC'))
    now_paris = now_utc.astimezone(timezone('Europe/Paris'))
    strdate = now_paris.strftime("%Y-%m-%dT%H:%M:%S.%fZ")
    now_paris = now_paris.replace(tzinfo=None)
    try:
        if fields['cmdType'] == "DumpPreUserCmd":
            client.write_points(preBackup(fields, tags, now_paris))
        if fields['cmdType'] == "DumpPostUserCmd":
            client.write_points(postBackup(fields, tags, now_paris, client, db, strdate))
    except:
        err['message'] = msg_write
        print(err)
        return 1
    return 0

def main():
    parser = argparse.ArgumentParser(description='Writes backup information into influxdb')
    parser.add_argument('--xferok', help='xferOK', required=True)
    parser.add_argument('--host', help='Host', required=True)
    parser.add_argument('--type', help='Type', required=True)
    parser.add_argument('--client', help='Client', required=True)
    parser.add_argument('--user', help='User', required=True)
    parser.add_argument('--moreusers', help='moreUsers', required=False)
    parser.add_argument('--hostip', help='Host IP', required=True)
    parser.add_argument('--share', help='Share', required=True)
    parser.add_argument('--xfermethod', help='xferMethod', required=True)
    parser.add_argument('--sshpath', help='ssh Path', required=True)
    parser.add_argument('--cmdtype', help='Command type', choices=['DumpPreUserCmd', 'DumpPostUserCmd'], required=True)
    args = vars(parser.parse_args())	
    f = open("/etc/hostname", "r")
    hostname = f.read()
    hostname = hostname.rstrip('\n')
    fields = dict(backupServer = hostname, xferOK = int(args['xferok']), Type = args['type'], client = args['client'], user = args['user'], moreusers= args['morusers'], host = args['host'], hostIP = args['hostip'], share = args['share'], XferMethod = args['xfermethod'], sshPath = args['sshpath'], cmdType = args['cmdtype'])
    tags = dict(host = args['host'])
    return(insert_logs(DATABASE_NAME, INFLUXDB_USER, INFLUXDB_PASSWORD, INFLUXDB_HOSTNAME, INFLUXDB_PORT, fields, tags))

main()
