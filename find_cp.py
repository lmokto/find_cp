#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import csv
import re
import unicodedata

prov_cp = {
    'jujuy': ['Y', 'Y4600', ['4411 4655']], 'san_luis': ['D', 'D5700', ['5421 5888', '6721 6389']], 
    'la_pampa': ['L', 'L6300', ['5621 5621', '6200 6621', '8133 8336']], 
    'catamarca': ['K', 'K4700', ['4139 4753', '5260 5345']], 'caba': ['C', 'C1425', []], 
    'salta': ['A', 'A4400', ['4126 4651', '3636 3636']], 
    'chubut': ['U', 'U9103', ['9000 9227', '8415 8532']], 
    'santa_fe': ['S', 'S3000', ['2000 2921', '3000 3592', '6009 6106']], 
    'santa_cruz': ['Z', 'Z9400', ['9011 9420']], 'chaco': ['H', 'H3500', ['3500 3734']], 
    'mendoza': ['M', 'M5500', ['5435 5645', '6279 6279']], 
    'la_rioja': ['F', 'F5300', ['5263 5717']], 
    'tierra_del_fuego': ['V', 'V9410', ['9409 9421']], 
    'buenos_aires': ['B', 'B1878', ['7000 7641', '2700 2946', '6000 6748', '8151 8512', '1601 1987']], 
    'neuquen': ['Q', 'Q8300', ['8300 8407']], 
    'misiones': ['N', 'N3300', ['3300 3386']], 
    'corrientes': ['W', 'W3400', ['3185 3641']], 
    'formosa': ['P', 'P3600', ['3511 3636']], 
    'cordoba': ['X', 'X5000', ['5000 5988', '2189 2686', '6101 6279']], 
    'entre_rios': ['E', 'E3100', ['2000 2854', '3100 3287', '1647 1647']], 
    'santiago_del_estero': ['G', 'G4200', ['4176 4613', '5249 5266', '2340 2357', '3061 3766']], 
    'san_juan': ['J', 'J5400', []], 
    'tucuman': ['T', 'T4000', ['4000 4434']], 
    'rio_negro': ['R', 'R8500', ['9210 9210', '8134 8536']]
}

cap_cp = {
    'Y4600': 'san_salvador_de_jujuy', 
    'E3100': 'entre_rios', 
    'K4700': 'san_fernando_del_valle_de_catamarca', 
    'V9410': 'tierra_del_fuego', 'P3600': 'formosa', 
    'D5700': 'san_luis', 'X5000': 'cordoba', 
    'S3000': 'santa_fe', 'M5500': 'mendoza', 
    'A4400': 'salta', 'T4000': 'tucuman', 
    'H3500': 'resistencia', 
    'R8500': 'rio_negro', 
    'J5400': 'san_juan', 
    'W3400': 'corrientes', 
    'N3300': 'posadas', 
    'L6300': 'santa_rosa', 
    'B1878': 'la_plata', 
    'Q8300': 'neuquen', 
    'G4200': 'santiago_del_estereo', 
    'U9103': 'rawson', 
    'Z9400': 'rio_gallego', 
    'F5300': 'la_rioja'
}

MAIN_PATH  = ''
__filename = MAIN_PATH + '/list_cp/{0}.csv'

def elimina_tildes(s):
    #elimina_tildes(u'cadenaconacento') --> u'cadenasinacento'
    return ''.join((c for c in unicodedata.normalize('NFD', s) if unicodedata.category(c) != 'Mn')).encode('utf-8')

def fileopen(provin):

    prov = provin.replace(' ', '_').lower()
    filename = __filename.format(prov)
    reader = csv.DictReader(open(filename))
    
    return reader

