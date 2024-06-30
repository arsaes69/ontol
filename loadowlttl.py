'''
Created on 19 Jan 2021

@author: ejimenez-ruiz
'''
from owlready2 import *
from rdflib import Graph, Literal, RDF, URIRef, Namespace

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
    # Método de owlready
    onto = get_ontology(urionto).load()
    
    # Crear un grafo RDF
    g = Graph()
    ex = Namespace("http://example.org/")
    g.bind("ex", ex)

    # Obtener clases
    classes = getClasses(onto)
    for cls in classes:
        class_uri = URIRef(cls.iri)
        g.add((class_uri, RDF.type, URIRef("http://www.w3.org/2002/07/owl#Class")))
        g.add((class_uri, ex.name, Literal(cls.name)))
        for label in getRDFSLabelsForEntity(cls):
            g.add((class_uri, URIRef("http://www.w3.org/2000/01/rdf-schema#label"), Literal(label)))
    
    # Obtener propiedades de datos
    data_properties = getDataProperties(onto)
    for dp in data_properties:
        data_property_uri = URIRef(dp.iri)
        g.add((data_property_uri, RDF.type, URIRef("http://www.w3.org/2002/07/owl#DatatypeProperty")))
        g.add((data_property_uri, ex.name, Literal(dp.name)))
        for label in getRDFSLabelsForEntity(dp):
            g.add((data_property_uri, URIRef("http://www.w3.org/2000/01/rdf-schema#label"), Literal(label)))
    
    # Obtener propiedades de objeto
    object_properties = getObjectProperties(onto)
    for op in object_properties:
        object_property_uri = URIRef(op.iri)
        g.add((object_property_uri, RDF.type, URIRef("http://www.w3.org/2002/07/owl#ObjectProperty")))
        g.add((object_property_uri, ex.name, Literal(op.name)))
        for label in getRDFSLabelsForEntity(op):
            g.add((object_property_uri, URIRef("http://www.w3.org/2000/01/rdf-schema#label"), Literal(label)))
    
    # Obtener individuos
    individuals = getIndividuals(onto)
    for ind in individuals:
        individual_uri = URIRef(ind.iri)
        g.add((individual_uri, RDF.type, URIRef("http://www.w3.org/2002/07/owl#NamedIndividual")))
        g.add((individual_uri, ex.name, Literal(ind.name)))
        for label in getRDFSLabelsForEntity(ind):
            g.add((individual_uri, URIRef("http://www.w3.org/2000/01/rdf-schema#label"), Literal(label)))

    # Guardar el grafo en un archivo Turtle
    g.serialize(destination="output/mouse.ttl", format="turtle")

# Cargar ontología desde URI o archivo local
# urionto = "data/cmt.owl"
# urionto = "data/ekaw.owl"
# urionto = "data/confOf.owl"
# urionto = "data/human.owl"
urionto = "data/mouse.owl"

loadOntology(urionto)
