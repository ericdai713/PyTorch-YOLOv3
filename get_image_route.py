import random
import os

lst = [x+1 for x in range(10000)]
random.shuffle(lst)
for j in range(len(lst)):
	if j < len(lst)*0.8:
		with open('train.txt', 'a') as file:
			file.write('data/custom/images/{:d}.png'.format(lst[j]))
			file.write('\n')
	else:
		with open('valid.txt', 'a') as file:
			file.write('data/custom/images/{:d}.png'.format(lst[j]))
			file.write('\n')