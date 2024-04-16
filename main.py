import streamlit as st
import staffingdb as stdb
from PIL import Image
import pandas as pd
import altair as alt
# You can always call this function where ever you want

# Function to create bar chart
def create_bar_chart(df):
    chart = alt.Chart(df.reset_index()).encode(
        x=alt.X('Location', sort=list(df.index)),  # Sorting by index
        y=alt.Y('Project Staffing Percentage', axis=alt.Axis(format='%'))
    )
    return chart.mark_bar(color='#384268') + chart.mark_text(baseline='top', fontSize=16, fontWeight="bold").encode(text=alt.Text('Project Staffing Percentage', format='.0%'), color=alt.value("white"))

def add_logo(logo_path, width, height):
    """Read and return a resized logo"""
    logo = Image.open(logo_path)
    modified_logo = logo.resize((width, height))
    return modified_logo

my_logo = add_logo(logo_path="./TLLogo.png", width=800, height=100)
st.image(my_logo)

#st.set_page_config(layout="centered")
#st.title(':green[Jeff]')


customer_name = st.text_input("Customer Name", key='customer')
customer_address = st.text_input("Customer Email Address", key='address')

project_name = st.text_input("Project Name", key='projectname')
project_type = st.selectbox("Project Type", ["Data Engineering","Data Migration","Pipelines and Intergration","Data Story Telling"
,"Application Development","Testing/ Functional UAT"], key='projecttype') 
project_desc = st.text_input("Project Description", key='projectdesc')

#st.divider()
with st.sidebar:
    st.title('Global Staffing Options')
    st.write('Our staffing model includes a mix of onshore, nearshore, and offshore resources by default. Clients can adjust the staffing mix by unchecking the respective boxes for nearshore or offshore options. The default mix prioritizes savings, adjusting based on restrictions or client preferences.')
    col1, col2 = st.columns(2)
    nearshore_cb = col1.checkbox('Near Shore', value=True, help='Our near shore team are fluent English speakers located in Bogota, Columbia')
    offshore_cb = col2.checkbox('Off Shore', value=True, help='Our off shore team are fluent English speakers located in Pakistan')
st.sidebar.title('Choose Project Priorities')
project_area_names_complexity = st.sidebar.slider("Go To Market Strategy", min_value=1, max_value=5, help='Describe the level of planning needed to deliver the product' ,key='complex')
with st.sidebar:
    if project_area_names_complexity ==1:
        st.sidebar.write('Proof of Concept')
    elif project_area_names_complexity ==2:
        st.write('Protoytpe Development')
    elif project_area_names_complexity ==3: 
        st.write('MVP')
    elif project_area_names_complexity ==4:
        st.write('Scaling Strategy Development')
    else:
        st.write('Full Feature Launch')
#    st.divider()
project_area_names_innovate = st.sidebar.slider("Innovation & Process Maturity", min_value=1, max_value=5, help='Describe the need to be more Strategic or Tactical', key='innovate')
with st.sidebar:
    if project_area_names_innovate ==1:
        st.write('Routine')
    elif project_area_names_innovate ==2:
        st.write('Flexible Process')
    elif project_area_names_innovate ==3:
        st.write('Strategic Innovation')
    elif project_area_names_innovate ==4:
        st.write('Transformational Innovation')
    else:
        st.write('Disruptor')
#st.divider()
#project_area_names_cost = st.sidebar.slider("Savings", min_value=1, max_value=5, help='Your enagagment funding level has been allocated', key='cost')
# if project_area_names_cost <3:
#     st.sidebar.write('Conservative Spend')
# elif project_area_names_cost >=3 and project_area_names_cost <5:
#     st.sidebar.write('Business Case Required for Additional Spend')
# elif project_area_names_cost >=5 and project_area_names_cost <7:
#     st.sidebar.write('Discretionary Budget Available')
# elif project_area_names_cost >=7 and project_area_names_cost <10:
#     st.sidebar.write('Budget Contingency Available')
# else:
#     st.sidebar.write('Large Investment Made')
#st.divider()
project_area_names_speed = st.sidebar.slider("Time To Deliver", min_value=1, max_value=5, help='Describe the amount of capacity to deliver the product', key='speed')
with st.sidebar:
    if project_area_names_speed ==1:
        st.sidebar.write('4-6 Weeks')
    elif project_area_names_speed ==2:
        st.write('6-12 Weeks')
    elif project_area_names_speed ==3: 
        st.write('12-20 Weeks')
    elif project_area_names_speed ==4:
        st.write('20-30 Weeks')
    else:
        st.write('30+ Weeks')
