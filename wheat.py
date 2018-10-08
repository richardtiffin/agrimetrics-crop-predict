import helper
from credentials import agrimetrics_key
from pprint import pprint

headers = {
    'Ocp-Apim-Subscription-Key': agrimetrics_key,
}
baseuri = 'https://api.agrimetrics.co.uk'
names = helper.getPlantNames(baseuri, headers)
nres = 14000000
skip = 1000000

plant='Wheat'
savedcrops2016 = []
savedcrops2017 = []
for i in range(0,nres-skip + 10,skip):
    print(i)
    ODataQuery = "?$filter=Field/hasRepresentativePoint/altitude gt 0&$select=Field/hasSownCrop&$top=1000&$skip=" + str(i)
    fieldlist = helper.fieldSearch(ODataQuery, baseuri, headers)

    try:
        for field in fieldlist['results']:
            for year in field['hasSownCrop']:
                if year['harvestYear'] == 2017:
                        savedcrops2017.append(year['label'])
                if year['harvestYear'] == 2016:
                    savedcrops2016.append(year['label'])
    except:
        pass


# print(len(fieldlist['results']))
# pprint(fieldlist)
pprint(savedcrops2016.count('Wheat')/len(savedcrops2016))
pprint(savedcrops2017.count('Wheat')/len(savedcrops2017))