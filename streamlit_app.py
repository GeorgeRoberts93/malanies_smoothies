# Import python packages
import streamlit as st
from snowflake.snowpark.functions import col, when_matched # import the snowpark column function
# New section to display smoothiefroot nutrition information 
import requests 

# Write directly to the app
st.title(":cup_with_straw: Customize Your Smoothie! :cup_with_straw:")
st.write("""Choose the fruits you want in your custom Smoothie!""")

title = st.text_input('Customer Name', ' ')

st.write('The current customer name is', title)

cnx = st.connection("snowflake")
session = cnx.session()

my_dataframe = session.table("smoothies.public.fruit_options").select(col('Fruit_name'),col('search_on')) # brings back the list of fruit not the whole table 
st.dataframe(data=my_dataframe, use_container_width=True) #dont need the data frame to display 
st.stop()

# Multiselect 

ingredients_list = st.multiselect(
    'Choose up to 5 ingredients:' 
    , my_dataframe
    , max_selections=5
    )

# if statement where if ingredients list is not null then do everything below the line thats indented. 
if ingredients_list:
    
    #crate ingredients_string variable 
    ingredients_string = ''

    
    # add the for block = for each fruit_chosen in ingredients_list multislect box: do everything below this line that is inented 
    for fruit_chosen in ingredients_list:
        ingredients_string += fruit_chosen + ' '  #+= means add this to what is already in the variable. so each time the for loop is repeated a new fruit name is added
        st.subheader(fruit_chosen + ' Nutrition Information')
        smoothiefroot_response = requests.get("https://my.smoothiefroot.com/api/fruit/" + fruit_chosen)
        sf_df = st.dataframe(data=smoothiefroot_response.json(), use_container_width=True)
        
    #st.write(ingredients_string) #output the string need to be part of the if block not the for

# This takes the name and fruit selection (the variable for name is title)
    my_insert_stmt = """ insert into smoothies.public.orders(ingredients, name_on_order) values
             ('""" +ingredients_string+ """', '""" +title+ """') """

    #st.write(my_insert_stmt)
    #st.stop()

    
#add a submit order button
time_to_insert = st.button('Submit Order')
    # second if block is dependant on the submit button being clicked rather than the fruit being clicked 
    
if time_to_insert:
        session.sql(my_insert_stmt).collect()

        # this allows once the ordered is sumbited it says the fstring 
        st.success(f"Your Smoothie is ordered, {title}!", icon="✅")
