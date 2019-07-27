import requests
import csv
from datetime import datetime
from multiprocessing.pool import ThreadPool as Pool



itemResponse = {}
descriptionResponse = {}

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
	with open(file + ".txt", "r") as ins:
	    array = []
	    for line in ins:
	    	line = line.replace('\n', '')
	    	line = line.replace('\r', '')
	        array.append(line)
	return array

def callApi(item):
	print('Obteniendo info del item ' + item)
	rtaItem = requests.get('https://api.mercadolibre.com/items/' + item).json()
	rtaDescription = requests.get('https://api.mercadolibre.com/items/' + item + '/description').json()
	itemResponse[item] = rtaItem
	descriptionResponse[item] = rtaDescription
	


def validatePictures(itemInfo):
	itemInfoSize = len(itemInfo)
	while(itemInfoSize < 6):
		itemInfo.insert (itemInfoSize, ' ')
		itemInfoSize += 1
	return itemInfo

def filterBlacklist(items, blacklist):
	itemsFiltered = [] 
	for item in items:
		if item not in blacklist:
			itemsFiltered.append(item)
		else:
			print("Item " + item + " descartado por blacklist")
	return itemsFiltered

def parseItems():
	i = 0
	itemInfo = []
	results = []
	for r in itemResponse:
		if('pictures' in itemResponse[r] and 'title' in itemResponse[r] and 'plain_text' in descriptionResponse[r]):
			print ("key = " + str(r))
			for picture in itemResponse[r]['pictures']:
				itemInfo.append(str(picture['url']))
			itemInfo = validatePictures(itemInfo)
			itemInfo.insert(6,itemResponse[r]['title'])
			itemInfo.insert(7,descriptionResponse[r]['plain_text'])
			itemInfo.insert(8,itemResponse[r]['price'])
			itemInfo.insert(9,r)
			results.append(itemInfo)
			itemInfo = [] 
		else:
			print('El item ' + array[i] + ' no fue encontrado o no contenia algun campo obligatorio.'
			+ ' mensaje de error:' + str(r[str(array[i])]))
		i += 1
	return results

def runThreads(numberOfThreads, items):
	pool = Pool(numberOfThreads)
	for item in items:
		pool.apply_async(callApi, (item,))
	pool.close()
	pool.join()




items = loadFile('items')
blacklist = loadFile('blacklist')
itemsFiltered = filterBlacklist(items, blacklist)
runThreads(20, itemsFiltered)
saveItemsInCsv(parseItems())
