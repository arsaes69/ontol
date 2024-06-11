'''
Created on 19 Jan 2021

@author: ejimenez-ruiz

@Modified: Arturo Sáez Esteve on 20240611
@Ayuda: para encontrar equivalencias he hecho uso de ChatGPT, soy sincero.

'''

from owlready2 import *
from rdflib import Graph, Literal, RDF, URIRef, Namespace
from fuzzywuzzy import fuzz

def getClasses(onto):        
    return list(onto.classes())
    
def getDataProperties(onto):        
    return list(onto.data_properties())
    
def getObjectProperties(onto):        
    return list(onto.object_properties())
    
def getIndividuals(onto):    
    return list(onto.individuals())

def getRDFSLabelsForEntity(entity):
    return entity.label

def loadOntology(urionto):
    onto = get_ontology(urionto).load()
    return onto

def find_equivalencias(entities1, entities2, umbral=80):
    equivalencias = []
    for e1 in entities1:
        for e2 in entities2:
            label1 = e1.name.replace("_", " ")
            label2 = e2.name.replace("_", " ")
            similarity = fuzz.ratio(label1, label2)
            if similarity >= umbral:
                equivalencias.append((e1, e2))
    return equivalencias

def add_to_graph(g, equivalencias, rdf_type, predicate):
    for e1, e2 in equivalencias:
        entity1_uri = URIRef(e1.iri)
        entity2_uri = URIRef(e2.iri)
        g.add((entity1_uri, RDF.type, rdf_type))
        g.add((entity1_uri, predicate, entity2_uri))
        g.add((entity1_uri, Literal("name"), Literal(e1.name)))
        g.add((entity2_uri, Literal("name"), Literal(e2.name)))
        for label in getRDFSLabelsForEntity(e1):
            g.add((entity1_uri, URIRef("http://www.w3.org/2000/01/rdf-schema#label"), Literal(label)))
        for label in getRDFSLabelsForEntity(e2):
            g.add((entity2_uri, URIRef("http://www.w3.org/2000/01/rdf-schema#label"), Literal(label)))

# Cargo ontologías
#ontology1 = loadOntology("data/cmt.owl")
ontology1 = loadOntology("data/confOf.owl")
ontology2 = loadOntology("data/ekaw.owl")
#ontology2 = loadOntology("data/confOf.owl")


# Extraigo entidades
classes1 = getClasses(ontology1)
classes2 = getClasses(ontology2)
data_properties1 = getDataProperties(ontology1)
data_properties2 = getDataProperties(ontology2)
object_properties1 = getObjectProperties(ontology1)
object_properties2 = getObjectProperties(ontology2)
individuals1 = getIndividuals(ontology1)
individuals2 = getIndividuals(ontology2)

# Encuentro equivalencias con un umbral del 80%
class_equivalencias = find_equivalencias(classes1, classes2)
data_property_equivalencias = find_equivalencias(data_properties1, data_properties2)
object_property_equivalencias = find_equivalencias(object_properties1, object_properties2)
individual_equivalencias = find_equivalencias(individuals1, individuals2)

# Creo grafo RDF
g = Graph()
owl_ns = Namespace("http://www.w3.org/2002/07/owl#")
rdfs_ns = Namespace("http://www.w3.org/2000/01/rdf-schema#")

# Añadir equivalencias al grafo
add_to_graph(g, class_equivalencias, owl_ns.Class, owl_ns.equivalentClass)
add_to_graph(g, data_property_equivalencias, owl_ns.DatatypeProperty, owl_ns.equivalentProperty)
add_to_graph(g, object_property_equivalencias, owl_ns.ObjectProperty, owl_ns.equivalentProperty)
add_to_graph(g, individual_equivalencias, owl_ns.NamedIndividual, owl_ns.sameAs)

# Guardo grafo RDF en archivo Turtle
#g.serialize(destination="output/cmt-ekaw.ttl", format="turtle")
#g.serialize(destination="output/cmt-confOf.ttl", format="turtle")
g.serialize(destination="output/confOf-ekaw.ttl", format="turtle")