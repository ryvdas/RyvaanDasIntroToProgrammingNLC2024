import streamlit as st
import pandas as pd
import json
# classes = pd.DataFrame(
#     [
#         {"Class Name": "", "Grade Earned": 0, "Rigor Class": False},
#         {"Class Name": "", "Grade Earned": 0, "Rigor Class": False}
#     ]
# )

# editedClasses = st.data_editor(classes)
# highest_grade = editedClasses.loc[editedClasses["Grade Earned"].idxmax()]["Class Name"]
# st.markdown(f"You got the highest grade in **{highest_grade}**")

st.set_page_config(layout="wide")
st.title('GPA Genie')
st.divider()
cols = st.columns(2)
tab1, tab2, tab3 = st.tabs(["Enter a Class", "Your Classes", "Insights and Results"])

classData_df = pd.read_csv('classData.csv')

with tab1:
    rigor = st.radio(
        "Select the class's rigor level:",
        ["On-Level", "Honors", "Advanced Placement", "Dual Enrollment"],
        captions = ["Non-honors, AP, or college classes", 
                    "Advanced, accelerated or honors classes", 
                    "AP classes", 
                    "College classes"])
    
    with open('classes.json', 'r') as classes_file:
        classes = json.load(classes_file)[rigor]
    className = st.selectbox("Select the name of your class: ", (classes))
    st.write("You selected: ", className)
    
    grade = st.number_input(label="Enter the grade earned: ", min_value=0, max_value=100, value=None, step=1)
    st.write("The grade you entered is ", grade)

    st.write("Are you sure you want to add the ", rigor, " class, ", className, ", with a grade of ", grade, "?")
    classEnterButton = st.button("Confirm")
    if classEnterButton:
        #classData_df = classData_df.append({"Class Rigor": rigor, "Class Name": className, "Grade Earned": grade}, ignore_index=True)
        # newDF = pd.DataFrame({"Class Rigor": [rigor], "Class Name": [className], "Grade Earned": [grade]})
        # #classData_df = classData_df.append(newDF, ignore_index = True)
        # concatDF = pd.concat([classData_df, newDF], ignore_index=True)
        
        # #classData_df.loc[len(classData_df.index)] = [rigor, className, grade]
        # #classEnterButton = False
        # print(classData_df)
        # print(newDF)
        # print(concatDF)
        # classData_df = concatDF

        classData_df = classData_df.append({"Class Rigor":rigor,"Class Name":className,"Grade Earned":grade},ignore_index=True)
        classData_df.to_csv('classData.csv', index = False)

with tab2:
    # @st.cache_data
    # def convert_df(df):
    #     return df.to_csv().encode("utf-8")
    
    # classDataCSV = convert_df(classData_df)
    # st.download_button(label="Save as CSV", data=classDataCSV, file_name="export.csv", mime="text/csv")
    # def updateClassData():
    #     classData_df = pd.read_csv(newFile)
    #     classData_df.to_csv('classData.csv', index = False)

    # newFile = st.file_uploader(label="Load from CSV", type=['csv'], on_change=updateClassData)
    deleteButton = st.button("Delete a Class")
    if deleteButton:
        classDeleter = st.selectbox(label="Select the class to delete:", options=classData_df)
        if classDeleter:
            print(classDeleter)
            classData_df = classData_df.drop([str(classDeleter)], inplace=True)
            #classData = st.dataframe(data=classData_df, hide_index=True)
            classData_df.to_csv('classData.csv', index = False)

    classData = st.dataframe(data=classData_df, hide_index=True)