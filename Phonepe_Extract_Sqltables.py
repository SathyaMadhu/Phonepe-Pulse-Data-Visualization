import os
import json
import pandas as pd
from pathlib import Path
import mysql.connector as sql
import streamlit as st
from streamlit_option_menu import option_menu

#agg_Transaction

Path = "E:/Guvi_Data_Science/MDT33/Capstone_Project/.venv/Phonepae/pulse/data/aggregated/transaction/country/india/state/"
Agg_Trans_list = os.listdir(Path)


# Initialize the dictionary to store the data
clm = {"State": [], "Year": [], "Quarter": [], "Transaction_type": [], "Transaction_Count": [], "Transaction_Amount": []}

# Loop through the states
for state in Agg_Trans_list:
    state_list=Path+state+"/"
    year_list= os.listdir(state_list)

    # Loop through the years
    for year in year_list:
        cur_year=state_list+year+"/"
        jfiles = os.listdir(cur_year)

        # Loop through the json files
        for jfile in jfiles:
            jfiles_list=cur_year+jfile
            
            # Open the data file
            JF =open(jfiles_list, "r")
            Agg_Trans_Data = json.load(JF)

            # Extract the data from the JSON object
            for transaction in Agg_Trans_Data["data"]["transactionData"]:
                clm["Transaction_type"].append(transaction["name"])
                clm["Transaction_Count"].append(transaction["paymentInstruments"][0]["count"])
                clm["Transaction_Amount"].append(transaction["paymentInstruments"][0]["amount"])
                clm["State"].append(state)
                clm["Year"].append(year)
                clm["Quarter"].append(int(jfile.strip(".json")))

# Create the DataFrame
Agg_Trans = pd.DataFrame(clm)
Agg_Trans["State"]=Agg_Trans["State"].str.replace("andaman-&-nicobar-islands", "Andaman & Nicobar Islands")
Agg_Trans["State"]=Agg_Trans["State"].str.replace("-", " ")
Agg_Trans["State"]=Agg_Trans["State"].str.title()
Agg_Trans["State"]=Agg_Trans["State"].str.replace("Dadra & Nagar Haveli & Daman & Diu", "Dadra and Nagar Haveli and Daman and Diu")

#Agg_user

Path1 = "E:/Guvi_Data_Science/MDT33/Capstone_Project/.venv/Phonepae/pulse/data/aggregated/user/country/india/state/"
Agg_user_list = os.listdir(Path1)

# Initialize the dictionary to store the data
clm1 = {"State": [], "Year": [], "Quarter": [], "Brand": [], "Transaction_Count": [], "Percentage": []}

# Loop through the State
for state in Agg_user_list:
    state_list=Path1+state+"/"
    year_list= os.listdir(state_list)

    # Loop through the years
    for year in year_list:
        cur_year=state_list+year+"/"
        jfiles = os.listdir(cur_year)

        # Loop through the json files
        for jfile in jfiles:
            jfiles_list=cur_year+jfile
            
            # Open the data file
            JF =open(jfiles_list, "r")
            Agg_User_Data = json.load(JF)
            try:
                for user in Agg_User_Data["data"]["usersByDevice"]:
                    brand=user["brand"]
                    count=user["count"]
                    percentage=user["percentage"]
                    clm1["Brand"].append(brand)
                    clm1["Transaction_Count"].append(count)
                    clm1["Percentage"].append(percentage)
                    clm1["State"].append(state)
                    clm1["Year"].append(year)
                    clm1["Quarter"].append(int(jfile.strip(".json")))
            except:
                pass
Agg_user=pd.DataFrame(clm1)
Agg_user["State"]=Agg_user["State"].str.replace("andaman-&-nicobar-islands", "Andaman & Nicobar Islands")
Agg_user["State"]=Agg_user["State"].str.replace("-", " ")
Agg_user["State"]=Agg_user["State"].str.title()
Agg_user["State"]=Agg_user["State"].str.replace("Dadra & Nagar Haveli & Daman & Diu", "Dadra and Nagar Haveli and Daman and Diu")

#Map_Trans

Path2 = "E:/Guvi_Data_Science/MDT33/Capstone_Project/.venv/Phonepae/pulse/data/map/transaction/hover/country/india/state/"
Map_trans_list = os.listdir(Path2)

# Initialize the dictionary to store the data
clm2 = {"State": [], "Year": [], "Quarter": [], "District": [], "Transaction_Count": [], "Transaction_Amount": []}

# Loop through the states
for state in Map_trans_list:
    state_list=Path2+state+"/"
    year_list= os.listdir(state_list)

    # Loop through the years
    for year in year_list:
        cur_year=state_list+year+"/"
        jfiles = os.listdir(cur_year)

        # Loop through the json files
        for jfile in jfiles:
            jfiles_list=cur_year+jfile
            
            # Open the data file
            JF =open(jfiles_list, "r")
            Map_Trans_Data = json.load(JF)
            
            for Map in Map_Trans_Data["data"]["hoverDataList"]:
                Name=Map["name"]
                count=Map["metric"][0]["count"]
                Amount=Map["metric"][0]["amount"]
                clm2["District"].append(Name)
                clm2["Transaction_Count"].append(count)
                clm2["Transaction_Amount"].append(Amount)
                clm2["State"].append(state)
                clm2["Year"].append(year)
                clm2["Quarter"].append(int(jfile.strip(".json")))

