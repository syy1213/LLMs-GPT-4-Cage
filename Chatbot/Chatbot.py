import tkinter as tk
from tkinter import simpledialog
from time import sleep
from tkinter import ttk
import threading
from PIL import Image, ImageTk
from openai import OpenAI
api_key = "***"
organization = '***'
client = OpenAI(api_key=api_key,organization=organization,base_url='https://api.openai.com/v1/')
file = client.files.create(
  file=open("original-database.json", "rb"),
  purpose='assistants'
)
VectorStore = client.beta.vector_stores.create(file_ids=[file.id],name='cage-database')
assistant = client.beta.assistants.create(
  instructions="""A table summarizing many organic molecular cages is given to you. \
  From left to right are the title of the article, the author, the organization, \
  the name of the molecular cage, the topology, the CCDC number, the specific surface area, \
  the synthesis conditions, the name of the monomer, and the conditions under which the monomer was synthesized. \
  Please answer the user's questions based on the table.""",
  model="gpt-4o",
  tools=[{"type": 'file_search'}],tool_resources={"file_search": {"vector_store_ids": [VectorStore.id]}})

def write_log(txt):
    with open('./chatbot_log.txt','a',encoding='gb18030') as f:
        f.write(txt)

# Getting the GPT response
def get_gpt_response(prompt):
    try:
        message = client.beta.threads.messages.create(thread_id=thread.id, role='user',content=prompt)
        run = client.beta.threads.runs.create(
                thread_id=thread.id,
                assistant_id=assistant.id
                )
        run_retrive = client.beta.threads.runs.retrieve(
                thread_id=thread.id,
                run_id=run.id)
        while(run_retrive.status == 'in_progress'):
            sleep(10)
            run_retrive = client.beta.threads.runs.retrieve(thread_id=thread.id,run_id=run.id)
        messages = client.beta.threads.messages.list(thread_id=thread.id)
        output_message = messages.data[0].content[0].text.value
        write_log(prompt+'/n'+output_message)
        return output_message
    except Exception as e:
        return str(e)

# Handling message sending and GPT responses
def handle_message():
    message = entry.get()
    if message:
        display_message("User", message, 'right', 'yellow')
        entry.delete(0, tk.END)
        
        # Show loading tips
        display_message("GPT", "Please wait...", 'left', 'light pink')
        threading.Thread(target=update_with_gpt_response, args=(message,)).start()

def update_with_gpt_response(message):
    response = get_gpt_response(message)
    # Delete the previous ‘Please wait...’ Tip.
    chat_box_frame.winfo_children()[-1].destroy()
    display_message("GPT", response, 'left', 'light pink')

def display_message(sender, message, side, bg_color):
    message_frame = tk.Frame(chat_box_frame, bg=bg_color, padx=10, pady=5, bd=1, relief='solid')
    message_label = tk.Label(message_frame, text=f"{sender}: {message}", bg=bg_color, font=("Times New Roman", 10), wraplength=500, justify='left')
    message_label.pack()
    if side == 'left':
        message_frame.pack(anchor='w', pady=10, padx=10)
    else:
        message_frame.pack(anchor='e', pady=10, padx=10)
    chat_box_canvas.yview_moveto(1)

thread = client.beta.threads.create()
root = tk.Tk()
root.title("GPT-4o Chat dialogue box")
root.geometry("400x600")

# Create display area for chat log 
chat_box_canvas = tk.Canvas(root, bg='light green')
chat_box_frame = tk.Frame(chat_box_canvas, bg='light green')
chat_box_scrollbar = ttk.Scrollbar(root, orient='vertical', command=chat_box_canvas.yview)
chat_box_canvas.configure(yscrollcommand=chat_box_scrollbar.set)

chat_box_scrollbar.pack(side='right', fill='y')
chat_box_canvas.pack(side='left', fill='both', expand=True)
chat_box_canvas.create_window((0, 0), window=chat_box_frame, anchor='nw')

def on_frame_configure(event):
    chat_box_canvas.configure(scrollregion=chat_box_canvas.bbox("all"))

chat_box_frame.bind("<Configure>", on_frame_configure)

# Creating Input Boxes and Send Buttons
entry_frame = tk.Frame(root, bg='lightgray', bd=2)
entry = tk.Entry(entry_frame, width=30, font=("Times New Roman", 12))
entry.pack(side='left', padx=5, pady=5)

send_button = tk.Button(entry_frame, text="send", command=handle_message, font=("Times New Roman", 12, 'bold'), bg='#4CAF50', fg='white')
send_button.pack(side='left', padx=5, pady=5)

entry_frame.pack(side='bottom', fill='x')

root.mainloop()
