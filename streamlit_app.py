import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt

# Page layout and text
st.set_page_config(
    page_title='Dashboard',
    layout='wide'
    )

st.title('Price Comparison')
st.markdown('version 2.0')


# Convert values in column with 'price' in them to float
@st.cache_data
def load_data(file):
    data = pd.read_csv(file)
    
    for column in data.columns:
        if 'price' in column.lower():  
            if data[column].dtype == 'object': 
                data[column] = data[column].str.replace(',', '.').astype(float)
    
    if 'matched_chip' in data.columns:
        data = data[data['matched_chip'].notna()]
            
    return data


    
df = load_data('matching_only.csv') # Dataframe 

# Add eur to the end of values in 'price' column
column_config = {}
for column in df.columns:
    if 'price' in column.lower():
        column_config[column] = st.column_config.NumberColumn(
            column,
            format='€%.2f'
        )


# Add 'Data Preview'
with st.expander('Data Preview'):
    st.dataframe(
        df,
        column_config=column_config
        )


# bar graph 

bar_chart = (df
    .set_index("name")[["price_dirk", "price_ah", "price_spar", "price_dekamarkt"]]
    .rename(columns={"price_dirk": "Dirk", "price_ah": "AH", "price_spar": "Spar", "price_dekamarkt": "Dekamarkt"})
)

fig, ax = plt.subplots(figsize=(14, 6))

bar_chart.plot(
    kind="bar",
    ax=ax,
    color=["#d62728", "#1f77b4", "#329954", "#ffc400"]  # Dirk, AH, Spar, Dekamarkt
)

ax.set_xlabel("Product")
ax.set_ylabel("Price (€)")
plt.xticks(rotation=45, ha="right")
plt.tight_layout()

st.pyplot(fig)


#boxplot 

df_box = (df
    .set_index("name")[["price_dirk", "price_ah", "price_spar", "price_dekamarkt"]]
    .rename(columns={"price_dirk": "Dirk", "price_ah": "AH", "price_spar": "Spar", "price_dekamarkt": "Dekamarkt"})
)

fig, ax = plt.subplots(figsize=(14, 6))
df_box.plot(kind="box", ax=ax)

ax.set_ylabel("Price (€)")
plt.tight_layout()

st.pyplot(fig)


#line graph 

df = (df
      .set_index("name")[["price_dirk", "price_ah", "price_spar", "price_dekamarkt"]]
      .rename(columns={"price_dirk": "Dirk", "price_ah": "AH", "price_spar": "Spar", "price_dekamarkt": "Dekamarkt"}))

fig, ax = plt.subplots(figsize=(14, 6))
df_box.plot(kind="line", ax=ax)

ax.set_ylabel("Price (€)")
plt.tight_layout()

st.pyplot(fig)
