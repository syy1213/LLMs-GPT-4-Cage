import re
import glob,os
import numpy as np
import pandas as pd
#download bertscore
import evaluate
bertscore = evaluate.load("./bertscore")

#check if GPT's output meet the format's requirement by computing the length of splitted output by '|' which is supposed to be 9
def check_output(all_answers):
    for i in range(len(all_answers)):
        standard = all_answers['Manual_answer'][i]
        GPT = all_answers['GPT_answer'][i]
        filename = all_answers['filename'][i]
        if GPT == GPT:
            standard_split = standard.split('\n')
            GPT_split = GPT.split('\n')
            for each_paragraph in standard_split:
                each_paragraph = each_paragraph.split('|')
                each_paragraph = list(filter(None, each_paragraph))
                length = len(each_paragraph)
                if length!=9:
                    print(filename,i,each_paragraph,length)
            for each_paragraph in GPT_split:
                each_paragraph_s = each_paragraph.split('|')
                each_paragraph_s = list(filter(None, each_paragraph_s))
                length = len(each_paragraph_s)
                if length!=9:
                    #print(filename,i,each_paragraph)
                    print(filename,length,each_paragraph_s[0])

def extract_number_plus_number(text):
    # Regular expression pattern to match text in the form of [number+number]
    pattern = r'\[\d+\+\d+\]'
    new_text = ''.join(text.split())
    matches = re.findall(pattern, new_text)
    if matches == []:
        matches = ['None']
    return matches

def process_topology(text):
    text_split = text.split('\n')
    for each_paragraph in text_split:
        each_paragraph = each_paragraph.split('|')
        each_paragraph = list(filter(None, each_paragraph))
        length = len(each_paragraph)
        if length == 9:
            long_topology = each_paragraph[1]
            topology = extract_number_plus_number(long_topology)
            topology = ' '.join(topology)
            if topology == '':
                topology = 'None'
        text = text.replace(long_topology,topology)
    return text
    
# compute overall similarities
def compute_overall_sim(all_answers):
    for i in range(len(all_answers)):
        index = all_answers['Index'][i]
        standard = all_answers['Manual_answer'][i]
        GPT = all_answers['GPT_answer'][i]
        if standard == '2022-zhou-et-al-inherently-chiral-cages-via-hierarchical-desymmetrization.txt':
            with open(standard,'r') as f:
                read_from_txt = f.read()
            standard = read_from_txt
            print('read from file')
        else:
            pass
        if standard == standard:
            GPT = process_topology(GPT)
            predictions = [GPT]
            references = [standard]
            results = bertscore.compute(predictions=predictions, references=references, lang="en", model_type = "distilbert-base-uncased")
            recall = results['recall']
            all_answers.loc[i, "overall_recall"] = recall[0]
            print(recall[0],index)
    return all_answers

def get_monomers(text):
    text_split = text.split('\n')
    matrix = []
    for each_paragraph in text_split:
        each_paragraph = each_paragraph.split('|')
        each_paragraph = list(filter(None, each_paragraph))
        length = len(each_paragraph)
        if length == 9:
            monomer1 = each_paragraph[-4]
            monomer2 = each_paragraph[-2]
            synthesis1 = each_paragraph[-3]
            synthesis2 = each_paragraph[-1]
            
            matrix.append([monomer1+';'+monomer2,synthesis1+';'+synthesis2])
        else:
            print('error',length,each_paragraph)
    matrix = list(map(list, zip(*matrix)))
    return matrix

def get_others(text):
    text_split = text.split('\n')
    matrix = []
    for each_paragraph in text_split:
        each_paragraph = each_paragraph.split('|')
        each_paragraph = list(filter(None, each_paragraph))
        length = len(each_paragraph)
        if length == 9:
            each_paragraph_ = [each_paragraph[i] for i in [0,2,3,4]]
            topology = extract_number_plus_number(each_paragraph[1])
            topology = ' '.join(topology)
            if topology == '':
                topology = 'None'
            each_paragraph_.append(topology)
            matrix.append(each_paragraph_)
        else:
            print('error',length,each_paragraph)
    matrix = list(map(list, zip(*matrix)))
    return matrix

# compute similarities of monomers and their synthesis route
def compute_monomer_sim(all_answers):
    for i in range(len(all_answers)):
        standard = all_answers['Manual_answer'][i]
        GPT = all_answers['GPT_answer'][i]
        # the content in "2022-zhou-et-al ..." cannot be saved in excel files due to the limitation of characters, so read from txt files specially
        if standard == '2022-zhou-et-al-inherently-chiral-cages-via-hierarchical-desymmetrization.txt':
            with open(standard,'r') as f:
                read_from_txt = f.read()
            standard = read_from_txt
        else:
            pass
        standard_matrix = get_monomers(standard)
        GPT_matrix = get_monomers(GPT)
        standard_matrix = ['|'.join(each_part) for each_part in standard_matrix]
        GPT_matrix = ['|'.join(each_part) for each_part in GPT_matrix]
        results = bertscore.compute(predictions=GPT_matrix, references=standard_matrix, lang="en", model_type = "distilbert-base-uncased")
        recall = str(results['recall'])
        all_answers.loc[i, "recall_monomer"] = recall
        name1,name2 = standard_matrix[0],GPT_matrix[0]
        print(i,recall,name1,name2)
    return all_answers

#compute similarities of other sections
def compute_others_sim(all_answers):
    for i in range(len(all_answers)):
        standard = all_answers['Manual_answer'][i]
        GPT = all_answers['GPT_answer'][i]
        # the content in "2022-zhou-et-al ..." cannot be saved in excel files due to the limitation of characters, so read from txt files specially
        if standard == '2022-zhou-et-al-inherently-chiral-cages-via-hierarchical-desymmetrization.txt':
            with open(standard,'r') as f:
                read_from_txt = f.read()
            standard = read_from_txt
        else:
            pass
        standard_matrix = get_others(standard)
        GPT_matrix = get_others(GPT)
        standard_matrix = ['|'.join(each_part) for each_part in standard_matrix]
        GPT_matrix = ['|'.join(each_part) for each_part in GPT_matrix]
        results = bertscore.compute(predictions=GPT_matrix, references=standard_matrix, lang="en", model_type = "distilbert-base-uncased")
        others_recall = str(results['recall'])
        all_answers.loc[i, "recall_others"] = others_recall
        print(standard_matrix[1],GPT_matrix[1],others_recall)
    return all_answers

# Replace the file path with your own
all_answers = pd.read_excel("Tabular Informations without bertscore.xlsx")
check_output(all_answers)
all_answers = compute_overall_sim(all_answers)
all_answers = compute_monomer_sim(all_answers)
all_answers = compute_others_sim(all_answers)
print(all_answers)
all_answers.to_excel('test.xlsx')