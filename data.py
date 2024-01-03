import urllib.request
import json 
from datetime import datetime, timedelta
import pytz
import csv

#The Goal: To take the JSON data that results from the City of Buffalo API and make a updateable CSV file with only the data needed for this project. 


#Generates a URL to grab the JSON data where the incident dateTime is within the last number of days given in the parameter. 

def urlGenerator(num):
  current_date = datetime.now(pytz.timezone('US/Eastern'))
  begin = current_date - timedelta(days=num)
  current_year = str(current_date.year)
  current_month = str(current_date.month)
  current_day = str(current_date.day)
  begin_year = str(begin.year)
  begin_month = str(begin.month)
  begin_day = str(begin.day)
  current_timeStamp = current_year + "-" + current_month + "-" + current_day + "T12:00:00"
  begin_timeStamp = begin_year + "-" + begin_month + "-" + begin_day + "T12:00:00"
  queryString = "$where=incident_datetime between '" + str(begin_timeStamp) + "' and '" + str(current_timeStamp) +"'"
  url = 'https://data.buffalony.gov/resource/d6g9-xbgu.json?'
  url += queryString
  url = url.replace(" ", "%20")
  url = url.replace("'", "%27")
  return str(url)
  
#This function creates a list of dictionaries based on the data json it recieves from the url that is its parameter.
  
def data_loader(url):
  content = urllib.request.urlopen(url) 
  json_string = content.read().decode() 
  list = json.loads(json_string) 
  return list


#This function takes a list of dictionaries and a list of keys as parameters. It deletes the key-value pairs in each dictionary in the list that do not correspond to a key in its second parameter, listOfKeys. 

def key_isolater(listOfDic, listOfKeys):
  original = listOfDic
  acc = [] 
  for dic in original: 
    newDic = {} 
    for key in dic: 
      if key in listOfKeys:  
          newDic[key] = dic[key]

    if 'longitude' in newDic and 'latitude' in newDic: 
      acc.append(newDic) 
  return acc 

#Function that will write a CSV file with the proper data. Here, fileName is the desired name of the CSV file, recenecyInDays is how far you want the data going back, and desired keys is which columns in the dataset you want represented in the CSV. 

def makeCSV(fileName, recencyInDays, desiredKeys): 
  fullData = data_loader(urlGenerator(recencyInDays))
  targetData = key_isolater(fullData, desiredKeys)
  with open(fileName, 'w') as f: 
    writer = csv.writer(f) 
    writer.writerow(desiredKeys) 
    for dic in targetData: 
      acc = [] 
      for key in dic: 
        acc.append(dic[key])
      writer.writerow(acc)

#The following function is a helper function for makeLOD that turns the data in a CSV file into a list of lists. 

def listOfLists(csvFileName): 
  acc = [] 
  with open (csvFileName) as f: 
    reader = csv.reader(f) 
    next(reader)
    for line in reader: 
      acc.append(line)
  return acc 

#The following function will take the contents of a CSV file and turn it into a list of dictionaries (so this is the function that undoes makeCSV). 

def makeLOD(csvFileName): 
  listData = listOfLists(csvFileName) 
  listOfDictionaries = [] 
  keyList = [] 
  with open(csvFileName) as f: 
    reader = csv.reader(f)
    for line in reader: 
      keyList.append(line)
    keyList = keyList[0]

    for list in listData: 
      dic = {} 
      for i in range(0, len(keyList)): 
        dic[keyList[i]] = list[i] 
      listOfDictionaries.append(dic)
  return listOfDictionaries

#This function takes one parameter, the recency in days, and returns an object representing the data need for the scatter plot mabox. It also creates a CSV file and saves the data in there.
  
def dataGenAndSave(recencyInDays): 
  url = urlGenerator(recencyInDays)
  preData = data_loader(url)
  list_of_keys = ['incident_datetime', 'incident_type_primary', 'latitude', 'longitude']
  data = key_isolater(preData, list_of_keys)
  makeCSV('PoliceData.csv', recencyInDays, list_of_keys)
  return data 

def adjustTime(listOfTimes): 
  newList = [] 
  for time in listOfTimes: 
    month = time[5] + time[6] 
    day = time[8] + time[9] 
    hour = time[11] + time[12] + ":" + time[14] + time[15]
    toAdd = str(month) + "/" + str(day) + " at " + hour
    
    newList.append(toAdd)
  return newList 

def listOfCrimesGen(recencyInDays): 
  data = dataGenAndSave(recencyInDays)
  acc = [] 
  for dic in data: 
    crime = dic['incident_type_primary']
    if crime not in acc: 
      acc.append(crime)
  return acc 

  


def crimeDicGen(recencyInDays, crime): 
  data = dataGenAndSave(recencyInDays)
  acc = {'longitude' : [], 'latitude' : [], 'labels' : []} 
  for dic in data: 
    if dic['incident_type_primary'] == crime: 
      addLongList = acc['longitude']
      currLong = dic['longitude']
      addLongList.append(currLong)
      acc['longitude'] = addLongList 

      addLatList = acc['latitude']
      currLat = dic['latitude']
      addLatList.append(currLat)
      acc['latitude'] = addLatList

      time = dic['incident_datetime']
      month = time[5] + time[6] 
      day = time[8] + time[9] 
      hour = time[11] + time[12] + ":" + time[14] + time[15]
      time = str(month) + "/" + str(day) + " at " + hour
      label = dic['incident_type_primary'] + " on " + time 

      labelList = acc['labels']
      labelList.append(label)
      acc['labels'] = labelList
  return acc 

def betterJSONDic(recencyInDays): 
  crimeList = listOfCrimesGen(int(recencyInDays))
  toSend = {}  
  for crime in crimeList: 
    toSend[crime] = crimeDicGen(recencyInDays, crime)
  return json.dumps(toSend)
  
  
  
  
  

  
  


    
    

  
  
  
  

  

  
      
        
        
        


      
      
      

    
    
    
  
  


  

  


  
     
    
    


  
  



  
  
  