# 🌐 Proxy Scraper & Tester

Ferramenta automática para buscar e testar proxies HTTP/HTTPS gratuitos de múltiplas fontes. Ideal para projetos que necessitam de proxies válidos e funcionais.

## ✨ Características

- 🔍 **Busca em múltiplas fontes**: Coleta proxies de 4 fontes diferentes
- ⚡ **Teste paralelo**: Usa multithreading para testar centenas de proxies simultaneamente
- 🎯 **Validação realista**: Testa proxies usando a API da Riot Games
- 💾 **Salvamento automático**: Salva apenas proxies funcionais
- 📊 **Estatísticas em tempo real**: Mostra progresso, ETA e taxa de sucesso
- 🎨 **Interface colorida**: Output formatado e fácil de ler

## 📋 Requisitos

- Python 3.7 ou superior
- Conexão com internet

## 🚀 Instalação

### 1. Clone ou baixe este repositório

```bash
git clone <seu-repositorio>
cd <pasta-do-proxy-scraper>
```

### 2. Instale as dependências

```bash
pip install -r requirements.txt
```

## 💻 Uso

### Executar o script

```bash
python proxy_scraper.py
```

### Fluxo de uso

1. **O script inicia automaticamente** a busca de proxies em 4 fontes:
   - ProxyScrape.com
   - Geonode.com
   - Free-Proxy-List.net
   - PubProxy.com

2. **Após a coleta**, você será perguntado se deseja testar os proxies:
   ```
   Testar proxies agora? (s/n):
   ```

3. **Se escolher testar (s)**:
   - Informe o número de threads (padrão: 50)
   - O script testará todos os proxies em paralelo
   - Proxies funcionais serão salvos em `proxies.txt`

4. **Se não testar (n)**:
   - Todos os proxies serão salvos sem teste em `proxies_untested.txt`

## 📊 Exemplo de Saída

```
╔═══════════════════════════════════════╗
║       PROXY SCRAPER & TESTER          ║
║          Free Proxies 🌐              ║
╚═══════════════════════════════════════╝

Iniciando busca de proxies...

[*] Buscando proxies em proxyscrape.com...
[✓] 250 proxies encontrados

[*] Buscando proxies em geonode.com...
[✓] 500 proxies encontrados

[✓] Total de proxies coletados: 698

Testar proxies agora? (s/n): s
Threads para teste (padrão 50): 50

[*] Testando 698 proxies...
[*] Threads: 50

[✓] 45.76.123.45:8080 - FUNCIONANDO (1 válidos)
[✓] 192.168.1.100:3128 - FUNCIONANDO (2 válidos)
[350/698] Válidos: 25 | ETA: 45s

==================================================
RESULTADO:
Total testados: 698
Funcionando: 42
Taxa de sucesso: 6.0%
==================================================

[✓] 42 proxies salvos em 'proxies.txt'
```

## 📁 Arquivos Gerados

### `proxies.txt`
Contém proxies testados e funcionais no formato:
```
192.168.1.100:8080
45.76.123.45:3128
103.152.112.162:80
```

### `proxies_untested.txt`
Contém todos os proxies coletados sem teste (apenas se você escolher não testar)

## ⚙️ Configurações

### Ajustar número de threads

Você pode ajustar o número de threads para testes mais rápidos ou mais lentos:

- **Threads baixas (10-30)**: Mais estável, menos uso de CPU
- **Threads médias (50-100)**: Balanceado (recomendado)
- **Threads altas (150-300)**: Mais rápido, mas pode causar timeout em conexões lentas

### Modificar fontes de proxies

Você pode adicionar ou remover fontes editando o método `run()`:

```python
def run(self):
    # Adicionar nova fonte
    self.scrape_proxyscrape()
    self.scrape_geonode()
    self.scrape_free_proxy_list()
    self.scrape_sua_nova_fonte()  # Nova fonte
```

## 🔧 Fontes de Proxies

O script busca proxies de:

1. **ProxyScrape.com** - API pública com milhares de proxies
2. **Geonode.com** - Lista atualizada de proxies globais
3. **Free-Proxy-List.net** - Lista web popular de proxies gratuitos
4. **PubProxy.com** - API pública com proxies verificados

## ⚠️ Avisos Importantes

