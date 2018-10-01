import requests, pprint
import numpy as np
# import iacshelp

def findField(lon,lat,baseuri,headers):
    # params = urllib.parse.urlencode({
    #     'lat': lat,
    #     'lon': lon,
    # })
    fullUri=baseuri + '/field-finder/?' + 'lat=' + str(lat[0]) + '&lon=' + str(lon[0])
    r = requests.get(fullUri,headers=headers)
    dict=r.json()
    return dict

def getField(id, ep, baseuri, headers):
    fullUri = baseuri + '/field-' + ep + '/' + id
    r = requests.get(fullUri, headers=headers)
    return r.json()

def getDictPage(baseURI, headers, pageNo, ep):
    fullURI = baseURI + '/' + ep + '/?pageNo=' + pageNo
    r = requests.get(fullURI, headers=headers)
    return r.json()

def getDict(baseURI, headers, ep):
    dic = getDictPage(baseURI, headers, str(1), ep)
    pages = int(dic['_links']['last']['href'].split('=')[1])
    lst=dic['results']
    for page in range(2,pages + 1, 1):
        new=getDictPage(baseURI, headers, str(page), ep)
        lst.extend(new['results'])
    return lst


def getPlantNames(baseURI, headers):
    lst = getDict(baseURI, headers, 'plant-species')
    names=[]
    for le in lst:
        try:
            names.append(le['preferredLabel'])
        except:
            pass
    return names

def getSoilNames(baseURI, headers):
    lst = getDict(baseURI, headers, 'soil-textures')
    names=[]
    for le in lst:
        try:
            names.append([le['preferredLabel'], le['@id']])
        except:
            pass
    return names

def findMatchCrop(list,string):
    fieldids=[]
    chosen=[]
    for i in list:
        try:
            if i['hasSownCrop'][1]['label'].lower() == string.lower():
                chosen.append(i)
                fieldids.append(i['_links']['ag:api:field-facts']['href'][-9:])
        except:
            pass
    return [chosen, fieldids]


def findSoilType(lst, fieldids, soil):
    newfieldids=[]
    for i in lst:
        try:
            # if i['_links']['self']['href'][-9:] in fieldids:
            if i['_links']['self']['href'][-9:] in fieldids and i['hasSoilLayer'][0]['hasSoilTexture']['hasSoilTextureType'].replace('soil-texture-types', 'soil-textures') == soil:
                newfieldids.append(i['_links']['self']['href'][-9:])
        except:
            pass
    return newfieldids


def annRainfall(lst, fieldids):
    arfl=[]
    for i in lst:
        if i['_links']['self']['href'][-9:] in fieldids:
            farfl=0
            for j in i['hasMonthlyTotalRainfall']['hasDatapoint']:
                farfl=farfl+j['value']/365
            arfl.append(farfl)
    return arfl

def ftntRainfall(lst, fieldids):
    ftfl=[]
    for i in lst:
        if i['_links']['self']['href'][-9:] in fieldids:
            farfl=0
            for j in i['hasDailyTotalRainfall']['hasDatapoint']:
                farfl=farfl+j['value']/14
            ftfl.append(farfl)
    return ftfl

def get2WksWeatherMean(list):
    maxtemp=[]
    mintemp=[]
    meantemp=[]
    windspeed=[]
    relativehumidity=[]
    rainfall=[]
    outdict={
        'maxtemp':maxtemp,
        'mintemp':mintemp,
        'meantemp':meantemp,
        'windspeed':windspeed,
        'relativehumidity':relativehumidity,
        'rainfall':rainfall
    }
    params=[
            "hasDailyMaximumTemperature",
            "hasDailyMinimumTemperature",
            "hasDailyMeanTemperature",
            "hasDailyMeanWindSpeed",
            "hasDailyMeanRelativeHumidity",
            "hasDailyTotalRainfall"
    ]
    for i in list:
        for j, k in zip(params, outdict):
            data=i[j]['hasDatapoint']
            store=[]
            for obs in data:
                store.append(obs['value'])
            mean=np.mean(store)
            outdict[k].append(mean)
    return outdict


