import streamlit as st
import requests
import json

st.set_page_config(
    page_title="GIF Huber - Legendas Shopee",
    page_icon="🛍️",
    layout="centered"
)

st.title("🛍️ GIF Huber - Legendas Shopee")
st.markdown("---")

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

if st.button("🚀 GERAR LEGENDAS", use_container_width=True):
    if not titulo or len(titulo.strip()) < 3:
        st.error("❌ Digite pelo menos 3 caracteres!")
    else:
        with st.spinner("⏳ Gerando legendas..."):
            try:
                api_key = st.secrets["GROQ_API_KEY"]

                estilos = {
                    "jovem": "linguagem jovem com girias e emojis",
                    "formal": "linguagem formal e profissional",
                    "urgencia": "urgencia e chamada para acao",
                }

                prompt = f"""Especialista em marketing Shopee.
Gere {quantidade} legendas para: {titulo}
Estilo: {estilos[estilo]}
Max 150 caracteres cada com emojis.
RETORNE APENAS JSON SEM EXPLICACOES:
[{{"legenda": "texto aqui", "chars": 100}}]"""

                response = requests.post(
                    "https://api.groq.com/openai/v1/chat/completions",
                    headers={
                        "Authorization": f"Bearer {api_key}",
                        "Content-Type": "application/json"
                    },
                    json={
                        "model": "llama3-8b-8192",
                        "messages": [
                            {"role": "user", "content": prompt}
                        ],
                        "temperature": 0.7
                    }
                )

                data = response.json()
                texto = data["choices"][0]["message"]["content"]
                texto = texto.replace("```json","").replace("```","").strip()
                legendas = json.loads(texto)

                st.markdown("---")
                st.success(f"✅ {len(legendas)} Legendas Geradas!")

                for i, item in enumerate(legendas, 1):
                    legenda = item["legenda"][:150]
                    chars = len(legenda)
                    st.markdown(f"**Legenda {i}** · {chars} caracteres")
                    st.info(legenda)
                    st.code(legenda, language=None)
                    st.markdown("---")

            except json.JSONDecodeError:
                st.error("❌ IA retornou formato inválido. Tente novamente!")
            except Exception as e:
                st.error(f"❌ Erro: {str(e)}")
