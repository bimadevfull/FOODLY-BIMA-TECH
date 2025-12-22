# ============================================================
# FOODLY - APP DE DELIVERY COMPLETO
# Sistema de pedidos online tipo iFood/Uber Eats
# Desenvolvido com Python 3.8+ e Streamlit 1.28+
# ============================================================

import streamlit as st
import pandas as pd
from datetime import datetime, timedelta
import time
import json
from typing import Dict, List

# ============================================================
# CONFIGURAÇÕES DA PÁGINA
# ============================================================

st.set_page_config(
    page_title="Foodly - Delivery",
    page_icon="🍔",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ============================================================
# ESTILOS CSS PERSONALIZADOS
# ============================================================

st.markdown("""
<style>
    /* Estilo principal */
    .main {
        background-color: #f8f9fa;
    }
    
    /* Cards de produtos */
    .product-card {
        background: white;
        padding: 20px;
        border-radius:  10px;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        margin: 10px 0;
        transition: transform 0.3s;
    }
    
    . product-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 4px 8px rgba(0,0,0,0.2);
    }
    
    /* Botões personalizados */
    .stButton>button {
        width: 100%;
        border-radius: 5px;
        font-weight: bold;
    }
    
    /* Títulos */
    h1, h2, h3 {
        color: #2c3e50;
    }
    
    /* Badges */
    .badge {
        display: inline-block;
        padding: 5px 10px;
        border-radius: 20px;
        font-size: 12px;
        font-weight:  bold;
        margin: 5px;
    }
    
    . badge-success {
        background-color:  #28a745;
        color: white;
    }
    
    .badge-warning {
        background-color: #ffc107;
        color: black;
    }
    
    . badge-danger {
        background-color: #dc3545;
        color: white;
    }
    
    /* Status do pedido */
    .status-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        padding: 20px;
        border-radius:  10px;
        margin: 10px 0;
    }
</style>
""", unsafe_allow_html=True)

# ============================================================
# CLASSES DE DADOS
# ============================================================

class Produto:
    def __init__(self, id: int, nome: str, categoria: str, preco: float, 
                 descricao: str, imagem:  str, avaliacao: float, tempo_preparo: int):
        self.id = id
        self.nome = nome
        self.categoria = categoria
        self.preco = preco
        self.descricao = descricao
        self.imagem = imagem
        self.avaliacao = avaliacao
        self.tempo_preparo = tempo_preparo
    
    def to_dict(self):
        return {
            'id': self. id,
            'nome': self.nome,
            'categoria':  self.categoria,
            'preco': self.preco,
            'descricao': self. descricao,
            'imagem': self.imagem,
            'avaliacao': self. avaliacao,
            'tempo_preparo': self.tempo_preparo
        }


class ItemCarrinho:
    def __init__(self, produto: Produto, quantidade: int, observacoes:  str = ""):
        self.produto = produto
        self.quantidade = quantidade
        self.observacoes = observacoes
    
    def subtotal(self):
        return self.produto.preco * self. quantidade


class Pedido:
    def __init__(self, id: int, itens: List[ItemCarrinho], 
                 endereco: str, forma_pagamento: str, cupom: str = None):
        self.id = id
        self.itens = itens
        self.endereco = endereco
        self.forma_pagamento = forma_pagamento
        self. cupom = cupom
        self.data = datetime.now()
        self.status = "Preparando"
        self.frete = 5.00
    
    def calcular_subtotal(self):
        return sum(item.subtotal() for item in self.itens)
    
    def calcular_desconto(self):
        if self.cupom == "FOODLY10":
            return self.calcular_subtotal() * 0.10
        elif self.cupom == "PRIMEIRA": 
            return self.calcular_subtotal() * 0.15
        elif self.cupom == "FRETEGRATIS": 
            return self.frete
        elif self.cupom == "NATAL25":
            return self.calcular_subtotal() * 0.25
        return 0
    
    def calcular_total(self):
        return self.calcular_subtotal() + self.frete - self.calcular_desconto()
    
    def tempo_estimado(self):
        tempo_preparo = max(item.produto.tempo_preparo for item in self.itens)
        tempo_entrega = 30
        return tempo_preparo + tempo_entrega

# ============================================================
# BANCO DE DADOS (SIMULADO)
# ============================================================

@st.cache_data
def carregar_produtos():
    """Carrega o catálogo de produtos"""
    produtos = [
        # PIZZAS
        Produto(1, "Pizza Margherita", "Pizzas", 45.90, 
                "Molho de tomate, mussarela, manjericão e azeite", 
                "🍕", 4. 8, 35),
        Produto(2, "Pizza Calabresa", "Pizzas", 49.90,
                "Calabresa, cebola, mussarela e azeitonas",
                "🍕", 4.7, 35),
        Produto(3, "Pizza Portuguesa", "Pizzas", 52.90,
                "Presunto, ovos, cebola, azeitonas e mussarela",
                "🍕", 4.6, 35),
        Produto(4, "Pizza Quatro Queijos", "Pizzas", 54.90,
                "Mussarela, gorgonzola, provolone e parmesão",
                "🍕", 4.9, 35),
        
        # HAMBÚRGUERES
        Produto(5, "X-Burger Clássico", "Hambúrgueres", 28.90,
                "Hambúrguer, queijo, alface, tomate e maionese",
                "🍔", 4.5, 20),
        Produto(6, "X-Bacon", "Hambúrgueres", 32.90,
                "Hambúrguer, bacon, queijo, alface e molho especial",
                "🍔", 4.7, 20),
        Produto(7, "X-Tudo", "Hambúrgueres", 38.90,
                "Hambúrguer, bacon, ovo, queijo, presunto, alface e tomate",
                "🍔", 4.8, 25),
        Produto(8, "Veggie Burger", "Hambúrgueres", 29.90,
                "Hambúrguer vegetariano, queijo vegano, alface e tomate",
                "🍔", 4.4, 20),
        
        # BEBIDAS
        Produto(9, "Coca-Cola 350ml", "Bebidas", 6.00,
                "Refrigerante Coca-Cola lata 350ml",
                "🥤", 4.9, 0),
        Produto(10, "Guaraná Antarctica 350ml", "Bebidas", 5.50,
                "Refrigerante Guaraná lata 350ml",
                "🥤", 4.8, 0),
        Produto(11, "Suco de Laranja 500ml", "Bebidas", 8.90,
                "Suco natural de laranja 500ml",
                "🧃", 4.7, 5),
        Produto(12, "Água Mineral 500ml", "Bebidas", 3.50,
                "Água mineral sem gás 500ml",
                "💧", 5.0, 0),
        
        # SOBREMESAS
        Produto(13, "Brownie de Chocolate", "Sobremesas", 15.90,
                "Brownie de chocolate com nozes",
                "🍰", 4.9, 10),
        Produto(14, "Petit Gateau", "Sobremesas", 18.90,
                "Bolinho de chocolate com sorvete de baunilha",
                "🍮", 5.0, 15),
        Produto(15, "Sorvete 2 Bolas", "Sobremesas", 12.90,
                "Escolha 2 sabores de sorvete",
                "🍨", 4.8, 5),
        Produto(16, "Pudim de Leite", "Sobremesas", 14.90,
                "Pudim de leite condensado com calda de caramelo",
                "🍮", 4.7, 10),
    ]
    return produtos


def carregar_cupons():
    """Carrega cupons de desconto disponíveis"""
    return {
        "FOODLY10":  {"desconto": 10, "tipo": "percentual", "descricao": "10% de desconto"},
        "PRIMEIRA": {"desconto": 15, "tipo": "percentual", "descricao": "15% OFF no primeiro pedido"},
        "FRETEGRATIS": {"desconto": 0, "tipo": "frete", "descricao": "Frete grátis"},
        "NATAL25": {"desconto": 25, "tipo": "percentual", "descricao": "25% OFF Natal"},
    }


# ============================================================
# INICIALIZAÇÃO DO SESSION STATE
# ============================================================

def inicializar_session_state():
    """Inicializa variáveis de sessão"""
    if 'carrinho' not in st.session_state:
        st.session_state.carrinho = []
    
    if 'usuario_logado' not in st.session_state:
        st.session_state.usuario_logado = None
    
    if 'pedidos' not in st.session_state:
        st.session_state.pedidos = []
    
    if 'favoritos' not in st.session_state:
        st.session_state.favoritos = []
    
    if 'endereco_selecionado' not in st. session_state:
        st. session_state.endereco_selecionado = None
    
    if 'pedido_atual' not in st.session_state:
        st.session_state.pedido_atual = None


# ============================================================
# FUNÇÕES DO CARRINHO
# ============================================================

def adicionar_ao_carrinho(produto:  Produto, quantidade: int, observacoes: str = ""):
    """Adiciona produto ao carrinho"""
    # Verifica se o produto já está no carrinho
    for item in st.session_state.carrinho:
        if item.produto. id == produto.id:
            item.quantidade += quantidade
            st.success(f"✅ {quantidade}x {produto.nome} adicionado(s) ao carrinho!")
            return
    
    # Se não está, adiciona novo item
    novo_item = ItemCarrinho(produto, quantidade, observacoes)
    st.session_state.carrinho.append(novo_item)
    st.success(f"✅ {quantidade}x {produto.nome} adicionado(s) ao carrinho!")


def remover_do_carrinho(produto_id: int):
    """Remove produto do carrinho"""
    st.session_state.carrinho = [item for item in st.session_state.carrinho 
                                  if item.produto.id != produto_id]
    st.success("Item removido do carrinho!")


def limpar_carrinho():
    """Limpa todo o carrinho"""
    st. session_state.carrinho = []


def calcular_total_carrinho():
    """Calcula o total do carrinho"""
    return sum(item.subtotal() for item in st.session_state.carrinho)


# ============================================================
# PÁGINA:  HOME
# ============================================================

def pagina_home():
    """Página principal do app"""
    # Banner principal
    st.markdown("""
    <div style='background:  linear-gradient(135deg, #667eea 0%, #764ba2 100%); 
                padding: 40px; border-radius: 10px; margin-bottom: 30px; text-align: center;'>
        <h1 style='color: white; margin: 0;'>🍔 FOODLY</h1>
        <p style='color: white; font-size: 20px; margin: 10px 0;'>
            Seu delivery favorito chegou! 🚀
        </p>
        <p style='color: white; margin: 0;'>
            Entrega rápida • Cupons de desconto • Avaliações reais
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    # Estatísticas
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("🍕 Produtos", "16+")
    
    with col2:
        st.metric("⭐ Avaliação", "4.8/5.0")
    
    with col3:
        st.metric("🚚 Entrega", "30-45 min")
    
    with col4:
        st.metric("💰 Frete", "A partir de R$ 5")
    
    st.divider()
    
    # Cupons em destaque
    st.subheader("🎉 Cupons Disponíveis")
    
    cupons_cols = st.columns(4)
    cupons = [
        ("FOODLY10", "10% OFF", "Em todo o cardápio"),
        ("PRIMEIRA", "15% OFF", "Primeiro pedido"),
        ("FRETEGRATIS", "Frete Grátis", "Sem valor mínimo"),
        ("NATAL25", "25% OFF", "Especial Natal"),
    ]
    
    for idx, (codigo, desconto, desc) in enumerate(cupons):
        with cupons_cols[idx]: 
            st.info(f"**{codigo}**\n\n{desconto}\n\n_{desc}_")
    
    st.divider()
    
    # Categorias
    st.subheader("📋 Categorias")
    
    cat_col1, cat_col2, cat_col3, cat_col4 = st. columns(4)
    
    with cat_col1:
        if st.button("🍕 Pizzas", use_container_width=True):
            st.session_state.categoria_filtro = "Pizzas"
            st.rerun()
    
    with cat_col2:
        if st.button("🍔 Hambúrgueres", use_container_width=True):
            st.session_state.categoria_filtro = "Hambúrgueres"
            st.rerun()
    
    with cat_col3:
        if st.button("🥤 Bebidas", use_container_width=True):
            st.session_state.categoria_filtro = "Bebidas"
            st.rerun()
    
    with cat_col4:
        if st.button("🍰 Sobremesas", use_container_width=True):
            st.session_state.categoria_filtro = "Sobremesas"
            st. rerun()


# ============================================================
# PÁGINA: CARDÁPIO
# ============================================================

def pagina_cardapio():
    """Página do cardápio completo"""
    st.title("📋 Cardápio Completo")
    
    produtos = carregar_produtos()
    
    # Filtros
    col1, col2, col3 = st.columns([2, 2, 1])
    
    with col1:
        categorias = ["Todas"] + list(set(p.categoria for p in produtos))
        categoria_selecionada = st.selectbox("Categoria", categorias)
    
    with col2:
        ordem = st.selectbox("Ordenar por", 
                            ["Mais populares", "Menor preço", "Maior preço", "Melhor avaliação"])
    
    with col3:
        st.write("")
        st.write("")
        mostrar_favoritos = st.checkbox("❤️ Favoritos")
    
    # Aplicar filtros
    produtos_filtrados = produtos
    
    if categoria_selecionada != "Todas": 
        produtos_filtrados = [p for p in produtos_filtrados if p.categoria == categoria_selecionada]
    
    if mostrar_favoritos:
        produtos_filtrados = [p for p in produtos_filtrados 
                            if p.id in st.session_state.favoritos]
    
    # Ordenar
    if ordem == "Menor preço":
        produtos_filtrados.sort(key=lambda x: x.preco)
    elif ordem == "Maior preço":
        produtos_filtrados.sort(key=lambda x: x.preco, reverse=True)
    elif ordem == "Melhor avaliação": 
        produtos_filtrados.sort(key=lambda x: x.avaliacao, reverse=True)
    
    st.divider()
    
    # Exibir produtos
    if not produtos_filtrados:
        st.warning("Nenhum produto encontrado com os filtros selecionados.")
        return
    
    # Grid de produtos (2 por linha)
    for i in range(0, len(produtos_filtrados), 2):
        cols = st.columns(2)
        
        for j in range(2):
            if i + j < len(produtos_filtrados):
                produto = produtos_filtrados[i + j]
                
                with cols[j]:
                    # Card do produto
                    with st.container():
                        st.markdown(f"### {produto.imagem} {produto.nome}")
                        
                        # Avaliação
                        estrelas = "⭐" * int(produto.avaliacao)
                        st.markdown(f"{estrelas} {produto.avaliacao}")
                        
                        st.write(produto.descricao)
                        
                        # Preço e tempo
                        col_preco, col_tempo = st. columns(2)
                        with col_preco:
                            st.markdown(f"**R$ {produto.preco:.2f}**")
                        with col_tempo:
                            st.markdown(f"🕒 {produto.tempo_preparo} min")
                        
                        # Botões
                        col_fav, col_qtd, col_add = st.columns([1, 2, 2])
                        
                        with col_fav:
                            is_favorito = produto. id in st.session_state. favoritos
                            if st.button("❤️" if is_favorito else "🤍", 
                                       key=f"fav_{produto.id}",
                                       help="Favoritar"):
                                if is_favorito:
                                    st.session_state.favoritos.remove(produto.id)
                                else:
                                    st.session_state.favoritos.append(produto.id)
                                st.rerun()
                        
                        with col_qtd:
                            quantidade = st.number_input("Qtd", min_value=1, max_value=10, 
                                                       value=1, key=f"qtd_{produto. id}",
                                                       label_visibility="collapsed")
                        
                        with col_add: 
                            if st.button("➕ Adicionar", key=f"add_{produto.id}", 
                                       use_container_width=True):
                                adicionar_ao_carrinho(produto, quantidade)
                                st.rerun()
                        
                        # Observações (expansível)
                        with st.expander("📝 Adicionar observações"):
                            obs = st.text_area("Observações para este item",
                                             key=f"obs_{produto.id}",
                                             placeholder="Ex: sem cebola, ponto da carne bem passado...")
                    
                    st.divider()


# ============================================================
# PÁGINA: CARRINHO
# ============================================================

def pagina_carrinho():
    """Página do carrinho de compras"""
    st.title("🛒 Meu Carrinho")
    
    if not st.session_state.carrinho:
        st.info("Seu carrinho está vazio.  Que tal adicionar alguns produtos deliciosos?  🍕")
        if st.button("🛍️ Ver Cardápio"):
            st.session_state.pagina = "Cardápio"
            st. rerun()
        return
    
    # Itens do carrinho
    st.subheader("📦 Itens")
    
    for idx, item in enumerate(st.session_state.carrinho):
        with st.container():
            col1, col2, col3, col4 = st.columns([3, 1, 2, 1])
            
            with col1:
                st. markdown(f"**{item.produto.imagem} {item.produto.nome}**")
                if item.observacoes:
                    st. caption(f"Obs: {item.observacoes}")
            
            with col2:
                st.write(f"x{item.quantidade}")
            
            with col3:
                st.write(f"R$ {item. subtotal():.2f}")
            
            with col4:
                if st.button("🗑️", key=f"remove_{idx}", help="Remover"):
                    remover_do_carrinho(item.produto.id)
                    st.rerun()
            
            st.divider()
    
    # Resumo do pedido
    st.subheader("💰 Resumo do Pedido")
    
    subtotal = calcular_total_carrinho()
    frete = 5.00
    
    # Cupom de desconto
    col1, col2 = st. columns([3, 1])
    
    with col1:
        cupom = st.text_input("Cupom de desconto", placeholder="Ex: FOODLY10")
    
    with col2:
        st.write("")
        st.write("")
        if st.button("Aplicar"):
            cupons_validos = carregar_cupons()
            if cupom. upper() in cupons_validos:
                st.session_state.cupom_aplicado = cupom.upper()
                st.success(f"✅ Cupom {cupom.upper()} aplicado!")
                st.rerun()
            else:
                st.error("❌ Cupom inválido")
    
    # Cálculo do desconto
    desconto = 0
    if hasattr(st.session_state, 'cupom_aplicado'):
        cupom_info = carregar_cupons()[st.session_state.cupom_aplicado]
        if cupom_info['tipo'] == 'percentual': 
            desconto = subtotal * (cupom_info['desconto'] / 100)
        elif cupom_info['tipo'] == 'frete':
            desconto = frete
    
    # Exibir valores
    st.markdown(f"""
    | Item | Valor |
    |------|-------|
    | Subtotal | R$ {subtotal:.2f} |
    | Frete | R$ {frete:.2f} |
    | Desconto | -R$ {desconto:.2f} |
    | **TOTAL** | **R$ {(subtotal + frete - desconto):.2f}** |
    """)
    
    st.divider()
    
    # Botões de ação
    col1, col2 = st.columns(2)
    
    with col1:
        if st.button("🗑️ Limpar Carrinho", use_container_width=True):
            limpar_carrinho()
            if hasattr(st.session_state, 'cupom_aplicado'):
                delattr(st.session_state, 'cupom_aplicado')
            st.rerun()
    
    with col2:
        if st.button("✅ Finalizar Pedido", type="primary", use_container_width=True):
            st.session_state.pagina = "Checkout"
            st.rerun()


# ============================================================
# PÁGINA: CHECKOUT
# ============================================================

def pagina_checkout():
    """Página de finalização do pedido"""
    st.title("✅ Finalizar Pedido")
    
    if not st.session_state.carrinho:
        st.warning("Seu carrinho está vazio!")
        return
    
    # Etapa 1: Endereço
    st.subheader("1️⃣ Endereço de Entrega")
    
    endereco = st.text_input("Rua e número", placeholder="Ex: Rua das Flores, 123")
    complemento = st.text_input("Complemento (opcional)", placeholder="Ex: Apto 45")
    
    col1, col2 = st. columns(2)
    with col1:
        bairro = st.text_input("Bairro", placeholder="Ex: Centro")
    with col2:
        cidade = st.text_input("Cidade", placeholder="Ex:  São Paulo")
    
    endereco_completo = f"{endereco}, {bairro}, {cidade}"
    if complemento:
        endereco_completo += f" - {complemento}"
    
    st.divider()
    
    # Etapa 2: Forma de pagamento
    st.subheader("2️⃣ Forma de Pagamento")
    
    forma_pagamento = st.radio(
        "Escolha a forma de pagamento",
        ["💳 Cartão de Crédito", "💳 Cartão de Débito", "📱 PIX", "💵 Dinheiro"],
        horizontal=True
    )
    
    if "Dinheiro" in forma_pagamento:
        troco_para = st.number_input("Precisa de troco para quanto?", 
                                     min_value=0.0, step=10.0)
    
    st.divider()
    
    # Resumo final
    st.subheader("3️⃣ Resumo do Pedido")
    
    subtotal = calcular_total_carrinho()
    frete = 5.00
    desconto = 0
    
    if hasattr(st.session_state, 'cupom_aplicado'):
        cupom_info = carregar_cupons()[st.session_state.cupom_aplicado]
        if cupom_info['tipo'] == 'percentual':
            desconto = subtotal * (cupom_info['desconto'] / 100)
        elif cupom_info['tipo'] == 'frete':
            desconto = frete
    
    total = subtotal + frete - desconto
    
    # Exibir itens
    st.markdown("**Itens do pedido:**")
    for item in st.session_state.carrinho:
        st.write(f"• {item.quantidade}x {item.produto.nome} - R$ {item.subtotal():.2f}")
    
    st.divider()
    
    # Valores
    col1, col2 = st. columns(2)
    
    with col1:
        st. write("Subtotal:")
        st.write("Frete:")
        if desconto > 0:
            st.write("Desconto:")
        st.markdown("**TOTAL:**")
    
    with col2:
        st.write(f"R$ {subtotal:.2f}")
        st.write(f"R$ {frete:.2f}")
        if desconto > 0:
            st.write(f"-R$ {desconto:.2f}")
        st.markdown(f"**R$ {total:.2f}**")
    
    st.divider()
    
    # Tempo estimado
    tempo_preparo = max(item.produto.tempo_preparo for item in st.session_state.carrinho)
    tempo_entrega = 30
    tempo_total = tempo_preparo + tempo_entrega
    
    st.info(f"⏰ Tempo estimado de entrega: **{tempo_total} minutos**")
    
    # Botão confirmar
    if st.button("🚀 Confirmar Pedido", type="primary", use_container_width=True):
        if not endereco or not bairro or not cidade:
            st.error("❌ Por favor, preencha o endereço completo!")
        else:
            # Criar pedido
            cupom_usado = st.session_state.cupom_aplicado if hasattr(st.session_state, 'cupom_aplicado') else None
            pedido = Pedido(
                id=len(st.session_state.pedidos) + 1,
                itens=st.session_state. carrinho. copy(),
                endereco=endereco_completo,
                forma_pagamento=forma_pagamento,
                cupom=cupom_usado
            )
            
            st. session_state.pedidos.append(pedido)
            st.session_state.pedido_atual = pedido
            limpar_carrinho()
            
            if hasattr(st.session_state, 'cupom_aplicado'):
                delattr(st. session_state, 'cupom_aplicado')
            
            st.session_state.pagina = "Acompanhar"
            st.rerun()


# ============================================================
# PÁGINA: ACOMPANHAR PEDIDO
# ============================================================

def pagina_acompanhar():
    """Página de acompanhamento do pedido"""
    st.title("📦 Acompanhar Pedido")
    
    if not st.session_state. pedido_atual:
        st.warning("Você ainda não fez nenhum pedido.")
        return
    
    pedido = st.session_state. pedido_atual
    
    # Banner de sucesso
    st.success("🎉 Pedido confirmado com sucesso!")
    
    # Informações do pedido
    st. markdown(f"""
    <div class='status-card'>
        <h2 style='margin: 0; color: white;'>Pedido #{pedido.id}</h2>
        <p style='margin: 10px 0; font-size: 18px;'>
            Status: <strong>{pedido.status}</strong>
        </p>
        <p style='margin:  0;'>
            ⏰ Tempo estimado: <strong>{pedido.tempo_estimado()} minutos</strong>
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    st.divider()
    
    # Linha do tempo do pedido
    st.subheader("📍 Status da Entrega")
    
    status_options = ["Confirmado", "Preparando", "Saiu para entrega", "Entregue"]
    
    # Simular progresso (em produção, isso viria do backend)
    progress = status_options.index(pedido. status) if pedido.status in status_options else 0
    
    for idx, status in enumerate(status_options):
        if idx <= progress:
            st.markdown(f"✅ **{status}**")
        else:
            st.markdown(f"⭕ {status}")
    
    # Botão para simular mudança de status (apenas para demo)
    if pedido.status != "Entregue":
        if st. button("⏭️ Avançar Status (Demo)", help="Apenas para demonstração"):
            current_idx = status_options.index(pedido.status)
            if current_idx < len(status_options) - 1:
                pedido.status = status_options[current_idx + 1]
                st.rerun()
    
    st.divider()
    
    # Detalhes do pedido
    st.subheader("📋 Detalhes do Pedido")
    
    col1, col2 = st. columns(2)
    
    with col1:
        st. markdown("**Itens:**")
        for item in pedido.itens:
            st.write(f"• {item.quantidade}x {item.produto.nome}")
    
    with col2:
        st.markdown("**Entrega:**")
        st.write(f"📍 {pedido.endereco}")
        st.write(f"💳 {pedido.forma_pagamento}")
        st.write(f"💰 R$ {pedido. calcular_total():.2f}")
    
    st.divider()
    
    # Se entregue, mostrar avaliação
    if pedido.status == "Entregue":
        st.subheader("⭐ Avalie seu pedido")
        
        avaliacao = st.slider("Como foi sua experiência?", 1, 5, 5)
        comentario = st.text_area("Deixe um comentário (opcional)")
        
        if st.button("📝 Enviar Avaliação", type="primary"):
            st.success("✅ Obrigado pela sua avaliação!")
            st.balloons()


# ============================================================
# PÁGINA: HISTÓRICO
# ============================================================

def pagina_historico():
    """Página de histórico de pedidos"""
    st.title("📜 Histórico de Pedidos")
    
    if not st.session_state.pedidos:
        st.info("Você ainda não fez nenhum pedido.")
        return
    
    # Listar todos os pedidos
    for pedido in reversed(st.session_state.pedidos):
        with st.expander(f"Pedido #{pedido.id} - {pedido.data. strftime('%d/%m/%Y %H:%M')} - R$ {pedido.calcular_total():.2f}"):
            st.markdown(f"**Status:** {pedido.status}")
            st.markdown(f"**Endereço:** {pedido.endereco}")
            st.markdown(f"**Pagamento:** {pedido.forma_pagamento}")
            
            st.markdown("**Itens:**")
            for item in pedido.itens:
                st.write(f"• {item.quantidade}x {item.produto.nome} - R$ {item.subtotal():.2f}")
            
            st.divider()
            
            col1, col2, col3 = st.columns(3)
            
            with col1:
                st.metric("Subtotal", f"R$ {pedido.calcular_subtotal():.2f}")
            
            with col2:
                st.metric("Frete", f"R$ {pedido. frete:. 2f}")
            
            with col3:
                st.metric("Total", f"R$ {pedido.calcular_total():.2f}")
            
            if pedido.cupom:
                st.success(f"💎 Cupom aplicado: {pedido.cupom} (-R$ {pedido.calcular_desconto():.2f})")
            
            # Botão para ver detalhes
            if st.button(f"👁️ Ver detalhes", key=f"ver_{pedido.id}"):
                st.session_state.pedido_atual = pedido
                st.session_state.pagina = "Acompanhar"
                st. rerun()


# ============================================================
# SIDEBAR (MENU LATERAL)
# ============================================================

def sidebar_menu():
    """Menu lateral do app"""
    with st.sidebar:
        st. image("https://raw.githubusercontent.com/Tarikul-Islam-Anik/Animated-Fluent-Emojis/master/Emojis/Food/Hamburger.png", 
                 width=100)
        
        st.title("FOODLY")
        
        st.divider()
        
        # Menu de navegação
        menu_options = {
            "Home": "🏠",
            "Cardápio": "📋",
            "Carrinho": "🛒",
            "Acompanhar": "📦",
            "Histórico":  "📜",
        }
        
        for pagina, icone in menu_options.items():
            if st.button(f"{icone} {pagina}", use_container_width=True,
                        type="primary" if st.session_state.get('pagina') == pagina else "secondary"):
                st.session_state.pagina = pagina
                st.rerun()
        
        st.divider()
        
        # Informações do carrinho
        if st.session_state.carrinho:
            qtd_itens = sum(item.quantidade for item in st.session_state.carrinho)
            total = calcular_total_carrinho()
            
            st.metric("🛒 Itens no carrinho", qtd_itens)
            st.metric("💰 Total", f"R$ {total:. 2f}")
        else:
            st.info("Carrinho vazio")
        
        st.divider()
        
        # Rodapé
        st.caption("📞 Atendimento: (11) 99999-9999")
        st.caption("📧 contato@foodly.com")
        st.caption("🕒 Seg-Dom:  10h às 23h")
        
        st. divider()
        
        st.caption("Feito com ❤️ usando Streamlit")


# ============================================================
# FUNÇÃO PRINCIPAL
# ============================================================

def main():
    """Função principal do aplicativo"""
    
    # Inicializar session state
    inicializar_session_state()
    
    # Página padrão
    if 'pagina' not in st. session_state:
        st. session_state.pagina = "Home"
    
    # Menu lateral
    sidebar_menu()
    
    # Roteamento de páginas
    if st.session_state.pagina == "Home":
        pagina_home()
    elif st.session_state.pagina == "Cardápio":
        pagina_cardapio()
    elif st.session_state. pagina == "Carrinho": 
        pagina_carrinho()
    elif st.session_state.pagina == "Checkout":
        pagina_checkout()
    elif st.session_state.pagina == "Acompanhar":
        pagina_acompanhar()
    elif st.session_state.pagina == "Histórico":
        pagina_historico()


# ============================================================
# EXECUTAR APP
# ============================================================

if __name__ == "__main__": 
    main()