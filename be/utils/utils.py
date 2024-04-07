from concurrent.futures import ThreadPoolExecutor

from phashes import PERCEPTUAL_HASHES
import requests


def apply_phashes(image):
    # with ThreadPoolExecutor() as executor:
    #     futures = {
    #         k: executor.submit(PERCEPTUAL_HASHES[k], image) for k in PERCEPTUAL_HASHES
    #     }

    #     results = {}
    #     for k, future in futures.items():
    #         try:
    #             results[k] = future.result()
    #         except Exception as e:
    #             results[k] = f"Error: {str(e)}"

    #     return results
    return {hash: PERCEPTUAL_HASHES[hash](image) for hash in PERCEPTUAL_HASHES}


def download_file(url):
    """
    Download a file from a URL
    Return a buffer
    """
    response = requests.get(url)

    if response.status_code == 200:
        return response.content
    else:
        print(f"Failed to download file, {response.status_code} url: {url}")
        return None 
