import os
import sys
import shutil
from subprocess import call
import logging
import pdb
import argparse
import json

#sys.path.insert(1, os.path.dirname(shutil.which('xtract')))
#import edirect

LOGLEVEL = os.environ.get('LOGLEVEL', 'INFO').upper()
logging.basicConfig(filename='log.txt',level=LOGLEVEL)

def extract_data_from_xml(data, raw_data_output):
    xtract_str = f"""xtract -input {data} -pattern PubmedArticle -sep " "\
                 -element MedlineCitation/PMID ArticleTitle \
                 AbstractText >> {raw_data_output}"""
       
    #formatted_data = edirect.execute(xtract_str)
    call(xtract_str,shell=True)
    logging.debug(xtract_str)


def read_formatted_data(data_path):
    with open(data_path,'r') as fil:
        data = fil.readlines()
    return data


def get_data_path(query):
    query_id, query_str = query.split(',')
    query_id = query_id.strip()
    query_str = query_str.strip()
    formatted_query_str = query_str.replace(' ','_')

    raw_data_path = f'raw/{formatted_query_str}.xml'
    formatted_data_dir = f'cleaned/{query_id}'
    if not os.path.exists(formatted_data_dir):
        os.makedirs(formatted_data_dir)
    formatted_data_path = f'{formatted_data_dir}/{formatted_query_str}.txt'
    if os.path.exists(formatted_data_path):
        os.remove(formatted_data_path)
    return raw_data_path, formatted_data_path


def format_data_to_trec(query, data):
    #output format: queryid#docid_textfield
    query_id, query_str = query.split(',')
 
    trec_list = list()
    json_list = list()
    for doc in data:
        splitted_doc = doc.strip().split('\t')
        try:
            doc_id, doc_title, doc_abstract = splitted_doc

            trec_title = f'{query_id}#{doc_id}_title\t{query_str}\t{doc_title}'
            trec_abstract = f'{query_id}#{doc_id}_abstract\t{query_str}\t{doc_abstract}'
            trec_list.append(trec_title)
            trec_list.append(trec_abstract)

            json_content = f"{doc_title}\n{doc_abstract}"
            json_list.append({ "id":f'{doc_id}', "contents":json_content })

        except:
            try:
                doc_id, doc_title = splitted_doc
                trec_title = f'{query_id}#{doc_id}_title\t{query_str}\t{doc_title}'
                trec_list.append(trec_title)

                json_content = f"{doc_title}\n "
                json_list.append({ "id":f'{doc_id}', "contents":json_content })

            except:
                logging.info(f'Missing field at document:\n{splitted_doc}')

    return trec_list, json_list
       

def save_trec_data_to_file(trec_data, trec_output_path):
    with open(trec_output_path, 'w') as f:
        for item in trec_data:
            it = item.replace('\n','')
            f.write(f"{it}\n")


def save_json_data_to_file(json_data, json_output_path):
    with open(json_output_path, 'w') as f:
        for item in json_data:
            f.write(json.dumps(item) + "\n")


if __name__=='__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('query_list', type=str, help='''a list of query data, 
                                                     e.g.: 01,sample''')
    args = parser.parse_args()
    output_filename = 'pubmed'

    with open(args.query_list,'r') as fil:
        query_data = fil.readlines()

    trec_data_list = list()
    json_data_list = list()
    for query in query_data:
        logging.info(f'formatting data from query: {query}')
        raw_data_path, formatted_data_path = get_data_path(query)
        extract_data_from_xml(raw_data_path, formatted_data_path)

        logging.info(f'converting data to trec')
        formatted_data = read_formatted_data(formatted_data_path)
        trec_data, json_data = format_data_to_trec(query, formatted_data)
        trec_data_list.append(trec_data)
        json_data_list.append(json_data)

    trec_data = [i for item in trec_data_list for i in item]
    trec_output_path = f'trec/{output_filename}'
    save_trec_data_to_file(trec_data, trec_output_path)

    json_data = [i for item in json_data_list for i in item]
    json_output_path = f'json/{output_filename}.json'
    save_json_data_to_file(json_data, json_output_path)
