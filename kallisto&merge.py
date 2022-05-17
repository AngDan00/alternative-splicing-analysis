#runnare nella cartella contenente le reads trimmate, e il fasta per la generazione dell'index di kallisto 
import os
import subprocess
import pandas as pd
wdir = os.getcwd()
os.chdir(wdir)
files = os.listdir(wdir)
fasta = [item for item in files if item.startswith('IPS')]
for i in range(0,len(fasta),2):
    x=' '.join((fasta[i], fasta[i+1]))
    name = str(fasta[i][:-16])
    subprocess.call('kallisto index -i index.idx your_transcripts.fasta', shell = True)
    subprocess.call('kallisto quant -i index.idx -o output_' + name +' '+ x +' --plaintext -t 8 --rf-stranded --pseudobam', shell = True)
outputs = [j for j in files if j.startswith('output')]
prefix = wdir + '/'
outputs = [prefix + sub for sub in outputs]
for index, item in enumerate(outputs):
    os.chdir(item)
    counts = os.listdir(item)
    filepath = item + '/' + counts[0]
    colname = str(item[70:])
    if index == 0:
        df_all = pd.read_table(filepath)
        colname1 = str(item[70:])
    else:
        df = pd.read_table(filepath)
        merged_df = pd.merge(df_all[['target_id', 'tpm']], df[['target_id','tpm']], on = ['target_id'], suffixes = (colname1, colname))
        merged_df.columns = merged_df.columns.map(lambda x: x.removeprefix("tpm"))