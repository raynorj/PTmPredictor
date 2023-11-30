import os
import pandas as pd
import requests, time, re

compilation = pd.DataFrame()

organism_paths =  ["Organisms/" + file for file in os.listdir("Organisms")]
cell_line_paths = ["Cell Lines/" + file for file in os.listdir("Cell Lines")]

for file_path in organism_paths + cell_line_paths:
	data = pd.read_excel(file_path)
	extract = data[["UNIPROT_ID", "Tm_(C)"]]
	
	for i in range(len(extract)):
		if str(type(extract.at[i, "Tm_(C)"])) == "<class \'str\'>":
			extract.at[i, "Tm_(C)"] = float(extract.at[i, "Tm_(C)"].split(" ")[0]) 

	if compilation.empty:
		compilation = extract.copy()
	else:
		compilation = pd.concat([compilation, extract])

#-----------------------------

sequences = []
seq_regex = re.compile("\"sequence\"\:\"([^\"]+)")

#get list of currently downloaded sequences
with open("temp_data.tsv", "r") as fh:
	current_ids = [line.strip().split("\t")[0] for line in fh.readlines()]

total_ids = [id for id in compilation["UNIPROT_ID"]]

print("Currently downloaded id count: " + str(len(current_ids)))
print("All ids count: " + str(len(total_ids)))