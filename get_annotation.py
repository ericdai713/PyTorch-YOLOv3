import numpy as np
import cv2
import os
import pandas as pd
import h5py

def get_name(index, hdf5_data):
	name = hdf5_data['/digitStruct/name']
	return ''.join([chr(v[0]) for v in hdf5_data[name[index][0]].value])

def get_bbox(index, hdf5_data):
	attrs = {}
	item = hdf5_data['digitStruct']['bbox'][index].item()
	for key in ['label', 'left', 'top', 'width', 'height']:
		attr = hdf5_data[item][key]
		values = [hdf5_data[attr.value[i].item()].value[0][0]
				  for i in range(len(attr))] if len(attr) > 1 else [attr.value[0][0]]
		attrs[key] = values
	return attrs
	
f = h5py.File('./digitStruct.mat','r')
print(f['/digitStruct/bbox'].shape[0])
for j in range(10000):
	im = cv2.imread('./images/'+str(j+1)+'.png')
	im_h, im_w, _ = im.shape
	#print('image height: ', im_h)
	img_name = get_name(j, f)
	row_dict = get_bbox(j, f)
	print('image name: ', img_name)
	#print('label: ', row_dict['label'])
	#print('left: ', row_dict['left'])
	#print('top: ', row_dict['top'])
	row_dict['bottom'] = [row_dict['top'][i] + row_dict['height'][i] for i in range(len(row_dict['top']))]
	#print('bottom: ', row_dict['bottom'])
	row_dict['right'] = [row_dict['left'][i] + row_dict['width'][i] for i in range(len(row_dict['left']))]
	#print('right: ', row_dict['right'])
	row_dict['x'] = [(row_dict['left'][i] + (row_dict['right'][i]-row_dict['left'][i])/2)/im_w for i in range(len(row_dict['label']))]
	row_dict['y'] = [(row_dict['top'][i] + (row_dict['bottom'][i]-row_dict['top'][i])/2)/im_h for i in range(len(row_dict['label']))]
	row_dict['w'] = [(row_dict['right'][i]-row_dict['left'][i])/im_w for i in range(len(row_dict['label']))]
	row_dict['h'] = [(row_dict['bottom'][i]-row_dict['top'][i])/im_h for i in range(len(row_dict['label']))]
	with open('./labels/'+str(j+1)+'.txt', 'a') as file:
		for i in range(len(row_dict['label'])):
			if int(row_dict['label'][i])==10:
				row_dict['label'][i] = 0
			file.write(str(int(row_dict['label'][i]))+' '+str(row_dict['x'][i])+' '+str(row_dict['y'][i])+' '+str(row_dict['w'][i])+' '+str(row_dict['h'][i]))
			file.write('\n')