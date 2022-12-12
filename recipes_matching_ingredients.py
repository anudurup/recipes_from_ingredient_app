import glob
import os
import json
import streamlit as st

def get_recipes_matching_ingredient(ingr):
    files = glob.glob('segregated_recipes/**/*.json')
    total_dict = dict()
        
    for file in files:
        f = open(file)
        file_dict = json.load(f)      
        recipe_dict = file_dict["ingredients"]
        url_dict = file_dict["recipe_url"]
        for key,values in recipe_dict.items():
            if ingr in values:
                location = "Meal: " + os.path.basename(file).replace('.json','')
                total_dict[key] = [location,values,url_dict[key]] 
    return total_dict

def intersection(lst1, lst2):
    return list(set(lst1) & set(lst2))

def find_recipes_with_max_matched_ingredients(ingr_list):
    total_dict = get_recipes_matching_ingredient(ingr_list[0])    
    intersection_recipe_names = list(total_dict.keys())

    for ingr in ingr_list[1:]:
        total_dict = get_recipes_matching_ingredient(ingr)
        recipe_list = list(total_dict.keys())
        intersection_recipe_names = intersection(intersection_recipe_names, recipe_list)
    
    intersection_locations = list()
    intersection_ingredients = list()
    intersection_urls = list()
    for recipe_name in intersection_recipe_names:
        intersection_locations.append(total_dict[recipe_name][0]) 
        intersection_ingredients.append(total_dict[recipe_name][1])
        intersection_urls.append(total_dict[recipe_name][2])
    return intersection_recipe_names,intersection_locations,intersection_ingredients,intersection_urls

def get_ingredient_list():
    with open('ingredient_list.txt','r') as f:
        ingredient_list = f.readlines()
    return ingredient_list

def write_ingredient(ingredient_list):
    with open('ingredient_list.txt','w+') as f:
        f.writelines(ingredient_list)

ingredient_list = get_ingredient_list()

def add_ingredient():
    ingr = st.session_state["ingr"] + "\n"
    ingredient_list.append(ingr)
    write_ingredient(ingredient_list)

st.set_page_config(layout = "wide")
st.title("Find recipes for your ingredient")
st.subheader("Enter ingredients you want in the recipes you are searching for.")

st.text_input(label="Enter ingredient", placeholder="Enter ingredient...",
on_change=add_ingredient, key="ingr")

for index, ingr in enumerate(ingredient_list):
    checkbox = st.checkbox(ingr, key=ingr)
    if checkbox:
        ingredient_list.pop(index)
        write_ingredient(ingredient_list)
        del st.session_state[ingr]
        st.experimental_rerun()

if (ingredient_list):
    usable_list = [x.rstrip() for x in ingredient_list]
    intersection_recipe_names,intersection_locations,intersection_ingredients,intersection_urls = find_recipes_with_max_matched_ingredients(usable_list)
    #for index,recipe_name in enumerate(intersection_recipe_names):
    location_flag = 1
    prev_location = ''
    for index,location in enumerate(intersection_locations):
        if (location_flag) or (prev_location != location):
            st.subheader(intersection_locations[index])
            location_flag = 0
    #st.write(intersection_locations[index])
        st.write(intersection_recipe_names[index])
        st.write(intersection_ingredients[index])
        st.write(intersection_urls[index])
        prev_location = location