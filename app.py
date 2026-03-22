import streamlit as st
from groq import Groq
import json
import os

# Configuração da página
st.set_page_config(
    page_title="GIF Huber - Legendas Shopee",
    page_icon="🛍️",
    layout="centered"
)

# CSS personalizado
st.markdown("""
    <style>
    .main { background-color: #f5f5f5; }
    .stButton>button {
        background-color: #ee4d2d;
        color: white;
        font-size: 18px;
        font-weight: bold;
        border-radius: 12px;
        width: 100%;
        padding: 12px;
        border: none;
    }
    .stButton>button:hover {
        background-color: #d44226;
    }
    .legenda-box {
        background-color: white;
        border: 1px solid #ffd5cc;
        border-radius: 12px;
        padding: 16px;
        margin-bottom: 12px;
    }
    </style>
""", unsafe_allow_html=True)

# Título
st.markdown("# 🛍️ GIF Huber - Legendas Shopee")
st.markdown("---")

# Formulário
titulo = st.text_input(
    "📦 Título do Produto",
    placeholder="Ex: Tênis Nike Air Max"
)

col1, col2 = st.columns(2)
with col1:
    quantidade = st.selectbox(
        "🔢 Quantidade",
        options=[3, 5, 7, 10],
        index=1
    )
with col2:
    estilo = st.selectbox(
        "🎨 Estilo",
        options=["jovem", "formal", "urgencia"],
        format_func=lambda x: {
            "jovem": "😎 Jovem/Informal",
            "formal": "💼 Formal",
            "urgencia": "🔥 Urgência/Oferta"
        }[x]
    )

# Botão gerar
if st.button("🚀 GERAR LEGENDAS"):
    if not titulo or len(titulo.strip()) < 3:
        st.error("❌ Digite pelo menos 3 caracteres!")
    else:
        with st.spinner("⏳ Gerando legendas..."):
            try:
                api_key = st.secrets["GROQ_API_KEY"]
                client = Groq(api_key=api_key)

                estilos = {
                    "jovem": "linguagem jovem com girias e emojis",
                    "formal": "linguagem formal e profissional",
                    "urgencia": "urgencia e chamada para acao",
                }
                estilo_desc = estilos[estilo]

                prompt = f"""Especialista em marketing Shopee.
Gere {quantidade} legendas para: {titulo}
Estilo: {estilo_desc}
Max 150 caracteres cada com emojis.

RETORNE APENAS ESTE JSON SEM EXPLICACOES:
[
  {{"legenda": "texto aqui", "chars": 100}},
  {{"legenda": "texto aqui", "chars": 100}}
]"""

                response = client.chat.completions.create(
                    model="llama3-8b-8192",
                    messages=[{"role": "user", "content": prompt}],
                    temperature=0.7,
                )

                texto = response.choices[0].message.content
                texto = texto.replace("```json","").replace("```","").strip()
                legendas = json.loads(texto)

                st.markdown("---")
                st.markdown(f"### ✅ {len(legendas)} Legendas Geradas!")

                for i, item in enumerate(legendas):
                    legenda = item["legenda"][:150]
                    chars = len(legenda)
                    st.markdown(f"""
                    <div class="legenda-box">
                        <p style="font-size:15px;color:#333;">{legenda}</p>
                        <p style="font-size:12px;color:#999;">
                            {chars} caracteres
                        </p>
                    </div>
                    """, unsafe_allow_html=True)
                    st.code(legenda, language=None)

            except json.JSONDecodeError:
                st.error("❌ Erro ao processar resposta da IA. Tente novamente!")
            except Exception as e:
                st.error(f"❌ Erro: {str(e)}")
