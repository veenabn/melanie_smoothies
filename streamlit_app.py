# Import python packages
import streamlit as st
import requests
import pandas
from snowflake.snowpark.functions import col

# Write directly to the app
st.title(":cup_with_straw: Customise Your Smoothie :cup_with_straw:")
st.write(
    """Choose the fruits you want in your smoothie!.
    """
)

name_on_order = st.text_input('Name on the Smoothie:')
st.write('Name on your Smoothie will be ',name_on_order  )
cnx = st.connection("snowflake")
session = cnx.session()
my_dataframe = session.table("smoothies.public.fruit_options").select(col('FRUIT_NAME'), col('SEARCH_ON'))
#st.dataframe(data=my_dataframe, use_container_width=True)
#st.stop()
# Convert Snowflake dataframe to pandas snowframe
pd_df= my_dataframe.to_pandas()
#st.dataframe(pd_df)
#st.stop()

ingredient_list = st.multiselect('choose up to 5 ingredients:', my_dataframe,max_selections=5)

if ingredient_list:
    #st.write(ingredient_list)
    st.text(ingredient_list)
    ingredients_string = ''
    for fruit_chosen in ingredient_list:
        ingredients_string +=fruit_chosen + ' '
        search_on=pd_df.loc[pd_df['FRUIT_NAME'] == fruit_chosen, 'SEARCH_ON'].iloc[0]
        #st.write('The search value for ', fruit_chosen,' is ', search_on, '.')
        st.subheader(fruit_chosen + 'Nutrition Informatuion')
        fruityvice_response = requests.get("https://fruityvice.com/api/fruit/" + search_on )
        fv_df = st.dataframe( data = fruityvice_response.json(),use_container_width=True)


    my_insert_stmt = """ insert into smoothies.public.orders(ingredients,name_on_order)
            values ('""" + ingredients_string + """' ,  '""" +name_on_order+ """')"""
     
    #st.write(my_insert_stmt)
    #st.stop
    time_to_insert = st.button('Submit Order')
    if time_to_insert:
        session.sql(my_insert_stmt).collect()
        st.success('Your Smoothie is ordered ' +  name_on_order + '!', icon="✅")
