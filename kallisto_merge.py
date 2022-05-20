#library needed
import os
import subprocess
import pandas as pd
#parameters
dir_in = '/data01/users_space/adriano/projects/monica/charme_hs_seq_files/trimmed/'
dir_out = '/data01/users_space/adriano/projects/monica/charme_hs_seq_files/angelo/kallisto/'
#file path to the fasta to generate kallisto index 
fasta_tx = '/data01/common_data_files/transcriptome/rsem_Homo_sapiens.GRCh38_charmed.86.transcripts.fa' 
#how you want to name kallisto index file 
kallisto_index = 'kallisto_index.idx' 
#suffix of your read 
suffix_read1 = "_R1_001.fastq.gz"
suffix_read2 = "_R2_001.fastq.gz"
bin_kallisto = '/opt/kallisto/build/src/kallisto'

#settings
os.chdir(dir_in)
files = os.listdir(dir_in)
samples = [item for item in files if item.startswith('IPS')]
samples = [x.replace(suffix_read1," ").replace(suffix_read2," ") for x in samples]
samples = list(set(samples))
for index,sample in enumerate(samples):
    read1 = dir_in + sample.replace(" ", "") + suffix_read1
    read2 = dir_in + sample.replace(" ", "") + suffix_read2
    print(read1)
    print(read2)
    dir_sample = dir_out + str(sample)
    
    if os.path.exists(dir_sample) == False:
        os.makedirs(dir_sample)


    if index == 0:
        #kallisto index
        subprocess.call(bin_kallisto + ' index -i ' + kallisto_index + ' ' + fasta_tx, shell = True)
        #kallisto quant
        subprocess.call(bin_kallisto + ' quant -i '+ kallisto_index + ' -o ' + dir_sample + ' --plaintext -t 8 --rf-stranded --pseudobam '+ read1+' '+ read2, shell = True)
    else:
        subprocess.call(bin_kallisto + ' quant -i '+ kallisto_index + ' -o ' + dir_sample + ' --plaintext -t 8 --rf-stranded --pseudobam '+ read1+' '+ read2 , shell = True)

outputs = os.listdir(dir_out)
for index, item in enumerate(outputs):
    os.chdir(item)
    outputs_file = os.listdir(item)
    count_file = [item for item in outputs_files if item.contains('abundance')]
    colname = item[0]
    if index == 0:
        df_all = pd.read_table(count_file)
        colname1 = samples[index]
    else:
        df = pd.read_table(count_file)
        merged_df = pd.merge(df_all[['target_id', 'tpm']], df[['target_id','tpm']], on = ['target_id'], suffixes = (colname1, colname))
        merged_df.columns = merged_df.columns.map(lambda x: x.removeprefix("tpm"))
os.chdir(dir_out)
outputs = os.listdir(dir_out)
for index, item in enumerate(outputs):
    sub_out = dir_out + '/' + item
    os.chdir(sub_out)
    output_files = os.listdir(sub_out)
    count_file = [item for item in output_files if item == 'abundance.tsv']
    count_file_path = sub_out + '/' + count_file[0]
    colname = item
    if index == 0:
        df_all = pd.read_table(count_file_path)
        colname1 = item
    else:
        df = pd.read_table(count_file_path)
        merged_df = pd.merge(df_all[['target_id', 'tpm']], df[['target_id','tpm']], on = ['target_id'], suffixes = (colname1, colname))
        merged_df.columns = merged_df.columns.map(lambda x: x.removeprefix("tpm"))
merged_df.to_csv(dir_out + '/' + 'merged_count.tsv', sep = '\t')