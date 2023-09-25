# input: file to read(e.g. sensor_accel_0), folders to read from
# e.g. python3 plotter.py sensor_accel_0 -a 230925_atck -b 230925_vanilla
# flags: -a --attack: attacked log folder to read from
#        -b --benign: benign   log folder to read from
# plot using matplotlib and seaborn library
# output:   plot of the data, time-value graph
#           green for benign, red for attacked
#           saved as png file
#           plot title: sensor_accel_0 -a 230925_atck -b 230925_vanilla
#           plot name:  sensor_accel_0-230925_atck-230925_vanilla.png

import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import argparse
import os

# parse arguments
parser = argparse.ArgumentParser()
parser.add_argument("file", help="file to read")
parser.add_argument("-a", "--attack", help="attack folder to read from")
parser.add_argument("-b", "--benign", help="benign folder to read from")
args = parser.parse_args()

# AREA: read attacked data
# first, find the attacked log file from attack folder. find a file thats name contains the args.file string
# get a list of all files in the directory
files = os.listdir(args.attack)

# loop through the list to find the file that contains the args.file string value
atk_file = None
for file in files:
    if args.file in file:
        atk_file = file
        break

if atk_file is None:
    print(f"No log file found in {args.attack} directory that contains {args.file} string.")
    exit()
else:
    print(f"Found attack log file: {atk_file}")

# now read from the log file
pd_atk = pd.read_csv(os.path.join(args.attack, atk_file))
print(pd_atk.head())

# AREA: read benign data
# then, find the benign log file from benign folder. find a file thats name contains the args.file string    import os
# get a list of all files in the directory
files = os.listdir(args.benign)

# loop through the list to find the file that contains the args.file string value
ben_file = None
for file in files:
    if args.file in file:
        ben_file = file
        break

if ben_file is None:
    print(f"No log file found in {args.benign} directory that contains {args.file} string.")
    exit()
else:
    print(f"Found benign log file: {ben_file}")

# now read from the log file
pd_ben = pd.read_csv(os.path.join(args.benign, ben_file))
print(pd_ben.head())

# AREA: merge data
# reset timestamp to start from 0
pd_atk['timestamp'] = pd_atk['timestamp'] - pd_atk['timestamp'][0]
pd_ben['timestamp'] = pd_ben['timestamp'] - pd_ben['timestamp'][0]

# merge the two dataframes, after changing the column names
# atk: x,y,z > atk_x, atk_y, atk_z | ben: x,y,z > ben_x, ben_y, ben_z
pd_merged = pd.DataFrame()
pd_merged['timestamp'] = pd_atk['timestamp']
pd_merged['atk_x'] = pd_atk['x']
pd_merged['atk_y'] = pd_atk['y']
pd_merged['atk_z'] = pd_atk['z']
pd_merged['ben_x'] = pd_ben['x']
pd_merged['ben_y'] = pd_ben['y']
pd_merged['ben_z'] = pd_ben['z']
print(pd_merged.head())

# AREA: plot

fig = plt.figure(figsize=(30, 10))
plt.title(f"{args.file} -a {args.attack} -b {args.benign}")
plt.subplot(3, 1, 1)
plt.plot(pd_merged['timestamp'], pd_merged['atk_x'], color='red', label='attacked')
plt.plot(pd_merged['timestamp'], pd_merged['ben_x'], color='green', label='benign')
plt.legend(loc='upper right')
plt.xlabel('time')
plt.ylabel('accel_x')
plt.subplot(3, 1, 2)
plt.plot(pd_merged['timestamp'], pd_merged['atk_y'], color='red', label='attacked')
plt.plot(pd_merged['timestamp'], pd_merged['ben_y'], color='green', label='benign')
plt.legend(loc='upper right')
plt.xlabel('time')
plt.ylabel('accel_y')
plt.subplot(3, 1, 3)
plt.plot(pd_merged['timestamp'], pd_merged['atk_z'], color='red', label='attacked')
plt.plot(pd_merged['timestamp'], pd_merged['ben_z'], color='green', label='benign')
plt.legend(loc='upper right')
plt.xlabel('time')
plt.ylabel('accel_z')


plt.savefig(f"{args.file}-{args.attack[2:]}-{args.benign[2:]}.png")
plt.show()
