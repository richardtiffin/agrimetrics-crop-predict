import helper
from credentials import agrimetrics_key
from pprint import pprint

headers = {
    'Ocp-Apim-Subscription-Key': agrimetrics_key,
}
baseuri = 'https://api.agrimetrics.co.uk'
names = helper.getPlantNames(baseuri, headers)

for plant in names:
    print(plant)
    ODataQuery = "Field/hasSownCrop/label eq \'" + plant + "\' and Field/hasSownCrop/harvestYear eq 2016&$select=Field/hasSownCrop"

    fieldlist = helper.fieldSearch(ODataQuery, baseuri, headers)

    savedcrops=[]
    try:
        for field in fieldlist['results']:
            for year in field['hasSownCrop']:
                if year['harvestYear'] == 2017:
                        savedcrops.append(year['label'])
    except:
        pass


    print(savedcrops)