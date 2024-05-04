import streamlit as st
import pandas as pd
import altair as alt


# loading data
df = pd.read_csv("excess_deaths.csv")

# widening layout
st.set_page_config(layout="wide")


# defining sidebar selection of chronic diseases
st.sidebar.title("Select Cause of Death:")
cause = st.sidebar.selectbox("Cause of Death:", df["Cause of Death"].unique()[:],key="death_selector")


# filtering the data based on the selected cause of death and calculate the age-adjusted death rate
df_filtered = df[df["Cause of Death"] == cause]
deaths = df_filtered["Potentially Excess Deaths"].mean()


# defining sidebar tabs
tab = ["About", "National Level", "State Level", "Description"]
chosen_tab = st.sidebar.radio("Select A Tab For Additional Information:", tab)


# defining cause
cause_description = {
   "Cancer": "Cancer is a genetic disease that is caused by changes to genes that control the way cells function, especially how they grow and divide. Cancer can grow on any organ or tissue cell uncontrollably and spread to other parts of the body. For more information, please visit [cancer.gov.](https://www.cancer.gov/about-cancer/understanding/what-is-cancer#:~:text=Cancer%20is%20a%20disease%20caused,are%20also%20called%20genetic%20changes.)",
   "Chronic Lower Respiratory Disease": "Chronic Lower Respiratory Disease, or CLRD, is a group of disorders affecting the lungs and airways. CLRD encompasses four commonly overlapping chronic diseases: chronic obstructive pulmonary disease (COPD), asthma, emphysema, and chronic bronchitis. According to the Centers for Disease Control and Prevention (CDC), cigarette smoking is the major cause of these illnesses, accounting for about 80% of cases. However, exposure to air pollutants in the home and workplace, genetic factors, and respiratory infections can also play a role in the development of chronic lower respiratory disease. For more information, please visit [verywellhealth](https://www.verywellhealth.com/what-is-chronic-lower-respiratory-disease-2224212).",
   "Heart Disease": "Heart disease refers to several types of heart conditions, with the most common in the United States is coronary artery disease (CAD), affecting the blood flow to heart which can lead to a heart attack. Sometimes heart disease may be “silent” and not diagnosed until a person experiences signs or symptoms of a heart attack, heart failure, or an arrhythmia. For more information on risk factors of heart disease and how to reduce those risks, please visit [cdc.gov](https://www.cdc.gov/heartdisease/about.htm) .",
   "Stroke": "A stroke can occur when blood flow to the brain is blocked or there is sudden bleeding in the brain. There are two types of strokes. A stroke that occurs because blood flow to the brain is blocked is called an ischemic stroke. The brain cannot get oxygen and nutrients from the blood. Without oxygen and nutrients, brain cells begin to die within minutes. A stroke that occurs because of sudden bleeding in the brain is called a hemorrhagic stroke. The leaked blood results in pressure on brain cells, damaging them. For more information, please visit [nhlbi.nih.gov](https://www.nhlbi.nih.gov/health/stroke).",
   "Unintentional Injury": "Unintentional injury is an injury or poisoning that is not inflicted by deliberate means, including those injuries and poisonings described as unintended or “accidental”, regardless of whether the injury was inflicted by oneself or by another person. Also, it includes injury or poisoning where no indication of intent to harm was documented in the ED record. Some of the most common types of unintentional injuries in the United States include: motor vehicle accidents, suffocation, drowning, poisoning, fire/burns, falls and sports and recreation.",
}


