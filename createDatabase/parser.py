import csv
import sys


def main(argv):
	fields = []
	rows = []
	newRows = ''

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


	for i in range(0,50):
		curRow = str(rows[i])
		listInfo = curRow.split()

		try:
			test = float(listInfo[8])
			for i in range(0, 11):
				curInfo = listInfo[i]
				newRows = newRows + curInfo + "|"
			newRows = newRows + "\n"
			#Cur line is a CourseID|
		except ValueError:
			continue
			#print("useless line (no valuable info)")
		except IndexError:
			continue
			#print("index error/poss useless line")
			#continue;

	#print(newRows + "\n")
	#print("3rd value is " + newRows[3][0] + "\n")

	newRows = newRows.replace("\'", "")
	newRows = newRows.replace("[", "")


	newRows = newRows.split("\n")
	#print(newRows[1])

	f1 = open('courseList.dat', 'a')

	#curLine[0] throws index OOB,
	for i in range(0, len(newRows) - 1):
		curLine = str(newRows[i])
		#print("cur line is + \n" + curLine)
		if isInt(curLine[0]):
			#test = int(newRows[i])
			f1.write("\"STAT\"|")
			#f1.write(newRows[i].replace(".", "0"))
			newRows[i] = newRows[i].replace(".|", "0|")
			newLine = str(newRows[i])
			newLine = newLine[:-1]
			#print(newLine)
			f1.write(newLine)
			f1.write("\n")
		else:
			print("\n" + newRows[i] + "|||||REMOVED")
	f1.close()


	#for i in range(0, len(newRows)):
		#print("")





	#newRows.append()
def isInt(s):
	try:
		int(s)
		return True
	except ValueError:
		return False
	except IndexError:
		return False

if __name__ == '__main__':
    main(sys.argv)
