"""
Query the GSQ Open Data Portal API to find all GeoSoft GDB (Geodatabase) datasets.
Uses urllib (Python standard library) - no external dependencies.
"""
import urllib.request
import urllib.parse
import json

API_BASE = 'https://geoscience.data.qld.gov.au/api/3/action/'

def search_gdb_datasets(limit=1000, offset=0):
    """
    Search for datasets containing GDB resources.
    GDB (GeoSoft Geodatabase) format files.
    """
    # Try different query approaches
    
    # Approach 1: Search by format in query string
    print("Searching for GDB format resources...\n")
    
    params = urllib.parse.urlencode({
        'q': 'GDB',
        'rows': limit,
        'start': offset
    })
    
    url = f"{API_BASE}package_search?{params}"
    print(f"URL: {url}\n")
    
    try:
        with urllib.request.urlopen(url) as response:
            data = json.loads(response.read().decode())
            
            if data.get('success'):
                count = data['result']['count']
                datasets = data['result']['results']
                print(f"Found {count} search results for 'GDB'\n")
                
                gdb_datasets = []
                for ds in datasets:
                    # Find GDB resources in this dataset
                    gdb_resources = [r for r in ds.get('resources', []) 
                                   if r.get('resource:format', '').upper() == 'GDB']
                    
                    if gdb_resources:
                        gdb_datasets.append((ds, gdb_resources))
                
                print(f"Datasets with GDB resources: {len(gdb_datasets)}\n")
                
                for ds, gdb_resources in gdb_datasets:
                    print(f"Title: {ds.get('title', 'N/A')}")
                    print(f"  ID: {ds.get('id')}")
                    print(f"  Type: {ds.get('type')}")
                    print(f"  URL: https://geoscience.data.qld.gov.au/dataset/{ds.get('id')}")
                    
                    for r in gdb_resources:
                        print(f"  GDB Resource: {r.get('name')}")
                        print(f"    Size: {r.get('resource:size', 'N/A')} bytes")
                        print(f"    URL: {r.get('url')}")
                    print()
            else:
                print("API returned error:", data.get('error'))
    except urllib.error.HTTPError as e:
        print(f"HTTP Error {e.code}: {e.reason}")
        print(f"URL: {e.url}")
    except Exception as e:
        print(f"Error: {e}")

if __name__ == '__main__':
    search_gdb_datasets()