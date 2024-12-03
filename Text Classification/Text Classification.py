import PyPDF2
import ast
import tiktoken
import requests
import re
import os,glob
import time
from random import sample
import numpy as np
import pandas as pd
from openai import OpenAI
# Please replace the asterisk ‘***’ with your own api key and organization code
api_key = "*** ***"
organization = '*** ***'
client = OpenAI(api_key=api_key,organization=organization)

def count_tokens(text):
    encoding = tiktoken.get_encoding("cl100k_base")
    num_tokens = len(encoding.encode(text))
    return num_tokens

def get_txt_from_pdf(pdf_files,filter_ref = False, combine=False):
    data = []
    pdf_content_dict = {}
    for pdf in pdf_files:
        all_pdf_txt = ''
        print(pdf)
        with open(pdf, 'rb') as pdf_content:
            pdf_reader = PyPDF2.PdfReader(pdf_content)
            for page_num in range(len(pdf_reader.pages)):
                page = pdf_reader.pages[page_num]
                page_text = page.extract_text()
                all_pdf_txt += page_text
            all_pdf_txt = re.split('\n',all_pdf_txt)
            all_pdf_txt = [txt1 for txt in all_pdf_txt for txt1 in re.split('\n \n',txt)]
            for i, para_part in enumerate(all_pdf_txt):
                data.append({
                    'file name': pdf,
                    'paragraph number': i+1,
                    'content': para_part
                })
    df = pd.DataFrame(data)
    return df

def combine_text(df):
    start_index = 0
    all_groups = []
    data = []
    for i in range(len(df)):
        pdf = df['file name'][i]
        content_split = df['content'][i].split()
        if content_split != []:
            content_end = content_split[-1][-1]
            if content_end == '.' or content_end == '*':
                all_groups.append(range(start_index,i+1))
                new_content = ''
                for j in range(start_index,i+1):
                    new_content += df['content'][j]
                data.append({
                            'file name': pdf,
                            'content': new_content
                            })
                start_index = i+1
    new_df = pd.DataFrame(data)
    return new_df

def organize_text_to_input(new_df):
    index = 1
    part_num = 1
    txt = ''
    inputs = {}
    for i in range(len(new_df)):
        content = new_df.loc[i,'content']
        filename1 = new_df.loc[i,'file name']
        if i>0:
            filename2 = new_df.loc[i-1,'file name']
            if  filename1!=filename2  or i == len(new_df)-1:
                index = 1
                inputs[filename2+'part'+str(part_num)] = txt
                txt = ''
                part_num = 1
            if  token_num > 3300-count_tokens(content) or index >= 20:
                index = 1
                inputs[filename1+'part'+str(part_num)] = txt
                part_num += 1
                txt = ''
        txt += str(index)+'、'+content+'\n \n'
        token_num = count_tokens(txt)
        new_df.loc[i,'index'] = index
        new_df.loc[i,'new_content'] = str(index)+'、'+content
        new_df.loc[i,'part'] = filename1+'part'+str(part_num)
        index += 1
    return inputs

def run_GPT(inputs):
    all_inputs_list = list(inputs.keys())
    outputs = {}
    with open('./classification.txt','r',encoding='utf-8') as f:
        prompt = f.read()
    assistant = """You are a classifier and you have learned the examples given in the system, \
    now you are given a text containing many numbered paragraphs separated by a blank line, \
    please output the category of each paragraph.Each category must be unambiguous, separated by a semicolon. \
    If there is more than one category in a paragraph, output the main category.\
    Write only the category in your answer, not the original text."""
    
    for index, key in enumerate(all_inputs_list):
        text = inputs[key]
        try:
            response = client.chat.completions.create(
                               model='gpt-4',
                                messages=[      {"role": "assistant", "content": assistant},
                                                {"role": "system", "content": prompt},
                                                {"role": "user", "content": text}
                                            ]
                            )
            answers = response.choices[0].message.content
            with open('gpt-4-new.log','a+',encoding='gb18030') as f:
                contents = 'text:\n'+text+'answers:\n'+answers
                f.write(key+':\n\n'+'INPUTS:\n'+contents+'\n\n')
            outputs[key] = answers
            print(index+1,key)
        except Exception as e:
            print(f"Error: {str(e)}")
    return outputs

def organize_answer(inputs,outputs):
    data = []
    for index, key in enumerate(inputs.keys()):
        if key in outputs.keys():
            text = inputs[key].split('\n \n')
            text = [text_ for text_ in text if text_ != '']
            answers = outputs[key]
            answers_split1 = answers.split('\n')
            answers_split2 = answers.split(';')
            distance1 = abs(len(answers_split1)-len(text))
            distance2 = abs(len(answers_split2)-len(text))
            if distance1 < distance2:
                answers = answers_split1
            else:
                answers = answers_split2
            answers = [answer for answer in answers if answer != '']
            if len(text) > len(answers):
                for i in range(len(text)):
                    para = text[i]
                    if i<len(answers):
                        answer = answers[i]
                        data.append({
                                'file name': key,
                                'content': para,
                                'categories': answer
                                })
                    else:
                        data.append({
                                'file name': key,
                                'content': para,
                                'categories': 'no answer'
                                })
            else:
                for i in range(len(answers)):
                    answer = answers[i]
                    if i<len(text):
                        para = text[i]
                        data.append({
                                    'file name': key,
                                    'content': para,
                                    'categories': answer
                                    })
                    else:
                        data.append({
                                    'file name': key,
                                    'content': 'extra answer',
                                    'categories': answer
                                    })
    class_df = pd.DataFrame(data)
    return class_df

def main(pdf_list):
    df = get_txt_from_pdf(pdf_list)
    new_df = combine_text(df)
    inputs = organize_text_to_input(new_df)
    outputs = run_GPT(inputs)
    class_df = organize_answer(inputs,outputs)
    return class_df

# replace the variables of the main() function with a list of your pdf files
class_df = main(["./papers/science-aax7427.pdf"])
class_df.to_excel('test.xlsx')
