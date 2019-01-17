import json
import requests
from datetime import datetime, timedelta, timezone
from time import gmtime, strftime, strptime
import time
from personasmatriz import matrizper


def sumDias (tiempo, dias):
    second = round(int(tiempo) / 1000)
    second = second + (86400 * dias) # sumo un día
    print ('timestamp en segundos = {}'.format(second))
    formatofecha = datetime.utcfromtimestamp(second)
    print ('formatofecha = {}'.format(formatofecha))
    microsecond = round((int(second) * 1000 ))
    print ('microsecond fecha final = {}'.format(microsecond))
    return microsecond


if __name__ == "__main__":
    #includeData=true&aggregationType=COUNT&startTimestamp=1543708800000&endTimestamp=1543795200000&queryMode=TOTAL&entity=SERVICE-28ECDEF7C6E49AE0&Api-Token=kMV7IUkPSWCrQbZz5-vN2'
    url = 'https://fht16218.live.dynatrace.com/api/v1/timeseries/com.dynatrace.builtin%3Aservicemethod.requests?'
    args = {'includeData':'true',
    'aggregationType':'COUNT',
    'startTimestamp':'1544054400000',
    'endTimestamp':'1544140800000',
    'predict': 'false',
    'queryMode':'Total',
    'entity':'SERVICE_METHOD-8C302CE5F8850849',
    'Api-Token':'kMV7IUkPSWCrQbZz5-vN2'}
    for dias in range(3):
        if dias != 0:
            startTime = sumDias(args.get('startTimestamp'), 1)
            args['startTimestamp'] = startTime
            endTime = sumDias(args.get('startTimestamp'), 1)
            args['endTimestamp'] = endTime
        for y in range(0,len(matrizper)):
            args['entity'] = matrizper[y]
            req = requests.get(url,params=args)
            if req.status_code == 200:
                content = req.content
                nombrefile =  str(datetime.utcfromtimestamp(round(int(args['startTimestamp']) / 1000)).strftime('%Y_%m_%d_')) + str(matrizper[y]) + '_dynabchile_servicesrequest.json'
                file = open(nombrefile, 'wb')
                file.write(content)
                file.close
                response_json = req.json()
                servicio = json.loads(content)
                result = response_json['dataResult']
                datapoint = result['dataPoints']
                nombre = result['entities']
                tipo = result['aggregationType']
                for entidad in nombre:
                    for x in datapoint[entidad]:
                        hora = datetime.utcfromtimestamp(int(round(int(x[0]) / 1000)))
                        print ('servicio {} fecha {} ({}) : data {} tipo {}'.format(nombre[entidad], hora, x[0], x[1], tipo))
            else:
                print ('Error al leer la Api de dynatrace')
