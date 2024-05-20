import streamlit as st
import pandas as pd
import json 
import os
import mysql.connector as sql
import requests
from streamlit_option_menu import option_menu
import plotly.express as px
import seaborn as sns
import matplotlib.pyplot as plt

connection = sql.connect(
                    host="localhost",
                    user="root",
                    password="Nisama@2021",
                    database="phonepae")

            
#streamlit part

st.set_page_config(layout = "wide")

st.title("PHONEPAE PULSE DATA VISUVALISATION and EXPLORATION USING STREAMLIT AND PLOTLY")

with st.sidebar:
    
    select = option_menu ("Main Menu",["TRANSACTION ANALYSIS", "USER ANALYSIS", "INSIGHTS"])

if select=="HOME":
        pass

elif select=="TRANSACTION ANALYSIS":

    # Define tabs for Transaction and User Analysis
    tab1, tab2,tab3= st.tabs(["AGGREGATED ANALYSIS", "DISTRICT ANALYSIS","PINCODE ANALYSIS"])
   
    with tab1:
        Module=st.radio("Select the Module", ["AGGREGATED DATA EXPLORATION", "AGGREGATED TRANS ANALYSIS", "AGGREGATED TRANSTYPE ANALYSIS"])
   
        if Module == "AGGREGATED DATA EXPLORATION":

            # Aggregate Analysis Subtab
            def Aggregated_DataExploration_tab():
                
                col1, col2, col3 = st.columns(3)

                with col1:
                    
                    Year = st.selectbox('Year', ['2018', '2019', '2020', '2021', '2022', '2023'])

                with col2:
                    
                    Quarter = st.selectbox('Quarter', ['1', '2', '3', '4'])

                with col3:
                
                    Transaction_type = st.selectbox('Transaction Type',
                                                            ['Recharge & bill payments', 
                                                             'Peer-to-peer payments',
                                                            'Merchant payments', 'Financial Services', 'Others'])
                            

                with st.expander("Transaction Amount Data"):
                    connection = sql.connect(
                    host="localhost",
                    user="root",
                    password="Nisama@2021",
                    database="phonepae")

                    cursor=connection.cursor()

                    cursor.execute("select* from Agg_Trans")
                    table1 = cursor.fetchall()
                    Agg_Trans1 = pd.DataFrame(table1, columns=("State", "Year", "Quarter", "Transaction_type", 
                                                           "Transaction_Count", "Transaction_Amount"))

                    transaction_query = f"""
                    SELECT State, Year, Transaction_amount, Transaction_type
                    FROM agg_trans
                    WHERE Year = '{Year}' 
                    AND Quarter = '{Quarter}'

                    AND Transaction_type = '{Transaction_type}'"""

                    cursor.execute(transaction_query)
                    transaction_data = cursor.fetchall()
                    connection.commit()
                    transaction_df = pd.DataFrame(transaction_data, columns=['State', 'Year', 'Transaction_amount', 'Transaction_type'])
                

                
                col1,col2=st.columns(2)
                
                with col1:

                    # Visualize data as a bar chart
                    color_map = {'Recharge & bill payments': 'yellow', 'Peer-to-peer payments': 'blue', 
                                'Merchant payments': 'red', "Financial Services" : "white", "Others" : "green"}
                    transaction_df_sorted = Agg_Trans1.sort_values(by='Transaction_Amount', ascending=False)
                    Fig_Tran_Amount = px.bar(transaction_df_sorted, x='State', y='Transaction_Amount', color='Transaction_type',
                                    labels={'Transaction_amount': 'Transaction Amount'}, color_discrete_map=color_map)
                    Fig_Tran_Amount.update_layout(title={'text': f" TRANSACTION_AMOUNT  Vs  year : {Year} Quarter : {Quarter}", 
                                                        'x': 0.4, 'xanchor': 'center'}, width=600, height=600,
                                                        legend=dict(x=0.01, y=-1.00, orientation='h'))
                    st.plotly_chart(Fig_Tran_Amount)

                    with st.expander("Transaction Count Data"):
                        transaction_count_query = f"""
                        SELECT State, Year, Quarter, Transaction_count,Transaction_type
                        FROM agg_trans
                        WHERE Year = '{Year}' 
                        AND Quarter = '{Quarter}'
                        AND Transaction_type = '{Transaction_type}'"""

                        cursor.execute(transaction_count_query)
                        transaction_count_data = cursor.fetchall()
                        connection.commit()
                        transaction_count_df = pd.DataFrame(transaction_count_data, columns=['State', 'Year', 'Quarter','Transaction_count', 'Transaction_type'])

                with col2:
                    # Visualize data using Plotly Bar Chart
                    trans_count_df_sorted = transaction_count_df.sort_values(by='Transaction_count', ascending=False)
                    color_map = {'Recharge & bill payments': 'yellow', 'Peer-to-peer payments': 'lightblue', 
                                'Merchant payments': 'orange', "Financial Services" : "white", "Others" : "grey"}
                    Fig_Tran_count = px.bar(trans_count_df_sorted, x='State', y='Transaction_count', 
                                            color='Transaction_type',
                                    labels={'Transaction_count': 'Transaction count'}, 
                                    color_discrete_map=color_map)
                    Fig_Tran_count.update_layout(title={'text': f" TRANSACTION_COUNT  Vs  year : {Year} Quarter : {Quarter}", 
                                                        'x': 0.4, 'xanchor': 'center'}, width=600, height=600,
                                                        legend=dict(x=0.55, y=1.10, orientation='h'))
                    st.plotly_chart(Fig_Tran_count)

                with col1:
                        Fig_TAIndia_1 = px.choropleth(transaction_df, geojson="https://gist.githubusercontent.com/jbrobst/56c13bbbf9d97d187fea01ca62ea5112/raw/e388c4cae20aa53cb5090210a42ebb9b765c0a36/india_states.geojson", 
                                                  locations="State", featureidkey="properties.ST_NM",
                                                    color="Transaction_amount", color_continuous_scale="blues",
                                                    range_color=(transaction_df["Transaction_amount"].min(),transaction_df["Transaction_amount"].max()),
                                                    hover_name="State", title=f" TRANSACTION_AMOUNT Vs. State", fitbounds="locations",
                                                    )
                        Fig_TAIndia_1.update_geos(visible=False)
                        st.plotly_chart(Fig_TAIndia_1)

                with col2:    
                    Fig_TCIndia_2 = px.choropleth(transaction_count_df, geojson="https://gist.githubusercontent.com/jbrobst/56c13bbbf9d97d187fea01ca62ea5112/raw/e388c4cae20aa53cb5090210a42ebb9b765c0a36/india_states.geojson", 
                                                  locations="State", featureidkey="properties.ST_NM",
                                            color="Transaction_count", color_continuous_scale="greens",
                                            range_color=(transaction_count_df["Transaction_count"].min(),transaction_count_df["Transaction_count"].max()),
                                            hover_name="State",title=f" TRANSACTION_COUNT Vs. State",
                                            fitbounds="locations")
                    Fig_TCIndia_2.update_geos(visible=False)
                    st.plotly_chart(Fig_TCIndia_2)
                                    
        # AGGREGATED DATA EXPLORATION 
        if Module == "AGGREGATED DATA EXPLORATION":
            Aggregated_DataExploration_tab()

        elif  Module=="AGGREGATED TRANS ANALYSIS":
            st.markdown("## :violet[AGGREGATED TRANS ANALYSIS]")
            def Agg_transaction_tab():
                connection = sql.connect(
                    host="localhost",
                    user="root",
                    password="Nisama@2021",
                    database="phonepae")

                col1, col2 = st.columns(2)
                
                with col1:
                
                    State = st.selectbox('**State**', (
                            'Andaman & Nicobar Islands', 'Andhra Pradesh', 'Arunachal Pradesh', 'Assam', 'Bihar', 'Chandigarh', 
                            'Chhattisgarh', 'Dadra and Nagar Haveli and Daman and Diu', 'Delhi', 'Goa', 'Gujarat', 'Haryana', 
                            'Himachal Pradesh', 'Jammu & Kashmir', 'Jharkhand', 'Karnataka', 'Kerala', 'Ladakh', 'Lakshadweep', 
                            'Madhya Pradesh', 'Maharashtra', 'Manipur', 'Meghalaya', 'Mizoram', 'Nagaland', 'Odisha', 'Puducherry', 
                            'Punjab', 'Rajasthan', 'Sikkim', 'Tamil Nadu', 'Telangana', 'Tripura', 'Uttar Pradesh', 'Uttarakhand', 
                            'West Bengal'), key='State')

                with col2:
                    pass
                
                st.markdown("## :LEMONYELLOW[TOTAL TRANSACTION DATA]")
                
                 
                cursor=connection.cursor()
                # Execute query to get total and average transaction amount
                total_trans_query = f"""SELECT 'Sum' as Agg, SUM(Transaction_amount) as Trans_Amount,
                                        sum(Transaction_count) as Trans_count
                                        FROM agg_trans 
                                        WHERE State = '{State}'
                                        union all
                                        Select 'Average' as Agg, Avg(Transaction_amount) as Trans_Count,
                                        avg(Transaction_count) as Trans_count
                                        FROM agg_trans  
                                        WHERE State = '{State}'"""
                cursor.execute(total_trans_query)
                total_amount_data = cursor.fetchall()
                df_state_total_trans = pd.DataFrame(total_amount_data, columns=['Agg','Trans_Amount', 'Trans_Count'])
                df_state_total_trans['Index'] = range(1, len(df_state_total_trans) + 1)
                df_state_total_trans.set_index('Index', inplace=True)
                st.dataframe(df_state_total_trans)
                
                with st.expander("Transaction Amount Data"):
                    
                    query = f"""
                    SELECT Year, Transaction_Amount
                    FROM agg_trans
                    Where State = '{State}'
                    """
                    cursor.execute(query)
                    transaction_data = cursor.fetchall()
                    connection.commit()
                    Statetransaction_df = pd.DataFrame(transaction_data, columns=['Year', 'Transaction_Amount'])
                
                col1,col2=st.columns(2)
                with col1:
                    
                
                    # Visualize data as a bar chart
                    Statetransaction_df_sorted = Statetransaction_df.sort_values(by='Transaction_Amount', ascending=False)
                    Fig_Tran_Amount = px.bar(Statetransaction_df_sorted, x='Year', y='Transaction_Amount',
                                    labels={'Transaction_amount': 'Transaction Amount'})
                    Fig_Tran_Amount.update_layout(title={'text': f" TRANSACTION AMOUNT by {State}", 
                                                        'x': 0.4, 'xanchor': 'center'}, width=600, height=600,
                                                        legend=dict(x=0.45, y=1.05, orientation='h'))
                    st.plotly_chart(Fig_Tran_Amount)

                    with st.expander("Transaction Count Data"):
                        transaction_count_query = f"""
                        SELECT Year, Transaction_count
                        FROM agg_trans
                        Where State = '{State}'"""

                        cursor.execute(transaction_count_query)
                        transaction_count_data = cursor.fetchall()
                        connection.commit()
                        transaction_count_df = pd.DataFrame(transaction_count_data, columns=['Year', 'Transaction_count'])

                with col2:
                    # Visualize data using Plotly Bar Chart
                    trans_count_df_sorted = transaction_count_df.sort_values(by='Transaction_count', ascending=False)
                    Fig_Tran_count = px.bar(trans_count_df_sorted, x='Year', y='Transaction_count', 
                                    labels={'Transaction_count': 'Transaction count'})
                    Fig_Tran_count.update_layout(title={'text': f" TRANSACTION COUNT  by {State}", 
                                                        'x': 0.4, 'xanchor': 'center'}, width=600, height=600,
                                                        legend=dict(x=0.55, y=1.10, orientation='h'))
                    st.plotly_chart(Fig_Tran_count)

               
                
                st.markdown("## :Magenta[DISTRIBUTION OF TRANSACTION TYPE  DATA BY STATE]")
                    
            # Fetch transaction data from MySQL
                State_trans_query = f"""
                SELECT State, Transaction_amount, Transaction_type,Transaction_count
                FROM agg_trans
                WHERE State = '{State}'
                """

                cursor.execute(State_trans_query)
                state_trans_data = cursor.fetchall()

                # Create DataFrame
                df = pd.DataFrame(state_trans_data, columns=['State',
                                                            'Transaction_amount', 
                                                            'Transaction_type','Transaction_count'])

                    
                col1,col2=st.columns(2)
                                
                with col1:
                # Plot pIE chart for transaction amounts by state
                    Pie_fig_TA= px.pie(df, names='Transaction_type', values='Transaction_amount')
                    Pie_fig_TA.update_layout(title= {'text': f"Transaction Type by Amount"},
                                            legend=dict(x=1, y=1.05, orientation='h'))
                    st.plotly_chart(Pie_fig_TA)
                
                with col2:
                    
                    # Plot pie chart for transaction amounts by transaction type
                    pie_fig_TC = px.pie(df, names='Transaction_type', values='Transaction_count')
                    pie_fig_TC.update_layout(title= {'text': f"Transaction Type by Count"})
                    pie_fig_TC.update_layout(title_x=0.15)
                    st.plotly_chart(pie_fig_TC)
                
        if  Module =="AGGREGATED TRANS ANALYSIS":
                Agg_transaction_tab()
        
        elif Module =="AGGREGATED TRANSTYPE ANALYSIS":
             def transtype_year_analysis():
            
                connection = sql.connect(
                                    host="localhost",
                                    user="root",
                                    password="Nisama@2021",
                                    database="phonepae")

                cursor=connection.cursor()
                
                cursor.execute("select* from agg_Trans")
                table5 = cursor.fetchall()
                Agg_Trans1 = pd.DataFrame(table5, columns=("State", "Year", "Quarter", "Transaction_type", "Transaction_Count", "Transaction_Amount"))
                
                col1,col2 = st.columns(2)
                with col1:
                    Transaction_type = st.selectbox("**Transaction_type**",Agg_Trans1["Transaction_type"].unique(), key='Transaction_type')
                with col2:
                     pass
                with col1:
                    
                    PTA = Agg_Trans1[(Agg_Trans1["Transaction_type"]==Transaction_type)]                     
                    PTA=PTA.groupby("Year")[["Transaction_Amount", "Transaction_Count"]].sum()
                    PTA.reset_index(inplace=True)
                    PTA_sorted = PTA.sort_values(by='Transaction_Amount', ascending=False)
                
                st.markdown("## :Orange[Total Transacion Type Data]")
                cursor=connection.cursor()
                
                # Execute query to get total and average transaction amount
                total_trans_query = f"""SELECT 'Sum' as Agg, SUM(Transaction_amount) as Trans_Amount,
                                        sum(Transaction_count) as Trans_count
                                        FROM agg_trans 
                                        WHERE Transaction_type = '{Transaction_type}'
                                        union all
                                        Select 'Average' as Agg, Avg(Transaction_amount) as Trans_Count,
                                        avg(Transaction_count) as Trans_count
                                        FROM agg_trans  
                                        WHERE Transaction_type = '{Transaction_type}'"""
                cursor.execute(total_trans_query)
                total_amount_data = cursor.fetchall()
                df_state_total_trans = pd.DataFrame(total_amount_data, columns=['Agg','Trans_Amount', 'Trans_Count'])
                df_state_total_trans['Index'] = range(1, len(df_state_total_trans) + 1)
                df_state_total_trans.set_index('Index', inplace=True)
                st.dataframe(df_state_total_trans)
               
                with st.expander("Transaction_type Analysis"):
                    st.markdown("## :Yellow[Transaction_type Data Year wise]")
                    st.dataframe(PTA_sorted)

                col1,col2=st.columns(2)
                with col1:
                    # Plot bar chart for Transaction_Amount
                    Fig_Tran_Amount = px.bar(PTA_sorted, x='Year', y='Transaction_Amount', color='Transaction_Amount',
                                            title = "TRANSACTION_AMOUNT vs Year",
                                                        labels={'Transaction_amount': 'Transaction Amount'})
                    Fig_Tran_Amount.update_layout(title={'text': f" TRANSACTION_AMOUNT vs {Transaction_type}", 
                                                                        'x': 0.4, 'xanchor': 'center'}, width=600, height=600,
                                                                        showlegend = False)
                    st.plotly_chart(Fig_Tran_Amount)

                
                with col2:   
                    # Plot bar chart for Transaction_Count
                    Fig_Tran_Count = px.bar(PTA_sorted, x='Year', y='Transaction_Count', color='Transaction_Count',
                                            title = "TRANSACTION_COUNT vs Year",
                                                        labels={'Transaction_Count': 'Transaction Count'})
                    Fig_Tran_Count.update_layout(title={'text': f" TRANSACTION_COUNT vs {Transaction_type}", 
                                                                        'x': 0.4, 'xanchor': 'center'}, width=600, height=600,
                                                                        showlegend = False)
                    st.plotly_chart(Fig_Tran_Count)
                
        if Module =="AGGREGATED TRANSTYPE ANALYSIS":
             transtype_year_analysis()

    
    with tab2:
            
        Method=st.radio("Select the Method", ["DISTRICT DATAEXPLORATION ANALYSIS", "DISTRICT TRANSACTION ANALYSIS", "DISTRICT YEARWISE ANALYSIS"])
        
        if Method=="DISTRICT DATAEXPLORATION ANALYSIS":

            #District Transaction Analysis
            def District_dataexp_tab():   

                connection = sql.connect(
                        host="localhost",
                        user="root",
                        password="Nisama@2021",
                        database="phonepae")

                cursor=connection.cursor()
                #Map_trans_Dataframe
                cursor.execute("select* from Map_trans")
                table3 = cursor.fetchall()
                Map_trans1 = pd.DataFrame(table3, columns=("State", "Year", "Quarter", "District", "Transaction_Count", "Transaction_Amount"))
                Map_trans1['Year'] = Map_trans1['Year'].astype(str).str.replace(',', '')
                Map_trans1['Transaction_Count'] = Map_trans1['Transaction_Count'].astype(str).str.replace(',', '')
                Map_trans1['Transaction_Amount'] = Map_trans1['Transaction_Amount'].astype(str).str.replace(',', '')
        
                col1,col2,col3 = st.columns(3)
                with col1:
                    State = st.selectbox("**State**",Map_trans1["State"].unique())
                with col2 :
                    Year = st.selectbox("**Year**",Map_trans1["Year"].unique())
                with col3:
                    Quarter = st.selectbox("**Quarter**",Map_trans1["Quarter"].unique())
                with col1:
                    
                    DTA = Map_trans1[(Map_trans1["State"] == State) & (Map_trans1["Year"]==Year) & 
                                                            (Map_trans1["Quarter"] == Quarter)]
                    DTA=DTA.groupby("District")[["Transaction_Amount", "Transaction_Count"]].sum()
                    DTA_sorted = DTA.sort_values(by='Transaction_Amount', ascending=False)
                
                with st.expander("District Transaction Data"):
                    st.dataframe(DTA_sorted)

                col1,col2=st.columns(2)
                with col1:
                    # Plot bar chart for Transaction_Amount
                    Fig_Tran_Amount = px.bar(DTA_sorted, x=DTA_sorted.index, y='Transaction_Amount', color='Transaction_Amount',
                                             title = "TRANSACTION_AMOUNT vs District",
                                                        labels={'Transaction_amount': 'Transaction Amount'})
                    Fig_Tran_Amount.update_layout(title={'text': f" TRANSACTION_AMOUNT vs District", 
                                                                        'x': 0.4, 'xanchor': 'center'}, width=600, height=600,
                                                                        showlegend = False)
                    st.plotly_chart(Fig_Tran_Amount)

                
                with col2:   
                    # Plot bar chart for Transaction_Count
                    Fig_Tran_Count = px.bar(DTA_sorted, x=DTA_sorted.index, y='Transaction_Count', color='Transaction_Count',
                                             title = "TRANSACTION_COUNT vs District",
                                                        labels={'Transaction_Count': 'Transaction Count'})
                    Fig_Tran_Count.update_layout(title={'text': f" TRANSACTION_COUNT vs District", 
                                                                        'x': 0.4, 'xanchor': 'center'}, width=600, height=600,
                                                                        showlegend = False)
                    st.plotly_chart(Fig_Tran_Count)
        
        if Method=="DISTRICT DATAEXPLORATION ANALYSIS":
                    District_dataexp_tab()
      
        elif Method=="DISTRICT TRANSACTION ANALYSIS":
            
            st.markdown("## :Yellow[DISTRICT TRANSACTION ANALYSIS]")
            def dt_transaction_tab():
                
                col1, col2 = st.columns(2)
                
                with col1:
                
                    State = st.selectbox('**State**', (
                            'Andaman & Nicobar Islands', 'Andhra Pradesh', 'Arunachal Pradesh', 'Assam', 'Bihar', 'Chandigarh', 
                            'Chhattisgarh', 'Dadra and Nagar Haveli and Daman and Diu', 'Delhi', 'Goa', 'Gujarat', 'Haryana', 
                            'Himachal Pradesh', 'Jammu & Kashmir', 'Jharkhand', 'Karnataka', 'Kerala', 'Ladakh', 'Lakshadweep', 
                            'Madhya Pradesh', 'Maharashtra', 'Manipur', 'Meghalaya', 'Mizoram', 'Nagaland', 'Odisha', 'Puducherry', 
                            'Punjab', 'Rajasthan', 'Sikkim', 'Tamil Nadu', 'Telangana', 'Tripura', 'Uttar Pradesh', 'Uttarakhand', 
                            'West Bengal'), key='State12')

                with col2:
                    pass
                
                st.markdown("## :LEMONYELLOW[TOTAL TRANSACTION DATA]")
                
                 
                cursor=connection.cursor()
                # Execute query to get total and average transaction amount
                total_trans_query = f"""SELECT 'Sum' as Agg, SUM(Transaction_amount) as Trans_Amount,
                                        sum(Transaction_count) as Trans_count
                                        FROM map_trans 
                                        WHERE State = '{State}'
                                        union all
                                        Select 'Average' as Agg, Avg(Transaction_amount) as Trans_Count,
                                        avg(Transaction_count) as Trans_count
                                        FROM map_trans  
                                        WHERE State = '{State}'"""
                cursor.execute(total_trans_query)
                total_amount_data = cursor.fetchall()
                df_state_total_trans = pd.DataFrame(total_amount_data, columns=['Agg','Trans_Amount', 'Trans_Count'])
                df_state_total_trans['Index'] = range(1, len(df_state_total_trans) + 1)
                df_state_total_trans.set_index('Index', inplace=True)
                st.dataframe(df_state_total_trans)
                
                st.markdown("## :Magenta[DISTRIBUTION OF TRANSACTION DATA BY DISTRICT]")
                    
            # Fetch transaction data from MySQL
                State_trans_query = f"""
                SELECT State, Transaction_amount, District,Transaction_count
                FROM map_trans
                WHERE State = '{State}'
                """

                cursor.execute(State_trans_query)
                state_trans_data = cursor.fetchall()

                # Create DataFrame
                df = pd.DataFrame(state_trans_data, columns=['State',
                                                            'Transaction_amount', 
                                                            'District','Transaction_count'])

                    
                col1,col2=st.columns(2)
                                
                with col1:
                # Plot pIE chart for transaction amounts by state
                    Pie_fig_TA= px.pie(df, names='District', values='Transaction_amount')
                    Pie_fig_TA.update_layout(title= {'text': f"Transaction Amount by {State}"},
                                            legend=dict(x=1, y=1.05, orientation='h'))
                    st.plotly_chart(Pie_fig_TA)
                
                with col2:
                    
                    # Plot pie chart for transaction amounts by transaction type
                    pie_fig_TC = px.pie(df, names='District', values='Transaction_count')
                    pie_fig_TC.update_layout(title= {'text': f"Transaction Count by {State}"})
                    pie_fig_TC.update_layout(title_x=0.15)
                    st.plotly_chart(pie_fig_TC)
                
        if  Method =="DISTRICT TRANSACTION ANALYSIS":
                dt_transaction_tab()
        
        elif Method =="DISTRICT YEARWISE ANALYSIS":
             def dt_year_analysis():
            
                connection = sql.connect(
                                    host="localhost",
                                    user="root",
                                    password="Nisama@2021",
                                    database="phonepae")

                cursor=connection.cursor()
                
                cursor.execute("select* from map_Trans")
                table5 = cursor.fetchall()
                Map_Trans1 = pd.DataFrame(table5, columns=("State", "Year", "Quarter", "District", "Transaction_Count", "Transaction_Amount"))
                Map_Trans1['Year'] = Map_Trans1['Year'].astype(str).str.replace(',', '')
                
                col1,col2 = st.columns(2)
                with col1:
                    District = st.selectbox("**District**",Map_Trans1["District"].unique(), key='District8')
                with col2:
                     pass
                with col1:
                    
                    PTA = Map_Trans1[(Map_Trans1["District"]==District)]                     
                    #DTA.reset_index(drop=True,inplace=True)
                    PTA=PTA.groupby("Year")[["Transaction_Amount", "Transaction_Count"]].sum()
                    PTA.reset_index(inplace=True)
                    PTA_sorted = PTA.sort_values(by='Transaction_Amount', ascending=False)
                    
                
                st.markdown("## :Orange[Total Transacion Type Data]")
                cursor=connection.cursor()
                # Execute query to get total and average transaction amount
                total_trans_query = f"""SELECT 'Sum' as Agg, SUM(Transaction_amount) as Trans_Amount,
                                        sum(Transaction_count) as Trans_count
                                        FROM map_trans 
                                        WHERE District = '{District}'
                                        union all
                                        Select 'Average' as Agg, Avg(Transaction_amount) as Trans_Count,
                                        avg(Transaction_count) as Trans_count
                                        FROM map_trans  
                                        WHERE District = '{District}'"""
                cursor.execute(total_trans_query)
                total_amount_data = cursor.fetchall()
                df_state_total_trans = pd.DataFrame(total_amount_data, columns=['Agg','Trans_Amount', 'Trans_Count'])
                df_state_total_trans['Index'] = range(1, len(df_state_total_trans) + 1)
                df_state_total_trans.set_index('Index', inplace=True)
                st.dataframe(df_state_total_trans)
               
                with st.expander("District Analysis"):
                    st.markdown("## :Yellow[District Transaction Data Year wise]")
                    st.dataframe(PTA_sorted)

                col1,col2=st.columns(2)
                with col1:
                    # Plot bar chart for Transaction_Amount
                    Fig_Tran_Amount = px.bar(PTA_sorted, x='Year', y='Transaction_Amount', color='Transaction_Amount',
                                            title = "TRANSACTION_AMOUNT vs Year",
                                                        labels={'Transaction_amount': 'Transaction Amount'})
                    Fig_Tran_Amount.update_layout(title={'text': f" TRANSACTION_AMOUNT vs {District}", 
                                                                        'x': 0.4, 'xanchor': 'center'}, width=600, height=600,
                                                                        showlegend = False)
                    st.plotly_chart(Fig_Tran_Amount)

                
                with col2:   
                    # Plot bar chart for Transaction_Count
                    Fig_Tran_Count = px.bar(PTA_sorted, x='Year', y='Transaction_Count', color='Transaction_Count',
                                            title = "TRANSACTION_COUNT vs Year",
                                                        labels={'Transaction_Count': 'Transaction Count'})
                    Fig_Tran_Count.update_layout(title={'text': f" TRANSACTION_COUNT vs {District}", 
                                                                        'x': 0.4, 'xanchor': 'center'}, width=600, height=600,
                                                                        showlegend = False)
                    st.plotly_chart(Fig_Tran_Count)
                
        if Method =="DISTRICT YEARWISE ANALYSIS":
             dt_year_analysis()

    
    with tab3:
        
        subtab1, subtab2, Subtab3= st.tabs(["Pincode Data Exploration", "Pincode Transaction Analysis", "Pincode Year Analysis" ])
        
        #Pincode Transaction Analysis
        with subtab1:
            
            def Pincode_transaction_tab():   

                col1, col2, col3 = st.columns(3)
                
                with col1:
                    
                        State = st.selectbox('**State**', (
                                'Andaman & Nicobar Islands', 'Andhra Pradesh', 'Arunachal Pradesh', 'Assam', 'Bihar', 'Chandigarh', 
                                'Chhattisgarh', 'Dadra and Nagar Haveli and Daman and Diu', 'Delhi', 'Goa', 'Gujarat', 'Haryana', 
                                'Himachal Pradesh', 'Jammu & Kashmir', 'Jharkhand', 'Karnataka', 'Kerala', 'Ladakh', 'Lakshadweep', 
                                'Madhya Pradesh', 'Maharashtra', 'Manipur', 'Meghalaya', 'Mizoram', 'Nagaland', 'Odisha', 'Puducherry', 
                                'Punjab', 'Rajasthan', 'Sikkim', 'Tamil Nadu', 'Telangana', 'Tripura', 'Uttar Pradesh', 'Uttarakhand', 
                                'West Bengal'), key='State1')

                with col2:
                        
                        Year = st.selectbox('Year', ['2018', '2019', '2020', '2021', '2022', '2023'], key='Year1')

                with col3:
                        
                        Quarter = st.selectbox('Quarter', ['1', '2', '3', '4'], key='Quarter1')
                    
                st.markdown("## :Pink[Pincode Transacion Data]")
                connection = sql.connect(
                    host="localhost",
                    user="root",
                    password="Nisama@2021",
                    database="phonepae")

                cursor=connection.cursor()

                Pincode_query = f"""
                SELECT State, Year, Quarter, Transaction_amount, Transaction_count, Pincode
                FROM Top_trans
                WHERE Year = '{Year}' 
                AND Quarter = '{Quarter}'
                AND State = '{State}'"""

                cursor.execute(Pincode_query)
                Pincode_Data = cursor.fetchall()
                connection.commit()
                Pincode_df = pd.DataFrame(Pincode_Data, columns=['State', 'Year', 'Quarter', 'Transaction_Amount', 'Transaction_count', 'Pincode'])
            
                col1,col2=st.columns(2)
                
                with col1:

                    # Visualize data as a bar chart
                    Pincode_df_sorted = Pincode_df.sort_values(by='Transaction_Amount', ascending=False)
                    Fig_Tran_Amount = px.bar(Pincode_df_sorted, x='Pincode', y='Transaction_Amount',
                                    labels={'Transaction_amount': 'Transaction Amount'})
                    Fig_Tran_Amount.update_layout(title={'text': f" TRANSACTION_AMOUNT  by  {Year} Quarter : {Quarter}", 
                                                        'x': 0.4, 'xanchor': 'center'}, width=600, height=600,
                                                        legend=dict(x=0.01, y=0.00, orientation='h'))
                    Fig_Tran_Amount.update_xaxes(type='category')
                    st.plotly_chart(Fig_Tran_Amount)

                with col2:
                    # Visualize data using Plotly Bar Chart
                    trans_count_df_sorted = Pincode_df.sort_values(by='Transaction_count', ascending=False)
                    Fig_Tran_count = px.bar(trans_count_df_sorted, x='Pincode', y='Transaction_count', 
                                    labels={'Transaction_count': 'Transaction count'})
                    Fig_Tran_count.update_layout(title={'text': f" TRANSACTION_COUNT  by {Year} Quarter : {Quarter}", 
                                                        'x': 0.4, 'xanchor': 'center'}, width=600, height=600,
                                                        legend=dict(x=0.01, y=0.00, orientation='h'))
                    Fig_Tran_count.update_xaxes(type='category')
                    st.plotly_chart(Fig_Tran_count)

            # Call the function to display its content
            Pincode_transaction_tab()
        
        with subtab2:
             
             def Pin_transaction_tab():

                col1, col2 = st.columns(2)
                
                with col1:
                    State = st.selectbox('**State**', (
                                'Andaman & Nicobar Islands', 'Andhra Pradesh', 'Arunachal Pradesh', 'Assam', 'Bihar', 'Chandigarh', 
                                'Chhattisgarh', 'Dadra and Nagar Haveli and Daman and Diu', 'Delhi', 'Goa', 'Gujarat', 'Haryana', 
                                'Himachal Pradesh', 'Jammu & Kashmir', 'Jharkhand', 'Karnataka', 'Kerala', 'Ladakh', 'Lakshadweep', 
                                'Madhya Pradesh', 'Maharashtra', 'Manipur', 'Meghalaya', 'Mizoram', 'Nagaland', 'Odisha', 'Puducherry', 
                                'Punjab', 'Rajasthan', 'Sikkim', 'Tamil Nadu', 'Telangana', 'Tripura', 'Uttar Pradesh', 'Uttarakhand', 
                                'West Bengal'), key='State2')
                    
                with col2:
                    pass
                
                st.markdown("## :Yellow[Pincode Transacion Data State wise]")
                
                connection = sql.connect(
                        host="localhost",
                        user="root",
                        password="Nisama@2021",
                        database="phonepae")
            
                cursor=connection.cursor()

                # Execute query to get total transaction data
                total_trans_query = f"""select State, Pincode, sum(transaction_amount) as tot_trans_amt, 
                                    sum(transaction_count) as tot_trans_count 
                                    from top_trans
                                    WHERE State = '{State}'
                                    group by State, Pincode"""
                cursor.execute(total_trans_query)
                total_amount_data = cursor.fetchall()
                df_Top_total_trans = pd.DataFrame(total_amount_data, columns=['State','Pincode', 'Tot_Trans_Amt', 'Tot_Trans_Count'])
                df_Top_total_trans['Index'] = range(1, len(df_Top_total_trans) + 1)
                df_Top_total_trans.set_index('Index', inplace=True)
                st.dataframe(df_Top_total_trans)
                   
                col1, col2 =st.columns(2)

                with col1:

                    # Create a donut chart for transacation amount
                    fig_donut = px.pie(df_Top_total_trans, values='Tot_Trans_Amt', names='Pincode',
                                 title="Distribution of Amount by Pincode")
                    st.plotly_chart(fig_donut)
                    
                with col2:

                    # Create a donut chart for transacation amount
                    fig_donut_C = px.pie(df_Top_total_trans, values='Tot_Trans_Count', names='Pincode',
                                    title="Distribution of Count by Pincode")
                    st.plotly_chart(fig_donut_C)
                
                fig = px.area(df_Top_total_trans, x='Tot_Trans_Amt', y='Tot_Trans_Count', 
                                    title='Transaction Amount vs Transaction Count by Pincode')
                fig.update_layout(xaxis_title='Transaction Amount', yaxis_title='Transaction Count', width =800, height=600)
                st.plotly_chart(fig)
                          

        with subtab2:
                Pin_transaction_tab()

        with Subtab3:
            
            def pin_year_analysis():
            
                connection = sql.connect(
                                    host="localhost",
                                    user="root",
                                    password="Nisama@2021",
                                    database="phonepae")

                cursor=connection.cursor()
                #Top_Trans_Dataframe
                cursor.execute("select* from Top_Trans")
                table5 = cursor.fetchall()
                Top_Trans1 = pd.DataFrame(table5, columns=("State", "Year", "Quarter", "Pincode", "Transaction_Count", "Transaction_Amount"))
                Top_Trans1 = Top_Trans1.dropna(subset=['Pincode'])
                Top_Trans1['Transaction_Count'] = Top_Trans1['Transaction_Count'].astype(str).str.replace(',', '')
                Top_Trans1['Transaction_Amount'] = Top_Trans1['Transaction_Amount'].astype(str).str.replace(',', '')
                Top_Trans1['Pincode'] = Top_Trans1['Pincode'].astype('category')
                Top_Trans1['Year'] = Top_Trans1['Year'].astype(str)
        
                col1,col2 = st.columns(2)
                with col1:
                    Pincode = st.selectbox("**Pincode**",Top_Trans1["Pincode"].unique(), key='Pincode1')
                with col2:
                     pass
                with col1:
                    
                    PTA = Top_Trans1[(Top_Trans1["Pincode"]==Pincode)]                     
                    #DTA.reset_index(drop=True,inplace=True)
                    PTA=PTA.groupby("Year")[["Transaction_Amount", "Transaction_Count"]].sum()
                    PTA.reset_index(inplace=True)
                    PTA_sorted = PTA.sort_values(by='Transaction_Amount', ascending=False)
                
                st.markdown("## :Orange[Total Pincode Transacion Data]")
                cursor=connection.cursor()
                # Execute query to get total and average transaction amount
                total_trans_query = f"""SELECT 'Sum' as Agg, SUM(Transaction_amount) as Trans_Amount,
                                        sum(Transaction_count) as Trans_count
                                        FROM Top_trans 
                                        WHERE Pincode = '{Pincode}'
                                        union all
                                        Select 'Average' as Agg, Avg(Transaction_amount) as Trans_Count,
                                        avg(Transaction_count) as Trans_count
                                        FROM Top_trans  
                                        WHERE Pincode = '{Pincode}'"""
                cursor.execute(total_trans_query)
                total_amount_data = cursor.fetchall()
                df_state_total_trans = pd.DataFrame(total_amount_data, columns=['Agg','Trans_Amount', 'Trans_Count'])
                df_state_total_trans['Index'] = range(1, len(df_state_total_trans) + 1)
                df_state_total_trans.set_index('Index', inplace=True)
                st.dataframe(df_state_total_trans)
               
                with st.expander("Pincode Transaction Data Year"):
                    st.markdown("## :Yellow[Pincode Transacion Data Year wise]")
                    st.dataframe(PTA_sorted)

                col1,col2=st.columns(2)
                with col1:
                    # Plot bar chart for Transaction_Amount
                    Fig_Tran_Amount = px.bar(PTA_sorted, x='Year', y='Transaction_Amount', color='Transaction_Amount',
                                            title = "TRANSACTION_AMOUNT vs Year",
                                                        labels={'Transaction_amount': 'Transaction Amount'})
                    Fig_Tran_Amount.update_layout(title={'text': f" TRANSACTION_AMOUNT vs {Pincode}", 
                                                                        'x': 0.4, 'xanchor': 'center'}, width=600, height=600,
                                                                        showlegend = False)
                    st.plotly_chart(Fig_Tran_Amount)

                
                with col2:   
                    # Plot bar chart for Transaction_Count
                    Fig_Tran_Count = px.bar(PTA_sorted, x='Year', y='Transaction_Count', color='Transaction_Count',
                                            title = "TRANSACTION_COUNT vs Year",
                                                        labels={'Transaction_Count': 'Transaction Count'})
                    Fig_Tran_Count.update_layout(title={'text': f" TRANSACTION_COUNT vs {Pincode}", 
                                                                        'x': 0.4, 'xanchor': 'center'}, width=600, height=600,
                                                                        showlegend = False)
                    st.plotly_chart(Fig_Tran_Count)
                
        with Subtab3:
             pin_year_analysis()