### Taxa de Sucesso
- É normal ter uma taxa de sucesso baixa (5-15%)
- Proxies gratuitos são instáveis e mudam constantemente
- Sempre teste os proxies antes de usar em produção

### Limitações
- Proxies gratuitos são geralmente lentos
- Podem estar bloqueados em alguns sites
- Não recomendado para uso comercial crítico
- Alguns podem registrar seu tráfego

### Uso Responsável
- Use apenas para fins legítimos e educacionais
- Respeite os termos de serviço dos sites que você acessa
- Não use para atividades ilegais ou maliciosas
- Alguns sites bloqueiam proxies conhecidos

## 🐛 Solução de Problemas

### Nenhum proxy encontrado
- Verifique sua conexão com internet
- Algumas fontes podem estar temporariamente offline
- Tente novamente mais tarde

### Todos os proxies falham no teste
- Proxies gratuitos mudam muito rápido
- Tente executar novamente para obter novos proxies
- Considere usar proxies premium para melhor confiabilidade

### Erro de timeout
- Reduza o número de threads
- Aumente o timeout no código (padrão: 10 segundos)
- Verifique sua conexão com internet

### Script trava durante teste
- Pode ser excesso de threads
- Tente com menos threads (20-30)
- Verifique se não há problemas de firewall

## 📈 Melhorias Futuras

Possíveis melhorias para o projeto:

- [ ] Suporte a proxies SOCKS4/SOCKS5
- [ ] Validação de anonimato (transparent, anonymous, elite)
- [ ] Teste de velocidade dos proxies
- [ ] Filtro por país/região
- [ ] Interface gráfica (GUI)
- [ ] Agendamento de buscas automáticas
- [ ] Cache de proxies funcionais
- [ ] Rotação automática de proxies

## 🤝 Contribuições

Contribuições são bem-vindas! Sinta-se livre para:

- Adicionar novas fontes de proxies
- Melhorar o algoritmo de teste
- Adicionar novos recursos
- Reportar bugs
- Melhorar a documentação

## 📄 Formato de Uso em Código

### Python Requests

```python
import requests

# Ler proxies do arquivo
with open('proxies.txt', 'r') as f:
    proxies_list = [line.strip() for line in f]

# Usar um proxy
proxy = proxies_list[0]
proxies = {
    'http': f'http://{proxy}',
    'https': f'http://{proxy}'
}

response = requests.get('https://api.example.com', proxies=proxies)
```

### Rotação de Proxies

```python
import requests
import random

# Ler proxies
with open('proxies.txt', 'r') as f:
    proxies_list = [line.strip() for line in f]

def get_random_proxy():
    proxy = random.choice(proxies_list)
    return {
        'http': f'http://{proxy}',
        'https': f'http://{proxy}'
    }

# Fazer requisição com proxy aleatório
response = requests.get('https://api.example.com', proxies=get_random_proxy())
```

## 📊 Estatísticas Típicas

| Métrica | Valor Esperado |
|---------|---------------|
| Proxies coletados | 500-1000 |
| Taxa de sucesso | 5-15% |
| Proxies funcionais | 30-100 |
| Tempo de coleta | 10-30 segundos |
| Tempo de teste (50 threads) | 1-3 minutos |

## 🔐 Segurança

- ⚠️ Proxies gratuitos podem ser inseguros
- Não envie dados sensíveis através de proxies gratuitos
- Use HTTPS sempre que possível
- Considere usar VPN para dados críticos
- Proxies podem registrar seu tráfego

## 📝 Licença

Este projeto é fornecido "como está", sem garantias de qualquer tipo.

**Desenvolvido para fins educacionais e de testes.**

---

## 💡 Dicas de Uso

### Para Web Scraping
- Use proxies com rotação automática
- Implemente retry logic para falhas
- Adicione delays entre requisições
- Monitore taxa de sucesso

### Para Testes
- Teste proxies regularmente (mudam rápido)
- Mantenha uma lista atualizada
- Use múltiplos proxies simultaneamente
- Implemente fallback para conexão direta

### Para Melhor Performance
- Aumente threads se tiver boa conexão
- Use proxies geograficamente próximos
- Cache proxies funcionais
- Implemente health check periódico

---

**⚡ Happy Proxying! ⚡**
