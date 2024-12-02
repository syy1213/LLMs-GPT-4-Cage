# LLMs-GPT-4-Cage
Knowledge Discovery from Porous Organic Cages Literature Using a Large Language Model 

We provide you with all the code for this work, and if interested in this workflow, you can do tests with the newly published literature.

## Contents

### GPT-4 Classification: 

In the path 'GPT-4 Classification/papers', there are some papers for testing.

'GPT-4 Classification.py': multi-label text classification and analysis

'Similarity of Information Extractions.py': calculation of similarity of information extraction

'Text_Fragments_labels.xlsx': results of text classification

'classification.txt' : prompt for multi-label text classification

### GPT-4 Information Extraction:

'GPT-4 Information Extraction.py': Information Extraction and Organization
  
'similarity_evaluation.py': Computing similarity between manual work and GPT-4 work
  
'single-cage instructions.txt' and 'multi-cage instructions.txt': Prompt of information extraction for papers containing only one cage and many cages, respectively
  
'Tabular Informations without bertscore.xlsx': for testing code in 'similarity_evaluation.ipynb'
  
'Tabular Informations with bertscore.xlsx': providing our results of similarity
  
'2022-zhou-et-al-inherently-chiral-cages-via-hierarchical-desymmetrization.txt': this paper's content is too long to be saved in excel so saved in txt
  
'./level1','./level2','level3': input csv_file for GPT-4 information extraction
  
'./bertscore': package for similarity's calculation
  
### CHATBOT: Building a chatbot based on cage's database

'CHATBOT.py': chatbot's construction

'cage's database.json': cage's database used in chatbot

### database:

'cage database.xlsx': final database by manual work

'read excel.py': open 'cage database.xlsx' by pandas 

## Dependencies

The libraries needed for running this code are listed below with their required versions:

### Name Version

openai  '1.54.4'

requests '2.32.3'

PyPDF2 '3.0.1'

pandas '2.2.2'

tiktoken '0.8.0'

bert_score '0.3.12'

torch '2.3.1+cpu'

numpy '1.26.4'

seaborn '0.13.2'

matplotlib '3.9.2'

evaluate '0.4.3'

PIL '10.4.0'
