import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

st.set_page_config(layout='wide',page_title='StartUp Analysis')

df=pd.read_csv('startup_cleaned.csv')
df['date']=pd.to_datetime(df['date'],errors='coerce')
df['month']=df['date'].dt.month
df['year']=df['date'].dt.year

def load_investor_details(investor):
    st.title(investor)
    # load the last 5 investments of the investor
    last5_df=df[df['Investors'].str.contains(investor)].head(5)[['date','startup','vertical','city','round','amount']]
    st.subheader('Most Recent Investments')
    st.dataframe(last5_df)

    col1,col2=st.columns(2)
    with col1:
        big_series=df[df['Investors'].str.contains(investor)].groupby('startup')['amount'].sum().sort_values(ascending=False).head()
        st.subheader('Biggest Investments')
        fig,ax=plt.subplots()
        ax.bar(big_series.index,big_series.values)

        st.pyplot(fig)
        
    with col2:
        vertical_series=df[df['Investors'].str.contains(investor)].groupby('vertical')['amount'].sum()
        st.subheader('Sectors Invested In')
        fig2,ax2=plt.subplots()
        ax2.pie(vertical_series,labels=vertical_series.index,autopct="%0.01f%%")
    
        st.pyplot(fig2)

    col3,col4=st.columns(2)
    with col3:
        city_series=df[df['Investors'].str.contains(investor)].groupby('city')['amount'].sum()
        st.subheader('City Invested In')
        fig3,ax3=plt.subplots()
        ax3.pie(city_series,labels=city_series.index,autopct="%0.01f%%")

        st.pyplot(fig3)
    with col4:
        round_series=df[df['Investors'].str.contains(investor)].groupby('round')['amount'].sum()
        st.subheader('Stage Invested In')
        fig4,ax4=plt.subplots()
        ax4.pie(round_series,labels=round_series.index,autopct="%0.01f%%")
    
        st.pyplot(fig4)


    df['year']=df['date'].dt.year
    year_series=df[df['Investors'].str.contains(investor)].groupby('year')['amount'].sum()
    st.subheader('YOY Investment')
    fig5,ax5=plt.subplots()
    ax5.plot(year_series.index,year_series.values)

    st.pyplot(fig5)

def load_startup_details(startup):
    st.title(startup)
    founders=df[df['startup']==startup]['Investors'].str.split(',').sum()
    st.header('Founders')
    st.dataframe(founders)
    col1,col2=st.columns(2)
    with col1:
        industry=df[df['startup']==startup]['vertical'].unique()
        st.header('Industry')
        st.dataframe(industry)
    with col2:
        sub_industry=df[df['startup']==startup]['subvertical'].unique()
        st.header('Sub Industry')
        st.dataframe(sub_industry)

    location=df[df['startup']==startup]['city'].unique()
    st.header('Locations')
    st.dataframe(location)


def load_overall_analysis():
    st.title("Overall Analysis")
    total=round(df['amount'].sum())
    max_funding=df.groupby('startup')['amount'].max().sort_values(ascending=False).head(1).values[0]
    avg_funding=df.groupby('startup')['amount'].sum().mean()
    num_startups=df['startup'].nunique()

    col1,col2,col3,col4=st.columns(4)
    
    with col1:
        # total investment amount
        st.metric('Total Amount',str(total)+'Cr')

    with col2:
        # max amount infused in a startup
        st.metric('Maximum Amount',str(max_funding)+'Cr')

    with col3:
        # average amount infused in startups
        st.metric('Average Amount',str(round(avg_funding))+'Cr')

    with col4:
        st.metric('Count Startups',num_startups)

    st.header('MOM Graph')
    selected_var=st.selectbox('Select Type',['Total','Count'])
    if selected_var=='Total':
        temp_df=df.groupby(['year','month'])['amount'].sum().reset_index()
        
    else:
        temp_df=df.groupby(['year','month'])['amount'].count().reset_index()
    temp_df['x-axis']=temp_df['month'].astype('str')+'-'+temp_df['year'].astype('str')

    fig7,ax7=plt.subplots()
    ax7.plot(temp_df['x-axis'],temp_df['amount'])

    st.pyplot(fig7)

st.sidebar.title("Startup Funding Analysis")

option=st.sidebar.selectbox('select one',['Overall Analysis','Startup','Investor'])

if option =='Overall Analysis':
    load_overall_analysis()
elif option=='Startup':
    select_startup=st.sidebar.selectbox('Select Startup',sorted(df['startup'].unique().tolist()))
    btn1=st.sidebar.button('Find StartUp Details')
    if btn1:
        load_startup_details(select_startup)
    
else:
    selected_investor=st.sidebar.selectbox('Select Investor',sorted(set(df['Investors'].str.split(',').sum())))
    btn2=st.sidebar.button('Find Investors Details')
    if btn2:
        load_investor_details(selected_investor)
    