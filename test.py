import argparse

parser = argparse.ArgumentParser()
parser.add_argument("-r","--range", nargs='*')
args = parser.parse_args()

print(args.range)
for i in range(len(args.range)):
    print(args.range[i])