Map_Trans=pd.DataFrame(clm2)
Map_Trans["State"]=Map_Trans["State"].str.replace("andaman-&-nicobar-islands", "Andaman & Nicobar Islands")
Map_Trans["State"]=Map_Trans["State"].str.replace("-", " ")
Map_Trans["State"]=Map_Trans["State"].str.title()
Map_Trans["District"]=Map_Trans["District"].str.title()
Map_Trans["State"]=Map_Trans["State"].str.replace("Dadra & Nagar Haveli & Daman & Diu", "Dadra and Nagar Haveli and Daman and Diu")

            
#Map_user

Path3 = "E:/Guvi_Data_Science/MDT33/Capstone_Project/.venv/Phonepae/pulse/data/map/user/hover/country/india/state/"
Map_user_list = os.listdir(Path3)

# Initialize the dictionary to store the data
clm3 = {"State": [], "Year": [], "Quarter": [], "District": [], "RegisteredUsers": [], "AppOpens": []}

# Loop through the State
for state in Map_user_list:
    state_list=Path3+state+"/"
    year_list= os.listdir(state_list)

    # Loop through the years
    for year in year_list:
        cur_year=state_list+year+"/"
        jfiles = os.listdir(cur_year)

        # Loop through the json files
        for jfile in jfiles:
            jfiles_list=cur_year+jfile
            
            # Open the data file
            JF =open(jfiles_list, "r")
            Map_User_Data = json.load(JF)

            for i in Map_User_Data["data"]["hoverData"].items():
                district=i[0]
                registeredUsers=i[1]["registeredUsers"]
                appOpens=i[1]["appOpens"]
                clm3["District"].append(district)
                clm3["RegisteredUsers"].append(registeredUsers)
                clm3["AppOpens"].append(appOpens)
                clm3["State"].append(state)
                clm3["Year"].append(year)
                clm3["Quarter"].append(int(jfile.strip(".json")))

Map_User=pd.DataFrame(clm3)
Map_User["State"]=Map_User["State"].str.replace("andaman-&-nicobar-islands", "Andaman & Nicobar Islands")
Map_User["State"]=Map_User["State"].str.replace("-", " ")
Map_User["State"]=Map_User["State"].str.title()
Map_User["District"]=Map_User["District"].str.title()
Map_User["State"]=Map_User["State"].str.replace("Dadra & Nagar Haveli & Daman & Diu", "Dadra and Nagar Haveli and Daman and Diu")

            
 
#Top_trans

Path4 = "E:/Guvi_Data_Science/MDT33/Capstone_Project/.venv/Phonepae/pulse/data/top/transaction/country/india/state/"
Top_Trans_list = os.listdir(Path4)

# Initialize the dictionary to store the data
clm3 = {"State": [], "Year": [], "Quarter": [], "Pincodes": [], "Transaction_count": [], "Transaction_amount": []}

# Loop through the states
for state in Top_Trans_list:
    state_list=Path4+state+"/"
    year_list= os.listdir(state_list)

    # Loop through the years
    for year in year_list:
        cur_year=state_list+year+"/"
        jfiles = os.listdir(cur_year)

        # Loop through the json files
        for jfile in jfiles:
            jfiles_list=cur_year+jfile
            
            # Open the data file
            JF =open(jfiles_list, "r")
            Top_trans_Data = json.load(JF)

            for i in Top_trans_Data["data"]["pincodes"]:
                entityName=i["entityName"]
                count=i["metric"]["count"]
                amount=i["metric"]["amount"]
                clm3["Pincodes"].append(entityName)
                clm3["Transaction_count"].append(count)
                clm3["Transaction_amount"].append(amount)
                clm3["State"].append(state)
                clm3["Year"].append(year)
                clm3["Quarter"].append(int(jfile.strip(".json")))

Top_trans=pd.DataFrame(clm3)
Top_trans["State"]=Top_trans["State"].str.replace("andaman-&-nicobar-islands", "Andaman & Nicobar Islands")
Top_trans["State"]=Top_trans["State"].str.replace("-", " ")
Top_trans["State"]=Top_trans["State"].str.title()
Top_trans["State"]=Top_trans["State"].str.replace("Dadra & Nagar Haveli & Daman & Diu", "Dadra and Nagar Haveli and Daman and Diu")


#Top_user

Path5 = "E:/Guvi_Data_Science/MDT33/Capstone_Project/.venv/Phonepae/pulse/data/top/user/country/india/state/"
Top_User_list = os.listdir(Path5)

# Initialize the dictionary to store the data
clm4 = {"State": [], "Year": [], "Quarter": [], "Pincodes": [], "RegisteredUsers": []}

# Loop through the states
for state in Top_User_list:
    state_list=Path5+state+"/"
    year_list= os.listdir(state_list)

    # Loop through the years
    for year in year_list:
        cur_year=state_list+year+"/"
        jfiles = os.listdir(cur_year)

        # Loop through the json files
        for jfile in jfiles:
            jfiles_list=cur_year+jfile
            
            # Open the data file
            JF =open(jfiles_list, "r")
            Top_user_Data = json.load(JF)


            for i in Top_user_Data["data"]["pincodes"]:
                name=i["name"]
                registeredUsers=i["registeredUsers"]
                clm4["Pincodes"].append(name)
                clm4["RegisteredUsers"].append(registeredUsers)
                clm4["State"].append(state)
                clm4["Year"].append(year)
                clm4["Quarter"].append(int(jfile.strip(".json")))


Top_user=pd.DataFrame(clm4)
Top_user["State"]=Top_user["State"].str.replace("andaman-&-nicobar-islands", "Andaman & Nicobar Islands")
Top_user["State"]=Top_user["State"].str.replace("-", " ")
Top_user["State"]=Top_user["State"].str.title()
Top_user["State"]=Top_user["State"].str.replace("Dadra & Nagar Haveli & Daman & Diu", "Dadra and Nagar Haveli and Daman and Diu")

           