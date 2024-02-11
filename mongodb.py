import pymongo
from pymongo import MongoClient
#set up information

key = "34a63dfcc24fadbc2f4cf435e4d56ed99a36115c"
cluster = MongoClient("mongodb+srv://adityabaradi:Aditya%40123@lil-chef.fevflcg.mongodb.net/?retryWrites=true&w=majority")

#set up mongodb

db = cluster["UserData"]
collection = db["Flask_mongo"]


def createUser(usr, hashpw, allergies, diet, age, pantry ):  
    user_name = usr 
    collection.insert_one({
        user_name:  {
            "password_hash": hashpw,
            "allergy": allergies,
            "diet_": diet,
            "age_": age,
            "pantry_": pantry}})

def getUserData(usr):
    diction= collection.find_one()
    for i in diction:
        info= i
        if info == usr:
            value= diction.get(i)
            second_val= value.values()
            final_val = list(second_val)
            return(final_val[1:])

def getAllergy(usr):
    diction = collection.find_one()
    for i in diction:
        info = i
        if info == usr:
            value = diction.get(i)
            second_val = value.values()
            final_val = list(second_val)
            return(final_val[1])

def getDiet(usr):
    diction= collection.find_one()
    for i in diction:
        info = i
        if info == usr:
            value = diction.get(i)
            second_val = value.values()
            final_val = list(second_val)
            return(final_val[2])
def getAge(usr):
    diction= collection.find_one()
    for i in diction:
        info = i
        if info == usr:
            value = diction.get(i)
            second_val= value.values()
            final_val = list(second_val)
            return(final_val[3])
        
def getPantry(usr):
    diction = collection.find_one()
    for i in diction:
        info = i
        if info == usr:
            value = diction.get(i)
            second_val = value.values()
            final_val = list(second_val)
            return(final_val)
        
def validateUser(usr,hash_pass):
    """Returns -1 if user not is database
    Returns 0 if user in database but user.hashpass != hashpass
    Returns 1 if user in database and hash_pass for the user and the parameter are the same"""
    diction = collection.find_one()
    for i in diction:
        info = i
        if info == usr:
            value = diction.get(i)
            second_val = value.values()
            final_val = list(second_val)
            if final_val[0] == hash_pass:
                return(1)
                
            else:
                return(0)
    return(-1)
def deleteUser(usr):
    diction = collection.find_one()
    for i in diction:
        info = i
        if info == usr:
            value = diction.get(i)
            collection.delete_one({usr:value})
