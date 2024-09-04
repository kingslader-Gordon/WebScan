from concurrent.futures import ThreadPoolExecutor, as_completed
import requests
from tqdm import tqdm


def File_Control():
    urls = set()
    with open('url.txt', 'r', encoding='utf-8') as f:
        for line in f:
            url = line.strip('\n')
            url = url.replace('http://', '')
            url = url.replace('https://', '')
            urls.add(url)
    return list(urls)


def Check_Url(url, client="https://"):
    req = client + url
    try:
        respone = requests.get(req, timeout=5)
        if 200 <= respone.status_code < 300:
            Result_File('200.txt', url)
        elif 300 <= respone.status_code < 400:
            Result_File('300.txt', url)
        elif 400 <= respone.status_code < 500:
            Result_File('400.txt', url)
        else:
            Result_File('500.txt', url)

    except requests.exceptions.RequestException as e:
        req = "https://" + url
        try:
            respone = requests.get(req, timeout=5)
            if 200 <= respone.status_code < 300:
                Result_File('200.txt', url)
            elif 300 <= respone.status_code < 400:
                Result_File('300.txt', url)
            elif 400 <= respone.status_code < 500:
                Result_File('400.txt', url)
            else:
                Result_File('500.txt', url)

        except requests.exceptions.RequestException as e:
            print(f"请求失败: {url}, 错误信息: {e}")
            return url, None

    return url, respone.status_code


def Result_File(filename, url):
    with open(filename, 'a+', encoding='utf-8') as f:
        f.write(url)
        f.write('\n')


def Threadings(urls):
    with ThreadPoolExecutor(max_workers=40) as executor:
        futures = [executor.submit(Check_Url, i) for i in urls]
        # print(type(urls), urls)
        for future in as_completed(futures):
            req_url, status = future.result()
            # print(f"req: {req_url}, status_code: {status}")


if __name__ == '__main__':
    urls = File_Control()
    for j in tqdm(range(0, len(urls), 40)):
        Threadings(urls=urls[j:j + 40])
