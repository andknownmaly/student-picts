import os
import json
import requests
from zipfile import ZipFile
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor, as_completed
import time

ANGKATAN_LIST = ['19', '20', '21', '22', '23', '24']
MAIN_FOLDER = 'foto_mhs'
ZIP_NAME = 'foto_mhs.zip'
PRODI_JSON_PATH = 'prodi.json'
MAX_WORKERS = 40
REQUEST_TIMEOUT = 10
DELAY_BETWEEN_REQUESTS = 0.1


def read_json(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        return json.load(f)


def download_image(url, save_path):
    try:
        response = requests.get(url, timeout=REQUEST_TIMEOUT)
        if response.status_code == 200:
            with open(save_path, 'wb') as f:
                f.write(response.content)
            print(f"Downloaded: {save_path}")
            return True
        else:
            print(f"Failed (Status {response.status_code}): {url}")
            return False
    except Exception as e:
        print(f"Error downloading {url}: {e}")
        return False

def create_folder(path):
    Path(path).mkdir(parents=True, exist_ok=True)

def scrape_foto_mhs(prodi_data, angkatan_list, main_folder):
    create_folder(main_folder)
    
    download_tasks = []
    for angkatan in angkatan_list:
        angkatan_full = f"20{angkatan}"
        for prodi in prodi_data:
            kode_prodi = prodi['kode']
            nama_prodi = prodi['nama_prodi']
            prodi_folder = os.path.join(main_folder, nama_prodi.replace(" ", "_"))
            create_folder(prodi_folder)
            
            for nim_int in range(0, 10000):
                nim = f"{nim_int:04d}"
                url = f"https://fotomhs.amikom.ac.id/{angkatan_full}/{angkatan}_{kode_prodi}_{nim}.jpg"
                #url = f"https://cdn.forumasisten.or.id/asisten/image/{angkatan}.{kode_prodi}.{nim}"
                save_filename = f"{angkatan}.{kode_prodi}.{nim}.jpg"
                save_path = os.path.join(prodi_folder, save_filename)
                download_tasks.append((url, save_path))
    
    print(f"Total download tasks: {len(download_tasks)}")
    
    with ThreadPoolExecutor(max_workers=MAX_WORKERS) as executor:
        future_to_url = {executor.submit(download_image, url, path): url for url, path in download_tasks}
        for future in as_completed(future_to_url):
            url = future_to_url[future]
            try:
                future.result()
            except Exception as e:
                print(f"Error downloading {url}: {e}")
            time.sleep(DELAY_BETWEEN_REQUESTS)

def create_zip(folder_path, output_zip):
    with ZipFile(output_zip, 'w') as zipf:
        for root, dirs, files in os.walk(folder_path):
            for file in files:
                file_path = os.path.join(root, file)
                arcname = os.path.relpath(file_path, start=os.path.dirname(folder_path))
                zipf.write(file_path, arcname)
    print(f"ZIP created: {output_zip}")

def main():
    try:
        prodi_data = read_json(PRODI_JSON_PATH)
    except FileNotFoundError:
        print(f"File {PRODI_JSON_PATH} tidak ditemukan. Pastikan file tersebut ada di direktori yang sama dengan skrip.")
        return
    except json.JSONDecodeError as e:
        print(f"Error membaca {PRODI_JSON_PATH}: {e}")
        return
    
    start_time = time.time()
    scrape_foto_mhs(prodi_data, ANGKATAN_LIST, MAIN_FOLDER)
    end_time = time.time()
    print(f"Scraping selesai dalam {end_time - start_time:.2f} detik.")
    
    create_zip(MAIN_FOLDER, ZIP_NAME)

if __name__ == "__main__":
    main()
