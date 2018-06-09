import csv
import sys


def main(argv):
	fields = []
	rows = []

  #  if len(argv) < 0:
  #     print >> sys.stderr, 'Usage: python skeleton_json_parser.py <path to json files>'
  #      sys.exit(1)
  #  # loops over all .json files in the argument
	with open('/Users/Richy/Downloads/Fall2017.csv', 'r') as csvfile:
		#print(csvfile) 
		csvreader = csv.reader(csvfile)
		fields = csvreader.next()

		for row in csvreader:
			rows.append(row)

	#print('\nFirst 2 rows are:\n')
	#for row in rows[:2]:
	#	for col in row:
	#		print("%10s"%col),
	#	print('\n')
	

	print("\n here is rows \n")
	print(rows[1])

if __name__ == '__main__':
    main(sys.argv)