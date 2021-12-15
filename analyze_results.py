import sys
import os
import argparse
import pdb

def format_pred_data(data, max_samples):
    data_list = list()

    for item in data[:max_samples]:
        query_id, _, doc_id, position, pred, _, doc_type = item.split('\t')

        data_dict = dict()
        data_dict['query_id'] = query_id
        data_dict['doc_id'] = doc_id
        data_dict['pred'] = pred
        data_dict['doc_type'] = doc_type.strip()

        data_list.append(data_dict)
    return data_list


def format_document_data(data):
    data_list = list()

    for item in data:
        query_doc_id, query_title, doc_str = item.split('\t')
        query_id, doc_type = query_doc_id.split('#')

        data_dict = dict()
        data_dict['query_id'] = query_id
        data_dict['query_title'] = query_title
        data_dict['doc_type'] = doc_type.strip()
        data_dict['doc_str'] = doc_str.strip()

        data_list.append(data_dict)
    return data_list


def save_results(output_list, output_file):
    with open(f'{output_file}.txt','w') as f:
        for item in output_list:
            item_str = '\t'.join(item.values())
            f.write(f'{item_str}\n')


def match_results(formatted_pred, formatted_document):
    output_list = list()

    for pred in formatted_pred:
        output_dict = dict()
        for document in formatted_document:
            if pred['doc_type'] == document['doc_type']:
                output_dict.update(pred)
                output_dict.update(document)
                output_list.append(output_dict)
                break

    return output_list


if __name__=='__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('pred', type=str,
                        help='''IR output prediction in trec  format''')
    parser.add_argument('documents', type=str, help='''documents''')
    parser.add_argument('output_file', type=str, help='''output file''')
    parser.add_argument('max_samples', type=int, help='''n document samples''')
    parser.add_argument('--type', type=str, help='''get worst predictions if
        worst argument is passed''')
    args = parser.parse_args()

    pred_file = args.pred
    document_file = args.documents
    max_samples = args.max_samples
    output_file = args.output_file
    sort_type = args.type

    with open(pred_file,'r') as fil:
        pred_data = fil.readlines()

    with open(document_file,'r') as fil:
        document_data = fil.readlines()

    if sort_type == 'worst':
        pred_data = pred_data[::-1]

    formatted_pred = format_pred_data(pred_data, max_samples)
    formatted_document = format_document_data(document_data)

    output_list = match_results(formatted_pred, formatted_document)
    save_results(output_list, output_file)