elif select == "USER ANALYSIS":
   
    tab1, tab2,tab3= st.tabs(["AGGREGATED USER ANALYSIS", "DISTRICT USER ANALYSIS","PINCODE USER ANALYSIS"])

    with tab1:
     
        subtab1,subtab2,subtab3 = st.tabs(["Aggregated User Data Exploration", "Aggregated User Trans Analysis", "Aggregated User Brand Analysis"])
   
        with subtab1:
        
            def Agg_User_Dataexp_tab():

                connection = sql.connect(
                                host="localhost",
                                user="root",
                                password="Nisama@2021",
                                database="phonepae")

                cursor=connection.cursor()
                
                #Agg_User_Dataframe
                cursor.execute("select* from Agg_user")
                table3 = cursor.fetchall()
                Agg_user1 = pd.DataFrame(table3, columns=("State", "Year", "Quarter", "Brand", "Transaction_Count", "Percentage"))
                
                col1,col2,col3 = st.columns(3)
                
                with col1:
                    Year = st.selectbox("**Year**",Agg_user1["Year"].unique())
                with col2 :
                    Quarter = st.selectbox("**Quarter**",Agg_user1["Quarter"].unique())
                with col3:
                    Brand = st.selectbox("**Brand**",Agg_user1["Brand"].unique())
                
                User_Analysis = Agg_user1[(Agg_user1["Year"]==Year) & (Agg_user1["Quarter"]==Quarter) & (Agg_user1["Brand"]==Brand)]                     
                User_Analysis.reset_index(drop=True,inplace=True)
                User_Analysis=User_Analysis.groupby("State")[["Transaction_Count", "Percentage","Brand"]].sum()
                User_Analysis.reset_index(inplace=True)
                User_Analysis = User_Analysis.sort_values(by='Transaction_Count', ascending=False)
                
                st.markdown("## :Yellow[Aggregated User Data Exploration]")
                
            
                # Visualize data as a bar chart
                color_map = {'Xiaomi':'blue', 'Samsung':'yellow', 'Vivo':'orange', 'Oppo':'green', 'OnePlus':'red', 'Realme':'purple', 'Apple':'white',
            'Motorola':'grey', 'Lenovo':'ash', 'Huawei':'darkgreen', 'Others':'lightgreen', 'Tecno':'pink', 'Gionee':'parrotgreen',
            'Infinix':'saffron', 'Asus':'lemon', 'Micromax':'violet', 'HMD Global':'gold', 'Lava':'silver', 'COOLPAD':'indigo'}
                User_Analysis_Sorted = User_Analysis.sort_values(by='Transaction_Count', ascending=False)
                Fig_Tran_Amount = px.bar(User_Analysis_Sorted, x='State', y='Transaction_Count',color="Brand",
                                labels={'Transaction_Count': 'Transaction Count'}, color_discrete_map =color_map)
                Fig_Tran_Amount.update_layout(title={'text': f" TRANSACTION_COUNT  Vs  year : {Year} Quarter : {Quarter}", 
                                                    'x': 0.4, 'xanchor': 'center'}, width=1000, height=600,
                                                    legend=dict(x=0.07, y=1.00, orientation='h'))
                st.plotly_chart(Fig_Tran_Amount)

                #State wise Aggregated User Data       
                Fig_TAIndia_1 = px.choropleth(User_Analysis, geojson="https://gist.githubusercontent.com/jbrobst/56c13bbbf9d97d187fea01ca62ea5112/raw/e388c4cae20aa53cb5090210a42ebb9b765c0a36/india_states.geojson", 
                                            locations="State", featureidkey="properties.ST_NM",
                                            color="Transaction_Count", color_continuous_scale="Greens",
                                            range_color=(User_Analysis["Transaction_Count"].min(),User_Analysis["Transaction_Count"].max()),
                                            hover_name="State", title=f" TRANSACTION_COUNT Vs. State", fitbounds="locations",
                                            )
                Fig_TAIndia_1.update_geos(visible=False)
                Fig_TAIndia_1.update_layout(geo=dict(showframe=False), width=1200, height=1000) 
                st.plotly_chart(Fig_TAIndia_1)

        with subtab1:
            
            Agg_User_Dataexp_tab()
        
        with subtab2:
             
             def Agguser_trans_tab():

                col1, col2 = st.columns(2)
                
                with col1:
                    State = st.selectbox('**State**', (
                                'Andaman & Nicobar Islands', 'Andhra Pradesh', 'Arunachal Pradesh', 'Assam', 'Bihar', 'Chandigarh', 
                                'Chhattisgarh', 'Dadra and Nagar Haveli and Daman and Diu', 'Delhi', 'Goa', 'Gujarat', 'Haryana', 
                                'Himachal Pradesh', 'Jammu & Kashmir', 'Jharkhand', 'Karnataka', 'Kerala', 'Ladakh', 'Lakshadweep', 
                                'Madhya Pradesh', 'Maharashtra', 'Manipur', 'Meghalaya', 'Mizoram', 'Nagaland', 'Odisha', 'Puducherry', 
                                'Punjab', 'Rajasthan', 'Sikkim', 'Tamil Nadu', 'Telangana', 'Tripura', 'Uttar Pradesh', 'Uttarakhand', 
                                'West Bengal'), key='State4')
                    
                with col2:
                    pass
                
                
                connection = sql.connect(
                        host="localhost",
                        user="root",
                        password="Nisama@2021",
                        database="phonepae")
            
                cursor=connection.cursor()
                st.markdown("## :Lavender[Brand Transacion Data]")
                with st.expander("Total Transaction Data "):
                
                    # Execute query to get total transaction data
                    total_trans_query = f"""select State, Brand, sum(Transaction_Count) as tot_trans_count,
                                        sum(Percentage) as Tot_Percent
                                        from agg_user
                                        WHERE State = '{State}'
                                        group by State, Brand"""
                    cursor.execute(total_trans_query)
                    total_amount_data = cursor.fetchall()
                    df_Top_total_trans = pd.DataFrame(total_amount_data, columns=['State','Brand', 'Tot_Trans_Count', 'Tot_Percent'])
                    df_Top_total_trans['Index'] = range(1, len(df_Top_total_trans) + 1)
                    df_Top_total_trans.set_index('Index', inplace=True)
                    st.dataframe(df_Top_total_trans)
                    
                col1, col2 =st.columns(2)

                with col1:
                    
                    # Visualize data as a bar chart
                    color_map = {'Xiaomi':'blue', 'Samsung':'yellow', 'Vivo':'orange', 'Oppo':'green', 'OnePlus':'red', 'Realme':'purple', 'Apple':'white',
                                'Motorola':'grey', 'Lenovo':'lavender', 'Huawei':'darkgreen', 'Others':'lightgreen', 'Tecno':'pink', 'Gionee':'parrotgreen',
                                'Infinix':'magenta', 'Asus':'lemon', 'Micromax':'violet', 'HMD Global':'gold', 'Lava':'silver', 'COOLPAD':'indigo'}
                    df_Top_total_trans_sort = df_Top_total_trans.sort_values(by='Tot_Trans_Count', ascending=False)
                    Fig_Tran_Amount = px.bar(df_Top_total_trans_sort, x='Brand', y='Tot_Trans_Count',color="Brand",
                                    labels={'Transaction_Count': 'Transaction Count'}, color_discrete_map =color_map)
                    Fig_Tran_Amount.update_layout(title={'text': f" Tot_Trans_Count  Vs  Brand", 
                                                        'x': 0.4, 'xanchor': 'center'}, width=1000, height=600,
                                                        legend=dict(x=0.07, y=1.00, orientation='h'))
                    st.plotly_chart(Fig_Tran_Amount)

                    # Create a donut chart for transacation amount
                    color_map = {'Xiaomi':'blue', 'Samsung':'yellow', 'Vivo':'orange', 'Oppo':'green', 'OnePlus':'red', 'Realme':'purple', 'Apple':'white',
                                'Motorola':'grey', 'Lenovo':'lavender', 'Huawei':'darkgreen', 'Others':'lightgreen', 'Tecno':'pink', 'Gionee':'parrotgreen',
                                'Infinix':'magenta', 'Asus':'lemon', 'Micromax':'violet', 'HMD Global':'gold', 'Lava':'silver', 'COOLPAD':'indigo'}
                    df_Top_total_trans_sort = df_Top_total_trans.sort_values(by='Tot_Percent', ascending=False)
                    Fig_Tran_Amount = px.bar(df_Top_total_trans_sort, x='Brand', y='Tot_Percent',color="Brand",
                                    labels={'Tot_Percentage': 'Tot_Percent'}, color_discrete_map =color_map)
                    Fig_Tran_Amount.update_layout(title={'text': f" Percentage  by  Brand", 
                                                        'x': 0.4, 'xanchor': 'center'}, width=1000, height=600,
                                                        legend=dict(x=0.07, y=1.00, orientation='h'))
                    st.plotly_chart(Fig_Tran_Amount)
                
        with subtab2:
            Agguser_trans_tab()

        with subtab3:
            
            def Au_year_analysis():
            
                connection = sql.connect(
                                    host="localhost",
                                    user="root",
                                    password="Nisama@2021",
                                    database="phonepae")

                cursor=connection.cursor()
                #agg_user_Dataframe
                cursor.execute("select* from agg_user")
                table5 = cursor.fetchall()
                Agg_user1 = pd.DataFrame(table5, columns=("State", "Year", "Quarter", "Brand", "Transaction_Count", "Percentage"))
                Agg_user1['Year'] = Agg_user1['Year'].astype(str)
        
                col1,col2 = st.columns(2)
                
                with col1:
                    Brand = st.selectbox("**Brand**",Agg_user1["Brand"].unique(), key='Brand1')
                with col2:
                     pass
                
                with col1:
                    
                    PTA = Agg_user1[(Agg_user1["Brand"]==Brand)]                     
                    PTA.reset_index(drop=True,inplace=True)
                    PTA=PTA.groupby("Year")[["Transaction_Count", "Percentage"]].sum()
                    PTA.reset_index(inplace=True)
                    PTA_sorted = PTA.sort_values(by='Transaction_Count', ascending=False)
                
                #with st.expander("Pincode Transaction Data Year"):
                st.markdown("## :Yellow[Brand Transacion Data Year wise]")
                st.dataframe(PTA_sorted)

                col1,col2=st.columns(2)
                with col1:
                    # Plot bar chart for Transaction_Amount
                    Fig_Tran_Amount = px.bar(PTA_sorted, x='Year', y='Transaction_Count', color='Transaction_Count',
                                            title = "TRANSACTION_COUNT vs Year",
                                                        labels={'Transaction_Count': 'Transaction Count'})
                    Fig_Tran_Amount.update_layout(title={'text': f" TRANSACTION_COUNT vs Year", 
                                                                        'x': 0.4, 'xanchor': 'center'}, width=600, height=600,
                                                                        showlegend = False)
                    st.plotly_chart(Fig_Tran_Amount)

                
                with col2:   
                    # Plot bar chart for Transaction_Count
                    Fig_Tran_Count = px.bar(PTA_sorted, x='Year', y='Percentage', color='Percentage',
                                            title = "Percentage vs Year",
                                                        labels={'Percentage': 'Percentage'})
                    Fig_Tran_Count.update_layout(title={'text': f" Percentage vs Pincode", 
                                                                        'x': 0.4, 'xanchor': 'center'}, width=600, height=600,
                                                                        showlegend = False)
                    st.plotly_chart(Fig_Tran_Count)
               
                #with st.expander("Total Transaction Data "):
                st.markdown("## :Orange[Total Brand Transacion Data]")
                cursor=connection.cursor()
                # Execute query to get total and average transaction amount
                total_trans_query = f"""SELECT 'Sum' as Agg, SUM(Transaction_Count) as Trans_Count,
                                        sum(Percentage) as Percentage
                                        FROM agg_user 
                                        WHERE Brand = '{Brand}'
                                        union all
                                        Select 'Average' as Agg, Avg(Transaction_Count) as Trans_Count,
                                        avg(Percentage) as Percentage
                                        FROM agg_user  
                                        WHERE Brand = '{Brand}'"""
                cursor.execute(total_trans_query)
                total_amount_data = cursor.fetchall()
                df_state_total_trans = pd.DataFrame(total_amount_data, columns=['Agg','Trans_Count', 'Percentage'])
                df_state_total_trans['Index'] = range(1, len(df_state_total_trans) + 1)
                df_state_total_trans.set_index('Index', inplace=True)
                st.dataframe(df_state_total_trans)
        
        with subtab3:
             Au_year_analysis()

    with tab2:
     
        subtab1,subtab2,subtab3 = st.tabs(["District User Data Exploration", "District User Trans Analysis", "District User Brand Analysis"])
   
        with subtab1:
        
            def Dt_User_Dataexp_tab():

                connection = sql.connect(
                                host="localhost",
                                user="root",
                                password="Nisama@2021",
                                database="phonepae")

                cursor=connection.cursor()
                
                #Agg_User_Dataframe
                cursor.execute("select* from map_user")
                table3 = cursor.fetchall()
                Map_User1 = pd.DataFrame(table3, columns=("State", "Year", "Quarter", "District", "RegisteredUsers", "AppOpens"))
                
                col1,col2,col3 = st.columns(3)
                
                with col1:
                    Year = st.selectbox("**Year**",Map_User1["Year"].unique(),key='Year9')
                with col2 :
                    Quarter = st.selectbox("**Quarter**",Map_User1["Quarter"].unique(),key='Quarter9')
                with col3:
                    State = st.selectbox("**State**",Map_User1["State"].unique(),key='State13')
                
                User_Analysis = Map_User1[(Map_User1["Year"]==Year) & (Map_User1["Quarter"]==Quarter) & (Map_User1["State"]==State)]                     
                User_Analysis.reset_index(drop=True,inplace=True)
                User_Analysis=User_Analysis.groupby("District")[["RegisteredUsers", "AppOpens","State"]].sum()
                User_Analysis.reset_index(inplace=True)
                User_Analysis = User_Analysis.sort_values(by='RegisteredUsers', ascending=False)
                
                st.markdown("## :Yellow[District User Data Exploration]")
                
                col1,col2=st.columns(2)

                with col1:
                    # Visualize data as a bar chart
                    color_map = {'Xiaomi':'blue', 'Samsung':'yellow', 'Vivo':'orange', 'Oppo':'green', 'OnePlus':'red', 'Realme':'purple', 'Apple':'white',
                'Motorola':'grey', 'Lenovo':'ash', 'Huawei':'darkgreen', 'Others':'lightgreen', 'Tecno':'pink', 'Gionee':'parrotgreen',
                'Infinix':'saffron', 'Asus':'lemon', 'Micromax':'violet', 'HMD Global':'gold', 'Lava':'silver', 'COOLPAD':'indigo'}
                    User_Analysis_Sorted = User_Analysis.sort_values(by='RegisteredUsers', ascending=False)
                    Fig_Tran_Amount = px.bar(User_Analysis_Sorted, x='District', y='RegisteredUsers',color="District",
                                    labels={'RegisteredUsers': 'RegisteredUsers'}, color_discrete_map =color_map)
                    Fig_Tran_Amount.update_layout(title={'text': f" RegisteredUsers  by District :  year : {Year} Quarter : {Quarter}", 
                                                        'x': 0.4, 'xanchor': 'center'}, width=600, height=600,
                                                        legend=dict(x=0.07, y=-1.00, orientation='h'))
                    st.plotly_chart(Fig_Tran_Amount)

                    #State wise Aggregated User Data       
                    Fig_TAIndia_1 = px.choropleth(User_Analysis, geojson="https://gist.githubusercontent.com/jbrobst/56c13bbbf9d97d187fea01ca62ea5112/raw/e388c4cae20aa53cb5090210a42ebb9b765c0a36/india_states.geojson", 
                                                locations="State", featureidkey="properties.ST_NM",
                                                color="RegisteredUsers", color_continuous_scale="Rainbow",
                                                range_color=(User_Analysis["RegisteredUsers"].min(),User_Analysis["RegisteredUsers"].max()),
                                                hover_name="State", title=f" RegisteredUsers Vs. State", fitbounds="locations",
                                                )
                    Fig_TAIndia_1.update_geos(visible=False)
                    st.plotly_chart(Fig_TAIndia_1)

                with col2:
                    # Visualize data as a bar chart
                    color_map = {'Xiaomi':'blue', 'Samsung':'yellow', 'Vivo':'orange', 'Oppo':'green', 'OnePlus':'red', 'Realme':'purple', 'Apple':'white',
                'Motorola':'grey', 'Lenovo':'ash', 'Huawei':'darkgreen', 'Others':'lightgreen', 'Tecno':'pink', 'Gionee':'parrotgreen',
                'Infinix':'saffron', 'Asus':'lemon', 'Micromax':'violet', 'HMD Global':'gold', 'Lava':'silver', 'COOLPAD':'indigo'}
                    User_Analysis_Sorted = User_Analysis.sort_values(by='AppOpens', ascending=False)
                    Fig_Tran_Amount = px.bar(User_Analysis_Sorted, x='District', y='AppOpens',color="District",
                                    labels={'AppOpens': 'AppOpens'}, color_discrete_map =color_map)
                    Fig_Tran_Amount.update_layout(title={'text': f" AppOpens  by District :  year : {Year} Quarter : {Quarter}", 
                                                        'x': 0.4, 'xanchor': 'center'}, width=600, height=600,
                                                        legend=dict(x=0.07, y=-1.00, orientation='h'))
                    st.plotly_chart(Fig_Tran_Amount)

                    #State wise Aggregated User Data       
                    Fig_TAIndia_1 = px.choropleth(User_Analysis, geojson="https://gist.githubusercontent.com/jbrobst/56c13bbbf9d97d187fea01ca62ea5112/raw/e388c4cae20aa53cb5090210a42ebb9b765c0a36/india_states.geojson", 
                                                locations="State", featureidkey="properties.ST_NM",
                                                color="AppOpens", color_continuous_scale="Rainbow",
                                                range_color=(User_Analysis["AppOpens"].min(),User_Analysis["AppOpens"].max()),
                                                hover_name="State", title=f" AppOpens Vs. State", fitbounds="locations",
                                                )
                    Fig_TAIndia_1.update_geos(visible=False)
                    st.plotly_chart(Fig_TAIndia_1)

        with subtab1:
            
            Dt_User_Dataexp_tab()
        
        with subtab2:
             
             def dtuser_RegApp_tab():

                col1, col2 = st.columns(2)
                
                with col1:
                    State = st.selectbox('**State**', (
                                'Andaman & Nicobar Islands', 'Andhra Pradesh', 'Arunachal Pradesh', 'Assam', 'Bihar', 'Chandigarh', 
                                'Chhattisgarh', 'Dadra and Nagar Haveli and Daman and Diu', 'Delhi', 'Goa', 'Gujarat', 'Haryana', 
                                'Himachal Pradesh', 'Jammu & Kashmir', 'Jharkhand', 'Karnataka', 'Kerala', 'Ladakh', 'Lakshadweep', 
                                'Madhya Pradesh', 'Maharashtra', 'Manipur', 'Meghalaya', 'Mizoram', 'Nagaland', 'Odisha', 'Puducherry', 
                                'Punjab', 'Rajasthan', 'Sikkim', 'Tamil Nadu', 'Telangana', 'Tripura', 'Uttar Pradesh', 'Uttarakhand', 
                                'West Bengal'), key='State5')
                    
                with col2:
                    pass
                
                
                connection = sql.connect(
                        host="localhost",
                        user="root",
                        password="Nisama@2021",
                        database="phonepae")
            
                cursor=connection.cursor()
                st.markdown("## :Lavender[District User Data]")
                with st.expander("Total District User Data "):
                
                    # Execute query to get total transaction data
                    total_user_query = f"""select State, District, sum(RegisteredUsers) as Tot_Reg_User,
                                        sum(AppOpens) as Tot_AppOpens
                                        from Map_user
                                        WHERE State = '{State}'
                                        group by State, District"""
                    cursor.execute(total_user_query)
                    total_user_data = cursor.fetchall()
                    df_dt_user_data = pd.DataFrame(total_user_data, columns=['State','District', 'Tot_Reg_User', 'Tot_AppOpens'])
                    df_dt_user_data['Index'] = range(1, len(df_dt_user_data) + 1)
                    df_dt_user_data.set_index('Index', inplace=True)
                    st.dataframe(df_dt_user_data)
                    
                fig = px.area(df_dt_user_data, x='District', y=['Tot_Reg_User', 'Tot_AppOpens'], 
                                  title='Total Registered Users and App Opens by District')
                fig.update_layout(xaxis_title='District', yaxis_title='Count', width=1000, height=600)
                st.plotly_chart(fig)
                
                col1, col2 =st.columns(2)

                with col1:
                    
                    # Visualize data as a bar chart
                    color_map = {'Xiaomi':'blue', 'Samsung':'yellow', 'Vivo':'orange', 'Oppo':'green', 'OnePlus':'red', 'Realme':'purple', 'Apple':'white',
                                'Motorola':'grey', 'Lenovo':'lavender', 'Huawei':'darkgreen', 'Others':'lightgreen', 'Tecno':'pink', 'Gionee':'parrotgreen',
                                'Infinix':'magenta', 'Asus':'lemon', 'Micromax':'violet', 'HMD Global':'gold', 'Lava':'silver', 'COOLPAD':'indigo'}
                    df_dt_user_data_sort = df_dt_user_data.sort_values(by='Tot_Reg_User', ascending=False)
                    Fig_user_data = px.pie(df_dt_user_data_sort, names='District', values='Tot_Reg_User',color="District",
                                    hole=0.5, title="Distribution of RegisteredUsers by District", color_discrete_map =color_map)
                    st.plotly_chart(Fig_user_data)
                   
                with col2:

                    # Create a donut chart for transacation amount
                    color_map = {'Xiaomi':'blue', 'Samsung':'yellow', 'Vivo':'orange', 'Oppo':'green', 'OnePlus':'red', 'Realme':'purple', 'Apple':'white',
                                'Motorola':'grey', 'Lenovo':'lavender', 'Huawei':'darkgreen', 'Others':'lightgreen', 'Tecno':'pink', 'Gionee':'parrotgreen',
                                'Infinix':'magenta', 'Asus':'lemon', 'Micromax':'violet', 'HMD Global':'gold', 'Lava':'silver', 'COOLPAD':'indigo'}
                    df_dt_user_data_sort = df_dt_user_data.sort_values(by='Tot_AppOpens', ascending=False)
                    Fig_user_data = px.pie(df_dt_user_data_sort, names='District', values='Tot_AppOpens',color="District",
                                    hole=0.5, title="Distribution of AppOpens by District", color_discrete_map =color_map)
                    st.plotly_chart(Fig_user_data)
            
            
                
                    



        with subtab2:
            dtuser_RegApp_tab()

        with subtab3:
            
            def dt_RegAppyear_analysis():
            
                connection = sql.connect(
                                    host="localhost",
                                    user="root",
                                    password="Nisama@2021",
                                    database="phonepae")

                cursor=connection.cursor()
                #agg_user_Dataframe
                cursor.execute("select* from map_user")
                table5 = cursor.fetchall()
                Map_User1 = pd.DataFrame(table5, columns=("State", "Year", "Quarter", "District", "RegisteredUsers", "AppOpens"))
                Map_User1['Year'] = Map_User1['Year'].astype(str)
        
                col1,col2 = st.columns(2)
                
                with col1:
                    District = st.selectbox("**District**",Map_User1["District"].unique(), key='District1')
                with col2:
                     pass
                
                with col1:
                    
                    DURAD = Map_User1[(Map_User1["District"]==District)]                     
                    DURAD.reset_index(drop=True,inplace=True)
                    DURAD=DURAD.groupby("Year")[["RegisteredUsers", "AppOpens"]].sum()
                    DURAD.reset_index(inplace=True)
                    DURAD_sorted = DURAD.sort_values(by='RegisteredUsers', ascending=False)
                
                #with st.expander("Pincode Transaction Data Year"):
                st.markdown("## :Yellow[RegisteredUsers and AppOpens Data Year wise]")
                st.dataframe(DURAD_sorted)

                col1,col2=st.columns(2)
                with col1:
                    # Plot bar chart for Transaction_Amount
                    Fig_Tran_Amount = px.bar(DURAD_sorted, x='Year', y='RegisteredUsers', color='AppOpens',
                                            title = "RegisteredUsers vs Year",
                                                        labels={'RegisteredUsers': 'RegisteredUsers'})
                    Fig_Tran_Amount.update_layout(title={'text': f" RegisteredUsers vs Year", 
                                                                        'x': 0.4, 'xanchor': 'center'}, width=600, height=600,
                                                                        showlegend = False)
                    st.plotly_chart(Fig_Tran_Amount)

                
                with col2:   
                    # Plot bar chart for Transaction_Count
                    Fig_Tran_Count = px.bar(DURAD_sorted, x='Year', y='AppOpens', color='AppOpens',
                                            title = "AppOpens vs Year",
                                                        labels={'AppOpens': 'AppOpens'})
                    Fig_Tran_Count.update_layout(title={'text': f" AppOpens vs Year", 
                                                                        'x': 0.4, 'xanchor': 'center'}, width=600, height=600,
                                                                        showlegend = False)
                    st.plotly_chart(Fig_Tran_Count)
               
                #with st.expander("Total Users Data "):
                st.markdown("## :Orange[Total RegisteredUsers and AppOpens Data]")
                cursor=connection.cursor()
                # Execute query to get total and average transaction amount
                total_RegUAO_query = f"""SELECT 'Sum' as Agg, SUM(RegisteredUsers) as Tot_RegisteredUsers,
                                        sum(AppOpens) as AppOpens
                                        FROM map_user 
                                        WHERE District = '{District}'
                                        union all
                                        Select 'Average' as Agg, Avg(RegisteredUsers) as Avg_Reg_Users,
                                        avg(AppOpens) as Avg_AppOpens
                                        FROM map_user  
                                        WHERE District = '{District}'"""
                cursor.execute(total_RegUAO_query)
                total_regapp_data = cursor.fetchall()
                df_state_total_trans = pd.DataFrame(total_regapp_data, columns=['Agg','Tot_RegisteredUsers', 'Avg_Reg_Users'])
                df_state_total_trans['Index'] = range(1, len(df_state_total_trans) + 1)
                df_state_total_trans.set_index('Index', inplace=True)
                st.dataframe(df_state_total_trans)
        
        with subtab3:
             dt_RegAppyear_analysis()

    with tab3:
        
        subtab1, subtab2, Subtab3= st.tabs(["Pincode UserData Exploration", "Pincode User Analysis", "Pincode User Year Analysis" ])
        
        #Pincode User Analysis
        with subtab1:
            
            def Pincode_UsrDataExp_tab():   

                col1, col2, col3 = st.columns(3)
                
                with col1:
                    
                        State = st.selectbox('**State**', (
                                'Andaman & Nicobar Islands', 'Andhra Pradesh', 'Arunachal Pradesh', 'Assam', 'Bihar', 'Chandigarh', 
                                'Chhattisgarh', 'Dadra and Nagar Haveli and Daman and Diu', 'Delhi', 'Goa', 'Gujarat', 'Haryana', 
                                'Himachal Pradesh', 'Jammu & Kashmir', 'Jharkhand', 'Karnataka', 'Kerala', 'Ladakh', 'Lakshadweep', 
                                'Madhya Pradesh', 'Maharashtra', 'Manipur', 'Meghalaya', 'Mizoram', 'Nagaland', 'Odisha', 'Puducherry', 
                                'Punjab', 'Rajasthan', 'Sikkim', 'Tamil Nadu', 'Telangana', 'Tripura', 'Uttar Pradesh', 'Uttarakhand', 
                                'West Bengal'), key='State6')

                with col2:
                        
                        Year = st.selectbox('Year', ['2018', '2019', '2020', '2021', '2022', '2023'], key='Year4')

                with col3:
                        
                        Quarter = st.selectbox('Quarter', ['1', '2', '3', '4'], key='Quarter4')
                    
                st.markdown("## :Pink[Pincode User Data]")
                connection = sql.connect(
                    host="localhost",
                    user="root",
                    password="Nisama@2021",
                    database="phonepae")

                cursor=connection.cursor()

                Pincode_Ur_query = f"""
                SELECT State, Year, Quarter, Pincode, RegisteredUsers
                FROM Top_user
                WHERE Year = '{Year}' 
                AND Quarter = '{Quarter}'
                AND State = '{State}'"""

                cursor.execute(Pincode_Ur_query)
                Pincode_Data = cursor.fetchall()
                connection.commit()
                Pincode_df = pd.DataFrame(Pincode_Data, columns=['State', 'Year', 'Quarter', 'Pincode', 'RegisteredUsers'])
            
                col1,col2=st.columns(2)
                
                with col1:

                    # Visualize data as a bar chart
                    Pincode_df_sorted = Pincode_df.sort_values(by='RegisteredUsers', ascending=False)
                    Fig_Treemap = px.treemap(Pincode_df_sorted, path=['Pincode'], values='RegisteredUsers', 
                         title=f"Registered Users by Pincode",
                         labels={'RegisteredUsers': 'Registered Users'})

                    # Update layout
                    Fig_Treemap.update_layout(width=800, height=600)
                    st.plotly_chart(Fig_Treemap)

           # Call the function to display its content
            Pincode_UsrDataExp_tab()
        
        with subtab2:
             
             def Pin_useranalysis_tab():

                col1, col2 = st.columns(2)
                
                with col1:
                    State = st.selectbox('**State**', (
                                'Andaman & Nicobar Islands', 'Andhra Pradesh', 'Arunachal Pradesh', 'Assam', 'Bihar', 'Chandigarh', 
                                'Chhattisgarh', 'Dadra and Nagar Haveli and Daman and Diu', 'Delhi', 'Goa', 'Gujarat', 'Haryana', 
                                'Himachal Pradesh', 'Jammu & Kashmir', 'Jharkhand', 'Karnataka', 'Kerala', 'Ladakh', 'Lakshadweep', 
                                'Madhya Pradesh', 'Maharashtra', 'Manipur', 'Meghalaya', 'Mizoram', 'Nagaland', 'Odisha', 'Puducherry', 
                                'Punjab', 'Rajasthan', 'Sikkim', 'Tamil Nadu', 'Telangana', 'Tripura', 'Uttar Pradesh', 'Uttarakhand', 
                                'West Bengal'), key='State9')
                    
                with col2:
                    pass
                
                st.markdown("## :Yellow[Pincode User State wise]")
                
                connection = sql.connect(
                        host="localhost",
                        user="root",
                        password="Nisama@2021",
                        database="phonepae")
            
                cursor=connection.cursor()

                # Execute query to get total transaction data
                total_trans_query = f"""select State, Pincode, sum(RegisteredUsers) as Tot_Reg_Users
                                    from top_user
                                    WHERE State = '{State}'
                                    group by State, Pincode"""
                cursor.execute(total_trans_query)
                total_amount_data = cursor.fetchall()
                df_Top_total_trans = pd.DataFrame(total_amount_data, columns=['State','Pincode', 'Tot_Reg_Users'])
                df_Top_total_trans['Index'] = range(1, len(df_Top_total_trans) + 1)
                df_Top_total_trans.set_index('Index', inplace=True)
                st.dataframe(df_Top_total_trans)
                
                # Create a donut chart for transacation amount
                fig_donut = px.pie(df_Top_total_trans, values='Tot_Reg_Users', names='Pincode',
                hole=0.5, title="Distribution of RegisteredUsers by Pincode")
                st.plotly_chart(fig_donut)
                
                
        with subtab2:
                Pin_useranalysis_tab()

        with Subtab3:
            
            def pinuser_year_analysis():
            
                connection = sql.connect(
                                    host="localhost",
                                    user="root",
                                    password="Nisama@2021",
                                    database="phonepae")

                cursor=connection.cursor()
                #Top_user_Dataframe
                cursor.execute("select* from Top_user")
                table5 = cursor.fetchall()
                Top_user1 = pd.DataFrame(table5, columns=("State", "Year", "Quarter", "Pincode", "RegisteredUsers"))
                Top_user1 = Top_user1.dropna(subset=['Pincode'])
                Top_user1['Year'] = Top_user1['Year'].astype(str)
        
                col1,col2 = st.columns(2)
                with col1:
                    Pincode = st.selectbox("**Pincode**",Top_user1["Pincode"].unique(), key='Pincode3')
                with col2:
                     pass
                with col1:
                    
                    PTA = Top_user1[(Top_user1["Pincode"]==Pincode)]                     
                    PTA=PTA.groupby("Year")["RegisteredUsers"].sum().reset_index()
                    #PTA.reset_index(inplace=True)
                    #PTA_sorted = PTA.sort_values(by='RegisteredUsers', ascending=False)
                
                with st.expander("Pincode Users Data Year"):
                    st.markdown("## :Yellow[Pincode Users Data Year wise]")
                    st.dataframe(PTA)

                # Plot bar chart for Transaction_Amount
                Fig_Tran_Amount = px.bar(PTA, x='Year', y='RegisteredUsers', color='RegisteredUsers',
                                        title = "RegisteredUsers vs Year",
                                                    labels={'RegisteredUsers': 'RegisteredUsers'})
                Fig_Tran_Amount.update_layout(title={'text': f" RegisteredUsers vs Year", 
                                                                    'x': 0.4, 'xanchor': 'center'}, width=600, height=600,
                                                                    showlegend = False)
                st.plotly_chart(Fig_Tran_Amount)

                 #with st.expander("Total Transaction Data "):
                st.markdown("## :Orange[Total Pincode Users Data]")
                cursor=connection.cursor()
                # Execute query to get total and average transaction amount
                total_trans_query = f"""SELECT 'Sum' as Agg, SUM(RegisteredUsers) as Tot_Reg_Users
                                        FROM Top_user 
                                        WHERE Pincode = '{Pincode}'
                                        union all
                                        Select 'Average' as Agg, Avg(RegisteredUsers) as Avg_Reg_Users
                                        FROM Top_user  
                                        WHERE Pincode = '{Pincode}'"""
                cursor.execute(total_trans_query)
                total_amount_data = cursor.fetchall()
                df_state_total_trans = pd.DataFrame(total_amount_data, columns=['Agg','Tot_Reg_Users'])
                df_state_total_trans['Index'] = range(1, len(df_state_total_trans) + 1)
                df_state_total_trans.set_index('Index', inplace=True)
                st.dataframe(df_state_total_trans)
        
        with Subtab3:
             pinuser_year_analysis()

