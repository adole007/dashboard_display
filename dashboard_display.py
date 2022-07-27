#link database server to python
import mysql.connector
import pyodbc

#install packages
import numpy as np
import pandas as pd
import streamlit as st 
#import plotly.express as px

import pandas as pd
import numpy as np
  
#%matplotlib inline
import plotly.graph_objects as go
from plotly import __version__
import cufflinks as cf
  
from plotly.offline import download_plotlyjs, init_notebook_mode, plot, iplot
import plotly.express as px  
# to get the connection
init_notebook_mode(connected = True)
  
# plotly also serves online,
# but we are using just a sample
cf.go_offline()

import time as t 
import datetime
import matplotlib.pyplot as plt
import time # to simulate a real 


##Basic dashboard configuration 
st.set_page_config(
    page_title="Analysing the Vieunite App",
    page_icon="✅",
    layout="wide",
)

##connect to the database server
# Creating connection object
mydb = mysql.connector.connect(
    host = "http_address",
    user = "username",
    password = "********",
    database = "database_name"
)



### Selection of Task to Visualize



def main():
    ##GUI designs
    # Title
    st.title("Real-Time Data Visualisation for Vieunite")

#filter task using sidebar
    menu = ["User & Artist Analysis","Sales Analysis"]
    choice_selection = st.sidebar.selectbox("Menu",menu)
    placeholder =st.empty() #used for creating single container
    
    # near real-time / live feed simulation
    #for seconds in range((20)):       
    if choice_selection == 'User & Artist Analysis':
        
        """section to analyse user and artist data and 
        display on the dashboard
         select SQL table to insert in dataframe."""
         
        query_user = "SELECT * FROM pframe_user;"
        query_order_g = "SELECT * FROM pframe_order_goods;" 
        query_artwork =  "SELECT * FROM pframe_artwork;"
        query_user_browse = "SELECT * FROM pframe_user_browse_image_log;" 
        query_artwork_category = "SELECT * FROM pframe_artwork_category;" 
        query_artist = "SELECT * FROM pframe_artist;" 
       
        
        #convert sql table to pandas dataframe
        d_f = pd.read_sql(query_user, mydb)
        order_g = pd.read_sql(query_order_g, mydb)
        artwork_g = pd.read_sql(query_artwork,mydb)
        user_browse_g = pd.read_sql(query_user_browse,mydb)
        artwork_category_g = pd.read_sql(query_artwork_category,mydb)
        d_f_artist = pd.read_sql(query_artist, mydb)
  
        #dataframe of tables
        daf=pd.DataFrame(d_f)
        daf_query_order_g=pd.DataFrame(order_g)
        daf_query_artwork = pd.DataFrame(artwork_g)
        daf_query_user_browse_g=pd.DataFrame(user_browse_g)
        daf_query_artwork_category_g=pd.DataFrame(artwork_category_g)
        daf_artist=pd.DataFrame(d_f_artist)


