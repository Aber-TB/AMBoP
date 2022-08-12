import glob
import os
import enum
import collections
import gzip
import seaborn as sns
import matplotlib.ticker as ticker


import matplotlib.pyplot as plt


# Enum for size units
class SIZE_UNIT(enum.Enum):
   BYTES = 1
   KB = 2
   MB = 3
   GB = 4

def convert_unit(size_in_bytes, unit):
   """ Convert the size from bytes to other units like KB, MB or GB"""
   if unit == SIZE_UNIT.KB:
       return size_in_bytes/1024
   elif unit == SIZE_UNIT.MB:
       return size_in_bytes/(1024*1024)
   elif unit == SIZE_UNIT.GB:
       return size_in_bytes/(1024*1024*1024)
   else:
       return size_in_bytes


def get_file_size(file_name, size_type = SIZE_UNIT.BYTES ):
   """ Get file in size in given unit like KB, MB or GB"""
   size = os.path.getsize(file_name)
   return convert_unit(size, size_type)

dir_name = '/ibers/repository03/archive/aber_tb/apha/'
#dir_name = './'

files = collections.defaultdict(list)

# Get a list of files (file paths) in the given directory
list_of_files = filter( os.path.isfile,
                        glob.glob(dir_name + '*.fastq.gz') )

sizes_list = []
num_seqs_list = []

file_num = 0

for file_path in list_of_files:
    size = format(get_file_size(file_path, SIZE_UNIT.GB),'.2f')
    num_seqs = len([1 for line in gzip.open(file_path, 'rt') if line.startswith('@')])
    files[file_path].append(size)
    files[file_path].append(num_seqs)

    sizes_list.append(float(size))
    num_seqs_list.append(num_seqs)

    print(file_num)
    file_num += 1
    if file_num == 4:
        break


sns.distplot(sizes_list, kde=True)

plt.savefig('file_sizes.png')


sns.distplot(num_seqs_list, kde=True)

plt.savefig('seq_num.png')

#
# from scipy.stats import norm
# ############ Plot file sizes
# x = sizes_list
#
# y = norm.pdf(x,0,1)
#
# fig, ax = plt.subplots(figsize=(9,6))
# ax.plot(x,y)
#
# plt.style.use('fivethirtyeight')
#
# plt.savefig('file_sizes.png')
#
#
# ############# Plot seq nums
#
# x = num_seqs_list
#
# y = norm.pdf(x,0,1)
#
# fig, ax = plt.subplots(figsize=(9,6))
# ax.plot(x,y)
#
# plt.style.use('fivethirtyeight')
#
# plt.savefig('seq_nums.png')
#
# # plt.plot(sizes_list)
# # plt.show()





























