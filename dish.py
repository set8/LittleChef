from openai import OpenAI
import json
from os import environ
# from ratelimit import limits, sleep_and_retry
from dotenv import load_dotenv

load_dotenv()

apk = "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"


client = OpenAI(api_key = apk)

def generate(userdata):
    
    food_names = []
    food_quantity = []

    for i in userdata['pantry'].keys():
        food_names.append(i)
        
    for i in userdata['pantry'].values():
        food_quantity.append(i)


    restrictions = f"The person you are cooking for someone who is allergic to {userdata['allergies']}"
    restrictions+=f". The person you are cooking for is on a {userdata['diet']}."
    if userdata["age"]<21:
        
        restrictions+=f" The person you are cooking for is {userdata['age']} do not include any substances that would be illegal for them to consume "

    response_1 = client.chat.completions.create(
        messages=[
            
        {
        "role": "system", "content": "You are provided with a specific list of ingredients and their available quantities. Your task is to create a recipe that"
         +" adheres to the provided dietary restrictions. The recipe must exclusively use the ingredients listed and must not exceed the available quantities." 
         +"It is imperative to follow the dietary restrictions closely, ensuring the recipe is suitable for the consumer's needs. FOLLOW ANY INSTRUCTIONS TELLONG YOU TO PRINT ON A NEW LINE"
         },
        
        
        {
        "role":"user", "content":f"Please create a recipe using any combination of these ingredients: {food_names} without exceeding the quantities provided: {food_quantity}."
        +f"The recipe must comply with the following dietary restrictions: {restrictions}. Once you select a recipe, begin by printing the recipe title."
        +"Then, on a seperate line, print 'Ingredients:' followed by, on a seperate line, a list of the ingredients with the quantities used in the format 'ingredient name: quantity used'."
        +"Next, on a spereate line, print out 'Instructions:', and then on a new line, start listing the preparation steps in order, the instructions cannot mentino any ingredients that were not"
        +"mentinoed in the ingredients list. Ensure the ingredient quantities used do not exceed what's available"
        +"and strictly adhere to the dietary restrictions specified. The name of the dish must remain consistent throughout the description. "
        +"Prioritize the safety and dietary needs of the consumer by strictly adhering to the restrictions provided."
        }
        
    ],    
        
        model = "gpt-3.5-turbo-0125"
            
    )
    
    
    output = json.loads(response_1.json())["choices"][0]["message"]["content"].split('\n')
    output = [x for x in output if x]
    return output

def getName(userdata):
    return generate(userdata)[0]
    
        
def getIngredients(userdata):
    output = generate(userdata)
    a = output.index('Ingredients:')
    b = output.index('Instructions:')
    return output[a:b]
    
def getRecipe(userdata):
    output = generate(userdata)
    return output[output.index('Instructions:'):]
        
def getImage(userdata):
    
    output = generate(userdata)
    
    response_2 = client.images.generate(
        model="dall-e-2",
        prompt=f"Make a picture of {generate(userdata)[0]},  be really simple"
        +f"the dish should reflect the ingredients used {output[output.index('Ingredients:'):output.index('Instructions:')]}, "
        +"there should be nothing else but the dish in the image",
        size="1024x1024",
        quality="standard",
        n=1,
    )

    image_url = response_2.data[0].url
    return image_url

class Dish:
    dishes = []

    def __init__(self, userdata):
        self.name = getName(userdata)
        self.ingredients = [x[1:] for x in getIngredients(userdata)][1:]
        self.recipe = [x[2:] for x in getRecipe(userdata)][1:]
        self.image = getImage(userdata)
        
        Dish.dishes.append(self)

    def __str__(self):
        return f"{self.name}:{self.image}\n\n{self.ingredients}\n\n{self.recipe}"