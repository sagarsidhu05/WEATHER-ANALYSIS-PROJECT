import pandas as pd
import streamlit as st
from streamlit_option_menu import option_menu
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px
import plotly.graph_objects as go
import folium
from streamlit_folium import folium_static
from windrose import WindroseAxes
def prec():
     yearly_precipitation = df.groupby('year')['precipMM'].sum().reset_index()
     fig=px.bar(yearly_precipitation.drop(11),x='year', y='precipMM',template="xgridoff",color='precipMM')    
     st.plotly_chart(fig)

def precci(yea):     
     monthly_precipitation = df.groupby(['year', 'month'])['precipMM'].sum().reset_index()
     fig=px.bar(monthly_precipitation[monthly_precipitation.loc[:,"year"]==yea],x='month',y="precipMM",
                template="xgridoff",color="precipMM",title=f"Monthly precipitation of {yea}")
     fig.update_layout(title_x=0.3) 
     st.plotly_chart(fig)
def temp():
     col1,col2=st.columns(2)
     with col1:
          start_date = st.date_input("Start Date", value=pd.to_datetime("2009-01-01").date())
     with col2: 
          end_date = st.date_input("End Date", value=pd.to_datetime("2019-12-31").date())
     start_date = pd.to_datetime(start_date)
     end_date = pd.to_datetime(end_date)
     df1= df[(df['date_time'] >= start_date) & (df['date_time'] <= end_date)]
     fig=px.line(df1,x="date_time",y="maxtempC",title='Variation of Max Temperature (°C) Over Time')
     fig.update_layout(title_x=0.3) 
     fig.update_traces(line_color='green')
     st.plotly_chart(fig)
                         
def maxtemp(yea):
     monthly_maxtemp = df.groupby(['year', 'month'])['maxtempC'].mean().reset_index()
     fig = px.line(monthly_maxtemp[monthly_maxtemp.loc[:,"year"]==yea ], x='month', y='maxtempC',
                    labels={'maxtempC': 'Max Temperature (°C)', 'month': 'Month'},title=f'Variation of Max Temperature over Months in {yea}',
                    markers=True)
     fig.update_layout(title_x=0.3,template="plotly_dark") 
     fig.update_traces(line_color='lightgreen')  
     st.plotly_chart(fig) 

def hum():
     yearly_hum = df.groupby('year')['humidity'].mean().reset_index()
     fig=px.line(yearly_hum,x='year', y='humidity',markers=True)
     fig.update_layout(title_text='Variation of Humidity over time',title_x=0.3) 
     st.plotly_chart(fig)     

def humidity(yea):
     yearly_hum = df.groupby(['year','month'])['humidity'].mean().reset_index()
     fig = px.bar(yearly_hum[yearly_hum.loc[:,"year"]==yea ], x='month', y='humidity', 
                  color='humidity', template="xgridoff",labels={'maxtempC': 'Max Temperature (°C)', 'month': 'Month'},
                  title=f'Variation of humidity over Months in {yea}')
     fig.update_layout(title_x=0.3)
     st.plotly_chart(fig)  

def wind():
     fig=plt.figure(figsize=(8,8))
     ax = WindroseAxes.from_ax(fig=fig)
     ax.bar( df['winddirDegree'],  df['windspeedKmph'], normed=True, opening=0.8 ,edgecolor='white')
     ax.set_legend()
     st.pyplot(fig) 

def corr():
     df1 = df.drop(columns=['date_time','totalSnow_cm','uvIndex1','moon_illumination','moonrise', 'moonset','sunrise', 'sunset',"tempC","DewPointC","WindGustKmph"])
     correlation_matrix = df1.corr()
     fig=plt.figure(figsize=(16,12))
     sns.heatmap(correlation_matrix, annot=True, cmap='viridis', linewidths=0.5)
     plt.title('Correlation Heatmap of Weather Parameters')
     st.pyplot(fig)  

def sun(city):
     monthly_sunshine = df.groupby(['month'])['sunHour'].mean().reset_index()
     fig = px.bar(monthly_sunshine, x='month', y='sunHour', title=f'Average Monthly Sunshine Hours in {city}',color="month")
     fig.update_layout(title_x=0.3) 
     st.plotly_chart(fig)
     
def uv():
     monthly_uv = df.groupby(['year', 'month'])['uvIndex'].mean().unstack().drop(2020)
     fig= plt.figure(figsize=(12, 8))
     sns.heatmap(monthly_uv, annot=True, fmt=".1f", cmap='magma')
     plt.title('Average UV Index Over Different Months')
     plt.xlabel('Month')
     plt.ylabel('Year')
     st.pyplot(fig)
