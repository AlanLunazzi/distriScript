import requests
import csv
from datetime import datetime

today = datetime.today().strftime('%Y%m%d')
namefile = 'publicaciones' + today + '.csv'
c = csv.writer(open(namefile , "w"), delimiter=';', lineterminator = '\n')

def writeResult(results, initial):
	i = 0
	if(initial == True):
		print ("Se escribe archivo por primera vez")
		c.writerow(['Item', 'Titulo', 'Descripcion', 'Precio', 'Imagen 1', 'Imagen 2', 'Imagen 3', 'Imagen 4', 'Imagen 5']) 
	else:
		for urls in results:
			print ("Se guarda resultado del item " + urls[8])
			c.writerow([urls[8], unicode(urls[5]).encode('utf-8'), unicode(urls[6]).encode('utf-8') , urls[7], urls[0], urls[1], urls[2], urls[3], urls[4]]) 
			i += 1



token = 'APP_USR-7278287269671778-072623-c6d4136fb211d41df48c4179cb7c1cbb-135124707'
respuestas = []
urls = []
results = []
descriptions = []
text_description = []

writeResult(results, True)

with open("items.txt", "r") as ins:
    array = []
    for line in ins:
    	line = line.replace('\n', '')
        array.append(line)

i = 1
for item in array:
	print('Llamamos al item ' + str(i) + ' de ' + str(len(array)) + ' ' + item)
	respuestas.append(requests.get('https://api.mercadolibre.com/items/' + item + '?access_token=' + token).json())
	descriptions.append(requests.get('https://api.mercadolibre.com/items/' + item + '/description' + '?access_token=' + token).json())
	i += 1


i = 0
for r in respuestas:
	if('pictures' in r and 'title' in r and 'plain_text' in descriptions[i]):
		for picture in r['pictures']:
			urls.append(str(picture['url']))
		urls.insert(5,r['title'])
		urls.insert(6,descriptions[i]['plain_text'])
		urls.insert(7,r['price'])
		urls.insert(8,array[i])
		results.append(urls)
		urls = [] 
	else:
		print('El item ' + array[i] + ' no fue encontrado o no contenia algun campo obligatorio.'
		+ ' mensaje de error:' + str(r) + str(descriptions[i]))
	i += 1

writeResult(results, False)
print("Archivo " + namefile + " cargado correctamente! =)")
