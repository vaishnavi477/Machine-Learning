import os, openai
import datetime
from dotenv import load_dotenv, find_dotenv
from langchain.chains import RetrievalQA, ConversationalRetrievalChain # type: ignore
from langchain_openai import OpenAIEmbeddings # type: ignore
from langchain_chroma import Chroma # type: ignore
from langchain.prompts import PromptTemplate # type: ignore
from langchain_openai import ChatOpenAI # type: ignore
from langchain.text_splitter import RecursiveCharacterTextSplitter # type: ignore
from langchain_community.document_loaders import PyPDFLoader # type: ignore
from langchain.memory import ConversationBufferMemory # type: ignore
import panel as pn # type: ignore
import param # type: ignore

# Step 1: Overview of the workflow for RAG
# Load a document, create a vector database, perform similarity search, 
# create an LLM, set up a RetrievalQA Chain, and finally build a conversational chain with memory.

# Initialize the Panel extension for web-based interface
pn.extension()

# Load the OpenAI API key and select the LLM model based on the current date
load_dotenv(find_dotenv())
openai.api_key = os.getenv('OPENAI_API_KEY')

current_date = datetime.datetime.now().date()
llm_name = "gpt-3.5-turbo-0301" if current_date < datetime.date(2023, 9, 2) else "gpt-3.5-turbo"
print(f"\nUsing LLM Model: {llm_name}")

# Step 2: Load document and create VectorDB (i.e., Vectorstore)
persist_directory = 'docs/chroma/'
embedding = OpenAIEmbeddings()
vectordb = Chroma(persist_directory=persist_directory, embedding_function=embedding)

# Step 3: Similarity Search to select relevant chunks (splits)
question = "What are major topics?"
docs = vectordb.similarity_search(question)
print("\nNumber of documents: ",len(docs))

# Step 4: Create LLM
# Initialize the LLM and vectorstore to handle the similarity search and storage of embeddings
llm = ChatOpenAI(model=llm_name, temperature=0)


# Step 5: RetrievalQA Chain - optional
# Step 5.1: Create a prompt template for the QA chain
template = """Use the following context to answer the question at the end.
If you don't know the answer, say you don't know. Use three sentences maximum.
Always end with "thanks for asking!".
{context}
Question: {question}
Helpful Answer:"""
QA_CHAIN_PROMPT = PromptTemplate(input_variables=["context", "question"], template=template)

# Step 6: ConversationalRetrievalChain
# Step 6.1: Create Memory - use memory to track conversation history for context continuity
memory = ConversationBufferMemory(memory_key="chat_history", return_messages=True)
retriever = vectordb.as_retriever()
# Step 6.2: QA with ConversationalRetrievalChain - setting up conversational retrieval with memory
qa_chain = ConversationalRetrievalChain.from_llm(
    llm,
    retriever=retriever,
    memory=memory
)

# Step 7: Create a chatbot that works on your documents
# Function to load documents and create vector database with relevant parameters
def load_db(file, chain_type="stuff", k=4):
    loader = PyPDFLoader(file)
    documents = loader.load()
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=150)
    docs = text_splitter.split_documents(documents)
    db = Chroma.from_documents(docs, embedding)
    retriever = db.as_retriever(search_type="similarity", search_kwargs={"k": k})
    return ConversationalRetrievalChain.from_llm(
        llm=llm,
        retriever=retriever,
        return_source_documents=True,
        return_generated_question=True
    )

# Step 7.1: Create Business Logic
# Define a class for the chatbot, handling loading, conversation, and history management
class CustomerSupportChatbot(param.Parameterized):
    chat_history = param.List([])
    answer = param.String("")
    db_query = param.String("")
    db_response = param.List([])

    def __init__(self, **params):
        super().__init__(**params)
        self.panels = []
        self.loaded_file = "docs/cs229_lectures/sfbu-2024-2025-university-catalog-8-20-2024.pdf"
        self.qa = load_db(self.loaded_file)

    def call_load_db(self, count):
        # Load PDF and set up vectorstore for new file if provided
        if count == 0 or file_input.value is None:  
            return pn.pane.Markdown(f"Loaded File: {self.loaded_file}")
        else:
            file_input.save("temp.pdf")
            self.loaded_file = file_input.filename
            self.qa = load_db("temp.pdf")
        self.clr_history()
        return pn.pane.Markdown(f"Loaded File: {self.loaded_file}")

    def clr_history(self):
        # Clear the chat history for new interactions
        self.chat_history.clear()
        self.panels.clear()

    def convchain(self, query):
        # Process user input, perform conversational QA and update response panel
        if not query:
            return pn.WidgetBox(pn.Row('User:', pn.pane.Markdown("")), scroll=True)
        result = self.qa.invoke({"question": query, "chat_history": self.chat_history})
        self.chat_history.extend([(query, result["answer"])])
        self.db_query = result["generated_question"]
        self.db_response = result["source_documents"]
        self.answer = result['answer'] 
        self.panels.extend([
            pn.Row('User:', pn.pane.Markdown(query)),
            pn.Row('ChatBot:', pn.pane.Markdown(self.answer))
        ])
        inp.value = ''  # Clears input field
        return pn.WidgetBox(*self.panels, scroll=True)

    def display_db_query(self):
        # Display the generated database query based on user input
        return pn.pane.Markdown(f"DB query: {self.db_query}")

    def display_db_response(self):
        # Display the response documents retrieved from the database
        rlist = [pn.Row(pn.pane.Markdown("Result of DB lookup:"))]
        for doc in self.db_response:
            rlist.append(pn.Row(pn.pane.Markdown(str(doc))))
        return pn.WidgetBox(*rlist, scroll=True)

# Step 7.2: Create a web-based user interface
# Define the UI components and interaction handlers for the web-based chatbot
cbfs_instance = CustomerSupportChatbot()
inp = pn.widgets.TextInput(name="Your Query")
button = pn.widgets.Button(name="Submit Query", button_type="primary")
button.on_click(lambda event: cbfs_instance.convchain(inp.value))  # Passes inp.value to convchain
file_input = pn.widgets.FileInput(accept=".pdf")
button_load = pn.widgets.Button(name="Load PDF", button_type="primary")
button_load.on_click(lambda event: cbfs_instance.call_load_db(count=1))

# Layout to display the web-based chatbot UI
dashboard = pn.Column(
    pn.pane.Markdown("## Customer Support Chatbot"),
    pn.Row(file_input, button_load),
    pn.Row(inp, button),
    cbfs_instance.display_db_query,
    cbfs_instance.display_db_response
)

# Launch the web interface for the chatbot
dashboard.show()