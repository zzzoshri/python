import sys

# this is basically sort -u..... before I knew sort had this flag......
#


# USAGE: python setify.py [INPUT_FILE] [OUTPUT_FILE]
#



def main():
	with open(sys.argv[1], "r") as in_f:
		in_dat = in_f.readlines()

	input_set = set(in_dat)

	with open(sys.argv[2], "w") as out_f:
		out_f.write(''.join(input_set))
	
if __name__ == '__main__':
	main()
