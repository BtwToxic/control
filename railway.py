import requests
from config import RAILWAY_API_KEY

API="https://backboard.railway.app/graphql/v2"
H={"Authorization":f"Bearer {RAILWAY_API_KEY}","Content-Type":"application/json"}

def q(query,v=None):
    r=requests.post(API,headers=H,json={"query":query,"variables":v or {}},timeout=8)
    return r.json()

def projects():
    return q("{projects{edges{node{id name}}}}")["data"]["projects"]["edges"]

def services(pid):
    return q("query($i:ID!){project(id:$i){services{edges{node{id name}}}}}",{"i":pid})["data"]["project"]["services"]["edges"]

def logs(sid):
    return q("query($i:ID!){service(id:$i){logs(limit:50)}}",{"i":sid})["data"]["service"]["logs"]

def metrics(sid):
    return q("query($i:ID!){service(id:$i){metrics{cpu memory}}}",{"i":sid})["data"]["service"]["metrics"]

def start(sid):
    q("mutation($i:ID!){serviceScale(serviceId:$i,replicas:1){id}}",{"i":sid})

def stop(sid):
    q("mutation($i:ID!){serviceScale(serviceId:$i,replicas:0){id}}",{"i":sid})

def restart(sid):
    q("mutation($i:ID!){serviceRedeploy(serviceId:$i){id}}",{"i":sid})