elif select == "INSIGHTS":

    #Creation of Dataframe from SQL Tables
    connection = sql.connect(
                        host="localhost",
                        user="root",
                        password="Nisama@2021",
                        database="phonepae")

    cursor=connection.cursor()

    #Agg_Trans_Dataframe
    cursor.execute("select* from agg_trans")
    table2 = cursor.fetchall()
    Agg_Trans1 = pd.DataFrame(table2, columns=("State", "Year", "Quarter", "Transaction_Type", "Transaction_Amount", "Transaction_Count"))

    #Agg_user_Dataframe
    cursor.execute("select* from Agg_user")
    table2 = cursor.fetchall()
    Agg_user1 = pd.DataFrame(table2, columns=("State", "State", "Quarter", "Brand", "Transaction_Count", "Percentage"))

    #Map_Trans_Dataframe
    cursor.execute("select* from Map_User")
    table3 = cursor.fetchall()
    Map_Trans1 = pd.DataFrame(table3, columns=("State", "Year", "Quarter", "District", "Transaction_Count", "Transaction_Amount"))

    #Map_user_Dataframe
    cursor.execute("select* from Map_User")
    table4 = cursor.fetchall()
    Map_User1 = pd.DataFrame(table4, columns=("State", "Year", "Quarter", "District", "RegisteredUsers", "AppOpens"))

    #Top_Trans_Dataframe
    cursor.execute("select* from top_trans")
    table5 = cursor.fetchall()
    Top_Trans1 = pd.DataFrame(table5, columns=("State", "Year", "Quarter", "Pincode", "Transaction_Count", "Transaction_Amount"))
    Top_Trans1['Pincode'] = Top_Trans1['Pincode'].astype(str)

    #Top_user_Dataframe
    cursor.execute("select* from top_user")
    table6 = cursor.fetchall()
    Top_user1 = pd.DataFrame(table6, columns=("State", "Year", "Quarter", "Pincode", "RegisteredUsers"))

    # Close the cursor
    cursor.close() 

    def top_low_trans_data(df,group_column,summary_column1, bar_color):
        
        Summary = df.groupby(group_column).agg({summary_column1: 'sum'}).reset_index()

        col1, col2 = st.columns(2)
        
        with col1:
            with st.expander(f"Top 10 {group_column}s by Total {summary_column1}"):
                top_t_count_states = Summary.nlargest(10, summary_column1).sort_values(by=summary_column1, ascending=False)
                fig = px.bar(top_t_count_states, x=group_column, y=summary_column1, 
                             title=f"Top 10 {group_column}s by Total {summary_column1}", color_discrete_sequence=[bar_color])
                fig.update_xaxes(type='category')
                st.plotly_chart(fig, use_container_width=True)
            
        with col2:    
            with st.expander(f"Lowest 10 {group_column}s by Total {summary_column1}"):
                bottom_t_count_states = Summary.nsmallest(10, summary_column1).sort_values(by=summary_column1)
                fig = px.bar(bottom_t_count_states, x=group_column, y=summary_column1, 
                             title=f"Lowest 10 {group_column}s by Total {summary_column1}", color_discrete_sequence=[bar_color])
                fig.update_xaxes(type='category')
                st.plotly_chart(fig, use_container_width=True)

    top_low_trans_data(Agg_Trans1,group_column='State',summary_column1='Transaction_Amount', bar_color='green')               

    top_low_trans_data(Agg_Trans1,group_column='State',summary_column1='Transaction_Count', bar_color='Yellow')               
    
    top_low_trans_data(Map_Trans1,group_column='District',summary_column1='Transaction_Count', bar_color='Yellow')               

    top_low_trans_data(Map_Trans1,group_column='District',summary_column1='Transaction_Amount', bar_color='Yellow')  

    top_low_trans_data(Agg_user1,group_column='Brand',summary_column1='Transaction_Count', bar_color='lightblue')  

    top_low_trans_data(Map_User1,group_column='District',summary_column1='RegisteredUsers', bar_color='cyan')  

    top_low_trans_data(Map_User1,group_column='District',summary_column1='AppOpens', bar_color='rosybrown')

    top_low_trans_data(Top_Trans1,group_column='Pincode',summary_column1='Transaction_Count', bar_color='pink')
    
    top_low_trans_data(Top_Trans1,group_column='Pincode',summary_column1='Transaction_Amount', bar_color='lightgreen')

    top_low_trans_data(Top_user1,group_column='Pincode',summary_column1='RegisteredUsers', bar_color='mediumslateblue')
    

    