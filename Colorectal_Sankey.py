import pandas as pd
import numpy as np
import plotly.graph_objects as go
import plotly.express as px
import streamlit as st

st.set_page_config(layout="wide")

st.title("Colorectal Appointments")
st.subheader("Non-attendances")





df = pd.read_csv('ColorectalAppt.csv')
appt_select = st.radio("Please select initial appointment",
                            df["Appt_Type"].unique()
                        )
col_1, col_2 = st.columns(2)
with col_1:
# Sankey Chart
    
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

with col_2:
# Table
    appt_table = df.groupby(["Appt_Type","Missed_Appt"]
                        )["Patient_ID"].count().reset_index()

    appt_table.columns = ["Appointment Type",
                        "Missed Appointment",
                        "No. of Patients"]
    st.write('<style>div.st-bf{flex-direction:column;} div.st-ag{font-weight:bold;padding-left:2px;}</style>', unsafe_allow_html=True)

    

    appt_table = appt_table[appt_table["Appointment Type"] == appt_select]


    #st.dataframe(appt_table, column_order=("Missed Appointment", "No. of Patients"))
    fig2 = px.bar(
        appt_table, x="Missed Appointment", y= "No. of Patients"
    )
    st.plotly_chart(fig2)

