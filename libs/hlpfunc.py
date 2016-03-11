def getByAttrVal(objlist, attr, val):
	matches = [getattr(obj, attr) == val for obj in objlist]
	index = matches.index(True)
	return objlist[index]

def getAllItems(page):
	ret = page().items
	while hasattr(page(), 'next'):
		page = page().next()
		ret.extend(page().items)
	return ret
