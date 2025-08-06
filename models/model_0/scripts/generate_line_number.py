import argparse

parser = argparse.ArgumentParser(description="Generate a txt file with 1-n lines.")
parser.add_argument("cnt", help="Count of numbers needed")
args = parser.parse_args()

cnt = int(args.cnt)

with open("lines.txt", 'w') as file:
    for i in range(1, cnt + 1):
        file.write(str(i) + '\n')
