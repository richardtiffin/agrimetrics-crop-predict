import helper
from credentials import agrimetrics_key
from pprint import pprint
import pandas as pd
import matplotlib.pyplot as plt
import plotly.plotly as py
import plotly.graph_objs as go

headers = {
    'Ocp-Apim-Subscription-Key': agrimetrics_key,
}
baseuri = 'https://api.agrimetrics.co.uk'
names = helper.getPlantNames(baseuri, headers)

result = []
for plant in names:
    print(plant)
    ODataQuery = "Field/hasSownCrop/any(c: c/label eq \'" + plant + "\' and c/harvestYear eq 2016)&$select=Field/hasSownCrop"

    fieldlist = helper.fieldSearch(ODataQuery, baseuri, headers)

    savedcrops=[]
    try:
        for field in fieldlist['results']:
            for year in field['hasSownCrop']:
                if year['harvestYear'] == 2017:
                        savedcrops.append(year['label'])
    except:
        pass

    countdict = {i:savedcrops.count(i) for i in set(savedcrops)}

    if countdict != {}:
        result.append([plant, countdict])

df = pd.DataFrame()
data = []
for crop in result:
    total = sum(crop[1].values())
    for elem in crop[1].keys():
        crop[1][elem] = crop[1][elem]/total
    dfinsert = pd.DataFrame(crop[1], index=[crop[0]])

df.to_pickle(dataframe)