def uv1(siz):
     year_humidity=df.groupby('year')['uvIndex'].mean()
     year_hum=year_humidity.to_frame()
     year_hum.drop(2020,inplace=True)
     fig2=px.scatter(year_hum,x=year_hum.index,y="uvIndex",color="uvIndex",template="xgridoff",log_x=True, size=siz,
     title=" Variation of UVindex over time")   
     st.plotly_chart(fig2)  

def heat():
     year_heat = df.groupby('year')['HeatIndexC'].mean().reset_index()
     year_heat.drop(11,inplace=True)
     fig=px.line(year_heat,y='HeatIndexC',x="year",markers=True,title="VARAITION OF HEATINDEX OVER TIME")
     fig.update_layout(title_text="VARAITION OF HEATINDEX OVER TIME",title_x=0.3) 
     fig.update_traces(line_color='lightgreen')     
     st.plotly_chart(fig)
     fig1 = px.scatter(df, x='maxtempC', y='HeatIndexC',
     labels={'maxtempC': 'Max Temperature (°C)', 'HeatIndexC': 'Heat Index (°C)'})
     fig1.update_layout(title_text="scatter Plot of Max Temperature vs. Heat Index",title_x=0.3,) 
     st.plotly_chart(fig1) 
     fig3 = px.scatter(df, y='HeatIndexC', x='humidity', labels={'HeatIndexC': 'Heat Index (C)', 'humidity': 'Humidity (%)'},color="HeatIndexC")
     fig3.update_layout(title_text="Scatter plot of HeatIndex vs Humidity",title_x=0.3) 
     st.plotly_chart(fig3)

with st.sidebar:
   option=option_menu('Menu',("Home","Dataset","Graphs","About us"),icons=["house","table","bar-chart","people"],menu_icon="cast",default_index=0)
if option=="Home":
     st.write("<h1 style='text-align: center;'>Weather Analysis Dashboard    🌤️</h1>", unsafe_allow_html=True)
     
     st.markdown("""
     Welcome to the **Weather Analysis Dashboard**! 🌤️🌧️
     This app provides an in-depth analysis of the weather trends across multiple cities in India. Here, you can explore historical weather data, track real-time weather conditions, and compare weather parameters like temperature, humidity, and pollution levels across cities.
     """)
     col1, col2, col3 = st.columns([1, 2, 1])  
     with col2:
          st.image("weather.jpeg", caption="Weather Analysis",width=300)
     st.subheader("Features of the Dashboard")
     st.markdown("""
     - **Interactive Weather Maps**: Explore maps with markers showing weather data across different cities.
     
     - **Data Comparison**: Compare temperature, humidity, and other weather parameters for multiple cities.
     - **Advanced Data Visualizations**: Visualize weather data through graphs, heatmaps, and 3D charts.
     ### How to Use:
     1. **Select a City**: Choose a city from the sidebar to view its weather data.
     2. **Analyze Trends**: View temperature, humidity, and pollution trends over time.
     3. **Compare Cities**: Compare the weather data of multiple cities.
     """)
     st.write("Feel free to explore the features of this app using the navigation bar on the sidebar!")
     st.markdown("""
     This project was developed as part of a weather data analysis and visualization initiative. The goal is to provide valuable insights for understanding weather patterns and trends across different cities.
     """)
            
