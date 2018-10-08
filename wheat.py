import helper
from credentials import agrimetrics_key
from pprint import pprint

headers = {
    'Ocp-Apim-Subscription-Key': agrimetrics_key,
}
baseuri = 'https://api.agrimetrics.co.uk'
names = helper.getPlantNames(baseuri, headers)
nres = 10000
skip = 1000

plant='Wheat'
savedcrops=[]
for i in range(0,nres-skip + 10,skip):
    print(i)
    ODataQuery = "?$filter=Field/hasSownCrop/any(c: c/label eq \'" + plant + "\' and c/harvestYear eq 2016)&$select=Field/hasSownCrop&$top=1000&$skip=" + str(i)
    fieldlist = helper.fieldSearch(ODataQuery, baseuri, headers)

    try:
        for field in fieldlist['results']:
            for year in field['hasSownCrop']:
                if year['harvestYear'] == 2017:
                        savedcrops.append(year['label'])
    except:
        pass


# print(len(fieldlist['results']))
# pprint(fieldlist)
pprint(savedcrops)