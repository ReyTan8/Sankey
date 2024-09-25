import pandas as pd
import numpy as np
import plotly.graph_objects as go
import plotly.express as px
import streamlit as st

st.set_page_config(layout="centered")

st.title("Colorectal Appointments")
st.subheader("Non-attendances")

df = pd.read_csv('ColorectalAppt.csv')

links = df.groupby(["Appt_Type","Missed_Appt"]
                      )["Patient_ID"].count().reset_index()
links.columns = ["source","target","value"]

unique_source_target = list(pd.unique(links[["source",
                                             "target"]].values.ravel("K")))

mapping_dict = {k: v for v, k in enumerate(unique_source_target)}

links["source"] = links["source"].map(mapping_dict)
links["target"] = links["target"].map(mapping_dict)

links_dict = links.to_dict(orient = "list")



color_node = [
    '#75F4F4','#B8B3E9','#D999B9','#D17B88',
    '#90E0F3','#FBD87F','#4E3D42','#157A6E',
    '#499F68','#397367','#F2CEE6','#E54F6D',
    '#1C7293','#A69CAC','#E0777D'
]


color_link = [
    '#75F4F4','#B8B3E9','#D999B9','#D17B88'
]

fig = go.Figure(data=[go.Sankey(
    node = dict(
        pad = 15,
        thickness = 20,
        label = unique_source_target,
        color = color_node        
        ),
    
    link = dict(
        source = links_dict["source"],
        target = links_dict["target"],
        value = links_dict["value"]
        #color = color_link
    ),

    textfont=dict(
            family="Arial",
            size=12,
            color="black")
)]
)

fig.update_layout()
#fig.show()

st.plotly_chart(fig)