def getLTAWeather(list):
    maxtemp=[]
    mintemp=[]
    meantemp=[]
    rainfall=[]
    airfrost=[]
    groundfrost=[]
    sunshine=[]
    rainfall1=[]
    rainfall10=[]
    gdd=[]
    outdict={
        "maxtemp": maxtemp,
        "mintemp": mintemp,
        "meantemp": meantemp,
        "rainfall": rainfall,
        "airfrost": airfrost,
        "groundfrost": groundfrost,
        "sunshine": sunshine,
        "rainfall1": rainfall1,
        "rainfall10": rainfall10,
        "gdd": gdd
    }
    params=[
        "hasLongTermAverageMonthlyMaximumTemperature",
        "hasLongTermAverageMonthlyMinimumTemperature",
        "hasLongTermAverageMonthlyMeanTemperature",
        "hasLongTermAverageMonthlyTotalRainfall",
        "hasLongTermAverageMonthlyDaysOfAirFrost",
        "hasLongTermAverageMonthlyDaysOfGroundFrost",
        "hasLongTermAverageMonthlyHoursOfSunshine",
        "hasLongTermAverageMonthlyDaysOfRainfallAbove1mm",
        "hasLongTermAverageMonthlyDaysOfRainfallAbove10mm",
        "hasLongTermAverageMonthlyGrowingDegreeDays"
    ]
    loop=0
    for i in list:
        for j, k in zip(params, outdict):
            data=i[j]['hasDatapoint']
            store=[]
            for obs in data:
                store.append(obs['value'])
            outdict[k].append(store)

    return outdict

def ltaForMonth(ltamatrix, month):
    store=[]
    for field in ltamatrix:
        store.append(field[month-1])
    return store

def fieldsSubset(lst, fieldids):
    ftfl=[]
    for i in lst:
        if i['_links']['self']['href'][-9:] in fieldids:
            ftfl.append(i)
    return ftfl

def elimNan(a, b):
    aa=[]
    bb=[]
    for i, j in zip(a, b):
        if i == i:
            if j == j:
                aa.append(i)
                bb.append(j)
    return[aa,bb]

def removeOutlier(a, b, val,operator):
    aa=[]
    bb=[]
    for i, j in zip(a, b):
        if operator == 'lt':
            if i < val:
                if j < val:
                    aa.append(i)
                    bb.append(j)
        if operator == 'gt':
            if i > val:
                if j > val:
                    aa.append(i)
                    bb.append(j)
    return[aa,bb]

def iacsToFieldID(baseuri, headers, iacs):
    l = iacshelp.iacsToLonLat(iacs)
    iddict = findField([l.longitude], [l.latitude], baseuri, headers)
    try:
        id = iddict['@id'][-9:]
    except:
        id = 'No id for that code'
    return id

def get2WksWeather(forecasts):
    maxtemp=[]
    mintemp=[]
    meantemp=[]
    windspeed=[]
    relativehumidity=[]
    rainfall=[]
    outdict={
        'maxtemp':maxtemp,
        'mintemp':mintemp,
        'meantemp':meantemp,
        'windspeed':windspeed,
        'relativehumidity':relativehumidity,
        'rainfall':rainfall
    }
    params=[
            "hasDailyMaximumTemperature",
            "hasDailyMinimumTemperature",
            "hasDailyMeanTemperature",
            "hasDailyMeanWindSpeed",
            "hasDailyMeanRelativeHumidity",
            "hasDailyTotalRainfall"
    ]
    for j, k in zip(params, outdict):
        data=forecasts[j]['hasDatapoint']
        store=[]
        for obs in data:
            outdict[k].append(obs['value'])

    return outdict

def fieldSearch(OData, baseuri, headers):
    fullUri = baseuri + '/field-search/' + '?$filter=' + OData
    print(fullUri)
    r = requests.get(fullUri, headers=headers)
    return r.json()


