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
		if str(type(extract.at[i, "UNIPROT_ID"])) != "<class \'str\'>":
			extract.at[i, "UNIPROT_ID"] = str(extract.at[i, "UNIPROT_ID"])

	if compilation.empty:
		compilation = extract.copy()
	else:
		compilation = pd.concat([compilation, extract])

#-----------------------------

sequences = []
seq_regex = re.compile("\"sequence\"\:\"([^\"]+)")

#get list of currently downloaded sequences
with open("temp_data.tsv", "r") as fh:
	already_have = [line.strip().split("\t")[0] for line in fh.readlines()]

#get remaining sequences
fh = open("temp_data.tsv", "a")

for id in compilation["UNIPROT_ID"]:
	if id not in already_have:
		print(id)
		time.sleep(30)
		response = requests.get("https://www.ebi.ac.uk/proteins/api/features/" + id)
		if not response.ok:
			sequences.append(None)
		else:
			seq_match = seq_regex.search(response.text)

			if seq_match == None:
				sequences.append(None)
			else:
				sequences.append(seq_match[1])

		fh.write("{0}\t{1}\n".format(id, sequences[-1]))
		already_have.append(id)

fh.close()
compilation.insert(0, "sequences", sequences)

#----------------------------

#save compilation to csv
compilation.to_csv("final_data.tsv", sep = "\t")