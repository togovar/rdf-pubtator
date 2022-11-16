# _*_ coding: utf-8 _*_

import os
import sys
import re
import argparse
import gzip
from rdflib import Namespace, URIRef, Graph, BNode, Literal
from rdflib.namespace import RDF, RDFS

# make rdf file

ns_oa       = Namespace("http://www.w3.org/ns/oa#")
ns_dcterms  = Namespace("http://purl.org/dc/terms/")
ns_pubmed   = Namespace("http://rdf.ncbi.nlm.nih.gov/pubmed/")
ns_dbsnp    = Namespace("http://identifiers.org/dbsnp/")
ns_ncbigene = Namespace("http://identifiers.org/ncbigene/")
ns_mesh     = Namespace("http://id.nlm.nih.gov/mesh/")
ns_omim     = Namespace("http://identifiers.org/omim/")
ns_subj     = Namespace("http://purl.jp/bio/10/pubtator-central/Gene/")

def init_graph():

    g = Graph()
    g.bind('oa', ns_oa)
    g.bind('dcterms', ns_dcterms)
    g.bind('pubmed', ns_pubmed)
    g.bind('dbsnp', ns_dbsnp)
    g.bind('ncbigene', ns_ncbigene)
    g.bind('mesh', ns_mesh)
    g.bind('omim', ns_omim)
    g.bind('pc', ns_subj)

    return(g)

def make_rdf(start_number, step_count, inputfile, out_format):

    file_name, file_extension = os.path.splitext(inputfile)
    try:
      if(file_extension == ".gz"):
        f = gzip.open(inputfile, 'rt')
      elif(file_name == ""):
        f = sys.stdin
      else:
        f = open(inputfile)
    except FileNotFoundError:
      sys.stderr.write("Couldn't open the file:" + inputfile + "\n")
      exit(-1)

    row_num = start_number
    count = 0

    for line in f.readlines():
        if(count == 0):
            g = init_graph()
        elif(count == step_count):
            count = 0
            sys.stdout.write(g.serialize(format=out_format).decode('utf-8'))
            g = init_graph()

        row = line.rstrip('\n').split('\t')
        #print(str(row))
        pmid      = row[0]
        rtype     = row[1]
        ncbi_gene = row[2]
        list_gene = ncbi_gene.split(';')
        mention   = row[3]
        list_mention = mention.split('|')
        resource  = row[4]        
        list_resource = resource.split('|')

        # skip header
        if pmid == "PMID":
            continue

        # skip non rs number
        match = re.match(r'^[0-9;]+$|None', ncbi_gene)
        if not match:
            print('Error: "' + ncbi_gene + '" is not match RS number format', file=sys.stderr)
            continue

        subject = URIRef(ns_subj + str(row_num))

        g.add( (subject, RDF.type, URIRef(ns_oa.Annotation)) )
        for mention in list_mention:
            g.add( (subject, RDFS.label, Literal(mention)) )
        g.add( (subject, URIRef(ns_dcterms + 'subject'), Literal(rtype)) )
        g.add( (subject, URIRef(ns_oa.hasTarget), URIRef(ns_pubmed + pmid)) )
        for gene in list_gene:
            g.add( (subject, URIRef(ns_oa.hasBody), URIRef(ns_ncbigene + gene)) )
        for s in list_resource:
            g.add( (subject, URIRef(ns_dcterms.source), Literal(s)) )

        row_num = row_num + 1
        count = count + 1

    f.close()
    if(count > 0):
        sys.stdout.write(g.serialize(format=out_format).decode('utf-8'))

    return

# main
if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description='--start <start id:int> --step <step count:int> --format <turtle or ntriples, default=turtle> <input file ("-" is STDIN)>')
    parser.add_argument('-s', '--start', type=int, default=0)
    parser.add_argument('-t', '--step', type=int, default=1000)
    parser.add_argument('-f', '--format', type=str, default="turtle")
    parser.add_argument('file', nargs='?')
    args = parser.parse_args()
#    print(args)
    if (args.file == None):
        inputfile = ""
    elif(args.file == "-"):
        inputfile = ""
    else:
        inputfile = args.file

    make_rdf(args.start, args.step, inputfile, args.format)