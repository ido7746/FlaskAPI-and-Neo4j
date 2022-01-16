from flask import Flask
from flask_restful import Api, Resource
from neo4j import GraphDatabase
import time
data = {
"Person" : [
{"name":"Ross", "age":"34", "gender":"Male"},
{"name":"Chandler", "age":"32", "gender":"Male"},
{"name":"Joey", "age":"32", "gender":"Male"},
{"name":"Phebe", "age":"31", "gender":"Female"},
{"name":"Monica", "age":"34", "gender":"Female"},
{"name":"Emma", "age":"1", "gender":"Female"},
{"name":"Rachel", "age":"32", "gender":"Female"},
],
"Apartment":[
    {"number":"19"},
    {"number":"20"}
],
"Sibiling":[
    ("Monica", "Ross"),
    ("Ross", "Monica")
],
"Parent_of":[
    ("Rachel","Emma"),
    ("Ross","Emma")
],
"Married_to":[
    ("Monica","Chandler"),
    ("Chandler","Monica")
],
"Lives_in":[
    ("Chandler","19"),
    ("Joey","19"),
    ("Monica","20"),
    ("Rachel","20"),
    ("Phebe","null"),
    ("Ross","null")
]
}

app = Flask(__name__)
api = Api(app)

#connect to neo4j
time.sleep(2)
graph = GraphDatabase.driver(uri = "bolt://neo4j:7687", auth = ("neo4j", "test"))



def loadData():
    session  = graph.session()
    #delete all the data
    session.run("match (a) -[r] -> () delete a, r")
    session.run("match (n) delete n")

    #insert data
    persons = data["Person"]
    for person in data["Person"]:
        session.run("CREATE (n:Person {name: '"+ person["name"] +"', age: "+person["age"]+" , gender:'"+person["gender"]+"'})")
    
    for apartment in data["Apartment"]:
        session.run("CREATE (n:Apartment {number:"+apartment["number"]+ "})")

    for sibiling in data["Sibiling"]:
        line1 = "match (a:Person) , (b:Person) "
        line2 = "where a.name='" + sibiling[0] + "' AND "+"b.name='"+sibiling[1] + "'"
        line3 = " create (a)-[sib:Sibiling]->(b)"
        session.run(line1+line2+line3)

    for parent in data["Parent_of"]:
        line1 = "match (a:Person) , (b:Person) "
        line2 = "where a.name='" + parent[0] + "' AND "+"b.name='"+parent[1] + "'"
        line3 = " create (a)-[par:Parent_of]->(b)"
        session.run(line1+line2+line3)

    for married in data["Married_to"]:
        line1 = "match (a:Person) , (b:Person) "
        line2 = "where a.name='" + married[0] + "' AND "+"b.name='"+married[1] + "'"
        line3 = " create (a)-[mar:Married_to]->(b)"
        session.run(line1+line2+line3)

    for lives in data["Lives_in"]:
        if lives[1]=="null":
            line1 = "match (a:Person) "
            line2 = "where a.name='" + lives[0] + "' "
            line3 = "create (b:Apartment{number:" + lives[1] +"}),"
            line4 = "(a)-[lives:Lives_in]->(b)"
            session.run(line1+line2+line3+line4)

        else:
            line1 = "match (a:Person), (b:Apartment)"
            line2 = "where a.name='" + lives[0] + "' AND  b.number="+lives[1]+" "
            line3 = "create (a)-[lives:Lives_in]->(b)"
            session.run(line1+line2+line3)
    session.close()
    print('------Load all the data!-------')


class FindByAddress(Resource):
    def get(self, number):
        session  = graph.session()
        line1 = "match (a:Person), (b:Apartment) "
        line2 = "where b.number=" + str(number) + " AND (a)-[:Lives_in]->(b) "
        line3 = "return a"
        data = session.run(line1+line2+line3).data()
        session.close()
        persons = [] #the list of the persons who live in apartment
        for p in data:#create list of the names
            persons.append(p['a']['name'])
        return persons

class FindAunt(Resource):
    def get(self):
        session  = graph.session()
        line1 = "match (aunt:Person), (kid:Person) "
        line2 = "where (aunt)-[:Sibiling]->(:Person)-[:Parent_of]->(kid) "
        line3 = "return aunt, kid"
        data = session.run(line1+line2+line3).data()
        session.close()
        return data


api.add_resource(FindByAddress, "/FindByAddress/<int:number>")
api.add_resource(FindAunt, "/FindAunt")


if __name__ == "__main__":
    #run the API server
    loadData()
    app.run(host='0.0.0.0',port=8000)
    