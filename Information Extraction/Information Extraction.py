from time import sleep
import glob,os
import pandas as pd
import numpy as np
np.float = float
np.int = int
np.object = object
np.bool = bool
from openai import OpenAI
# Please replace the asterisk ‘***’ with your own api key and organization code
api_key = "*** ***"
organization = '*** ***'
client = OpenAI(api_key=api_key,organization=organization)
assistant = client.beta.assistants.create(
  name="cage table organizer",
  instructions='Follow the instructions, extract the information related to organic molecular cages from the given text and organize them into a table',
  model="gpt-4o"
)

with open('./single-cage instructions.txt','r',encoding='gb18030') as f:
    level_1_description = f.read()

with open('./multi-cage instructions.txt','r',encoding='gb18030') as f:
    level_2_3_description = f.read()

def GPT_extract_information(input_csv,level='level1'):
    if level == 'level1':
        prompt = level_1_description
    elif level == 'level2' or level == 'level3':
        prompt = level_2_3_description
    else:
        print('unknown level')
    thread = client.beta.threads.create()
    with open(input_csv,'r',encoding='gb18030',errors='ignore') as f:
        f_content = f.read()
    try:
        message = client.beta.threads.messages.create(thread_id=thread.id, role='user',content=prompt+f_content)
        run = client.beta.threads.runs.create(
        thread_id=thread.id,
        assistant_id=assistant.id
        )
        sleep(10)
        print(run.id)
        run_retrive = client.beta.threads.runs.retrieve(
        thread_id=thread.id,
        run_id=run.id)
        print(run_retrive.status)
        while(run_retrive.status == 'in_progress'):
            sleep(10)
            run_retrive = client.beta.threads.runs.retrieve(thread_id=thread.id,run_id=run.id)
        print(run_retrive.status)
        messages = client.beta.threads.messages.list(thread_id=thread.id)
        output_message = messages.data[0].content[0].text.value
        with open('gpt-4o-table.log','a+',encoding='gb18030') as f:
            f.write(input_csv+'INPUT:\n\n'+f_content+'OUTPUT:\n\n'+output_message+'\n\n')
        i = output_message.find("|")
        j = output_message.rfind("|")
        gpt_answer = output_message[i:j+1].replace('--','').replace('|-|','')
        print(input_csv,'finished')
    except Exception as e:
        print(str(e))
        print(key)
    return gpt_answer

# Replace the folder path with your own
csv_folder = glob.glob('./level1/*.csv')
csv_folder = csv_folder[:5]
data = []
for csv_file in csv_folder:
    gpt_answer = GPT_extract_information(csv_file,level='level1')
    data.append({'csv_file':csv_file,'gpt_answer':gpt_answer})
df = pd.DataFrame(data)
df.to_excel('test.xlsx')