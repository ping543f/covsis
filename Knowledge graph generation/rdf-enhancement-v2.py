import geonamescache
from geonamescache.mappers import country
import pycountry_convert as pc

def country_to_continent(country_name):
    country_alpha2 = pc.country_name_to_country_alpha2(country_name)
    country_continent_code = pc.country_alpha2_to_continent_code(country_alpha2)
    country_continent_name = pc.convert_continent_code_to_continent_name(country_continent_code)
    return country_continent_name


f = open('Local-weight-symptom-map-v3.csv','r')
ntwrite = open('country-symptoms-rdf_V_4_weight.nt','a+',encoding='utf-8')
lines = f.readlines()

country_list = []
symptom_list = []
for line in lines:
    line = line.rstrip('\n')
    country = line.split(',')[0]
    country = country.replace(' ','_')
    country_list.append(country)
    weight = line.split(',')[1]
    symp = line.split(',')[2]
    symp = symp.replace(' ','_')
    symp = symp.lower()
    symptom_list.append(symp)
    # ntwrite.write("<http://ontology.ontotext.com/" + country+ ">" + " <http://ontology.ontotext.com#encounters" + "> <http://ontology.ontotext.com/" + symp + "> .\n")
    ntwrite.write("<http://ontology.ontotext.com/" + country+ ">" + " <http://ontology.ontotext.com#"+ weight + "> <http://ontology.ontotext.com/" + symp + "> .\n")
    # print(country,'========',symp)
    # if country == 'Iran' or country =='Taiwan' or country =='Argentina':
    #     entity_pairs.append([country,symp])


print(len(country_list))

country_set = set(country_list)
continent_list = []
print(len(country_set))

country_explicit=['Vatican',
'U.S. Virgin Islands','Kosovo','Timor Leste',
'Curacao','Sint Maarten','Western Sahara']

for country in country_set:
    try:
        country_name = country.replace("_"," ")
        continent = country_to_continent(country_name)
        continent = continent.replace(" ","_")
        continent_list.append(continent)
        ntwrite.write("<http://ontology.ontotext.com/" + country+ "> <http://www.w3.org/1999/02/22-rdf-syntax-ns#type> <http://ontology.ontotext.com/country> ." +"\n")
        ntwrite.write("<http://ontology.ontotext.com/" + country+ "> <http://ontology.ontotext.com#Is_in> <http://ontology.ontotext.com/"+continent+"> .\n")
        # print(country)
    except KeyError:
        pass

symp_set = set(symptom_list)

for symptom in symp_set:
    ntwrite.write("<http://ontology.ontotext.com/" + symptom+ "> <http://www.w3.org/1999/02/22-rdf-syntax-ns#type> <http://ontology.ontotext.com/symptom> ." +"\n")


continent_set = set(continent_list)

for cont in continent_set:
   ntwrite.write("<http://ontology.ontotext.com/" + cont+ "> <http://www.w3.org/1999/02/22-rdf-syntax-ns#type> <http://ontology.ontotext.com/continent> ." +"\n") 


f.close()
ntwrite.close()