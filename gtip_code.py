import pandas as pd
import requests
import json
import time
file_path = "gtip_internet.xlsx"
output_file_path = "gtip.xlsx"
sheet_name = "gtip"  

df = pd.read_excel(file_path, sheet_name=sheet_name)

filtered_df = df[df['GUMRUK TARIF ISTATISTIK NUMARASI'].str.len() == 4]
filtered_df = filtered_df[['GUMRUK TARIF ISTATISTIK NUMARASI']]
filtered_df.to_excel(output_file_path, index=False)
code_list = filtered_df['GUMRUK TARIF ISTATISTIK NUMARASI'].values.tolist()
#print(code_list)
#print(type(code_list[0]))

base_url2 = "https://www.tradeatlas.com/tr/getfindHsCodes?q="

results_dict2 = {}

counter=0
for code in code_list:
    counter=counter+1
    print(f'Getting the code {code} {counter}/{len(code_list)}')
    full_url = base_url2 + code
    time.sleep(0.1)
    code=100
    while code !=200:
        try:
            response = requests.get(full_url)
            code=response.status_code
        except:
            time.sleep(1)       
    #print(response.text)
    json_data2 = response.json()
    #print(json_data)
    for key, value in json_data2.items():
        if not value==None:
            results_dict2[value['hs_code']] = value['name']

excel_output_file = "output_last.xlsx"
df_results = pd.DataFrame(results_dict2.items(), columns=["hs_code", "name"])
df_results.to_excel(excel_output_file, index=False, encoding='utf-8')

base_url = "https://www.tradeatlas.com/tr/p1/search?q="
results_dict = {}
counter2=0

for code in code_list:
    counter2=counter2+1
    print(f'Getting the code {code} {counter}/{len(code_list)}')
    full_url = base_url + code
    time.sleep(0.1)
    code=100
    while code !=200:
        try:
            response = requests.get(full_url)
            code=response.status_code
        except:
            time.sleep(1)        
    #print(response.text)
    json_data = response.json()
    for element in json_data:
        results_dict[element['hs_code']] = element['name']
    #print(results_dict)


df_results = pd.DataFrame(results_dict.items(), columns=["hs_code", "name"])
excel_output_file = "output.xlsx"
df_results.to_excel(excel_output_file, index=False, encoding='utf-8')

file1_path = "output.xlsx"
sheet1_name = "Sheet1" 
df1 = pd.read_excel(file1_path, sheet_name=sheet1_name, dtype=str)

file2_path = "output_last.xlsx"
sheet2_name = "Sheet1"  
df2 = pd.read_excel(file2_path, sheet_name=sheet2_name, dtype=str)

merged_df = pd.concat([df1, df2], ignore_index=True)
output_file_path = "combined_excel.xlsx"
merged_df.to_excel(output_file_path, index=False)
merged_df_sorted = merged_df.sort_values(by='hs_code', ascending=True)
merged_df_sorted.to_excel("sirali_combined_excel.xlsx", index=False)





