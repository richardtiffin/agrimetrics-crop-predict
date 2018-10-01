import helper
from credentials import agrimetrics_key
from pprint import pprint

headers = {
    'Ocp-Apim-Subscription-Key': agrimetrics_key,
}
baseuri = 'https://api.agrimetrics.co.uk'
ODataQuery = "Field/hasSownCrop/label eq \'Wheat\' and Field/hasSownCrop/harvestYear eq 2016&$select=Field/hasSownCrop"

fieldlist = helper.fieldSearch(ODataQuery, baseuri, headers)

savedcrops=[]
for field in fieldlist['results']:
    for year in field['hasSownCrop']:
        if year['harvestYear'] == 2017:
                savedcrops.append(year['label'])

print(savedcrops)