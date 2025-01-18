import streamlit as st 
import pandas as pd
import numpy as np 
import matplotlib.pyplot as plt
import seaborn as sns

st.title('ANALISIS DATA BIKE SHARING 2011 - 2012')
st.markdown(
    "<h2 style='text-align: center;'>Bike Sharing Analytics Dashboard</h2>", 
    unsafe_allow_html=True
)

col1, col2, col3 = st.columns([1, 2, 1])
with col2:
    st.image("sepeda.jpg", width=400)

st.markdown("<br><br>", unsafe_allow_html=True)

st.subheader('Explanation of Data')

st.write(
        """	- instant: record index
	- dteday : date
	- season : season (1:springer, 2:summer, 3:fall, 4:winter)
	- yr : year (0: 2011, 1:2012)
	- mnth : month ( 1 to 12)
	- hr : hour (0 to 23)
	- holiday : weather day is holiday or not (extracted from http://dchr.dc.gov/page/holiday-schedule)
	- weekday : day of the week
	- workingday : if day is neither weekend nor holiday is 1, otherwise is 0.
	+ weathersit : 
		- 1: Clear, Few clouds, Partly cloudy, Partly cloudy
		- 2: Mist + Cloudy, Mist + Broken clouds, Mist + Few clouds, Mist
		- 3: Light Snow, Light Rain + Thunderstorm + Scattered clouds, Light Rain + Scattered clouds
		- 4: Heavy Rain + Ice Pallets + Thunderstorm + Mist, Snow + Fog
	- temp : Normalized temperature in Celsius. The values are divided to 41 (max)
	- atemp: Normalized feeling temperature in Celsius. The values are divided to 50 (max)
	- hum: Normalized humidity. The values are divided to 100 (max)
	- windspeed: Normalized wind speed. The values are divided to 67 (max)
	- casual: count of casual users
	- registered: count of registered users
	- cnt: count of total rental bikes including both casual and registered
        """
    )

st.markdown("<br><br>", unsafe_allow_html=True)

st.markdown(
    "<h3 style='text-align: center;'>Bike Sharing by Day</h3>", 
    unsafe_allow_html=True
)
libur = pd.read_csv('data_liburan.csv')
fig, ax = plt.subplots()
ax.plot(libur.index, libur['cnt'], marker='o')
ax.set_title("Total Count by Weekday")
ax.set_xlabel("Weekday")
ax.set_ylabel("Count")
ax.grid(True)
st.pyplot(fig)

with st.expander("Description about graph"):
    st.write(
        """
        It is known that bicycle borrowing during 2011 - 2012 has a significant 
        increase every day, especially on Saturday which has the largest sharing  
        bike value compared to other days
        """
    )

st.markdown("<br><br>", unsafe_allow_html=True)

st.markdown(
    "<h3 style='text-align: center;'>Bike Sharing by Month</h3>", 
    unsafe_allow_html=True
)
bulan = pd.read_csv('bulan.csv')
x = np.arange(len(bulan['mnth']))
width=0.4
fig, ax = plt.subplots(figsize=(20, 10))
ax.bar(x-width/2, bulan['casual'], width, label='casual')
ax.bar(x+width/2, bulan['registered'], width, label='registered')
ax.legend()
st.pyplot(fig)
with st.expander("Description about graph"):
    st.write(
        """
        It is known that registered bike sharing have more value than casual 
        bike sharing. The development of bike sharing every month in 2011 - 2012 
        in registered bicycle loans experienced the highest increase in the 6th 
        month and decreased in the 9th month
        """
    )

st.markdown("<br><br>", unsafe_allow_html=True)

st.markdown(
    "<h2 style='text-align: center;'>Interactive Dashboard</h2>", 
    unsafe_allow_html=True
)

data =  pd.read_csv('data.csv')

st.markdown("<br>", unsafe_allow_html=True)

st.markdown(
    "<h3 style='text-align: center;'>Bike Sharing by Month</h3>", 
    unsafe_allow_html=True
)

data['dteday'] = pd.to_datetime(data['dteday'])
data['tanggalan'] = data['dteday'].dt.strftime('%Y-%m-%d')
pilih = st.selectbox(
    "Date :",
    options=data['tanggalan'].unique(),
    index=0
)
ftanggal = data[data['tanggalan'] == pilih]
jam = ftanggal.groupby('hr').agg({'cnt': 'sum'}).reset_index()
jam_max = jam.loc[jam['cnt'].idxmax()]
jam_min = jam.loc[jam['cnt'].idxmin()]

fig, ax = plt.subplots(figsize=(20,10))
ax.plot(
    jam['hr'], 
    jam['cnt'], 
    marker='o', 
    linestyle='-', 
    color='b', 
    label='Bike Sharing'
)
ax.set_title(f'Bike Sharing by {pilih}', fontsize=16)
ax.set_xlabel('Hour', fontsize=12)
ax.set_ylabel('Count', fontsize=12)
ax.legend()
ax.set_xticks(range(0, 24, 1))
st.pyplot(fig)
with st.expander("Description about graph"):
    st.write(
        f"""
        In the following graph, it is known that the highest borrower value is in the 
        **{jam_max['hr']}** with a value **{jam_max['cnt']}**. The lowest borrower 
        value in this chart exists in hours **{jam_min['hr']}** with value 
        **{jam_min['cnt']}**.
        """
    )
