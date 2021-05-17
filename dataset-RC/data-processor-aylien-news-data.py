import json
import geonamescache

ID_counter = 0

gc = geonamescache.GeonamesCache()
countries = gc.get_countries()

def gen_dict_extract(var, key):
    if isinstance(var, dict):
        for k, v in var.items():
            if k == key:
                yield v
            if isinstance(v, (dict, list)):
                yield from gen_dict_extract(v, key)
    elif isinstance(var, list):
        for d in var:
            yield from gen_dict_extract(d, key)
            
countries = [*gen_dict_extract(countries, 'name')]



def get_data_from_jsonl(line):
    global ID_counter
    parsed = json.loads(line)
    ID_counter += 1
    location = ''
    symptoms = ''
    
    for i in parsed['entities']['body']:
        if 'Country' in i['types'] or 'State' in i['types'] or 'Location' in i['types'] or 'Place' in i['types'] or 'PopulatedPlace' in i['types'] or 'City' in i['types'] :
            if i['text'] in countries:
                location += str(i['text']) + '; '
                # print(i['text'], '==>', i['types'])
        
        if 'Disease' in i['types']:
            symptoms += str(i['text']) + '; '
            # print(i['text'], '==>', i['types'])
    
    fwrite.write(str(ID_counter) + "\t" + location + "\t" + symptoms  + "\t" + str(parsed['source']['domain']) + "\t" + str(parsed['published_at']) + "\n")
    # fwrite.write(str(ID_counter) + "\t" + location + "\t" + symptoms + "\t" + str(parsed['source']['domain']) + "\t" + str(parsed['links']['permalink']) + "\n")
    print("Processed News Item: ==>", ID_counter)
    # print(location)
    # print(symptoms)
    # print(parsed['source']['domain'])
    # print(parsed['links']['permalink'])
    


fwrite = open("Newsdata-filtered-with-pub-date-domain.tsv", "a+", encoding="utf-8")
# fwrite.write("ID" + "\t" + "Location" + "\t" + "Symptoms" + "\t" + "Domain" + "\t" + "News Link" + "\n")

f = open('aylien_covid_news_data.jsonl','r',encoding='utf-8')
for lines in f:
    get_data_from_jsonl(lines)

fwrite.close()