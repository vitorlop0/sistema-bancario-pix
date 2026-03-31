# Sistema Bancário PIX

Sistema bancário simples desenvolvido em Python com funcionalidades de depósito, envio de PIX com geração de QR Code dinâmico e persistência de dados em arquivo JSON.

**Status:** projeto em desenvolvimento, com foco em refatoração, organização do código e evolução das funcionalidades.

---

## Sobre o projeto

Este projeto foi desenvolvido com o objetivo de praticar lógica de programação, manipulação de arquivos e geração de QR Code em Python. O sistema simula operações bancárias básicas com persistência de dados entre sessões.

---

## Funcionalidades

- Ver saldo atual
- Realizar depósitos
- Enviar PIX com geração de QR Code dinâmico (padrão Banco Central)
- Visualizar extrato com data e hora de cada movimentação
- Somar total de PIX enviados
- Persistência de dados em arquivo JSON (os dados são mantidos mesmo após fechar o programa)

---

## Tecnologias utilizadas

- Python 3
- [qrcode](https://pypi.org/project/qrcode/) — geração de QR Code
- [python-dotenv](https://pypi.org/project/python-dotenv/) — segurança e variáveis de ambiente
- `json` — persistência de dados
- `os` — integração com sistema operacional
- `datetime` — registro de data e hora

---

## Como rodar o projeto

**1. Clone o repositório**
```bash
git clone https://github.com/seu-usuario/seu-repositorio.git
cd seu-repositorio
```

**2. Instale as dependências**
```bash
pip install -r requirements.txt
```

**3. Configure suas informações de PIX**

O projeto utiliza um arquivo .env para proteger dados sensíveis.

Renomeie o arquivo .env.example para .env

Abra o arquivo .env e preencha com os seus dados reais (Nome, Cidade e Chave PIX).

**4. Execute**
```bash
python main.py
```

---

## Estrutura do projeto

```
seu-repositorio/
├── main.py              # Código principal e lógica do sistema
├── requirements.txt     # Lista de dependências do projeto
├── .env.example         # Template seguro para variáveis de ambiente
├── .gitignore           # Arquivo de segurança do Git
├── dados_banco.json     # Gerado automaticamente na primeira execução
├── qr_code_gerado.png   # Gerado dinamicamente a cada PIX enviado
└── README.md
```

---

## Observações

- O arquivo `dados_banco.json` é criado automaticamente na primeira execução
- O QR Code gerado segue o padrão EMV do Banco Central do Brasil
- Este projeto é para fins de estudo e portfólio

---

## Autor

**Vitor Lopes**
[LinkedIn](https://linkedin.com/in/vitorlopess/) • [GitHub](https://github.com/vitorlop0)
