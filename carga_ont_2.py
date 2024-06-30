'''
Created on 19 Jan 2021

@author: ejimenez-ruiz
'''
from owlready2 import *
from rdflib import Graph

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
    
    # Listas para almacenar resultados
    classes_list = []
    data_properties_list = []
    object_properties_list = []
    individuals_list = []

    # Obtener clases
    classes = getClasses(onto)
    print("Classes in Ontology: " + str(len(classes)))
    for cls in classes:
        class_info = {
            "iri": cls.iri,
            "name": cls.name,
            "labels": getRDFSLabelsForEntity(cls)
        }
        classes_list.append(class_info)
    
    # Obtener propiedades de datos
    data_properties = getDataProperties(onto)
    for dp in data_properties:
        data_property_info = {
            "iri": dp.iri,
            "name": dp.name,
            "labels": getRDFSLabelsForEntity(dp)
        }
        data_properties_list.append(data_property_info)
    
    # Obtener propiedades de objeto
    object_properties = getObjectProperties(onto)
    for op in object_properties:
        object_property_info = {
            "iri": op.iri,
            "name": op.name,
            "labels": getRDFSLabelsForEntity(op)
        }
        object_properties_list.append(object_property_info)
    
    # Obtener individuos
    individuals = getIndividuals(onto)
    for ind in individuals:
        individual_info = {
            "iri": ind.iri,
            "name": ind.name,
            "labels": getRDFSLabelsForEntity(ind)
        }
        individuals_list.append(individual_info)

    return classes_list, data_properties_list, object_properties_list, individuals_list

# Cargar ontología desde URI o archivo local
urionto = "data/cmt.owl"
# urionto = "data/ekaw.owl"
# urionto = "data/confOf.owl"
# urionto = "data/human.owl"
# urionto = "data/mouse.owl"

classes_list, data_properties_list, object_properties_list, individuals_list = loadOntology(urionto)

# Puedes verificar los resultados de la siguiente manera
print("Classes List:", classes_list)
print("Data Properties List:", data_properties_list)
print("Object Properties List:", object_properties_list)
print("Individuals List:", individuals_list)
