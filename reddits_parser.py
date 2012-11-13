import json



def parse_reddits(list_file):
	output_list = []
	temp_tab = []
	temp_group = []
	level = 0
	with open(list_file) as reddits_list:

		for line in reddits_list:
			line = line.strip()
			if line.startswith('#') or len(line) == 0: continue

			if level == 0:
				if line.startswith('**'): return 'error'
				elif line.startswith('*'):
					level += 1
					temp_tab = []
				else:
					return 'error'

			elif level == 1:
				if line.startswith('**'): 
					level += 1
					temp_group = []
					temp_tab = []
				elif line.startswith('*'):
					output_list.append(temp_tab)
				else:
					temp_tab.append(line)

			elif level == 2:
				if line.startswith('**'):
					temp_tab.append(temp_group)
					temp_group = []
				elif line.startswith('*'):
					level -= 1
					temp_tab.append(temp_group)
					output_list.append(temp_tab)
				else:
					temp_group.append(line)

		temp_tab.append(temp_group)
		output_list.append(temp_tab)


	return json.dumps(output_list, indent = 4)













if __name__ == "__main__":
	print parse_reddits('reddits_list.txt')