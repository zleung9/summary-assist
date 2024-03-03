import random
import gradio as gr
from gradio.blocks import Blocks
from gradio.components import (
    Markdown,
    Chatbot,
    Textbox,
    Button,
    Dropdown,
)
from gradio.layouts import Accordion, Group, Row


class Chat(Blocks):
    def __init__(self, fn, title="Chat"):
        """
        Parameters
        ----------
        fn : Callable
            The function to wrap the chat interface around. Should accept two parameters: a string input message and list of two-element lists of the form [[user_message, bot_message], ...] representing the chat history, and return a string response. See the Chatbot documentation for more information on the chat history format.
        title : str
            The tab title to display when this is opened in a browser window.
        
        """
        super().__init__(title)
        self.fn = fn
        self.title = title
        with self:
            Markdown(f"<h1 style='text-align: center; margin-bottom: 1rem'>{self.title}</h1>")
            self.user_checkbox = Dropdown(
                label="User", 
                choices=["Leon", "Inna", "Emilio", "Scott", "DP", "Zhu", "Esteban", "Syahmi"])
            
            self.chatbot = Chatbot(label="Chatbot", scale=1, height=200)
            with Row():
                self.textbox = Textbox(
                    container=False,
                    show_label=False,
                    label="Message",
                    placeholder="Type a message...",
                    scale=7,
                    autofocus=True,
                )
                self.submit_btn = Button("Submit", variant="primary", scale=1, min_width=150)
            with Row():
                self.save_bn = gr.Button("Save", variant="secondary", size="sm")
                self.clear_bn = gr.Button("Clear", variant="secondary", size="sm")
            

def random_response(message, history):
    return random.choice(["Yes", "No"])


if __name__ == "__main__":
    demo = Chat(random_response, "Chat with Me")
    demo.launch()