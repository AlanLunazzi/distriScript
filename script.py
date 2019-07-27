import requests
import csv
from datetime import datetime
from multiprocessing.pool import ThreadPool as Pool
from requests.adapters import HTTPAdapter
from requests.packages.urllib3.util.retry import Retry



itemResponse = {}
descriptionResponse = {}


def requests_retry_session(
	retries=3,
	backoff_factor=0.3,
	status_forcelist=(500, 502, 504),
	session=None,
):
	session = session or requests.Session()
	retry = Retry(
		total=retries,
		read=retries,
		connect=retries,
		backoff_factor=backoff_factor,
		status_forcelist=status_forcelist,
	)
	adapter = HTTPAdapter(max_retries=retry)
	session.mount('http://', adapter)
	session.mount('https://', adapter)
	return session

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
	try:
		itemResponse[item] = requests_retry_session().get('https://api.mercadolibre.com/items/' + item).json()
		descriptionResponse[item] = requests_retry_session().get('https://api.mercadolibre.com/items/' + item + '/description').json()
	except requests.exceptions.Timeout:
		print("Timeout!")
	except requests.exceptions.RequestException as e:
		print e



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
		try:
			itemSingular = itemResponse[r]
			descripcionSingular = descriptionResponse[r]
		except KeyError, e:
			print("Key error para el item: " + str(r) + " mensaje: " + e.message)
		if('pictures' in itemSingular and 'title' in itemSingular and 'plain_text' in descripcionSingular):
			for picture in itemSingular['pictures']:
				itemInfo.append(str(picture['url']))
			itemInfo = validatePictures(itemInfo)
			itemInfo.insert(6,itemSingular['title'])
			itemInfo.insert(7,descripcionSingular['plain_text'])
			itemInfo.insert(8,itemSingular['price'])
			itemInfo.insert(9,r)
			results.append(itemInfo)
			itemInfo = [] 
		else:
			print('El item ' + str(r) + ' no fue encontrado o no contenia algun campo obligatorio.'
			+ ' mensaje de error:' + str(itemSingular) + ' ' + str(descripcionSingular))
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
runThreads(50, itemsFiltered)
saveItemsInCsv(parseItems())