elif option=="Dataset":
      st.write("<h1 style='text-align: center;'>DATASETS</h1>", unsafe_allow_html=True)
      sel=st.selectbox('SELECT PLACE',options=("Bengaluru","Bombay","Delhi","Hyderabad","Jaipur","Kanpur","Nagpur",'Pune'),placeholder="select city or state")
      if sel=="Bengaluru":
           df=pd.read_csv("bengaluru.csv")
           st.dataframe(df)
           st.write("Download Dataset: [link](https://www.kaggle.com/datasets/hiteshsoneji/historical-weather-data-for-indian-cities?select=bengaluru.csv)")
      elif sel=="Bombay":
           df1=pd.read_csv("bombay.csv")
           st.dataframe(df1)
           st.write("Download Dataset: [link](https://www.kaggle.com/datasets/hiteshsoneji/historical-weather-data-for-indian-cities?select=bombay.csv)")
      elif sel=="Delhi":
           df2=pd.read_csv("delhi.csv")
           st.dataframe(df2)
           st.write("Download Dataset: [link](https://www.kaggle.com/datasets/hiteshsoneji/historical-weather-data-for-indian-cities?select=delhi.csv)")
      elif sel=="Hyderabad":
           df3=pd.read_csv("hyderabad.csv")
           st.dataframe(df3)
           st.write("Download Dataset: [link](https://www.kaggle.com/datasets/hiteshsoneji/historical-weather-data-for-indian-cities?select=hyderabad.csv)")
      elif sel=="Jaipur":
           df4=pd.read_csv("jaipur.csv")
           st.dataframe(df4)
           st.write("Download Dataset:[link](https://www.kaggle.com/datasets/hiteshsoneji/historical-weather-data-for-indian-cities?select=jaipur.csv)")
      elif sel=="Kanpur":
           df5=pd.read_csv("kanpur.csv")
           st.dataframe(df5)
           st.write("Download Dataset: [link](https://www.kaggle.com/datasets/hiteshsoneji/historical-weather-data-for-indian-cities?select=kanpur.csv)")
      elif sel=="Nagpur":
           df6=pd.read_csv("nagpur.csv")
           st.dataframe(df6)
           st.write("Download Dataset:[link](https://www.kaggle.com/datasets/hiteshsoneji/historical-weather-data-for-indian-cities?select=nagpur.csv)")
      elif sel=="Pune":
           df7=pd.read_csv("pune.csv")
           st.dataframe(df7)
           st.write("Download Dataset: [link](https://www.kaggle.com/datasets/hiteshsoneji/historical-weather-data-for-indian-cities?select=pune.csv)")    