# defining tab content
if chosen_tab == "About":
   st.markdown('''
# Potentially Excess Deaths From Five Leading Causes of Death, 2005-2015
''')
   st.write("Potentially excess deaths are defined in MMWR Surveillance Summary 66(No. SS-1):1-8 as deaths that exceed the numbers that would be expected if the death rates of states with the lowest rates (benchmarks) occurred across all states. They are calculated by subtracting expected deaths for specific benchmarks from observed deaths.")
   st.write("The data accompanies this app by presenting information on potentially excess deaths in nonmetropolitan and metropolitan areas at the state level (see Excess Deaths at State Level tab).")
   st.write("Not all potentially excess deaths can be prevented; some areas might have characteristics that predispose them to higher rates of death. However, many potentially excess deaths might represent deaths that could be prevented through improved public health programs that support healthier behaviors and neighborhoods or better access to health care services.")
   st.write("Reference: Moy E, Garcia MC, Bastian B, et al. Potentially Excess Deaths from the Five Leading Causes of Death in Nonmetropolitan and Metropolitan Areas in the United States, 2005-2015. National Center for Health Statistics. 2017.")
   st.write("Additional information is available [here](https://www.cdc.gov/nchs/data-visualization/potentially-excess-deaths/index.htm).")
   st.write("Using the sidebar, please click through each tab to view more information based on the different causes of death.")


elif chosen_tab == "National Level":
   # line chart for deaths at national level
   chart_data = df_filtered.groupby("Year")["Potentially Excess Deaths"].mean().reset_index()
   chart = alt.Chart(chart_data).mark_line(color="orange").encode(
       x=alt.X ("Year", axis=alt.Axis(format="")),
       y=alt.Y("Potentially Excess Deaths", scale=alt.Scale(zero=False))
   )
   st.write("# The Average Potentially Excess Deaths Over Time Nationally")
   st.write(f"The line chart below displays the average potentially excess deaths for {cause} at the national level from 2005 - 2015 in the United States.")
   st.altair_chart(chart, use_container_width=True)

   st.metric(value=f"{deaths:.2f}", label="National average of potentially excess deaths:")

   st.write("Use the sidebar to select a different cause of death.")


elif chosen_tab == "State Level":
   # area chart for deaths at state level
   st.write("# The Average Potentially Excess Deaths Over Time In Each State")
   state = df["State"].unique().tolist()
   chosen_state = st.selectbox("Select a State:", state)
   df_filtered = df.loc[(df["State"] == chosen_state) & (df["Cause of Death"] == cause)]
   avg_death = df_filtered["Potentially Excess Deaths"].mean()
   area_data = df_filtered.groupby(["Year"])[["Potentially Excess Deaths"]].mean().reset_index()
   chart = alt.Chart(area_data).mark_area(color="orange").encode(
       x=alt.X("Year", axis=alt.Axis(format="")),
       y= alt.Y("Potentially Excess Deaths", scale=alt.Scale(zero=False)),       
   ).properties(
   title=f'Potentially Excess Deaths (Avg) from {cause} in {chosen_state}.'
   )


   # displaying area chart
   st.altair_chart(chart, use_container_width=True)

   st.metric(value=f"{avg_death:.2f}", label="Average potentially excess deaths the state:")


   # bar chart for deaths by locality
   locality = df["Locality"].unique().tolist()
   chosen_locality = st.selectbox("Select Locality:", locality)
   df_filtered = df.loc[(df["Locality"] == chosen_locality) & (df["Cause of Death"] == cause) & (df["State"] == chosen_state)]

   avg_death = df_filtered["Potentially Excess Deaths"].mean()
   bar_data = df_filtered.groupby(["Locality"])[["Potentially Excess Deaths"]].mean().reset_index()
   bar_chart = alt.Chart(bar_data).mark_bar(color="blue").encode(
       x=alt.X("Locality", axis=alt.Axis(format="")),
       y= alt.Y("Potentially Excess Deaths", scale=alt.Scale(zero=False)),       
   ).properties(
   title=f'Potentially Excess Deaths (Avg) from {cause} in {chosen_locality} areas in {chosen_state}.'
   )


   # displaying bar chart
   st.altair_chart(bar_chart, use_container_width=True)

   st.metric(value=f"{avg_death:.2f}", label="Average potentially excess deaths in the locality:")

  
else:
   # cause descriptions
   if chosen_tab == "Description":
       st.write(f"# Description of: {cause} ")
       st.write(cause_description.get(cause, "No description available."))



  
       st.metric(value=f"{deaths:.2f}", label="National average of potentially excess deaths:")
