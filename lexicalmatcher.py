from rdflib import Graph, Namespace, URIRef, RDF
from fuzzywuzzy import fuzz

def load_ontology(file_path):
    g = Graph()
    g.parse(file_path, format="turtle")
    return g

def extract_entities(graph):
    classes = set(graph.subjects(RDF.type, URIRef("http://www.w3.org/2002/07/owl#Class")))
    properties = set(graph.subjects(RDF.type, URIRef("http://www.w3.org/1999/02/22-rdf-syntax-ns#Property")))
    instances = set(graph.subjects(RDF.type, None)) - classes - properties
    return classes, properties, instances

def find_equivalences(entities1, entities2, umbral=80):
    equivalences = []
    for e1 in entities1:
        for e2 in entities2:
            label1 = e1.split("#")[-1].replace("_", " ")
            label2 = e2.split("#")[-1].replace("_", " ")
            similarity = fuzz.ratio(label1, label2)
            if similarity >= umbral:
                equivalences.append((e1, e2))
    return equivalences

def save_alignments(equivalences, file_path):
    g = Graph()
    for e1, e2 in equivalences:
        if str(e1).startswith("http://"):
            namespace1, local_name1 = str(e1).rsplit('#', 1)
        else:
            namespace1, local_name1 = str(e1).rsplit('/', 1)
        if str(e2).startswith("http://"):
            namespace2, local_name2 = str(e2).rsplit('#', 1)
        else:
            namespace2, local_name2 = str(e2).rsplit('/', 1)
        ns1 = Namespace(namespace1 + "#")
        ns2 = Namespace(namespace2 + "#")
        g.add((ns1[local_name1], URIRef("http://www.w3.org/2002/07/owl#equivalentClass"), ns2[local_name2]))
    g.serialize(destination=file_path, format="turtle")

# Load ontologies
ontology1 = load_ontology("data/cmt.owl")
ontology2 = load_ontology("data/ekaw.owl")

# Extract entities
classes1, properties1, instances1 = extract_entities(ontology1)
classes2, properties2, instances2 = extract_entities(ontology2)

# Find equivalences
class_equivalences = find_equivalences(classes1, classes2)
property_equivalences = find_equivalences(properties1, properties2)
instance_equivalences = find_equivalences(instances1, instances2)

# Save alignments
save_alignments(class_equivalences, "class_alignments.ttl")
save_alignments(property_equivalences, "property_alignments.ttl")
save_alignments(instance_equivalences, "instance_alignments.ttl")
