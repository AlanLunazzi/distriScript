import requests
import csv
from datetime import datetime
from multiprocessing.pool import ThreadPool as Pool



itemResponse = []
descriptionResponse = []


def saveItemsInCsv(results):
	today = datetime.today().strftime('%Y%m%d')
	namefile = 'publicaciones' + today + '.csv'
	c = csv.writer(open(namefile , "w"), delimiter=';', lineterminator = '\n')
	print ("Se creo el archivo " + namefile)
	c.writerow(['Codigo', 'Titulo', 'Descripcion', 'Precio', 'Foto1', 'Foto2', 'Foto3', 'Foto4', 'Foto5', 'Foto6']) 
	for itemInfo in results:
		c.writerow([itemInfo[9], unicode(itemInfo[6]).encode('utf-8'), unicode(itemInfo[7]).encode('utf-8') , itemInfo[8], itemInfo[0], itemInfo[1], itemInfo[2], itemInfo[3], itemInfo[4], itemInfo[5]]) 
	print("Archivo " + namefile + " cargado correctamente! =) se guardaron " +str(len(results)) + ' resultados.')

def loadFile(file):
	if(file == 'items'):
		with open("items.txt", "r") as ins:
	else:
		with open("blacklist.txt", "r") as ins:
	array = []
	for line in ins:
	    line = line.replace('\n', '')
	   	line = line.replace('\r', '')
		array.append(line)
	return array


def callApis(array):
	token = 'APP_USR-7278287269671778-072705-c725ef3c8148d3189dce6b43a2ba3110-135124707'
	i = 1
	for item in array:
		print('Obteniendo info del item ' + str(i) + ' de ' + str(len(array)) + ' ' + item)
		itemResponse.append(requests.get('https://api.mercadolibre.com/items/' + item + '?access_token=' + token).json())
		descriptionResponse.append(requests.get('https://api.mercadolibre.com/items/' + item + '/description' + '?access_token=' + token).json())
		i += 1

def callApi(item):
	token = 'APP_USR-7278287269671778-072705-c725ef3c8148d3189dce6b43a2ba3110-135124707'
	print('Obteniendo info del item ' + item)

	rtaItem = requests.get('https://api.mercadolibre.com/items/' + item + '?access_token=' + token).json()
	rtaDescription = requests.get('https://api.mercadolibre.com/items/' + item + '/description' + '?access_token=' + token).json()
	itemResponse.append(rtaItem)
	descriptionResponse.append(rtaDescription)
	


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
		if('pictures' in r and 'title' in r and 'plain_text' in descriptionResponse[i]):
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

def runThreads(numberOfThreads, items, blacklist):
	pool = Pool(numberOfThreads)
	for item in items:
		if item not in blacklist
	    	pool.apply_async(callApi, (item,))
	pool.close()
	pool.join()


items = loadItems('items')
blacklist = loadItems('blacklist')
runThreads(20, items, blacklist)
saveItemsInCsv(parseItems(items))
