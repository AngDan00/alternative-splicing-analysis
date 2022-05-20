import os
import subprocess
fasta_dir =  '' #path to the folder containing unsorted fasta files
analysis_dir = '' #path to the folder where you want yout fasta sorted by name
for fasta in os.listdir(fasta_dir):
  fasta_index = fasta.split('R')[0].strip('_')
  target_dir = analysis_dir + '/' + str(fasta_index)
  os.rename(fasta_dir + '/' + fasta, target_dir + '/' + fasta)
#subfolders = os.listdir(analysis_dir)
os.chdir(analysis_dir)
subfolders = os.listdir()
prefix = analysis_dir + '/'
subfolders = [prefix + sub for sub in subfolders]
for i in subfolders:
    os.chdir(i)
    subprocess.call('/mnt/c/Users/angelo/Desktop/transcript_id/TrimGalore-0.6.6/trim_galore --paired --2colour 20 --clip_R1 1 --clip_R2 1 -j 6 -o trimmed_fa *.fastq', shell=True)
    
