import streamlit as st
from openai import OpenAI
import os

client = OpenAI(
	api_key=os.environ["API_KEY"],
	base_url="https://api.ai.it.cornell.edu",
)

#Read knowledge base from data/important_knowledge.txt
with open("data/important_knowledge.txt", "r") as f:
	knowledge_base = f.read()

st.set_page_config(page_title="Hello INFO-5940", layout="centered")
st.title("👋 Hello from INFO-5940!")

if "messages" not in st.session_state:
	st.session_state ["messages"] = [{"role": "system", "content": "You are a helpful assistant"}] 
	st.session_state ["messages"] += [{"role": "user", "content": "I want you to answer questions based on the knowledge base" + knowledge_base}] 
	st.session_state ["messages"] += [{"role": "assistant", "content": "Howdy"}] 
	
for msg in st.session_state.messages: 
	if msg ["role"] != "system" and msg ["content"] != "I want you to answer questions based on the knowledge base" + knowledge_base:
		 st.chat_message(msg["role"]).write(msg["content"]) 
  
# prompt = st.chat_input()
# if prompt:

if prompt := st.chat_input():
	st.session_state.messages.append({"role": "user", "content": prompt})
	st.chat_message("user").write(prompt)
    
	#block of content
	with st.chat_message("assistant"):
		stream = client.chat.completions.create(
			model="openai.gpt-4o",
			messages=st.session_state.messages, 
			stream=True
		) 
		response = st.write_stream(stream)
		
	st.session_state.messages.append({"role": "assistant", "content": response})