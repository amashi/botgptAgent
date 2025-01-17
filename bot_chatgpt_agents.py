 #!/usr/bin/env python3

import gradio as gr
import os
from os.path import join, dirname
from dotenv import load_dotenv
from sklearn import externals
import conversational_agent

# from conversational import conversatioalChatGPT

# from conversation import create_conversation
# dotenv_path = join(dirname(__file__), '.env')
# print(load_dotenv(dotenv_path))
load_dotenv()
print ("OPENAI_API_KEY",os.environ.get("OPENAI_API_KEY"))

# CONDENSE_TEMPLATE = """Given the following chat history and a follow up question, rephrase the follow up input question to be a standalone question.Or end the conversation if it seems like it's done.Chat History:\"""{chat_history} \"""Follow Up Input: \"""{question}\"""Standalone question:"""
# QA_TEMPLATE = """You are a friendly, conversational banking assistant. Talk about your  data  and answer any questions.It's ok if you don't know the answer.Context:\"""{context}\"""Question:\"{question}\"""Helpful Answer :"""
      

# OPENAI_API_KEY = "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"
# HUGGINGFACEHUB_API_TOKEN = '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'
# server_name="0.0.0.0"
#getpass('Enter your OpenAI key: ')
# os.environ["OPENAI_API_KEY"] = OPENAI_API_KEY
# os.environ["HUGGINGFACEHUB_API_TOKEN"] = HUGGINGFACEHUB_API_TOKEN
# os.environ["GRADIO_SERVER_NAME"] = server_name
# os.environ["GRADIO_SERVER_PORT"] = "8888"

qa = conversational_agent.conversatioalAgentsChatGPT().getConversational()

# def create_conversational():
#     # externals (qa)
#     qa = conversational_agent.conversatioalAgentsChatGPT().getConversational()

def create_conversational():
    # externals (qa)
    qanew = conversational_agent.conversatioalAgentsChatGPT().getConversational()
    qa=None
    qa=qanew



create_conversational()


def add_text(history, text):
    history = history + [(text, None)]
    return history, ""


def bot(history):
    question=history[-1][0]
    chat_history=history[:-1]
    res=qa.run(input=question)
    print("res",res)
    history[-1][1] = res
    return history

css = """
.qhebrew textarea { direction: rtl;}
"""

with gr.Blocks(css=".gradio-container {background-color: white }", rtl=True) as demo:
    
    with gr.Row():
        with gr.Column(scale=0.90):
            txt = gr.Textbox(show_label=False,placeholder="כתוב שאלה", container=False)
        with gr.Column(scale=0.05):
            submit_btn = gr.Button('שאל',variant='primary')
        with gr.Column(scale=0.05):
            clear_btn = gr.Button('נקה',variant='stop')

    chatbot = gr.Chatbot([], elem_id="chatbot", label='מומחה משכנתאות', elem_classes='qhebrew', height=500)

    txt.submit(add_text, [chatbot, txt], [chatbot, txt]).then(
        bot, chatbot, chatbot
    )

    submit_btn.click(add_text, [chatbot, txt], [chatbot, txt]).then(
        bot, chatbot, chatbot
    )
   
    clear_btn.click(lambda: None, None, chatbot, queue=False).then(
        create_conversational
    )

if __name__ == '__main__':    
    demo.queue(concurrency_count=3)
    demo.launch(share=True,server_name=os.environ.get("GRADIO_SERVER_NAME"),server_port=int(os.getenv("GRADIO_SERVER_PORT",8888)))
