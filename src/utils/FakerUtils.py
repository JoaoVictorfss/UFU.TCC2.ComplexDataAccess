from faker import Faker

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
        #Adicionar algumas classicações e retornar
        classifications = []      
        
        return classifications
    
    @staticmethod      
    def generateDateTimes(startDate, endDate, count):
        datetimes = []      
        faker = Faker()
        
        while len(datetimes) < count:
            datetimes.append(faker.date.between(startDate, endDate))
        
        return datetimes