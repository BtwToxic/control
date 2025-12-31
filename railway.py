import requests
from config import RAILWAY_API_KEY

API_URL = "https://backboard.railway.app/graphql/v2"

HEADERS = {
    "Authorization": f"Bearer {RAILWAY_API_KEY}",
    "Content-Type": "application/json"
}

def _query(query, variables=None):
    try:
        r = requests.post(
            API_URL,
            headers=HEADERS,
            json={
                "query": query,
                "variables": variables or {}
            },
            timeout=8
        )
        return r.json()
    except Exception as e:
        print("Railway API error:", e)
        return {}

# ================= PROJECTS =================

def list_projects():
    q = """
    {
      projects {
        edges {
          node {
            id
            name
          }
        }
      }
    }
    """
    return (
        _query(q)
        .get("data", {})
        .get("projects", {})
        .get("edges", [])
    )

# ================= SERVICES =================

def list_services(project_id):
    q = """
    query ($id: ID!) {
      project(id: $id) {
        services {
          edges {
            node {
              id
              name
            }
          }
        }
      }
    }
    """
    return (
        _query(q, {"id": project_id})
        .get("data", {})
        .get("project", {})
        .get("services", {})
        .get("edges", [])
    )

# ================= LOGS =================

def service_logs(service_id, limit=100):
    q = """
    query ($id: ID!) {
      service(id: $id) {
        logs(limit: %d)
      }
    }
    """ % limit

    return (
        _query(q, {"id": service_id})
        .get("data", {})
        .get("service", {})
        .get("logs", [])
    )

# ================= METRICS =================

def service_metrics(service_id):
    q = """
    query ($id: ID!) {
      service(id: $id) {
        metrics {
          cpu
          memory
        }
      }
    }
    """
    return (
        _query(q, {"id": service_id})
        .get("data", {})
        .get("service", {})
        .get("metrics", {})
    )

# ================= CONTROLS =================

def start_service(service_id):
    q = """
    mutation ($id: ID!) {
      serviceScale(serviceId: $id, replicas: 1) {
        id
      }
    }
    """
    _query(q, {"id": service_id})

def stop_service(service_id):
    q = """
    mutation ($id: ID!) {
      serviceScale(serviceId: $id, replicas: 0) {
        id
      }
    }
    """
    _query(q, {"id": service_id})

def restart_service(service_id):
    q = """
    mutation ($id: ID!) {
      serviceRedeploy(serviceId: $id) {
        id
      }
    }
    """
    _query(q, {"id": service_id})
