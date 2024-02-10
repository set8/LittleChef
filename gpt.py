from openai import OpenAI
from pprint import pprint
import json
from dish import Dish

'''
Test #1
Theoretical User Data
'''
userdata = {
    'pantry' : {
        "bread": "12 slices",          # 3 packages of pasta
        "ground meat": "5 lbs",           # 5 pounds of rice
        "lemons": "4",        # 2 pounds of almonds
        "tomatos": "12",   # 4 cans of tomato sauce
        "flour": "1 bag",          # 1 bag of flour
        "chocolate chips": "4 bags",# 3 bags of chocolate chips
        "olive oil": "12 floz",      # 1 bottle of olive oil
        "canned beans": "1 can",   # 6 cans of beans
        "canned corn": "1 box",      # 2 packages of spaghetti
        "eggs": "1 dozen"          # 2 pounds of quinoa
    },

        "allergies": "Nuts", 
        "diet": "Vegetarian", 
        "age": 25
}
    
goob = Dish(userdata)
print(goob)


