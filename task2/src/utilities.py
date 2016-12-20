from os.path import dirname, abspath, join


def get_base_dir():
	base_directory = dirname(dirname(abspath(__file__)))
	return base_directory


def open_file(file_name, mode="r"):
    return open(file_name, mode, encoding='utf-8', errors='ignore')


def saveResult( result ):
	file_path = join(get_base_dir(), "result.html")
	file_output = open_file(file_path, "w+")

	html = ''' 
	<!DOCTYPE html>
		<html>
			<head>
				<meta charset="utf-8">
				<title>Color Layout Descriptor</title>
				<link rel="stylesheet" type="text/css" href="result.css">
			</head>
			<body>	
				<div class="image-item input">
					<p>Input Picture:</p>
					<img class="input-img"src="PlantCLEF2016Test/'''
	
	
	html += str(result[0][0]) +'.jpg">'
	html += '<p> Image: ' + str(result[0][0]) + '.jpg</p></div>'

	count = 1

	# show 75 results, no results with a distance greater 7.5 

	while count <= 75:
		try:
			if result[count][1] > 7.5:
				break
			html += '''
			<div class="image-item">
				<img src="PlantCLEF2016Test/'''

			html += str(result[count][0]) +'.jpg">' 
			html += '<p> Image: ' + str(result[count][0]) + '.jpg<br />Distance: ' + '{0:.2f}'.format(result[count][1]) + '</p></div>'

			count += 1
		except Exception:
			break

	html += '''
			</body>
		</html> 
	'''

	file_output.write( html )

	return file_path
