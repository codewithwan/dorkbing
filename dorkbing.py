import requests
from bs4 import BeautifulSoup as bsoup
from random import choice
import time
from colorama import Fore, Style, init

init(autoreset=True)

USER_AGENTS = [
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/118.0.0.0 Safari/537.36',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:89.0) Gecko/20100101 Firefox/89.0',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:90.0) Gecko/20100101 Firefox/90.0',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.131 Safari/537.36',
    'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:93.0) Gecko/20100101 Firefox/93.0'
]

def bing_search(query, page):
    base_url = 'https://www.bing.com/search'
    headers = {'User-Agent': choice(USER_AGENTS)}
    params = {'q': query, 'first': page * 10 + 1}
    try:
        resp = requests.get(base_url, params=params, headers=headers)
        resp.raise_for_status()
    except requests.RequestException as e:
        print(Fore.RED + f'Error fetching page {page + 1}: {e}')
        return []

    soup = bsoup(resp.text, 'html.parser')
    links = soup.find_all('a', href=True)
    result = []
    for link in links:
        href = link['href']
        if 'http' in href and not (href.startswith('https://www.bing.com') or
                                    href.startswith('http://go.microsoft.com') or
                                    href.startswith('https://go.microsoft.com') or
                                    href.startswith('https://support.microsoft.com')):
            result.append(href)
    return result

def print_banner():
    banner = """
██████╗  ██████╗ ██████╗ ██╗  ██╗        ██████╗ ██╗███╗   ██╗ ██████╗ 
██╔══██╗██╔═══██╗██╔══██╗██║ ██╔╝        ██╔══██╗██║████╗  ██║██╔════╝ 
██║  ██║██║   ██║██████╔╝█████╔╝         ██████╔╝██║██╔██╗ ██║██║  ███╗
██║  ██║██║   ██║██╔══██╗██╔═██╗         ██╔══██╗██║██║╚██╗██║██║   ██║
██████╔╝╚██████╔╝██║  ██║██║  ██╗███████╗██████╔╝██║██║ ╚████║╚██████╔╝
╚═════╝  ╚═════╝ ╚═╝  ╚═╝╚═╝  ╚═╝╚══════╝╚═════╝ ╚═╝╚═╝  ╚═══╝ ╚═════╝ 
                                                
                        Creator: @codewithwan
    """
    print(Fore.GREEN + banner)

def validate_input(pages, time_limit):
    if not pages.isdigit() or int(pages) <= 0:
        print(Fore.RED + "Invalid number of pages. Setting default value of 1.")
        return 1, None
    pages = int(pages)
    
    if time_limit and (not time_limit.isdigit() or int(time_limit) < 0):
        print(Fore.RED + "Invalid time limit. Setting no time limit.")
        return pages, None
    time_limit = int(time_limit) if time_limit else None
    return pages, time_limit

def main():
    print_banner()

    query = input(Fore.CYAN + '[>] Enter search query: ')
    pages = input(Fore.CYAN + '[>] Enter number of pages (default 1): ')
    output_file = input(Fore.CYAN + '[>] Enter output file name (example.txt): ')
    time_limit = input(Fore.CYAN + '[>] Enter time limit in seconds (press Enter if no limit): ')
    
    pages, time_limit = validate_input(pages, time_limit)

    all_results = []
    start_time = time.time()

    print(Fore.GREEN + f'[+] Starting Bing Dorking for query: "{query}"')

    for page in range(pages):
        if time_limit and (time.time() - start_time) > time_limit:
            print(Fore.YELLOW + "Time limit reached, stopping...")
            break

        results = bing_search(query, page)
        if results:
            all_results.extend(results)
            for url in results:
                print(Fore.BLUE + url)
        time.sleep(2)

    unique_results = list(set(all_results))

    if unique_results:
        with open(output_file, 'w') as f:
            for url in unique_results:
                f.write(url + '\n')
        print(Fore.GREEN + f'[-] Finished. Results saved to {output_file}')
    else:
        print(Fore.RED + 'No results found.')

    elapsed_time = time.time() - start_time
    print(Fore.GREEN + f'Total time taken: {elapsed_time:.2f} seconds')

if __name__ == '__main__':
    main()
