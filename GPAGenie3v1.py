import streamlit as st
import pandas as pd
import json

st.set_page_config(layout="wide")

st.subheader('GPA Genie')
st.divider()
cols = st.columns(2)
tab1, tab2, tab3, tab4 = st.tabs(["Enter a Class", "Your Classes", "Insights and Results", "Chatbot"])

classData_df = pd.read_csv('data/classData.csv')

with st.sidebar:
    st.title("Help Menu")

with tab1:
    rigor = st.radio(
        "Select the class's rigor level:",
        ["On-Level", "Honors", "Advanced Placement", "Dual Enrollment"],
        captions = ["Non-honors, AP, or college classes", 
                    "Advanced, accelerated or honors classes", 
                    "AP classes", 
                    "College classes"])
    
    with open('data/classes.json', 'r') as classes_file:
        classes = json.load(classes_file)[rigor]
    className = st.selectbox("Select the name of your class: ", (classes))
    st.write("You selected: ", f"**:blue[{className}]**")
    
    grade = st.number_input(label="Enter the Grade Earned: ", min_value=0, max_value=100, value=None, step=1)
    st.write("You entered: ", f"**:blue[{grade}]**")
    
    st.write("Are you sure you want to add the ", f"**:blue[{rigor}]**", " class, ", f"**:blue[{className}]**", " with a grade of ", f"**:blue[{grade}]**", "?")
    classEnterButton = st.button("Confirm")

    if classEnterButton:
        classData_df.loc[len(classData_df.index)] = [rigor, className, grade]
        classData_df
        #classData_df = classData_df._append({"ClassRigor":rigor,"ClassName":className,"GradeEarned":grade},ignore_index=True)
        classData_df.to_csv('data/classData.csv', index = False)

with tab2:
    
    csvfn = 'data/classData.csv'

    def update(edf):
        edf.to_csv(csvfn, index=False)
        load_df.clear()
        

    @st.cache_data(ttl='1d')
    def load_df():
        return pd.read_csv(csvfn)

    classData_df = load_df()
    st.write("Edit your classes below!")
    edf = st.data_editor(pd.read_csv(csvfn),
                                     num_rows='dynamic',
                                     column_config={'ClassRigor':'Rigor',
                                                    'ClassName': 'Name',
                                                    'GradeEarned': 'Grade'})
    st.button('Save', on_click=update, args=(edf, ))