import streamlit as st
import pandas as pd
#langchain puede interactuar con modelos de lenguajes a gran escala
#langchain_experimental nos ayuda aque interactue directamente con pandas, poder hacerle preguntas sobre la base de datos
#langchain_groq interectua directamente con la API de groq.com
#tabule nos da las respuesta entablas o listas
from langchain_experimental.agents import create_pandas_dataframe_agent#podemos iteractuar con la IA
from langchain_groq import ChatGroq#nos conectamos con groq.com

st.set_page_config('LLMs con DataFrames')
st.title('LLMs con DataFrames')
st.subheader('Elaborado por Brusly')

#ejecutamos el ChatGroup
model = ChatGroq(
    model='llama3-70b-8192',
    temperature=0,#la precision es muy exacta en las respuesta quenos da
    max_tokens=None,#cantidad de caracteres que podemos enviar por cada pregunta
    max_retries=2,#cantidad de intentos para mejorar la respuesta que nos da la IA
    api_key=st.secrets['groq']['API_KEY'],#esta informacion esta en el archivo secrets.py
)


#inicializo una lista vacia efectivo para guarar chats
if 'messages' not in st.session_state:
    st.session_state.messages=[]


#borra todos los mensajes del chat actual
def reloadChat():
    st.session_state.messages=[]

file = st.file_uploader('Elige un arhivo csv', type=['csv','xlsx','xls','txt','json'],on_change=reloadChat)

if file is not None:
    df = pd.read_csv(file)
    agent = create_pandas_dataframe_agent(model,df,allow_dangerous_code=True)



if prompt := st.chat_input('Pregunta'):#Limpio el historial del chat cada vez que se escribe una pregunta

    st.session_state.messages = []#reicinico la lista a vacia
    prompt_final = f'eres una experta en datos,dame todas tus respuestas en español con la siguiente pregunta {prompt}, y caundo  pida mas de un registro damelo en tablas o listas de markdown '
    with st.chat_message('user'):
        st.markdown(prompt)#se visualiza el mensaje del usuario
        st.session_state.messages.append({'role':'user','content':prompt_final})

    with st.spinner('Validando datos...'):
            response = agent.run(st.session_state.messages)

        #la respuesta de la IA
    with st.chat_message('assistant'):
            st.markdown(response)


    st.session_state.messages.append({'role':'assistant','content':response})                       

