import os
import streamlit as st
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain
from langchain_groq import ChatGroq
from langchain_community.document_loaders import PyPDFLoader

# Set your Groq API Key
os.environ["GROQ_API_KEY"] = "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"  # Replace with actual key

st.title("Career Analysis from Resume")
st.markdown("Upload your **resume** or describe your **skills & goals**, and get smart career suggestions!")

# --- Resume Upload ---
resume_text = ""
uploaded_file = st.file_uploader("Upload your resume", type=["pdf"])

if uploaded_file is not None:
    with open("Temporary_resume.pdf", "wb") as f:
        f.write(uploaded_file.read())

    loader = PyPDFLoader("Temporary_resume.pdf")
    pages = loader.load()
    resume_text = "\n\n".join([page.page_content for page in pages])

    st.success(" Resume uploaded and parsed!")
    st.text_area(" Extracted Resume Text:", resume_text, height=200)


st.markdown("**Type your info manually**")
manual_input = st.text_area("Describe your background, skills, and goals")


with st.expander("Advanced Settings"):
    temperature = st.slider("Temperature", 0.0, 1.5, 0.7)
    top_p = st.slider("Top-p (nucleus sampling)", 0.0, 1.0, 0.9)
    top_k = st.slider("Top-k sampling", 0, 100, 50)


final_input = resume_text if resume_text.strip() != "" else manual_input.strip()


llm = ChatGroq(
    groq_api_key=os.environ["GROQ_API_KEY"],
    model="llama-3.1-8b-instant",
    temperature=0.7,
    top_p=1


)


prompt = PromptTemplate(
    input_variables=["user_input"],
    template="""
You are an expert career coach. Based on the user's resume or self-description, suggest 2–3 well-suited career paths.

Provide:
1. Career Title
2. Why it's a good fit
3. Skills needed (and if the user already has them)


User Description:
{user_input}

Career Suggestions:
"""
)

# --- Chain ---
chain = LLMChain(llm=llm, prompt=prompt)

# --- Generate Output ---
if final_input:
    with st.spinner("🔍 Analyzing your profile..."):
        result = chain.run(final_input)
        st.subheader("📌 Career Suggestions:")
        st.write(result)
else:
    st.info("📝 Please upload a resume or enter your skills manually.")