elif option=="Graphs":
     st.write("<h1 style='text-align: center;'>GRAPHS</h1>", unsafe_allow_html=True)
     a=st.sidebar.selectbox(" choose an option  ",options=["SINGLE CITY ANALYSIS","COMPARISON OF CITIES","GEOGRAPHICAL MAP"])
     @st.cache_data
     def load_data(file_path):
      return pd.read_csv(file_path)
     if a=="SINGLE CITY ANALYSIS":  
          st1= st.selectbox('SELECT PLACE',options=("Bengaluru","Bombay","Delhi","Hyderabad","Jaipur","Kanpur","Nagpur",'Pune'),placeholder="select city or state")
          if st1=="Delhi":  
               df=load_data("delhi.csv")
               df.loc[:,"month"]=df.loc[:,"date_time"].str.split("-").str[1]
               df.loc[:,"day"]=df.loc[:,"date_time"].str.split("-").str[0]
               df.loc[:,"year"]=df.loc[:,"date_time"].str.split("-").str[2]
               df.loc[:,"date"]=df.loc[:,"date_time"].str.split("-").str[1]+"-"+df.loc[:,"date_time"].str.split("-").str[0]+"-"+df.loc[:,"date_time"].str.split("-").str[2]
               df['date'] = pd.to_datetime(df['date'])
               df["year"]=df["date"].dt.year
               df["month"]=df["date"].dt.month
               a=st.sidebar.selectbox("Select Parameter to Visualize",options=["Temperature Trends","Yearly and Monthly Precipitaion(MM)","Humidity variation","UVindex","Heatindex","Wind Speed and Direction","Coorelation Analysis","sunhours"])
               if a=="Temperature Trends":
                    col1,col2=st.columns(2)
                    with col1:
                     start_date = st.date_input("Start Date", value=pd.to_datetime("2009-01-01").date())
                    with col2: 
                     end_date = st.date_input("End Date", value=pd.to_datetime("2019-12-31").date())
                    start_date = pd.to_datetime(start_date)
                    end_date = pd.to_datetime(end_date)
                    df1= df[(df['date'] >= start_date) & (df['date'] <= end_date)]
                    fig=px.line(df1,x="date",y="maxtempC",title='Variation of Max Temperature (°C) Over Time')
                    fig.update_layout(title_x=0.3) 
                    fig.update_traces(line_color='green')
                    st.plotly_chart(fig) 
                    l=st.slider("Year",min_value=2009,max_value=2019,step=1)
                    maxtemp(l)           
               elif a=="Yearly and Monthly Precipitaion(MM)":
                    st.title("YEARLY PRECIPITATION")
                    prec()
                    st.header("MONTHLY PRECIPITATION")
                    l=st.slider("Year",min_value=2009,max_value=2019,step=1)
                    precci(l)
               elif a=="Humidity variation":
                    hum()
                    q=st.slider("year",min_value=2009,max_value=2019,step=1)
                    humidity(q)
               elif a=="UVindex":  
                    uv1([140,100,50,90,105,107,107,160,180,200,220])
                    uv()
               elif a=="Heatindex":
                    heat()
               elif a=="Wind Speed and Direction":
                    st.title("WIND ROSE GRAPH BETWEEN WIND DIRECTION AND SPEED")
                    wind()
               elif a=="Coorelation Analysis":
                    st.title("CORRELATION ANALYSIS")
                    corr()
               elif a=="sunhours":
                    sun("delhi") 

          elif st1=="Bengaluru":
               df=load_data("bengaluru.csv")
               df['date_time'] = pd.to_datetime(df['date_time'])
               df["year"]=df["date_time"].dt.year
               df["month"]=df["date_time"].dt.month 
               avg_temp = df['maxtempC'].mean()
               avg_humidity = df['humidity'].mean()
               b=st.sidebar.selectbox("select trends",options=["Temperature Trends","Yearly and Monthly Precipitaion(MM)","Humidity variation","UVindex","Heatindex","Wind Speed and Direction","Coorelation Analysis","sunhours"])
               if b=="Temperature Trends":
                    temp()
                    e=st.slider("Year",min_value=2009,max_value=2019,step=1)
                    maxtemp(e)
               elif b=="Yearly and Monthly Precipitaion(MM)" :
                    st.title("YEARLY PRECIPITATION")
                    prec()
                    st.header("MONTHLY PRECIPITATION")
                    l=st.slider("Year",min_value=2009,max_value=2019,step=1)
                    precci(l)
               elif b=="Humidity variation":
                    hum()
                    q=st.slider("year",min_value=2009,max_value=2019,step=1)  
                    humidity(q)
               elif b=="UVindex":     
                    uv1([140,180,220,300,250,300,200,260,260,300,160])
                    uv()
               elif b=="Heatindex":
                   heat()
               elif b=="Wind Speed and Direction":
                    st.title("WIND ROSE GRAPH BETWEEN WIND DIRECTION AND SPEED")
                    wind()
               elif b=="Coorelation Analysis":
                    st.title("CORRELATION ANALYSIS")
                    corr() 
               elif b=="sunhours":
                   sun("Bengaluru") 
          
          elif st1=="Bombay": 
               c=st.sidebar.selectbox("select trends",options=["Temperature Trends","Yearly and Monthly Precipitaion(MM)","Humidity variation","UVindex","Heatindex","Wind Speed and Direction","Coorelation Analysis","sunhours"])
               df=load_data("bombay.csv")
               df['date_time'] = pd.to_datetime(df['date_time'])
               df["year"]=df["date_time"].dt.year
               df["month"]=df["date_time"].dt.month 
               if c=="Temperature Trends":  
                    temp() 
                    l=st.slider("Year",min_value=2009,max_value=2019,step=1)
                    maxtemp(l)
               elif c=="Yearly and Monthly Precipitaion(MM)" :
                    st.title("YEARLY PRECIPITATION")
                    prec()  
                    st.header("MONTHLY PRECIPITATION")
                    l=st.slider("select year",min_value=2009,max_value=2019,step=1)
                    precci(l)
               elif c=="Humidity variation": 
                    hum()
                    q=st.slider("year",min_value=2009,max_value=2019,step=1)   
                    humidity(q)     
               elif c=="Wind Speed and Direction":
                    st.title("WIND ROSE GRAPH BETWEEN WIND DIRECTION AND SPEED")
                    wind() 
               elif c=="UVindex":
                    uv1([200,100,170,175,150,300,200,90,220,400,95])   
                    uv()
               elif c=="Heatindex": 
                    heat()
               elif c=="Coorelation Analysis":
                    st.title("CORRELATION ANALYSIS")
                    corr() 
               elif c=="sunhours":
                    sun("Bombay")
                    
          elif st1=="Hyderabad": 
               d=st.sidebar.selectbox("select trends",options=["Temperature Trends","Yearly and Monthly Precipitaion(MM)","Humidity variation","UVindex","Heatindex","Wind Speed and Direction","Coorelation Analysis","sunhours"])
               df=load_data("hyderabad.csv")
               df['date_time'] = pd.to_datetime(df['date_time'])
               df["year"]=df["date_time"].dt.year
               df["month"]=df["date_time"].dt.month 
               if d=="Temperature Trends": 
                    temp() 
                    a=st.slider('SELECT YEAR',min_value=2009,max_value=2019,step=1) 
                    maxtemp(a)
               elif d=="Yearly and Monthly Precipitaion(MM)" :
                    st.title("YEARLY PRECIPITATION")
                    prec() 
                    st.header("MONTHLY PRECIPITATION")
                    l=st.slider("select year",min_value=2009,max_value=2019,step=1)
                    precci(l)
               elif d=="Humidity variation": 
                    hum()
                    q=st.slider("year",min_value=2009,max_value=2019,step=1)  
                    humidity(q) 
               elif d=="UVindex":
                    uv1([200,190,150,170,100,220,195,120,300,290,70])   
                    uv() 
               elif d=="Heatindex":
                    heat()    
               elif d=="Wind Speed and Direction":
                    st.title("WIND ROSE GRAPH BETWEEN WIND DIRECTION AND SPEED")
                    wind()
               elif d=="Coorelation Analysis":
                    st.title("CORRELATION ANALYSIS")
                    corr()
               elif d=="sunhours":
                    sun("Hyderabad")     
               
          elif st1=="Jaipur": 
               e=st.sidebar.selectbox("select trends",options=["Temperature Trends","Yearly and Monthly Precipitaion(MM)","Humidity variation","UVindex","Heatindex","Wind Speed and Direction","Coorelation Analysis","sunhours"])
               df=load_data("jaipur.csv")
               df['date_time'] = pd.to_datetime(df['date_time'])
               df["year"]=df["date_time"].dt.year
               df["month"]=df["date_time"].dt.month
               if e=="Temperature Trends":  
                    temp() 
                    l=st.slider("Year",min_value=2009,max_value=2019,step=1)
                    maxtemp(l)
               elif e=="Yearly and Monthly Precipitaion(MM)" :
                    st.title("YEARLY PRECIPITATION")
                    prec()
                    st.header("MONTHLY PRECIPITATION")
                    l=st.slider("select year",min_value=2009,max_value=2019,step=1)
                    precci(l)
               elif e=="Humidity variation": 
                    hum()
                    q=st.slider("year",min_value=2009,max_value=2019,step=1) 
                    humidity(q)               
               elif e=="UVindex":     
                    uv1([300,250,100,150,170,220,260,320,350,290,90])   
                    uv()
               elif e=="Heatindex": 
                    heat()
               elif e=="Wind Speed and Direction":
                    st.title("WIND ROSE GRAPH BETWEEN WIND DIRECTION AND SPEED")  
                    wind()
               elif e=="Coorelation Analysis":
                    st.title("CORRELATION ANALYSIS")
                    corr()
               elif e=="sunhours":
                    sun("Jaipur")
                    
          elif st1=="Kanpur": 
               f=st.sidebar.selectbox("select trends",options=["Temperature Trends","Yearly and Monthly Precipitaion(MM)","Humidity variation","UVindex","Heatindex","Wind Speed and Direction","Coorelation Analysis","sunhours"])
               df=load_data("kanpur.csv")
               df['date_time'] = pd.to_datetime(df['date_time'])
               df["year"]=df["date_time"].dt.year
               df["month"]=df["date_time"].dt.month 
               if f=="Temperature Trends":  
                    temp()
                    l=st.slider("Year",min_value=2009,max_value=2019,step=1)
                    maxtemp(l)
               elif f=="Yearly and Monthly Precipitaion(MM)" :
                    st.title("YEARLY PRECIPITATION")
                    prec()
                    st.header("MONTHLY PRECIPITATION")
                    l=st.slider("select year",min_value=2009,max_value=2019,step=1)
                    precci(l)
               elif f=="Humidity variation": 
                    hum()
                    q=st.slider("year",min_value=2009,max_value=2019,step=1) 
                    humidity(q) 
               elif f=="UVindex":    
                    uv1([150,250,50,170,180,270,300,260,350,260,180])        
                    uv()
               elif f=="Heatindex": 
                    heat() 
               elif f=="Wind Speed and Direction":
                    st.title("WIND ROSE GRAPH BETWEEN WIND DIRECTION AND SPEED")  
                    wind()
               elif f=="Coorelation Analysis":
                    st.title("CORRELATION ANALYSIS")
                    corr() 
               elif f=="sunhours":
                    sun("Kanpur") 

          elif st1=="Nagpur": 
               g=st.sidebar.selectbox("select trends",options=["Temperature Trends","Yearly and Monthly Precipitaion(MM)","Humidity variation","UVindex","Heatindex","Wind Speed and Direction","Coorelation Analysis","sunhours"])
               df=load_data("nagpur.csv")
               df['date_time'] = pd.to_datetime(df['date_time'])
               df["year"]=df["date_time"].dt.year
               df["month"]=df["date_time"].dt.month 
               if g=="Temperature Trends":  
                    temp() 
                    l=st.slider("Year",min_value=2009,max_value=2019,step=1)
                    maxtemp(l)
               elif g=="Yearly and Monthly Precipitaion(MM)" :
                    st.title("YEARLY PRECIPITATION")
                    prec()  
                    st.header("MONTHLY PRECIPITATION")
                    l=st.slider("select year",min_value=2009,max_value=2019,step=1)
                    precci(l)
               elif g=="Humidity variation": 
                    hum()
                    q=st.slider("year",min_value=2009,max_value=2019,step=1)  
                    humidity(q) 
               elif g=="UVindex":
                    uv1([50,230,100,150,80,300,230,160,270,250,50])   
                    uv()
               elif g=="Heatindex": 
                   heat()
               elif g=="Wind Speed and Direction":
                    st.title("WIND ROSE GRAPH BETWEEN WIND DIRECTION AND SPEED")   
                    wind() 
               elif g=="Coorelation Analysis":
                    st.title("CORRELATION ANALYSIS")
                    corr() 
               elif g=="sunhours":
                    sun("Nagpur")

          elif st1=="Pune": 
               h=st.sidebar.selectbox("select trends",options=["Temperature Trends","Yearly and Monthly Precipitaion(MM)","Humidity variation","UVindex","Heatindex","Wind Speed and Direction","Coorelation Analysis","sunhours"])
               df=load_data("pune.csv")
               df['date_time'] = pd.to_datetime(df['date_time'])
               df["year"]=df["date_time"].dt.year
               df["month"]=df["date_time"].dt.month 
               if h=="Temperature Trends":  
                    temp() 
                    l=st.slider("Year",min_value=2009,max_value=2019,step=1)
                    maxtemp(l)
               elif h=="Yearly and Monthly Precipitaion(MM)" :
                    st.title("YEARLY PRECIPITATION")
                    prec() 
                    st.header("MONTHLY PRECIPITATION")
                    l=st.slider("select year",min_value=2009,max_value=2019,step=1) 
                    precci(l)
               elif h=="Humidity variation": 
                    hum() 
                    q=st.slider("year",min_value=2009,max_value=2019,step=1) 
                    humidity(q) 
               elif h=="UVindex":
                    uv1([250,230,100,150,80,300,230,160,270,250,50])   
                    uv()
               elif h=="Heatindex":
                    heat()

               elif h=="Wind Speed and Direction":
                    st.title("WIND ROSE GRAPH BETWEEN WIND DIRECTION AND SPEED")   
                    wind()
               elif h=="Coorelation Analysis":
                    st.title("CORRELATION ANALYSIS")
                    corr() 
               elif h=="sunhours":
                   sun("Pune")                                                                                                                                                                                                                                 
     elif a=="COMPARISON OF CITIES":
          df=pd.read_csv("bengaluru.csv")
          df['date_time'] = pd.to_datetime(df['date_time'])
          df1=pd.read_csv("bombay.csv")
          df1['date_time'] = pd.to_datetime(df['date_time'])          
          df2=pd.read_csv("hyderabad.csv")
          df2['date_time'] = pd.to_datetime(df2['date_time'])          
          df3=pd.read_csv("jaipur.csv")
          df3['date_time'] = pd.to_datetime(df3['date_time'])          
          df4=pd.read_csv("kanpur.csv")
          df4['date_time'] = pd.to_datetime(df4['date_time'])         
          df5=pd.read_csv("nagpur.csv")
          df5['date_time'] = pd.to_datetime(df5['date_time'])
          df6=pd.read_csv("pune.csv")
          df6['date_time'] = pd.to_datetime(df6['date_time'])
          a=st.sidebar.radio("select trends",options=["Precipitation","Temperature","Sunhours","Visibility trends"])
          df["year"]=df["date_time"].dt.year
          yearly_precipitation = df['precipMM'].sum()

          df1["year"]=df1["date_time"].dt.year
          bombay_precipitation = df1['precipMM'].sum()

          df2["year"]=df2["date_time"].dt.year
          hyderabad_precipitation = df2['precipMM'].sum()

          df3["year"]=df3["date_time"].dt.year
          jaipur_precipitation = df3['precipMM'].sum()

          df4["year"]=df4["date_time"].dt.year
          kanpur_precipitation = df4['precipMM'].sum()

          df5["year"]=df5["date_time"].dt.year
          nagpur_precipitation = df5['precipMM'].sum()

          df6["year"]=df6["date_time"].dt.year
          pune_precipitation = df6['precipMM'].sum()
     
          if a=="Precipitation":# with st.expander("TOTAL PRECIPITATION(MM) IN DIFFERENT CITIES "):
               
               cities = ['bombay', 'benagluru','hyderabad','jaipur','kanpur','nagpur','pune']
               precipitation_values = [bombay_precipitation,yearly_precipitation,hyderabad_precipitation,jaipur_precipitation,
               kanpur_precipitation,nagpur_precipitation,pune_precipitation]
               fig = go.Figure([go.Bar(x=cities, y=precipitation_values)])
               fig.update_layout(title='Total Precipitation  from 2009 t0 2019',title_x=0.3,xaxis_title='City',yaxis_title='Total Precipitation (mm)')
               st.plotly_chart(fig)

          if a=="Temperature":# with st.expander("VARIATION IN RANGE OF MAX TEMPERATURE IN DIFFERENT CITIES "):
               fig = go.Figure()
               fig.add_trace(go.Box(y=df['maxtempC'], name="bengaluru ", marker_color='violet', whiskerwidth=0))
               fig.add_trace(go.Box(y=df1['maxtempC'], name="bombay ", marker_color='indigo'))
               fig.add_trace(go.Box(y=df2['maxtempC'], name="Hyderabad ", marker_color='blue'))
               fig.add_trace(go.Box(y=df3['maxtempC'], name="jaipur ", marker_color='green'))
               fig.add_trace(go.Box(y=df4['maxtempC'], name="kanpur ", marker_color='yellow'))
               fig.add_trace(go.Box(y=df5['maxtempC'], name="nagpur ", marker_color='orange'))
               fig.add_trace(go.Box(y=df6['maxtempC'], name="Pune ", marker_color='red'))
               fig.update_layout(title="Boxplot of Maximum Temperatures of diffrent cities",yaxis_title="Temperature (°C)",title_x=0.2,boxmode='group' )
               st.plotly_chart(fig) 
