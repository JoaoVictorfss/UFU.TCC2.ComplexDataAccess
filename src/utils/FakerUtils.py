from faker import Faker
import random
from datetime import datetime

class FakerUtils:
    @staticmethod
    def generateUniqueFirstNames(count):
        firstNames = set()
        faker = Faker()
              
        while len(firstNames) < count:
           firstName = faker.unique.first_name()
           
           if len(firstName) <= 60:
            firstNames.add(firstName)
                   
        return list(firstNames)
    
    @staticmethod      
    def generateUsPatentClassifications(count):
        classifications = []      
        for _ in range(count):
            section = chr(random.randint(65, 72))  
            subclass = random.randint(1, 99)
            main_group = random.randint(1, 9)
            subgroup = random.randint(1, 99)
            classification = f"{section}{subclass:02d}{main_group:01d}{subgroup:02d}"
            classifications.append(classification)
            
        return classifications
    
    @staticmethod      
    def generateDateTimes(startDate, endDate, count):
        datetimes = []      
        faker = Faker()
        format = "%Y-%m-%d %H:%M:%S"
        
        while len(datetimes) < count:
            generatedDate = faker.date_between(datetime.strptime(startDate, format), datetime.strptime(endDate, format))
            datetimes.append(generatedDate)       
        
        return datetimes