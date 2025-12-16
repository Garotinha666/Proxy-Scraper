import requests
from bs4 import BeautifulSoup
import concurrent.futures
from colorama import Fore, Style, init
import time

init(autoreset=True)

class ProxyScraper:
    def __init__(self):
        self.proxies = []
        self.working_proxies = []
        
    def print_banner(self):
        banner = f"""
{Fore.CYAN}╔═══════════════════════════════════════╗
║       PROXY SCRAPER & TESTER          ║
║          Free Proxies 🌐              ║
╚═══════════════════════════════════════╝{Style.RESET_ALL}
"""
        print(banner)
    
    def scrape_free_proxy_list(self):
        """Scrape de free-proxy-list.net"""
        try:
            print(f"{Fore.YELLOW}[*] Buscando proxies em free-proxy-list.net...{Style.RESET_ALL}")
            url = "https://free-proxy-list.net/"
            response = requests.get(url, timeout=10)
            soup = BeautifulSoup(response.content, 'html.parser')
            
            table = soup.find('table', {'class': 'table table-striped table-bordered'})
            if table:
                rows = table.find('tbody').find_all('tr')
                for row in rows:
                    cols = row.find_all('td')
                    if len(cols) >= 7:
                        ip = cols[0].text.strip()
                        port = cols[1].text.strip()
                        https = cols[6].text.strip()
                        
                        if https == 'yes':
                            self.proxies.append(f"{ip}:{port}")
                
                print(f"{Fore.GREEN}[✓] {len(self.proxies)} proxies encontrados{Style.RESET_ALL}")
        except Exception as e:
            print(f"{Fore.RED}[✗] Erro: {e}{Style.RESET_ALL}")
    
    def scrape_proxyscrape(self):
        """Scrape de proxyscrape.com API"""
        try:
            print(f"{Fore.YELLOW}[*] Buscando proxies em proxyscrape.com...{Style.RESET_ALL}")
            url = "https://api.proxyscrape.com/v2/?request=get&protocol=http&timeout=10000&country=all&ssl=all&anonymity=all"
            response = requests.get(url, timeout=10)
            
            if response.status_code == 200:
                proxies_list = response.text.strip().split('\n')
                initial_count = len(self.proxies)
                self.proxies.extend([p.strip() for p in proxies_list if p.strip()])
                new_count = len(self.proxies) - initial_count
                print(f"{Fore.GREEN}[✓] {new_count} proxies encontrados{Style.RESET_ALL}")
        except Exception as e:
            print(f"{Fore.RED}[✗] Erro: {e}{Style.RESET_ALL}")
    
    def scrape_geonode(self):
        """Scrape de geonode.com API"""
        try:
            print(f"{Fore.YELLOW}[*] Buscando proxies em geonode.com...{Style.RESET_ALL}")
            url = "https://proxylist.geonode.com/api/proxy-list?limit=500&page=1&sort_by=lastChecked&sort_type=desc&protocols=http%2Chttps"
            response = requests.get(url, timeout=10)
            
            if response.status_code == 200:
                data = response.json()
                initial_count = len(self.proxies)
                for proxy in data.get('data', []):
                    ip = proxy.get('ip')
                    port = proxy.get('port')
                    if ip and port:
                        self.proxies.append(f"{ip}:{port}")
                new_count = len(self.proxies) - initial_count
                print(f"{Fore.GREEN}[✓] {new_count} proxies encontrados{Style.RESET_ALL}")
        except Exception as e:
            print(f"{Fore.RED}[✗] Erro: {e}{Style.RESET_ALL}")
    
    def scrape_pubproxy(self):
        """Scrape de pubproxy.com API"""
        try:
            print(f"{Fore.YELLOW}[*] Buscando proxies em pubproxy.com...{Style.RESET_ALL}")
            initial_count = len(self.proxies)
            
            for _ in range(5):  # 5 requests = ~25 proxies
                url = "http://pubproxy.com/api/proxy?limit=5&format=txt&type=http"
                response = requests.get(url, timeout=10)
                if response.status_code == 200:
                    proxies_list = response.text.strip().split('\n')
                    self.proxies.extend([p.strip() for p in proxies_list if p.strip()])
                time.sleep(0.5)
            
            new_count = len(self.proxies) - initial_count
            print(f"{Fore.GREEN}[✓] {new_count} proxies encontrados{Style.RESET_ALL}")
        except Exception as e:
            print(f"{Fore.RED}[✗] Erro: {e}{Style.RESET_ALL}")
    
    def test_proxy(self, proxy):
        """Testa se o proxy funciona com a API da Riot"""
        try:
            proxies = {
                'http': f'http://{proxy}',
                'https': f'http://{proxy}'
            }
            
            # Testa com a API da Riot (mais realista)
            response = requests.get(
                'https://auth.riotgames.com/api/v1/authorization',
                proxies=proxies,
                timeout=10,
                verify=False
            )
            
            # Se chegou até aqui sem erro, proxy funciona
            if response.status_code in [200, 400, 404, 405]:
                return True
        except:
            pass
        
        return False
    
    def test_all_proxies(self, max_workers=50):
        """Testa todos os proxies em paralelo"""
        print(f"\n{Fore.CYAN}[*] Testando {len(self.proxies)} proxies...{Style.RESET_ALL}")
        print(f"{Fore.CYAN}[*] Threads: {max_workers}{Style.RESET_ALL}\n")
        
        tested = 0
        start_time = time.time()
        
        with concurrent.futures.ThreadPoolExecutor(max_workers=max_workers) as executor:
            future_to_proxy = {executor.submit(self.test_proxy, proxy): proxy for proxy in self.proxies}
            
            for future in concurrent.futures.as_completed(future_to_proxy):
                proxy = future_to_proxy[future]
                tested += 1
                
                try:
                    if future.result():
                        self.working_proxies.append(proxy)
                        print(f"{Fore.GREEN}[✓] {proxy} - FUNCIONANDO ({len(self.working_proxies)} válidos){Style.RESET_ALL}")
                    else:
                        print(f"{Fore.RED}[✗] {proxy} - FALHOU{Style.RESET_ALL}", end='\r')
                except:
                    print(f"{Fore.RED}[✗] {proxy} - ERRO{Style.RESET_ALL}", end='\r')
                
                # Progress
                if tested % 10 == 0:
                    elapsed = time.time() - start_time
                    speed = tested / elapsed
                    remaining = len(self.proxies) - tested
                    eta = remaining / speed if speed > 0 else 0
                    print(f"{Fore.CYAN}[{tested}/{len(self.proxies)}] Válidos: {len(self.working_proxies)} | ETA: {eta:.0f}s{Style.RESET_ALL}", end='\r')
    
    def save_proxies(self, filename='proxies.txt'):
        """Salva proxies funcionando em arquivo"""
        try:
            with open(filename, 'w', encoding='utf-8') as f:
                for proxy in self.working_proxies:
                    f.write(proxy + '\n')
            print(f"\n{Fore.GREEN}[✓] {len(self.working_proxies)} proxies salvos em '{filename}'{Style.RESET_ALL}")
        except Exception as e:
            print(f"{Fore.RED}[✗] Erro ao salvar: {e}{Style.RESET_ALL}")
    
    def run(self):
        """Executa o scraper"""
        self.print_banner()
        
        print(f"{Fore.CYAN}Iniciando busca de proxies...\n{Style.RESET_ALL}")
        
        # Buscar de múltiplas fontes
        self.scrape_proxyscrape()
        time.sleep(1)
        self.scrape_geonode()
        time.sleep(1)
        self.scrape_free_proxy_list()
        time.sleep(1)
        self.scrape_pubproxy()
        
        # Remover duplicatas
        self.proxies = list(set(self.proxies))
        
        print(f"\n{Fore.GREEN}[✓] Total de proxies coletados: {len(self.proxies)}{Style.RESET_ALL}\n")
        
        if len(self.proxies) == 0:
            print(f"{Fore.RED}[✗] Nenhum proxy encontrado!{Style.RESET_ALL}")
            return
        
        # Testar proxies
        test = input(f"{Fore.CYAN}Testar proxies agora? (s/n): {Style.RESET_ALL}").strip().lower()
        
        if test == 's':
            threads = input(f"{Fore.CYAN}Threads para teste (padrão 50): {Style.RESET_ALL}").strip()
            threads = int(threads) if threads else 50
            
            self.test_all_proxies(max_workers=threads)
            
            print(f"\n{Fore.CYAN}{'='*50}")
            print(f"RESULTADO:")
            print(f"Total testados: {len(self.proxies)}")
            print(f"Funcionando: {Fore.GREEN}{len(self.working_proxies)}{Style.RESET_ALL}")
            print(f"Taxa de sucesso: {(len(self.working_proxies)/len(self.proxies)*100):.1f}%")
            print(f"{'='*50}{Style.RESET_ALL}\n")
            
            if self.working_proxies:
                self.save_proxies()
            else:
                print(f"{Fore.RED}[✗] Nenhum proxy funcionando encontrado!{Style.RESET_ALL}")
        else:
            # Salvar sem testar
            self.working_proxies = self.proxies
            self.save_proxies('proxies_untested.txt')
            print(f"{Fore.YELLOW}[!] Proxies salvos SEM teste em 'proxies_untested.txt'{Style.RESET_ALL}")

if __name__ == "__main__":
    scraper = ProxyScraper()
    scraper.run()
    
    input(f"\n{Fore.GREEN}Pressione ENTER para sair...{Style.RESET_ALL}")
