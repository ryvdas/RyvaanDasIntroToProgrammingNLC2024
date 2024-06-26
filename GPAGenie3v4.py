# import necessary libraries
import streamlit as st
import pandas as pd
import json
from llama_index.core import VectorStoreIndex, ServiceContext, Document
from llama_index.llms.openai import OpenAI
import openai
from llama_index.core import SimpleDirectoryReader

# page setup
st.set_page_config(layout="wide")
st.image(image='1.png', width=300)
st.subheader('The Magical GPA Calculator!')
st.divider()
cols = st.columns(2)
tab1, tab2, tab3, tab4 = st.tabs(["Enter a Class", "Your Classes", "Insights and Results", "Chatbot"])

# access class data
classData_df = pd.read_csv('data/classData.csv')

# create help menu sidebar and buttons
with st.sidebar:
    st.title("Help Menu")
    st.write("Click the arrow to collapse")
    with st.popover("Adding Classes", use_container_width=True):
        st.write("1. Go to the 'Enter a Class' tab.")
        st.write("2. From there, enter the rigor of the class using the multiple choice buttons")
        st.write("3. Once you have selected the class type, find the class name in the dropdown below")
        st.write("4. Enter the grade you got in the text box, it must be a number from 0 to 100")
        st.write("5. Make sure the information in the bottom statement is correct, then press the 'Confirm' button")
        st.write("6. Check the 'Your Classes' tab and scroll to the bottom to see your new class added!")
    
    with st.popover("Viewing Your Classes", use_container_width=True):
        st.write("1. Go to the 'Your Classes tab'")
        st.write("2. You can see a table with all of your classes displayed")
    
    with st.popover("Deleting/Editing Classes", use_container_width=True):
        st.write("1. Go to the 'Your Classes' tab")
        st.write("2. Click the checkbox to the left of the clas you want to delete")
        st.write("3. Click on the trashcan button in the top right of the table")
        st.write("4. To edit a class, double click a box to change the grade")
        st.write("5. To finalize your changes, click the 'Save' button")

    with st.popover("Viewing your GPA", use_container_width=True):
        st.write("1. Go to the 'Insights and Results' tab")
        st.write("2. Your weighted and unweighted GPA's are listed")
        st.write("3. You can also see the number of classes you've taken and the number of classes in each type")
    
    with st.popover("Using the Chatbot", use_container_width=True):
        st.write("1. Go to the 'Chatbot' tab")
        st.write("2. Type a message in the text box and click the send button")
        st.write("3. The chatbot will respond and you can type a follow up question")

# create 
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
    
    grade = st.number_input(label="Enter the Grade Earned: ", min_value=0, max_value=100, value=0, step=1)
    st.write("You entered: ", f"**:blue[{grade}]**")
    
    st.write("Are you sure you want to add the ", f"**:blue[{rigor}]**", " class, ", f"**:blue[{className}]**", " with a grade of ", f"**:blue[{grade}]**", "?")
    
    classEnterButton = st.button("Confirm")
    if classEnterButton:
        
        classData_df.loc[len(classData_df.index)] = [rigor, className, grade]
    
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

openai.api_key = st.secrets.openai_key
with tab4:
    st.header("Chat with the GPA Genie for personal insights!")
    if "messages" not in st.session_state.keys(): # Initialize the chat message history
        st.session_state.messages = [
            {"role": "assistant", "content": "Ask me a question about your GPA!"}
        ]
    
    @st.cache_resource(show_spinner=False)
    def load_LLM_data():
        with st.spinner(text="Loading and processing your GPA info – hang tight! This should take 1-2 minutes."):
            reader = SimpleDirectoryReader(input_dir="./data", recursive=True)
            docs = reader.load_data()
            service_context = ServiceContext.from_defaults(llm=OpenAI(model="gpt-3.5-turbo", temperature=0.5, system_prompt="You are an expert on student GPA and your job is to answer questions a student has. Assume that all questions are related to their GPA. Keep your answers technical and based on facts – do not hallucinate features."))
            index = VectorStoreIndex.from_documents(docs, service_context=service_context)
            return index

    index = load_LLM_data()

    chat_engine = index.as_chat_engine(chat_mode="condense_question", verbose=True)

    if prompt := st.chat_input("Your question"): # Prompt for user input and save to chat history
        st.session_state.messages.append({"role": "user", "content": prompt})

    for message in st.session_state.messages: # Display the prior chat messages
        with st.chat_message(message["role"]):
            st.write(message["content"])
    
    # If last message is not from assistant, generate a new response
    if st.session_state.messages[-1]["role"] != "assistant":
        with st.chat_message("assistant"):
            with st.spinner("Thinking..."):
                response = chat_engine.chat(prompt)
                st.write(response.response)
                message = {"role": "assistant", "content": response.response}
                st.session_state.messages.append(message) # Add response to message history