def open_file(file_name, mode="r"):
    return open(file_name, mode, encoding='utf-8', errors='ignore')

def saveResult( result ):
	fileoutput = open("../result.html", "w+", encoding='utf-8', errors='ignore')

	html = ''' 
	<!DOCTYPE html>
		<html>
			<head>
				<meta charset="utf-8">
				<title>Color Layout Descriptor</title>
				<link rel="stylesheet" type="text/css" href="result.css">
			</head>
			<body>	
				<div class="input-image-item">
					<p>Input Picture:</p>
					<img src="PlantCLEF2016Test/'''
	
	
	html += str(result[0][0]) +'.jpg">'
	html += '<p> Image: ' + str(result[0][0]) + '.jpg</p></div>'

	count = 1

	while count <= 100 or result[count][1] > 15:
		html += '''
		<div class="image-item">
			<img src="PlantCLEF2016Test/'''

		html += str(result[count][0]) +'.jpg">' 
		html += '<p> Image: ' + str(result[count][0]) + '.jpg, Distance: ' + str(result[count][1]) + '</p></div>'

		count += 1

	html += '''
			</body>
		</html> 
	'''

	fileoutput.write( html ) 
