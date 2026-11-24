<div align="center">

# 🍔 FOODLY - App de Delivery 

### Sistema de pedidos online tipo iFood/Uber Eats desenvolvido com Python e Streamlit

[![Python Version](https://img.shields.io/badge/python-3.8%2B-blue)](https://www.python.org/downloads/)
[![Streamlit](https://img.shields.io/badge/streamlit-1.28%2B-FF4B4B)](https://streamlit.io/)
[![License](https://img.shields.io/badge/license-MIT-green)](LICENSE)
[![Status](https://img.shields.io/badge/status-active-success)]()

<img src="https://raw.githubusercontent.com/Tarikul-Islam-Anik/Animated-Fluent-Emojis/master/Emojis/Food/Pizza.png" alt="Pizza" width="200" height="200" />

[📋 Funcionalidades](#-funcionalidades) • 
[🚀 Demo](#-demo) • 
[💻 Instalação](#-instalação) • 
[📸 Screenshots](#-screenshots) • 
[🛠️ Tecnologias](#️-tecnologias)

</div>

---

## 📋 Funcionalidades

### 🍕 Sistema de Pedidos
- ✅ Catálogo completo de produtos por categorias
- ✅ Carrinho de compras interativo
- ✅ Sistema de cupons de desconto
- ✅ Cálculo automático de frete
- ✅ Múltiplas formas de pagamento

### 👤 Gerenciamento de Usuário
- ✅ Cadastro e login de clientes
- ✅ Endereços salvos
- ✅ Histórico de pedidos
- ✅ Produtos favoritos

### 📊 Acompanhamento em Tempo Real
- ✅ Status do pedido atualizado
- ✅ Tempo estimado de entrega
- ✅ Notificações de progresso

### ⭐ Avaliações
- ✅ Sistema de avaliação de produtos
- ✅ Comentários e feedback
- ✅ Ranking de pratos mais pedidos

---

## 🚀 Demo

### 🌐 Acesse online: 
**[🔗 foodly-app.streamlit.app](https://foodly-app.streamlit.app)** 

### 💻 Ou rode localmente:

```bash
# Clone o repositório
git clone https://github.com/seu-usuario/foodly-app.git

# Entre na pasta
cd foodly-app

# Instale as dependências
pip install -r requirements.txt

# Execute o app
streamlit run app.py
```

---

## 📸 Screenshots

<div align="center">

### 🏠 Página Principal
<img src="screenshots/home.png" alt="Home" width="600"/>

### 🛒 Carrinho de Compras
<img src="screenshots/cart.png" alt="Carrinho" width="600"/>

### 📦 Acompanhamento de Pedido
<img src="screenshots/tracking.png" alt="Tracking" width="600"/>

</div>

---

## 💻 Instalação

### 📋 Pré-requisitos

- Python 3.8 ou superior
- pip (gerenciador de pacotes Python)

### 🔧 Instalação Passo a Passo

#### Windows: 

```bash
# 1. Clone o repositório
git clone https://github.com/seu-usuario/foodly-app.git
cd foodly-app

# 2. Crie um ambiente virtual (recomendado)
python -m venv venv
venv\Scripts\activate

# 3. Instale as dependências
pip install -r requirements. txt

# 4. Execute o aplicativo
streamlit run app.py
```

#### Linux/Mac:

```bash
# 1. Clone o repositório
git clone https://github.com/seu-usuario/foodly-app.git
cd foodly-app

# 2. Crie um ambiente virtual (recomendado)
python3 -m venv venv
source venv/bin/activate

# 3. Instale as dependências
pip install -r requirements.txt

# 4. Execute o aplicativo
streamlit run app.py
```

### ⚡ Instalação Rápida (Windows)

Basta executar o arquivo `executar. bat`:

```batch
# Duplo clique em executar.bat
```

---

## 🛠️ Tecnologias

<div align="center">

| Tecnologia | Versão | Descrição |
|------------|--------|-----------|
| ![Python](https://img.shields.io/badge/Python-3.8+-3776AB?style=for-the-badge&logo=python&logoColor=white) | 3.8+ | Linguagem principal |
| ![Streamlit](https://img.shields.io/badge/Streamlit-1.28+-FF4B4B?style=for-the-badge&logo=streamlit&logoColor=white) | 1.28+ | Framework web |
| ![Pandas](https://img.shields.io/badge/Pandas-2.0+-150458?style=for-the-badge&logo=pandas&logoColor=white) | 2.0+ | Manipulação de dados |
| ![Plotly](https://img.shields.io/badge/Plotly-5.0+-3F4F75?style=for-the-badge&logo=plotly&logoColor=white) | 5.0+ | Visualizações interativas |

</div>

---

## 📁 Estrutura do Projeto

```
```

---

## 🎯 Como Usar

### 1️⃣ Faça Login ou Cadastre-se

```
👤 Usuário: demo@foodly.com
🔑 Senha: demo123
```

### 2️⃣ Navegue pelo Menu

- 🍕 **Pizzas**
- 🍔 **Hambúrgueres**
- 🍹 **Bebidas**
- 🍰 **Sobremesas**

### 3️⃣ Adicione ao Carrinho

- Selecione os produtos
- Escolha quantidade
- Adicione observações

### 4️⃣ Finalize o Pedido

- Aplique cupom de desconto (ex: `FOODLY10`)
- Escolha endereço de entrega
- Selecione forma de pagamento

### 5️⃣ Acompanhe seu Pedido

- Status em tempo real
- Tempo estimado
- Notificações de atualização

---

## 🎨 Cupons de Desconto Disponíveis

| Cupom | Desconto | Válido até |
|-------|----------|------------|
| `FOODLY10` | 10% OFF | 31/12/2025 |
| `PRIMEIRA` | 15% OFF | Primeiro pedido |
| `FRETEGRATIS` | Frete Grátis | 31/12/2025 |
| `NATAL25` | 25% OFF | 25/12/2025 |

---

## 📊 Funcionalidades Detalhadas

### 🛒 Sistema de Carrinho

```python
# Adicionar produto
adicionar_ao_carrinho(produto_id, quantidade)

# Aplicar cupom
aplicar_cupom("FOODLY10")

# Calcular total
total = calcular_total(itens, frete, desconto)
```

### 📍 Cálculo de Frete

- Até 3km: **R$ 5,00**
- 3km - 5km: **R$ 8,00**
- 5km - 10km: **R$ 12,00**
- Acima de 10km: **R$ 15,00**

### 💳 Formas de Pagamento

- 💵 Dinheiro
- 💳 Cartão de Crédito
- 💳 Cartão de Débito
- 📱 PIX

---

## 🤝 Contribuindo

Contribuições são bem-vindas! Siga os passos:

1. 🍴 Fork o projeto
2. 🔀 Crie uma branch (`git checkout -b feature/NovaFuncionalidade`)
3. ✏️ Commit suas mudanças (`git commit -m 'Adiciona nova funcionalidade'`)
4. 📤 Push para a branch (`git push origin feature/NovaFuncionalidade`)
5. 🎉 Abra um Pull Request

---

## 🐛 Reportar Bugs

Encontrou um bug? [Abra uma issue](https://github.com/seu-usuario/foodly-app/issues/new)

---

## 📝 Licença

Este projeto está sob a licença MIT. Veja o arquivo [LICENSE](LICENSE) para mais detalhes.

---

## 👨‍💻 Autor

<div align="center">

[![GitHub](https://img.shields.io/badge/GitHub-100000? style=for-the-badge&logo=github&logoColor=white)](https://github.com/seu-usuario)
[![LinkedIn](https://img.shields.io/badge/LinkedIn-0077B5? style=for-the-badge&logo=linkedin&logoColor=white)](https://linkedin.com/in/seu-perfil)
[![Email](https://img.shields.io/badge/Email-D14836?style=for-the-badge&logo=gmail&logoColor=white)](mailto:seu-email@gmail.com)

</div>

---

## ⭐ Mostre seu Apoio

Se este projeto te ajudou, dê uma ⭐️! 

---

<div align="center">

### 📈 Status do Projeto

![GitHub stars](https://img.shields.io/github/stars/seu-usuario/foodly-app?style=social)
![GitHub forks](https://img.shields.io/github/forks/seu-usuario/foodly-app?style=social)
![GitHub watchers](https://img.shields.io/github/watchers/seu-usuario/foodly-app? style=social)

### 💬 Tem alguma dúvida?

[![Ask Me Anything](https://img.shields.io/badge/Ask%20me-anything-1abc9c.svg)](https://github.com/seu-usuario/foodly-app/issues)

</div>
