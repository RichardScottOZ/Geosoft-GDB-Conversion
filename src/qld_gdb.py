"""
Download GeoSoft GDB files from the GSQ Open Data Portal.
Limits downloads to files smaller than 1 GB.
"""
import requests
import json
import os
import subprocess
import time
import re
from urllib import parse
from pathlib import Path

HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0.0.0 Safari/537.36'
}

CKAN_URL = 'https://geoscience.data.qld.gov.au/api/action/'
DATA_DIR = 'data/qld'
MAX_SIZE_MB = 1000  # Skip files larger than 1 GB

def search_gdb_datasets():
    """Search for all datasets containing GDB resources using fq=res_format:gdb"""
    query = CKAN_URL + 'package_search?fq=res_format:gdb&rows=1000'
    
    response = requests.get(query, headers=HEADERS)
    json_response = json.loads(response.text)
    total_results = json_response['result']['count']
    print(f"Total search results for format:gdb: {total_results}")

    getloop = int(total_results / 1000) + 1
    dataset_names = set()

    for i in range(getloop):
        loopq = query + "&start=" + str(i * 1000)
        response = requests.get(loopq, headers=HEADERS)
        for dataset in response.json()['result']['results']:
            dataset_names.add(dataset.get('name', ''))

    return sorted(dataset_names)

def download_with_powershell(url, dest_path, timeout_secs=600):
    ps_url = url.replace("'", "''")
    ps_dest = dest_path.replace("'", "''")
    ps_script = f"""
$url = '{ps_url}'
$dest = '{ps_dest}'
$headers = @{{
    "User-Agent" = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0.0.0 Safari/537.36"
    "Accept" = "*/*"
    "Upgrade-Insecure-Requests" = "1"
}}
try {{
    Invoke-WebRequest -Uri $url -Headers $headers -OutFile $dest -UseBasicParsing
    $size = (Get-Item $dest).Length
    Write-Host "OK:$size"
}} catch {{
    Write-Host "FAIL:$($_.Exception.Message)"
}}
"""
    result = subprocess.run(
        ['powershell', '-NoProfile', '-Command', ps_script],
        capture_output=True, text=True, timeout=timeout_secs
    )
    output = (result.stdout + result.stderr).strip()
    if output.startswith('OK:'):
        return True, int(output.split(':')[1])
    return False, output

def main():
    Path(DATA_DIR).mkdir(parents=True, exist_ok=True)
    dataset_names = search_gdb_datasets()
    
    downloaded_count = 0
    # Just grab the first few small ones for reverse engineering
    TARGET_DOWNLOADS = 10 

    for dataset_name in dataset_names:
        if downloaded_count >= TARGET_DOWNLOADS:
            break
            
        response = requests.get(CKAN_URL + 'package_show', dict(id=dataset_name), headers=HEADERS)
        if not response.ok: continue
        
        content = response.json().get('result', {})
        for resource in content.get('resources', []):
            res_format = resource.get('resource:format', '') or resource.get('format', '')
            res_name = resource.get('name', '') or resource.get('resource:name', '')
            
            if not (res_format.upper() == 'GDB' or res_name.upper().endswith('.GDB')):
                continue
                
            size = resource.get('resource:size', resource.get('size', 0))
            try:
                # Some sizes are strings like '1.5 MB', some are bytes in ints
                if isinstance(size, str):
                    if 'GB' in size.upper():
                        size_mb = float(size.upper().replace('GB','').strip()) * 1024
                    elif 'MB' in size.upper():
                        size_mb = float(size.upper().replace('MB','').strip())
                    elif 'KB' in size.upper():
                        size_mb = float(size.upper().replace('KB','').strip()) / 1024
                    else:
                        size_mb = float(size.strip()) / (1024*1024)
                else:
                    size_mb = size / (1024 * 1024)
            except:
                size_mb = 0
                
            if size_mb > MAX_SIZE_MB:
                print(f"Skipping {res_name} (Too large: {size_mb:.1f} MB)")
                continue

            filename = resource.get('url', '')
            while '%2' in filename:
                filename = parse.unquote_plus(filename)
            filename = os.path.basename(filename)
            if not filename:
                filename = res_name + '.gdb'
            filename = re.sub(r'[<>:"|?*]', '_', filename)
            
            download_link = resource.get('download_url') or resource.get('url')
            if not download_link: continue
            
            dest_path = os.path.join(DATA_DIR, filename)
            if os.path.exists(dest_path) and os.path.getsize(dest_path) > 1000:
                print(f'Already have {filename}')
                continue
                
            print(f'Downloading {filename} ({size_mb:.1f} MB)...')
            ok, result = download_with_powershell(download_link, dest_path)
            if ok:
                print(f'  Success: {result:,} bytes')
                downloaded_count += 1
                if downloaded_count >= TARGET_DOWNLOADS:
                    break
            else:
                print(f'  Failed: {result}')

if __name__ == '__main__':
    main()
