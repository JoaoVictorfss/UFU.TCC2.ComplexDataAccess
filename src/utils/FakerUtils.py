from faker import Faker
import random

MAX_DESCRIPTION_SIZE = 300
MAX_FIRST_NAME_SIZE = 60

class FakerUtils:
    @staticmethod
    def generateUniqueFirstNames(count):
        firstNames = set()
        faker = Faker()
              
        while len(firstNames) < count:
           firstName = faker.unique.first_name()
           
           if len(firstName) <= MAX_FIRST_NAME_SIZE:
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
        
        while len(datetimes) < count:
            datetimes.append(faker.date.between(startDate, endDate))
        
        return datetimes