# with st.expander("VARIATION IN RANGE OF MINIMUM TEMPERATURE IN DIFFERENT CITIES "):
               fig = go.Figure()
               fig.add_trace(go.Box(y=df['mintempC'], name="bengaluru ", marker_color='violet', whiskerwidth=0))
               fig.add_trace(go.Box(y=df1['mintempC'], name="bombay ", marker_color='indigo'))
               fig.add_trace(go.Box(y=df2['mintempC'], name="Hyderabad ", marker_color='blue'))
               fig.add_trace(go.Box(y=df3['mintempC'], name="jaipur ", marker_color='green'))
               fig.add_trace(go.Box(y=df4['mintempC'], name="kanpur ", marker_color='yellow'))
               fig.add_trace(go.Box(y=df5['mintempC'], name="nagpur ", marker_color='orange'))
               fig.add_trace(go.Box(y=df6['mintempC'], name="Pune ", marker_color='red'))
               fig.update_layout(title="Boxplot of Minimum Temperatures  variation of diffrent cities",
               yaxis_title="Temperature (°C)",title_x=0.2,boxmode='group' 
               )
               st.plotly_chart(fig)     
          if a=="Sunhours":# with st.expander("AVERAGE SUNHOURS OF DIFFERENT CITIES"):
               a=df["sunHour"].mean()
               b=df1["sunHour"].mean()
               c=df2["sunHour"].mean()
               d=df3["sunHour"].mean()
               e=df4["sunHour"].mean()
               f=df5["sunHour"].mean()
               g=df6["sunHour"].mean()
               cities = ['bombay', 'benagluru','hyderabad','jaipur','kanpur','nagpur','pune']
               sunhours = [a,b,c,d,e,f,g]
               fig = go.Figure(data=[go.Scatter(x=cities,y=sunhours,mode='markers',
               marker=dict(
                    color=[10.6,10.8,10.7,11.3,11.03,10.8,10.44],
                    size=[40,50,45,70,65,60,20],
                    showscale=True
                    ))])
               fig.update_layout( title='Scatter plot of avg sunhours in different cities ',
               title_x=0.3,xaxis_title='City',template="xgridoff",yaxis_title='avg sunhours' )
               st.plotly_chart(fig)    

          if a=="Visibility trends":  # with st.expander("VARIATION OF VISIBILITY IN DIFFERENT CITIES"):
               a=st.slider(" ",min_value=2009,max_value=2019,step=1)
               u=df.groupby('year')['visibility'].mean().reset_index()
               v=df1.groupby('year')['visibility'].mean().reset_index()
               w=df2.groupby('year')['visibility'].mean().reset_index()
               x=df3.groupby('year')['visibility'].mean().reset_index()
               y=df4.groupby('year')['visibility'].mean().reset_index()
               z=df5.groupby('year')['visibility'].mean().reset_index()
               q=df6.groupby('year')['visibility'].mean().reset_index()
               def visib(yea,num):
                    cities = ['bengaluru', 'bombay','hyderabad','jaipur','kanpur','nagpur','pune']
                    visi = [u.visibility[num],v.visibility[num],w.visibility[num],x.visibility[num],y.visibility[num],z.visibility[num],q.visibility[num]]
                    fig = px.line(x=cities,y=visi,markers=True)
                    fig.update_layout(title=f'line plot of  visibility in different cities in {yea} ',
                    title_x=0.3,xaxis_title='Cities',yaxis_title='visibility')
                    st.plotly_chart(fig) 
               if a==2009: 
                    visib(2009,0)
               if a==2010:
                    visib(2010,1)   
               if a==2011: 
                    visib(2011,2)
               if a==2012:  
                    visib(2012,3)
               if a==2013:
                    visib(2013,4)
               if a==2014:
                    visib(2014,5)                         
               if a==2015:
                    visib(2015,6)                        
               if a==2016:
                    visib(2016,7)
               if a==2017:
                    visib(2017,8)
               if a==2018:
                    visib(2018,9)
               if a==2019:
                    visib(2019,10)  
     elif a=="GEOGRAPHICAL MAP":
          data = {
               'City': ['Bengaluru', 'Bombay', 'Delhi', 'Hyderabad', 'Jaipur', 'Kanpur', 'Nagpur', 'Pune'],
               'Latitude': [12.9716, 19.0760, 28.7041, 17.3850, 26.9124, 26.4499, 21.1466, 18.5204],
               'Longitude': [77.5946, 72.8777, 77.1025, 78.4867, 75.7873, 80.3319, 79.0882, 73.8567],
               'Temperature': [29.64, 30.76, 32.68, 31.83, 32.78, 33.40, 33.63, 30.94],
               'Humidity': [64.89, 66.70, 41.32,52.87 ,37.58,44.37,47.14,57.86]  
               }
          df = pd.DataFrame(data)
          avg_temperature = df['Temperature'].mean()
          avg_humidity = df['Humidity'].mean()
          st.write(f"### Average Weather Parameters")
          st.write(f"- **Average Temperature**: {avg_temperature:.2f}°C")
          st.write(f"- **Average Humidity**: {avg_humidity:.2f}%")
          st.title("Weather Map with Data of different location(2009-2019)")
          m = folium.Map(location=[20.5937, 78.9629], zoom_start=5)  
          for i, row in df.iterrows():
               folium.Marker(
                    location=[row['Latitude'], row['Longitude']],
                    popup=f"<b>{row['City']}</b><br>Temperature: {row['Temperature']}°C<br>Humidity: {row['Humidity']}%",
                    icon=folium.Icon(color='blue') ,tooltip="Click for Info" 
               ).add_to(m)
          folium_static(m)
     
               
