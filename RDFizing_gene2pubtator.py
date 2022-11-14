# _*_ coding: utf-8 _*_

import sys
import json
import re
import codecs
from rdflib import Namespace, URIRef, Graph, BNode, Literal
from rdflib.namespace import RDF, RDFS, FOAF

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

def make_rdf(start_number):

    row_num = start_number
    step = 10000
    count = 0

    for line in sys.stdin:
        if(count == 0):
            g = init_graph()
        elif(count == step):
            count = 0
            sys.stdout.write(g.serialize(format='ntriples').decode('ascii'))
            g = init_graph()

        row = line.rstrip('\n').split('\t')
        #print(str(row))
        pmid      = row[0]
        rtype     = row[1]
        ncbi_gene = row[2]
        list_gene = ncbi_gene.split(';')
        mention   = row[3]
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
        g.add( (subject, URIRef(ns_dcterms + 'subject'), Literal(rtype)) )
        g.add( (subject, URIRef(ns_oa.hasTarget), URIRef(ns_pubmed + pmid)) )
        for gene in list_gene:
            g.add( (subject, URIRef(ns_oa.hasBody), URIRef(ns_ncbigene + gene)) )

        for s in list_resource:
            g.add( (subject, URIRef(ns_dcterms.source), Literal(s)) )

        row_num = row_num + 1
        count = count + 1

    if(count > 0):
        sys.stdout.write(g.serialize(format='ntriples').decode('ascii'))
    return

# main
if __name__ == "__main__":
    params = sys.argv
    if len(params) == 2:
        start_number = params[1]
    else:
        start_number = 0
    make_rdf(start_number)