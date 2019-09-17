import requests
import json
import os.path
import csv
import datetime
today = datetime.date.today()
from dateutil import relativedelta
from dateutil.relativedelta import relativedelta
from datetime import datetime, timedelta
import sys
import glob
import os
import config

y1 = datetime.strftime(datetime.now() - timedelta(1), '%Y-%m-%d')

def csv_output():

    file2 = open('gateway_needed_info.txt', 'r')
    lines = file2.readlines()
    todays=today.strftime('%Y-%m-%d')
    output_name = todays+'.csv'
    latest_file = y1 + '.csv'

    while True:
      try:
        file_stat = open(latest_file,'r')
        break
      except FileNotFoundError:
        print("yesterday's file not available")
        print("I am quitting....")
        sys.exit()
        
    x = open(output_name, 'w')
    x.write('MTag, Built On, Start Date, End Date, P/N, Cust. Name, Cust. No., Trigger')

    with open(latest_file,'r') as f:
      mycsv = csv.reader(f)
      header = next(mycsv)
      for row in mycsv:
        print(row[0],row[1],row[2])
        x.write("\n%s,%s,%s,%s,%s,%s,%s,%s" % (row[0],row[1],row[2],row[3],row[4],row[5],row[6],row[7]))
        x.flush()

    months_deal=0
    duration = 0

    for line in lines:
        master = line.split(",")[0].strip()
        template = line.split(",")[1].strip()
        cust_name = line.split(",")[-3].strip()
        cust_no = line.split(",")[-2].strip()
            ###API information integrated below
            
        if (master != "No Master Tag" and template == "On Boarding") or (master != "No Master Tag" and template == "No gateway template name"):
            with open(latest_file, 'r') as f:
              mycsv = csv.reader(f)
                #if master not found in f:1st column
          
              for line in mycsv:
                mpresent = False
                if master in line:
                  mpresent = True
                  break
            

            if mpresent == False:
              url = "https://vomapps.azurewebsites.net/managed-apis/device-data/v1/accounts/C40768/devices/" + master
              print("Calling url..............................", url)
              headers = {
                'x-api-key': "66R0NdzIztRFHuUMMQZLUqR2OxIk3Sv6D7AahoDYXQhpiHoO1txyvA==",
                'cache-control': "no-cache"
              }
              
              response_vom = requests.request("GET", url, headers=headers)
              json_vom = response_vom.json()
              ship_date = json_vom["assets"][0]["createDate"]

              shipdate = datetime.strptime(ship_date[0:10],'%Y-%m-%d')
              print ("The ship date is....%s",shipdate)
              
              month_diff = relativedelta(today, shipdate).months
              print ("The difference in months is....",month_diff)
              
              if month_diff>=6:
                pno = json_vom["assets"][0]["partNumber"]
                part_number = pno[0:6]
                if part_number in config.partnumber:
                    duration = config.partnumber.get(part_number)
                    due = today + relativedelta(months=duration)
                else:
                    duration = 0
                    due = "Wrong P/N"
                    print("Wrong Part number")
                    
                print("The duration is........................", duration)

                print("Part number for ", master, "is ", part_number)
                
                x.write("\n%s,%s,%s,%s,%s,%s,%s,%s" % (master,shipdate.date(),today,due,part_number,cust_name,cust_no,"6 Months"))
                x.flush()
                duration = 0
       
        elif (master != "No Master Tag" and template != "On Boarding") or (master != "No Master Tag" and template != "No gateway template name"): 
            with open(latest_file, 'r') as f:
              mycsv = csv.reader(f)
                #if master not found in f:1st column
                        
              for line in mycsv:
                found = False
                if master in line:
                  found = True
                  break

            if found == False:
              url = "https://vomapps.azurewebsites.net/managed-apis/device-data/v1/accounts/C40768/devices/" + master
              print("Calling url..............................", url)
              headers = {
                'x-api-key': "66R0NdzIztRFHuUMMQZLUqR2OxIk3Sv6D7AahoDYXQhpiHoO1txyvA==",
                'cache-control': "no-cache"  
              }
              
              response_vom = requests.request("GET", url, headers=headers)
              json_vom = response_vom.json()
              pno = json_vom["assets"][0]["partNumber"]
              part_number = pno[0:6]

              ship_date = json_vom["assets"][0]["createDate"]
              shipdate = datetime.strptime(ship_date[0:10],'%Y-%m-%d')
              print("shipdate is ................")
              if part_number in config.partnumber:
                    duration = config.partnumber.get(part_number)
                    due = today + relativedelta(months=duration)
              else:
                    duration = 0
                    due = "Wrong P/N"
                    print("Wrong Part number")
              print("The duration is........................", duration)
              print("Part number for ", master, "is ", part_number)              
              x.write("\n%s,%s,%s,%s,%s,%s,%s,%s" % (master,shipdate.date(),today,due,part_number,cust_name,cust_no,"Custom Template"))
              x.flush()
              duration = 0
           

    
                   
    x.close()
    f.close()
    file2.close()
    file_stat.close()
