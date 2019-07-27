import requests
import csv
from datetime import datetime

itemResponse = []
descriptionResponse = []

def saveItemsInCsv(results):
	today = datetime.today().strftime('%Y%m%d')
	namefile = 'publicaciones' + today + '.csv'
	c = csv.writer(open(namefile , "w"), delimiter=';', lineterminator = '\n')
	print ("Se escribe archivo por primera vez")
	c.writerow(['Codigo', 'Titulo', 'Descripcion', 'Precio', 'Foto1', 'Foto2', 'Foto3', 'Foto4', 'Foto5', 'Foto6']) 
	for itemInfo in results:
		print ("Se guarda resultado del item " + str(itemInfo[9]))
		c.writerow([itemInfo[9], unicode(itemInfo[6]).encode('utf-8'), unicode(itemInfo[7]).encode('utf-8') , itemInfo[8], itemInfo[0], itemInfo[1], itemInfo[2], itemInfo[3], itemInfo[4], itemInfo[5]]) 
	print("Archivo " + namefile + " cargado correctamente! =)")

def loadItems():
	with open("items.txt", "r") as ins:
	    array = []
	    for line in ins:
	    	line = line.replace('\n', '')
	    	line = line.replace('\r', '')
	        array.append(line)
	return array

def callApis(array):
	token = 'APP_USR-7278287269671778-072623-c6d4136fb211d41df48c4179cb7c1cbb-135124707'
	i = 1
	for item in array:
		print('Llamamos al item ' + str(i) + ' de ' + str(len(array)) + ' ' + item)
		itemResponse.append(requests.get('https://api.mercadolibre.com/items/' + item + '?access_token=' + token).json())
		descriptionResponse.append(requests.get('https://api.mercadolibre.com/items/' + item + '/description' + '?access_token=' + token).json())
		i += 1

def validatePictures(itemInfo):
	itemInfoSize = len(itemInfo)
	while(itemInfoSize < 6):
		itemInfo.insert (itemInfoSize, ' ')
		itemInfoSize += 1
	return itemInfo

def parseItems(array):
	i = 0
	itemInfo = []
	results = []
	for r in itemResponse:
		if('pictures' in r and 'title' in r):
			for picture in r['pictures']:
				itemInfo.append(str(picture['url']))
			itemInfo = validatePictures(itemInfo)
			itemInfo.insert(6,r['title'])
			itemInfo.insert(7,descriptionResponse[i]['plain_text'])
			itemInfo.insert(8,r['price'])
			itemInfo.insert(9,array[i])
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
