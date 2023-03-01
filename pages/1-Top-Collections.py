import streamlit as st
import requests
from streamlit_echarts import st_echarts
import plotly.express as px
import plotly.graph_objects as go

def is_image(metadata_uri: str):
    if metadata_uri.endswith('json'):
        return False
    else:
        return True

COLUMN_SIZE = 3

api_address = "http://aptos-mainnet.nodeinfra.com/api/"
api_endpoint = 'hotcollections'

total_collections = 0
total_activity = 0

collection_list = list()
volume_list = list()



st.set_page_config(
    page_title="NodeInfra",
    page_icon="./imgs/nodeinfra.png"
)
st.title("Hottest Collections")



hours = st.slider("Aggregate for selected time", min_value=72, max_value=168, step=1, value=160)
button = st.button("GET IT")
if button:
    print('-----------button----------')
    with st.spinner("Waitting..."):
        response = requests.get(api_address + api_endpoint, {'hours':hours})
        collection_volume_list = response.json()['collection_volumes']
        for collection_volume in collection_volume_list:
            # total_collections+=1
            # total_activity+=collection_volume['volume']
            collection_list.append(collection_volume['name'])
            volume_list.append(collection_volume['volume'])
            
        labels = collection_list
        values = volume_list
        
        
        st.write("Top 10 Volume of Collections")
        pie = go.Figure(data=[go.Pie(labels=labels, values=values)])
        st.plotly_chart(pie, use_container_width=True)
        for index, collection in enumerate(collection_volume_list):
            if index % COLUMN_SIZE == 0:
                col_list = st.columns(COLUMN_SIZE)
            metadata_uri = collection['metadata_uri']
            if not is_image(metadata_uri):
                response = requests.get(collection['metadata_uri']).json()
                collection['metadata_uri'] = response['image']
            col_list[index%COLUMN_SIZE].write('#' + str(index+1)+' ' + collection['name'])
            col_list[index%COLUMN_SIZE].image(collection['metadata_uri'])
