import os
import sys
import shutil
from subprocess import call
import logging
import pdb
import argparse

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
    return raw_data_path, formatted_data_path


def format_data_to_trec(query, data):
    #output format: queryid#docid_textfield
    query_id, query_str = query.split(',')
  
    trec_list = list()
    for doc in data:
        splitted_doc = doc.strip().split('\t')
        try:
            doc_id, doc_title, doc_abstract = splitted_doc
            trec_list.append(f'{query_id}#{doc_id}_title\t{query_str}\t{doc_title}')
            trec_list.append(f'{query_id}#{doc_id}_abstract\t{query_str}\t{doc_abstract}')
        except:
            try:
                doc_id, doc_title = splitted_doc
                trec_list.append(f'{query_id}#{doc_id}_title\t{query_str}\t{doc_title}')
            except:
                logging.info(f'Missing field at document:\n{splitted_doc}')

    return trec_list
       

def save_trec_data_to_file(trec_data, trec_output_path):
    with open(f'{trec_output_path}', 'w') as f:
        for item in trec_data:
            it = item.replace('\n','')
            f.write(f"{it}\n")


if __name__=='__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('query_list', type=str, help='''a list of query data, 
                                                     e.g.: 01,sample''')
    #parser.add_argument('output_filename', type=str, help='''output filename, 
    #                                    e.g.: formatted_data. The output is
    #                                    saved into trec/ folder by default ''')
    args = parser.parse_args()

    query_data_path = args.query_list
    #trec_output_filename = args.output_filename
    trec_output_filename = args.query_list

    with open(query_data_path,'r') as fil:
        query_data = fil.readlines()

    trec_data_list = list()
    for query in query_data:
        logging.info(f'formatting data from query: {query}')
        raw_data_path, formatted_data_path = get_data_path(query)
        extract_data_from_xml(raw_data_path, formatted_data_path)

        logging.info(f'converting data to trec')
        formatted_data = read_formatted_data(formatted_data_path)
        trec_data = format_data_to_trec(query, formatted_data)
        trec_data_list.append(trec_data)

    trec_data = [i for item in trec_data_list for i in item]
    trec_output_path = f'trec/{trec_output_filename}'
    save_trec_data_to_file(trec_data, trec_output_path)
