import streamlit as st
import pandas as pd
import json
import streamlit as st
from llama_index.core import VectorStoreIndex, ServiceContext, Document
from llama_index.llms.openai import OpenAI
import openai
from llama_index.core import SimpleDirectoryReader

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

with tab3:
    def update_GPA(currentClasses):
        uwGPA = 0
        wGPA = 0

        for i in currentClasses:
            if int(i[2]) > 89:
                uwGPA += 4
                wGPA += 4
                if (i[0] != "Honors") and (i[0] != "On-Level"):
                    wGPA += 1
            elif int(i[2]) > 79:
                uwGPA += 3
                wGPA += 3
                if (i[0] != "Honors") and (i[0] != "On-Level"):
                    wGPA += 1
            elif int(i[2]) > 69:
                uwGPA += 2
                wGPA += 2
                if (i[0] != "Honors") and (i[0] != "On-Level"):
                    wGPA += 1
            else:
                uwGPA += 0
                wGPA += 0
        if len(currentClasses) == 0:
            uwGPA = "N/A"
            wGPA = "N/A"
        else:
            uwGPA = round(uwGPA / len(currentClasses), 2)
            wGPA = round(wGPA / len(currentClasses), 2)

            col1.header("Unweighted GPA")
            col1.subheader(uwGPA)
            col1.header("Weighted GPA")
            col1.subheader(wGPA)
    
    def update_charts():
        # bar chart for type of class
        df = load_df()
        rigors = df["ClassRigor"]
        onLevelCount = 0
        honorsCount = 0
        APCount = 0
        DECount = 0
        for i in rigors:
            if i == "On-Level":
                onLevelCount += 1
            elif i == "Honors":
                honorsCount += 1
            elif i == "Advanced Placement":
                APCount += 1
            elif i == "Dual Enrollment":
                DECount += 1
        rigorCounts = [["On-Level", onLevelCount],
                       ["Honors", honorsCount],
                       ["Advanced Placement", APCount],
                       ["Dual Enrollment", DECount]]
        rigorCounts_df = pd.DataFrame(rigorCounts,
                                      columns=["Class Type",
                                               "# of Classes"])
        col2.bar_chart(data=rigorCounts_df,
                       x="Class Type",
                       y="# of Classes",
                       use_container_width=False,
                       width=500)

        col2.write("You've taken a total of " + f"**:blue[{len(enteredClasses)}]**"  + " classes")

    st.button('Update Results', on_click=update, args=(edf, ))

    col1, col2 = st.columns([1, 2])
    

    enteredClasses = [list(row) for row in classData_df.values]
    if len(enteredClasses) > 0:
        update_GPA(enteredClasses)
        update_charts()