elif option=="About us":
    st.write("<h1 style='text-align: center;'>ABOUT US</h1>", unsafe_allow_html=True)
    st.markdown("""
    
    At the **Weather Analysis Dashboard**, our mission is to provide insightful and interactive weather data analysis for cities across India. Whether you're curious about historical weather trends, seasonal changes, or city-wise comparisons, this platform is designed to make weather data accessible and engaging.
    ### Our Purpose
    Understanding weather patterns is essential for planning daily activities, preparing for extreme weather, and gaining insights into environmental changes. This dashboard empowers users with tools to analyze, visualize, and interpret weather data with ease.
    ### Key Features
    - **Comprehensive Data:** Analyze historical weather data for multiple Indian cities, including temperature, humidity, rainfall, and more.
    - **Interactive Visualizations:** Explore trends through line graphs, heatmaps, scatter plots, and wind roses.
    - **City Comparisons:** Compare weather parameters like temperature and precipitation across cities.
    - **Seasonal Insights:** Gain insights into how weather changes throughout the year.
    - **Health Advisory:** Stay informed with recommendations based on UV index and humidity levels.


    ### Our Goals
    1. **Accessibility:** Make weather data analysis simple for users, regardless of technical expertise.
    2. **Education:** Provide valuable insights into weather patterns for researchers, students, and enthusiasts.
    3. **Planning:** Help users make informed decisions about travel, events, or daily activities based on weather data.

    ---

    ### Our Story
    This project was initiated as part of a larger effort to understand and visualize weather trends using advanced data analysis tools. Developed using **Python**, **Streamlit**, **Pandas**, **Matplotlib**, **Seaborn**, and other libraries, it showcases the power of modern data visualization techniques in understanding complex datasets.

    - **SAGAR**: Developer & Data Analyst  
  
    - **Institution**: [DAV University]

    """, unsafe_allow_html=True)
