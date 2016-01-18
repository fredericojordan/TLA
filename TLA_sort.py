INPUT_FILE = "TLA.txt"
OUTPUT_FILE = "TLA_sorted.txt"

def sort(my_list):
	my_dict = { my_list[i][:3]:float(my_list[i][4:].replace(".","")) for i in range(len(my_list)) }
	return sorted(my_dict.items(), key=lambda x:x[1], reverse=True)

lines = [line.rstrip('\n') for line in open(INPUT_FILE)]

with open(OUTPUT_FILE, "w") as f:
	for line in sort(lines):
		f.write("{0}:{1:.0f}\n".format(line[0], line[1]))