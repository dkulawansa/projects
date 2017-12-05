import argparse
import six
import sys
import os

def main():
	"""This main function that read input data, parse it and write to an output file"""
	parser = argparse.ArgumentParser()
	parser.add_argument("input_filename", type=str, help="the input filename (string)")
	parser.add_argument("output_filename", type=str, help="the output filename (string)")
	args = parser.parse_args()
	try:
		with open(args.input_filename, 'r') as fhr:	
			data = fhr.read()
			if data == '':
				raise ValueError("No input data found")
			data_lst = data.split('\n')
	except ValueError as ex:
		sys.stderr.write("No data found in input file: {}".format(six.text_type(ex)))
		return
	except FileNotFoundError as ex:
		raise

	for item in data_lst:
		key, *data = item.split()
		if key == 'C':
			canvas(data, args.output_filename)
		elif key == 'L':
			line(data, args.output_filename)
		elif key == 'R':
			rectangle(data, args.output_filename)
		elif key == 'B':
			backfill(data, args.output_filename)	
			
def canvas(data, filename):
	""" create canvas for drawing"""
	x = [int(x) for x in data]
	width = x[0]
	heigth = x[1]
	with open(filename, 'w') as fh:
		for _ in range(width + 2): # 2 for margins 
			fh.write('-')
		fh.write('\n')
		for _ in range(heigth):
			fh.write('|')
			for _ in range(width):
				fh.write(' ')
			fh.write('|\n')
		for _ in range(width + 2):
			fh.write('-')
			
def get_canvas(filename_out):
	""" get the canvas dimensions of the existing canvas """
	try:
		with open(filename_out, 'r+') as fhr:
			canvas_data = fhr.read()
			if fhr.tell() == 0:
				raise ValueError("No canvas found")
			pos1 = canvas_data.find('\n')
			str1 = canvas_data[:pos1+1]
			pos2 = canvas_data.find(str1, pos1)
			height = canvas_data[pos1+1:pos2].count('\n')
			width = pos1 - 2
			canvas_length = (pos1 + 2)*(height +2) - 2
			cursor_new = fhr.tell()
			fhr.seek(cursor_new- canvas_length)
			content = fhr.read()
			fhr.write('\n')
			fhr.write(content)
			fhr.flush()
			os.fsync(fhr)
		return pos1, canvas_length, height
	except ValueError as ex:
		sys.stderr.write("Canvas should be created to draw anything in it: {}".format(six.text_type(ex)))
		raise
	except Exception as ex:
		raise
		
def line(data1, filename_out):
	""" draw a line between two points withing the canvas """

	x = [int(x) for x in data1]
	x1 = x[0]
	y1 = x[1]
	x2 = x[2]
	y2 = x[3]
	canvas_width, canvas_length, height = get_canvas(filename_out)
	with open(filename_out, 'r+') as fhr:
		fhr.read()
		cursor = fhr.tell()
		if y1 == y2:
			offset = (canvas_width +2) * y1 + x1
			fhr.seek(cursor- canvas_length + offset)
			xx = abs(x2 - x1)
			for _ in range(xx + 1):
				fhr.write('x')
				
		fhr.flush()
		os.fsync(fhr)
		if x1 == x2:
			for i in range(y1, y2+1):
				offset1 = (canvas_width +2) * i + x1
				fhr.seek(cursor- canvas_length + offset1)
				fhr.write('x')
					
def rectangle(rect_data, filename_out):
	""" draw a rectangle using coner coordinates withing the canvas"""
	x = [int(x) for x in rect_data]
	x1 = x[0]
	y1 = x[1]
	x2 = x[2]
	y2 = x[3]
	canvas_width, canvas_length, height = get_canvas(filename_out)
	with open(filename_out, 'r+') as fhr:
		canvas_data = fhr.read()
		cursor = fhr.tell()
		lst_y = [y1, y2]
		for yi in lst_y:
			offset = (canvas_width +2) * yi + x1
			fhr.seek(cursor- canvas_length + offset)
			xx = abs(x2 - x1)
			for _ in range(xx + 1):
				fhr.write('x')
				
		fhr.flush()
		os.fsync(fhr)
		lst_x = [x1, x2]
		for xi in lst_x:
			for i in range(y1, y2+1):
				offset1 = (canvas_width +2) * i + xi
				fhr.seek(cursor- canvas_length + offset1)
				fhr.write('x')

def backfill(bf_data, filename_out):
	"""" backfill the area withing the canvas"""
	x = [x for x in bf_data]
	x1 = int(x[0])
	y1 = int(x[1])
	fill = x[2] 
	canvas_width, canvas_length, height = get_canvas(filename_out)
	if (x1 > (canvas_width - 2) or y1 > height):
		return
	with open(filename_out, 'r+') as fhr:
		canvas_data = fhr.read()
		cursor = fhr.tell()
		offset = (canvas_width +2)
		fhr.seek(cursor- canvas_length + offset)
		str = fhr.read(canvas_length)
		lst = str.split('\n')
		data_lst1 = []
		data_lst2 = []
		data_lst3 = []
		i = 0
		for item in lst:
			i +=1
			if i <= height:
				if item[0:x1].rfind('x') != -1:
					x_tmp = item[0:x1].rfind('x')
					x_tmp += 1
				else:
					x_tmp = 1
				data_lst1.append((x_tmp, x1, i))
		i = 0	
		for item in lst:
			i +=1
			if i <= height:
				if item.find('x',x1) != -1:
					x_tmp = item.find('x',x1)
				else:
					x_tmp = canvas_width -1
				data_lst2.append((x1, x_tmp, i))
		
		for i in range(len(data_lst1)):
			data_lst3.append((data_lst1[i][0], data_lst2[i][1], i))

		start = fhr.seek(cursor- canvas_length + offset)
		for t in data_lst3:
			fhr.seek(start + t[0] + (canvas_width+2)*t[2])
			for _ in range(t[1] - t[0]):
				fhr.write(fill)
						
if __name__ == '__main__':
		main()
	