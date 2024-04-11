import streamlit as st
from langchain import PromptTemplate
#from langchain.llms import OpenAI #so vananenud rida ning asendatud allolevaga
from langchain_community.llms import OpenAI
import os

template = """
 Te olete turunduse kopeerikirjutaja, kellel on 20 aastat kogemust. Te analüüsite kliendi tausta, et kirjutada isikupärastatud toote kirjeldus, mida saab ainult see klient; 
    TOOTE sisendtekst: {content};
    KLIENDI vanuserühm (a): {agegroup};
    KLIENDI põhiline xyz: {xyz};
    ÜLESANNE: Kirjutage toote kirjeldus, mis on kohandatud sellele kliendile vanuserühma ja xyz järgi. Kasutage vanuserühma spetsiifilist slängi.;
    FORMAAT: Esitage tulemus järgmises järjekorras: (TOOTE KIRJELDUS), (EELISED), (KASUTUSJUHT);
    TOOTE KIRJELDUS: kirjeldage toodet 5 lauses;
    EELISED: kirjeldage 3 lauses, miks see toode on täiuslik, arvestades kliendi vanuserühma ja xyz;
    KASUTUSJUHT: kirjutage lugu 5 lauses, näites nädalavahetuse tegevusest, arvestades xyz {xyz} ja vanuse {agegroup}, kirjutage lugu esimeses isikus, näide "Alustasin laupäeva hommikut ...";
"""

prompt = PromptTemplate(
    input_variables=["agegroup", "xyz", "content"],
    template=template,
)

def load_LLM(openai_api_key):
    """Loogika selleks, et laadida soovitud ahel."""
    # Veenduge, et teie openai_api_key oleks seadistatud keskkonnamuutujana
    llm = OpenAI(model_name='gpt-3.5-turbo-instruct', temperature=.7, openai_api_key=openai_api_key)
    return llm

st.set_page_config(page_title="Isikupärastatud klienditeksti konverter", page_icon=":robot:")
st.header("Isikupärastatud turundusteksti konverter")

col1, col2 = st.columns(2)

with col1:
    st.markdown("Otstarve: tootekirjelduste isikupärastamine iga kliendi või kliendigrupi jaoks; väljundtekst on kohandatud kliendi a) vanuserühma ja b) xyz-ga; sisendtekstiks on neutraalne tootekirjeldus. \
    \n\n Kasutusjuhend: 1) valmistage ette tootekirjeldus (sisendtekst). 2) määrake kliendisegmendid vastavalt vanuserühmadele ja xyz kombinatsioonidele. 3) sisestage iga kliendisegmendi jaoks eeltoodud teave järjestikku rakenduse kasutajaliidesesse, saadke ära. \
    4) kopeerige iga kliendisegmendi jaoks rakenduse väljundtekst vastava toote tutvustuslehele.")

with col2:
    st.image(image='companylogo.jpg', caption='Looduslikud ja tervislikud särgid kõigile')

st.markdown("## Sisestage oma sisu konverteerimiseks")

def get_api_key():
    openai_api_key = os.getenv("OPENAI_API_KEY")
    if openai_api_key:
        return openai_api_key
    # Kui OPENAI_API_KEY keskkonnamuutujat ei ole seadistatud, küsige kasutajalt sisendit
    input_text = st.text_input(label="OpenAI API võti", placeholder="Näide: sk-2twmA8tfCb8un4...", key="openai_api_key_input")
    return input_text

openai_api_key = get_api_key()

col1, col2 = st.columns(2)
with col1:
    option_agegroup = st.selectbox(
        'Millist vanuserühma soovite oma sisu sihtida?',
        ('9-15', '16-19', '20-29', '30-39', '40-49', '50-59', '60-69', '70-79', '80-100'))
    
def get_hobby():
    input_text = st.text_input(label="Kliendi xyz", key="xyz_input")
    return input_text

xyz_input = get_hobby()

def get_text():
    input_text = st.text_area(label="Sisu sisend", label_visibility='collapsed', placeholder="Teie sisu...", key="content_input")
    return input_text

content_input = get_text()

if len(content_input.split(" ")) > 700:
    st.write("Sisestage lühem sisu. Maksimaalne pikkus on 700 sõna.")
    st.stop()

def update_text_with_example():
    print ("uuendatud")
    st.session_state.content_input = "Kollektsiooni The Korsars sügis-talv 23/24 kuuluv MILAN naisteparka saab energia Karl Korsari särtsakast LILLY kangatrükist. See omanäoline disain tõstab teie tuju ja pöörab pead, eriti nendel süngetel vihmastel päevadel."

st.button("*TEKSTI GENEREERIMINE*", type='secondary', help="Klõpsake sisu konverteerimise näidise nägemiseks.", on_click=update_text_with_example)

st.markdown("### Teie isikupärastatud kliendisisu:")

if content_input:
#    if not openai_api_key:
#        st.warning('Please insert OpenAI API Key. Instructions [here](https://help.openai.com/en/articles/4936850-where-do-i-find-my-secret-api-key)', icon="⚠️")
#        st.stop()

    llm = load_LLM(openai_api_key=openai_api_key)

    prompt_with_content = prompt.format(agegroup=option_agegroup, xyz=xyz_input, content=content_input)

    formatted_content = llm(prompt_with_content)

    st.write(formatted_content)
