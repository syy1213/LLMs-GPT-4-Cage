# LLMs-GPT-4-Cage
Knowledge Discovery from Porous Organic Cages Literature Using a Large Language Model 

We provide you with all the code for this work, and if interested in this workflow, you can do tests with the newly published literature.

## Contents

### GPT-4 Classification: 

In the path 'GPT-4 Classification/papers', there are some papers for testing.

'GPT-4 Classification.ipynb': multi-label text classification and analysis

'Text_Fragments_labels.xlsx': results of text classification

'classification.txt' : prompt for multi-label text classification

### GPT-4 Information Extraction:

'GPT-4 Information Extraction.ipynb': Information Extraction and Organization
  
'similarity_evaluation.ipynb': Computing similarity between manual work and GPT-4 work
  
'single-cage instructions.txt' and 'multi-cage instructions.txt': Prompt of information extraction for papers containing only one cage and many cages, respectively

---------------------------------------------------------------------
Give you some labeled texts containing information about a new research paper related to organic molecular cages. Please extract from it the name of the molecular cage, the specific surface area(give the whole sentence which describe it), the ccdc number, the topology(eg.[2+3],[4+6] etc.,you need to give the whole sentence which describe it), the comprehensive synthesis procedures, the name of the reactant needed for the synthesis, and the the comprehensive synthesis procedures of the reactant, and then organize these information into the following table:

|name of the organic molecular cage|topology|ccdc number|specific surface area|cage's synthesis procedure|reactant1|reactant1's synthesis procedure|reactant2|reactant2's synthesis procedure|

please note:
1.If some information is not given, use 'None'
2.The comprehensive synthesis procedures must contain amounts of reactant, solvent and catalysts.
3.There must be only one organic molecular cage, so the table must not contain multiple rows.
---------------------------------------------------------------------
Give you some labeled texts containing information about a new research paper related to organic molecular cages. Please extract from it the name of the molecular cage, the specific surface area(give the whole sentence which describe it), the ccdc number, the topology(eg.[2+3],[4+6] etc.,you need to give the whole sentence which describe it), the comprehensive synthesis procedures, the name of the reactant needed for the synthesis, and the the comprehensive synthesis procedures of the reactant, and then organize these information into the following table:

|name of the organic molecular cage|topology|ccdc number|specific surface area|cage's synthesis procedure|reactant1|reactant1's synthesis procedure|reactant2|reactant2's synthesis procedure|

please note:
1.If some information is not given, use 'None'
2.The comprehensive synthesis procedures must contain amounts of reactant, solvent and catalysts.
3.There may be more than one organic molecular cage, so the table may contain multiple rows.
---------------------------------------------------------------------
  
'Tabular Informations without bertscore.xlsx': for testing code in 'similarity_evaluation.ipynb'
  
'Tabular Informations with bertscore.xlsx': providing our results of similarity
  
'2022-zhou-et-al-inherently-chiral-cages-via-hierarchical-desymmetrization.txt': this paper's content is too long to be saved in excel so saved in txt
  
'./level1','./level2','level3': input csv_file for GPT-4 information extraction
  
'./bertscore': package for similarity's calculation
  
### CHATBOT: Building a chatbot based on cage's database

'CHATBOT.ipynb': chatbot's construction

'cage's database.json': cage's database used in chatbot

### database:

'cage database.xlsx': final database by manual work

'read excel.ipynb': open 'cage database.xlsx' by pandas 

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