#    st.divider()
project_area_names_expertise = st.sidebar.slider("Expertise Required", min_value=1, max_value=5, help='Skillset necessary for successful delivery of the initiative', key='expert')
with st.sidebar:
    if project_area_names_expertise <3:
        st.sidebar.write('Functional Expert')
    elif project_area_names_expertise >=3 and project_area_names_expertise <5:
        st.write('Skilled Practictioner')
    else:
        st.write('Subject Matter Experts')
project_area_names_laws = st.sidebar.slider("Laws & Regulations", min_value=1, max_value=5, help='Describe the barriers to using offshore due to the nature of the work', key='laws')
with st.sidebar:
    if project_area_names_laws ==1:
        st.write('Lenient')
    elif project_area_names_laws ==2:
        st.write('Moderate Oversight')
    elif project_area_names_laws ==3:
        st.write('Enhanced Oversight')
    elif project_area_names_laws ==4:
        st.write('Highly Regulated')
    else:
        st.write('Restrictive')
# st.divider()
project_area_names_accessibility = st.sidebar.slider("Response Time", min_value=1, max_value=5, help='Communication promptness required', key="accessible")
with st.sidebar:
    if project_area_names_accessibility ==1:
        st.write('Within 1-2 Business Days')
    elif project_area_names_accessibility ==2:
        st.write('Within 6-8 hours during Operating Hours')
    elif project_area_names_accessibility ==3:
        st.write('Within 4-6 hours during Operating Hours')
    elif project_area_names_accessibility ==4:
        st.write('Within 2-4 hours during Operating Hours')
    else:
        st.write('Fully accessible during Operating Hours')
#st.divider()
#project_area_names_criticallity = st.slider("Criticallity (Org Impact)", min_value=1, max_value=10, key='critical')
project_area_names_tz = st.sidebar.slider("Timezone Coordination", min_value=1, max_value=5, help='Describe the need for resources to be time zone aligned' ,key='timezone')
with st.sidebar:
    if project_area_names_tz ==1:
        st.write('Minimal Overlap Required')
    elif project_area_names_tz ==2:
        st.write('Overlap as requested')
    elif project_area_names_tz ==3:
        st.write('Adaptive Scheduling Required')
    elif project_area_names_tz ==4:
        st.write('Alignment Required for Most Deliverables')
    else:
        st.write('Required')
#st.divider()





#project_area_names_scalabilty = st.slider("Scalability", min_value=1, max_value=10, key='scalable')
#staff_name = st.text_input("Staff Name")
#staff_type_name = st.selectbox("Staff Type", ["Engineer", "Manager", "Designer"])
#staff_level_name = st.selectbox("Staff Level", ["Senior", "Junior", "MidLevel"])
#staff_location_name = st.selectbox("Staff Location", ["New York", "Los Angeles", "Chicago"])
#st.divider()


customer1 = stdb.ProjectAdd(
    customer_name
    #, customer_address
    , project_name
    , project_type
    # , 
    # project_area_names_cost
    , project_area_names_complexity
    , project_area_names_innovate
    , project_area_names_speed
    , project_area_names_expertise
    , project_area_names_laws
    , project_area_names_accessibility
    , project_area_names_tz
    #, project_area_names_criticallity


    #, project_area_names_scalabilty
    ,nearshore_cb, offshore_cb
                            )
#customer1.save()
spread_val = customer1.getspread()
def set_value():
    customer1.save()
    st.session_state['customer'] = ''
    st.session_state['address'] = ''
    st.session_state['projectname'] = ''
    st.session_state['projecttype'] = 'Data Engineering'
    st.session_state['projectdesc'] = ''
    st.session_state['cost'] = 1
    st.session_state['speed'] = 1
    #st.session_state['critical'] = 1
    st.session_state['timezone'] = 1
    st.session_state['complex'] = 1
    st.session_state['expert'] = 1
    st.session_state['laws'] = 1
    st.session_state['accessible'] = 1
    st.session_state['innovate'] = 1
    #st.session_state['scalable'] = 1
    st.write(f'Submission was added successfully')
st.divider()
st.write(f"Potential Savings utilizing Thought Logic's Ignition Staffing Model is {spread_val[1][0]} to {spread_val[1][1]}")

df = pd.DataFrame(spread_val[0], columns=['Location','Project Staffing Percentage'])
# Update and display bar chart
updated_bar_chart = create_bar_chart(df)
#st.subheader('Updated Bar Chart')
st.altair_chart(updated_bar_chart, use_container_width=True)

#st.write('Please submit selections if you would like to be contacted about your engagement')
#testresult = st.button(label="Submit", on_click=set_value)
#if testresult:
#    customer1.save()
