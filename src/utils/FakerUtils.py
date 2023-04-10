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
                   
        return firstNames
    
    @staticmethod      
    def generateDescriptions(count):
        descriptions = []      
        faker = Faker()
        
        while len(descriptions) < count:
            text = faker.text()
            
            if len(text) <= MAX_DESCRIPTION_SIZE:
              descriptions.append(text)
        
        return descriptions
    
    @staticmethod      
    def generateUsPatentClassifications(count):
        #Adicioanr algumas classicações e retornar
        classifications = []      
        
        return classifications
    
    @staticmethod      
    def generateDateTimes(count):
        datetimes = []      
        
        return datetimes