def find_cp(provin='', ciudad='', codigo_postal=0):
    
    """
        Se ingresar como parametro una provincia con ciudad o provincia con codigo postal 
        o ciudad con codigo postal, sino simplemente provincia, ciudad o codigo postal y 
        retorna, la provincia con su ciudad el codigo postal argentino y codigo postal.
    """

    provin = elimina_tildes(provin.decode('utf-8').lower()) if len(provin) > 2 else ''
    ciudad = elimina_tildes(ciudad.decode('utf-8').lower()) if len(ciudad) > 2 else ''
    code = codigo_postal if isinstance(codigo_postal, int) else False
    
    if provin.replace(' ', '_').lower() in prov_cp.keys() and ciudad:
        
        reader = fileopen(prov)

        for row in reader:
            rr = row.values()
            if ' '.join([str(x) for x in (rr[0].split()[1:])]).lower() == ciudad:
                cp = rr[0].split()[0]
                cpa = prov_cp[prov][0]+rr[0].split()[0]+"AAA"
                
        return provin, ciudad, cpa, str(cp)
        
    elif provin and code:

        ciudad = []
        reader = fileopen(prov)

        for row in reader:
            rr = row.values()
            if int(rr[0].split()[0]) == code:
                ciudad.append(' '.join([str(x) for x in (rr[0].split()[1:])]).lower())
                cpa = '{0}{1}AAA'.format(prov_cp[prov][0], code)
            else:
                cpa = ' '
                
        return prov.replace(' ', '_').title(), cpa, str(code), ciudad
        
    elif provin.replace(' ', '_') in prov_cp.keys():
        
        prov = provin.replace(' ', '_')
        reader = fileopen(provin)

        if prov in prov_cp.keys():
            capital_cp = prov_cp[prov][1]
            ciudad = cap_cp[capital_cp]
        
        provincia = prov.replace("_", " ").title()
        ciudad = ciudad.replace("_", " ").title()

        return provincia ,ciudad, str(capital_cp[1:len(capital_cp)]), capital_cp+'AAA'
        
    elif ciudad:
        try:
            for prov in prov_cp.keys():
                reader = fileopen(prov)
                for row in reader:
                    rr = row.values()
                    prov_ciudad = ' '.join([str(x) for x in (rr[0].split()[1:])]).lower()
                    if prov_ciudad in ciudad or prov_ciudad == ciudad:
                        provincia = prov.replace('_', ' ').title()
                        ciudad = ciudad.replace("_", " ").title()
                        cp = rr[0].split()[0]
                        cpa = prov_cp[prov][0]+rr[0].split()[0]+"AAA"
            return provincia, ciudad, str(cp), cpa
        except: 
            return ' ', ciudad, ' ', ' '
        
    elif code:

        ciudad = []

        for k, i in prov_cp.iteritems():
            if i[2]:
                r_size = len(i[2])
                for x in range(r_size):
                    r = i[2][x].split()
                    if code in range(int(r[0]), int(r[1])):
                        reader = fileopen(k)
                        for row in reader:
                            rr = row.values()
                            if int(rr[0].split()[0]) == code:
                                provincia = k
                                cp = code
                                cpa = '{0}{1}AAA'.format(prov_cp[k][0], code)
                                ciudad.append(' '.join([str(x) for x in (rr[0].split()[1:])]).lower())
                                
        return provincia, str(cp), cpa, ciudad
            
    else:
        return ' ', ' ', ' ', ' '
    

if __name__ == '__main__':

    #print find_cp(provin="buenos aires")    
    CPAProponente = [ 
        5000, 
        5000, 
        1878, 
        1640, 
        5721, 
        5000, 
        5000, 
        5000, 
        5000, 
        5634, 
        7225, 
        5000, 
        9400, 
        5000, 
        5000, 
        5000, 
        4512, 
        5000, 
        5000, 
        6634, 
        5750, 
        5000, 
        9400, 
        9400, 
        5000, 
        9400, 
        9400, 
        9400 
    ]
    
    # test
    for cp in CPAProponente:
        print find_cp(codigo_postal=cp)