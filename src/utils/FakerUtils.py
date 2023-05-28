from faker import Faker
import random
from datetime import datetime

#Fake's Data Generator
class FakerUtils:
    #Generates unique first names
    @staticmethod
    def generateNames(count):
        names = set()
        faker = Faker()
              
        while len(names) < count:
           name = faker.name()
           if len(name) <= 60:
            names.add(name)
                   
        return list(names)

    #Generates US patent's classifications  
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
    
    #Generates datetime between an start date and end date 
    @staticmethod      
    def generateDateTime(startDate, endDate):
        faker = Faker()        
        return faker.date_between(datetime.strptime(startDate, "%Y-%m-%d %H:%M:%S"), datetime.strptime(endDate, "%Y-%m-%d %H:%M:%S"))