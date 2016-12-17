def open_file(file_name, mode="r"):
    return open(file_name, mode, encoding='utf-8', errors='ignore')

def saveResult():
	fileoutput = open("result.html", "w+", encoding='utf-8', errors='ignore')

	html = ''' 
	<!DOCTYPE html>
		<html>
			<head>
				<meta charset="utf-8">
				<title>Color Layout Descriptor</title>
				<link rel="stylesheet" type="text/css" href="result.css">
			</head>
			<body>	
				
			</body>
		</html> 
	'''

	fileoutput.write( html ) 
