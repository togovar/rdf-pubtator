# _*_ coding: utf-8 _*_

import sys
import json
import re
import codecs
import csv
from rdflib import Namespace, URIRef, Graph, BNode, Literal
from rdflib.namespace import RDF, RDFS, FOAF

csv.field_size_limit(1000000000)


# make rdf file
def make_rdf(infile_pubtator, outfile_rdf):
    g = Graph()

    data        = Namespace("http://www.w3.org/ns/oa#")
    ns_oa       = Namespace("http://www.w3.org/ns/oa#")
    ns_dcterms  = Namespace("http://purl.org/dc/terms/")
    ns_pubmed   = Namespace("http://identifiers.org/pubmed/")
    ns_dbsnp    = Namespace("http://identifiers.org/dbsnp/")
    ns_ncbigene = Namespace("http://identifiers.org/ncbigene/")
    ns_mesh     = Namespace("http://id.nlm.nih.gov/mesh/")
    ns_omim     = Namespace("http://identifiers.org/omim/")
    
    g.bind('oa', ns_oa)
    g.bind('dcterms', ns_dcterms)
    g.bind('pubmed', ns_pubmed)
    g.bind('dbsnp', ns_dbsnp)
    g.bind('ncbigene', ns_ncbigene)
    g.bind('mesh', ns_mesh)
    g.bind('omim', ns_omim)


    fh_in = open(infile_pubtator, 'r')
    reader = csv.reader(fh_in, delimiter="\t")
    for row in reader:
        pmid      = row[0]
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

        blank = BNode()

        g.add( (blank, RDF.type, URIRef(ns_oa.Annotation)) )
        g.add( (blank, URIRef(ns_oa.hasTarget), URIRef(ns_pubmed + pmid)) )
        for gene in list_gene:
            g.add( (blank, URIRef(ns_oa.hasBody), URIRef(ns_ncbigene + gene)) )
        
        for s in list_resource:
            g.add( (blank, URIRef(ns_dcterms.source), Literal(s)) )
    
    # 
    g.serialize(destination=outfile_rdf, format='turtle')

    fh_in.close()
    return


# main
if __name__ == "__main__":
    params = sys.argv
    infile_pubtator  = params[1]
    outfile_rdf      = params[2]
    make_rdf(infile_pubtator, outfile_rdf)