#        @st.experimental_memo()
#        def get_data() -> pd.DataFrame:
#            return daf
#        df_user = get_data()


        st.subheader("User & Artist Analysis")
        
        #layout for columns
        no_user,no_artist = st.columns(2)
        with no_user:
            st.markdown("Number of Users by Date")
            #st.success("Filter Total Likes by Date")
            today_u = datetime.date.today()
            tomorrow_u = today_u + datetime.timedelta(days=1)
            start_date_u = st.date_input("User Count Start date", today_u)
            end_date_u = st.date_input("User Count End date",tomorrow_u)
            if start_date_u < end_date_u:
                Total=len(daf[(daf['create_time'] > ("%s" % start_date_u)) & (daf['create_time'] <  ("%s" % end_date_u))])
                st.markdown(Total)
            else:
                st.error("Error:End date must fall after Start date")
        
        with no_artist:
            st.markdown("Number of Artist by Date")
            today_a = datetime.date.today()
            tomorrow_a = today_a + datetime.timedelta(days=1)
            start_date_a = st.date_input("Artist Count Start date", today_a)
            end_date_a = st.date_input("Artist Count End date",tomorrow_a)
            if start_date_a < end_date_a:
                Total_a=len(daf_artist[(daf_artist['create_time'] > ("%s" % start_date_a)) & (daf_artist['create_time'] <  ("%s" % end_date_a))])
                st.markdown(Total_a)
            else:
                st.error("Error:End date must fall after Start date")
        
        col1,col2,artist1 = st.columns(3)
        col1.metric(label ="Total Number of Users registered",
                    value = len(daf))
        
        col2.metric(label ="Number of Users Presently using the App",value = daf.status.value_counts()[1])
        artist1.metric(label ="Total Number of Artist registered",
                    value = len(daf_artist))
       
        #creating columns for chart
        col3,col4 = st.columns((5,5))
        with col3:
            st.markdown("Users Artwork Purchase History")
            #col3.success("Bar chart of Artworks purchase by user")
            order_goods_artwork=daf_query_order_g.merge(daf_query_artwork, how='inner', left_on='artwork_id', right_on='id')
            user_order_goods_artwork=order_goods_artwork.merge(daf, how='inner', left_on='user_id', right_on='id')
            fig = px.pie(user_order_goods_artwork, values = 'num',names ='username',hover_data = ['price_x','amount'])
            #fig.show()
            #st.plotly_chart(fig)
            st.write(fig)
        
        with col4:
            st.markdown("Ranking of Artwork by User views")
            fig = px.pie(daf_query_user_browse_g.merge(daf_query_artwork, how='inner', left_on='image_id', right_on='id'),
                         values = 'image_id',names ='name',
                         hover_data = ['id_y','image_id'])
            st.write(fig)
        
        
        col5,col6 = st.columns((5,5))
        with col5:
            st.markdown("Artwork Genre most popular with Users")
            user_browse_g_artwork=daf_query_user_browse_g.merge(daf_query_artwork, how='inner', left_on='image_id', right_on='id')
            user_order_goods_artwork=user_browse_g_artwork.merge(daf_query_artwork_category_g, how='inner', left_on='artwork_category_id',
                                                                 right_on='id')
           
            fig=px.histogram(user_order_goods_artwork,y = 'image_id',x ='name_y',color="name_y")
            #fig.update_traces(textposition='inside', textinfo='percent+label')
            st.write(fig)
            
        with col6:
            st.markdown("Genre of Artwork most Produce by Artist")
            artwork_g_category=daf_query_artwork.merge(daf_query_artwork_category_g, how='inner', left_on='artwork_category_id', right_on='id')
            fig = px.pie(artwork_g_category,names ='name_y')
            st.write(fig)

   
    else:
       # """section to analyse Sales data and display on the dashboard"""
        st.subheader("Sales Analysis")
        #database table linking
        query_likes = "SELECT * FROM pframe_artwork_like;" 
        query_album = "SELECT * FROM pframe_artwork_album;"
        query_shares = "SELECT * FROM pframe_artwork_share;" 
        query_artwork =  "SELECT * FROM pframe_artwork;"
        
        artwork_g = pd.read_sql(query_artwork,mydb)
        df_shares = pd.read_sql(query_shares, mydb)
        df_album = pd.read_sql(query_album,mydb)
        df_likes = pd.read_sql(query_likes, mydb)
        
        daf_likes=pd.DataFrame(df_likes)
        daf_album = pd.DataFrame(df_album)
        daf_shares=pd.DataFrame(df_shares)
        daf_query_artwork = pd.DataFrame(artwork_g)
        
        
        no_likes,add_artwork = st.columns(2)
        with no_likes:
            st.markdown("Likes of Artwork by Date")
            #st.success("Filter Total Likes by Date")
            today = datetime.date.today()
            tomorrow = today + datetime.timedelta(days=1)
            start_date = st.date_input("Start date of Likes", today)
            end_date = st.date_input("End date of Likes",tomorrow)
            if start_date < end_date:
                Total=len(daf_likes[(daf_likes['create_time'] > ("%s" % start_date)) & (daf_likes['create_time'] <  ("%s" % end_date))])
                st.markdown(Total)
            else:
                st.error("Error:End date must fall after Start date")

        
        with add_artwork:
            st.markdown("Count of Artwork by Date")
            today_alb = datetime.date.today()
            tomorrow_alb = today_alb + datetime.timedelta(days=1)
            start_date_alb = st.date_input("Start date of album", today_alb)
            end_date_alb = st.date_input("End date of Album",tomorrow_alb)
            if start_date_alb < end_date_alb:
                Total_alb=len(daf_album[(daf_album['create_time'] > ("%s" % start_date_alb)) & (daf_album['create_time'] <  ("%s" % end_date_alb))])
                st.markdown(Total_alb)
            else:
                st.error("Error:End date must fall after Start date")
        
        artwork_1,artwork_share = st.columns((5,5))
        with artwork_1:
            share_art=daf_shares.merge(daf_query_artwork, how='inner', left_on='artwork_id', right_on='id')
            st.markdown("Number of Artwork share of Social Media")
            today_share = datetime.date.today()
            tomorrow_share = today_share + datetime.timedelta(days=1)
            start_date_share = st.date_input("Share Count Search Start date", today_share)
            end_date_share = st.date_input("Share Count End date",tomorrow_share)
            if start_date_share < end_date_share:
                Total_share=len(share_art[(share_art['create_time_x'] > ("%s" % start_date_share)) & (share_art['create_time_x'] <  ("%s" % end_date_share))])
                st.markdown(Total_share)
            else:
                st.error("Error:End date must fall after Start date")
            
        with artwork_share:
            st.markdown("Rating of Artwork Shared")
            fig = px.pie(share_art,names ='name')
            st.write(fig)
            
        
        # order_unit, pounds_value = st.columns((5,5))
        # with order_unit:
        #    #"""display the order unit per product searched(
        #    # using the pframe_order_goods and pframe_artwork_id)"""
    
        #     st.markdown("Number of Specific Product Sold within a Time frame")
            
        # with pounds_value:
        #  #   """ display the pounds value for each purchase within a Time frame
        #   #  using(pframe_order_goods, pframe_users"""
        #     st.markdown("Pounds Value for each Purchase")
        
        
        # artwork_sold, sales_percentage = st.columns((5,5))
        # with artwork_sold:
        #     st.markdown("Number of Atwork Sold within a Time frame")
            
        # with sales_percentage:
        #     st.markdown("Company Successful Sales Percentage with a Time frame")
            
    
    #time.sleep(1)

if __name__ == '__main__':
    main()

