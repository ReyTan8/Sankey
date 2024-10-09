
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import plotly.express as px
import streamlit as st
from plotly.offline import iplot, init_notebook_mode
init_notebook_mode(connected=True)

st.set_page_config(layout="wide")

with open("style.css") as css:
    st.markdown(f'<style>{css.read()}</style>', unsafe_allow_html=True)

df = pd.read_csv("ColorectalAppt.csv")
df = df.groupby(["Appt_Type","Missed_Appt"]
                        )["Patient_ID"].count().reset_index()
df.columns = ["First Appointment Type",
               "Missed Appointment",
               "Count of Patients"]

st.title("Colorectal Appointments")
st.subheader("Non-attendances")




selection_list = list(df["First Appointment Type"].unique())
selection_list = ["All"] + selection_list
#selection_list.append(list(df["First Appointment Type"].unique()))

appt_select = st.selectbox("First Appointment Type",
                           selection_list)


def genSankey(df, cat_cols=[], value_cols="",title=""):
    colorPalette = ["#4B8BBE","#306998","#FFE873","#FFD43B","#646464"]
    labelList = []
    colorNumList = []
    for catCol in cat_cols:
        labelListTemp = list(set(df[catCol].values))
        colorNumList.append(len(labelListTemp))
        labelList = labelList + labelListTemp

    labelList = list(dict.fromkeys(labelList))

    #define colours based on number of levels
    colorList = []
    for idx, colorNum in enumerate(colorNumList):
        colorList = colorList + [colorPalette[idx]]*colorNum
    
    #transform df into source-target pair
    for i in range(len(cat_cols)-1):
        if i==0:
            sourceTargetDf = df[[cat_cols[i], cat_cols[i+1], value_cols]]
            sourceTargetDf.columns = ["source","target","count"]
        else:
            tempDf = df[[cat_cols[i],cat_cols[i+1],value_cols]]
            tempDf.columns = ["source","target","count"]
            sourceTargetDf = pd.concat([sourceTargetDf,tempDf])
        sourceTargetDf = sourceTargetDf.groupby(
            ["source","target"]).agg({"count":"sum"}).reset_index()
        
    # add index for source-target pair
    sourceTargetDf["sourceID"] = sourceTargetDf[
        "source"].apply(lambda x: labelList.index(x))
    sourceTargetDf["targetID"] = sourceTargetDf[
        "target"].apply(lambda x: labelList.index(x))
    
    data = dict(
        type="sankey",
        node = dict(
          pad = 10,
          thickness = 30,
          line = dict(
            color = "black",
            width = 0.5
          ),
          label = labelList,
          color = colorList
        ),
        link = dict(
          source = sourceTargetDf["sourceID"],
          target = sourceTargetDf["targetID"],
          value = sourceTargetDf["count"]
        )
      )
    
    layout =  dict(
        font = dict(
          size = 14
        )
    )
       
    fig = dict(data=[data], layout=layout)
    return fig

# update layout with buttons, and show the figure
if appt_select != "All":
    df_sankey = df[df["First Appointment Type"]==appt_select]
else:
    df_sankey = df

col1, col2 = st.columns(2)

with col1:

  sankey_diag = genSankey(df_sankey, 
                          cat_cols =["First Appointment Type",
                                    "Missed Appointment"],
                          value_cols = "Count of Patients"
                          )
  fig = go.Figure(sankey_diag)
  fig.update_layout(margin={'t':10,'b':20})
#iplot(fig)
#fig.show()
  st.plotly_chart(fig)

with col2:
  st.dataframe(df_sankey, hide_index=True)



