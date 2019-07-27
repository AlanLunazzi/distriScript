import requests
import csv
from datetime import datetime

today = datetime.today().strftime('%Y%m%d')
namefile = 'publicaciones' + today + '.csv'
c = csv.writer(open(namefile , "w"), delimiter=';', lineterminator = '\n')
token = 'APP_USR-7278287269671778-072623-c6d4136fb211d41df48c4179cb7c1cbb-135124707'
itemResponse = []
descriptionResponse = []

def saveItemsInCsv(results):
	print ("Se escribe archivo por primera vez")
	c.writerow(['Item', 'Titulo', 'Descripcion', 'Precio', 'Imagen 1', 'Imagen 2', 'Imagen 3', 'Imagen 4', 'Imagen 5']) 
	for itemInfo in results:
		print ("Se guarda resultado del item " + itemInfo[8])
		c.writerow([itemInfo[8], unicode(itemInfo[5]).encode('utf-8'), unicode(itemInfo[6]).encode('utf-8') , itemInfo[7], itemInfo[0], itemInfo[1], itemInfo[2], itemInfo[3], itemInfo[4]]) 
	print("Archivo " + namefile + " cargado correctamente! =)")

def loadItems():
	with open("items.txt", "r") as ins:
	    array = []
	    for line in ins:
	    	line = line.replace('\n', '')
	        array.append(line)
	return array

def callApis(array):
	i = 1
	for item in array:
		print('Llamamos al item ' + str(i) + ' de ' + str(len(array)) + ' ' + item)
		itemResponse.append(requests.get('https://api.mercadolibre.com/items/' + item + '?access_token=' + token).json())
		descriptionResponse.append(requests.get('https://api.mercadolibre.com/items/' + item + '/description' + '?access_token=' + token).json())
		i += 1

def parseItems(array):
	i = 0
	itemInfo = []
	results = []
	for r in itemResponse:
		if('pictures' in r and 'title' in r and 'plain_text' in descriptionResponse[i]):
			for picture in r['pictures']:
				itemInfo.append(str(picture['url']))
			itemInfo.insert(5,r['title'])
			itemInfo.insert(6,descriptionResponse[i]['plain_text'])
			itemInfo.insert(7,r['price'])
			itemInfo.insert(8,array[i])
			results.append(itemInfo)
			itemInfo = [] 
		else:
			print('El item ' + array[i] + ' no fue encontrado o no contenia algun campo obligatorio.'
			+ ' mensaje de error:' + str(r) + str(descriptionResponse[i]))
		i += 1
	return results


items = loadItems()
callApis(items) 
saveItemsInCsv(parseItems(items))
