import requests
import json
import services.common.vars as vars
import services.common.tools as tools

def search(args):
    data = {}
    # If a specific pathway is given

    if 'identifier' in args.keys():
        org = 'map'
        if 'organism' in args.keys():
            org = args['organism']
        # If the pathway given is not actually a pathway, raise an exception
        if not tools.valid_pathway_id(args['identifier']):
            raise Exception('Not a valid identifier')        
        id = org + args['identifier']

        # If a field of the specific pathway is requested
        if 'field' in args.keys():
            url = vars.url + 'get/' + id
            text = tools.openurl(url)
            arr = tools.find_cat(text, args['field'])

            data = arr
        # No field is specified
        else:
            url = vars.url + 'list/' + id
            text = tools.openurl(url)
            data = tools.two_col_path(text, org if org != 'map' else '')
    elif 'term' in args.keys():
        term = args['term']
        if 'organism' not in args.keys():
            url = vars.url + 'find/pathway/' + term
            text = tools.openurl(url)
            data = tools.two_col_path(text, '')
        else:
            org = args['organism']
            url = vars.url + 'find/pathway/' + term
            text = tools.openurl(url)
            tempdata = tools.two_col_path(text, '')
            url2 = vars.url + 'list/pathway/' + org
            text2 = tools.openurl(url2)
            data2 = []
            lines = text2.split('\n')
            for line in lines:
                parts = line.split(vars.delimiter, 1);
                if len(parts) == 2:
                    data2.append(parts[0][8:])

            data = []
            for element in tempdata:
                if element['KEGG_pathway_id'] in data2:
                    data.append(element)
                        



    # No pathway is specified. Lists all pathways in Arabidopsis
    else:
        org = ''
        if 'organism' in args.keys():
                org = args['organism']
                
        url = vars.url + 'list/pathway/' + org
        text = tools.openurl(url)
        data = tools.two_col_path(text, org)
               

    print json.dumps(data)
