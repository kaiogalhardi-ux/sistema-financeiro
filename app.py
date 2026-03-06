import streamlit as st
import json
import os
import pandas as pd
import matplotlib.pyplot as plt
from fpdf import FPDF

ARQUIVO="dados.json"

def carregar():
    if os.path.exists(ARQUIVO):
        with open(ARQUIVO,"r") as f:
            return json.load(f)
    return {"membros":[],"clientes":[],"despesas":[]}

def salvar(d):
    with open(ARQUIVO,"w") as f:
        json.dump(d,f)

dados=carregar()

st.title("Sistema Financeiro")
st.write("Guia Online Parapuã")
st.write("Direitos reservados a Kaio Marin")

menu=st.sidebar.selectbox("Menu",[
"Adicionar membro",
"Adicionar cliente",
"Adicionar despesa",
"Relatório financeiro"
])

# ---------------- MEMBROS ----------------

if menu=="Adicionar membro":

    st.header("Cadastrar membro")

    nome=st.text_input("Nome do membro")

    if st.button("Cadastrar membro"):
        if nome:
            dados["membros"].append(nome)
            salvar(dados)
            st.success("Membro cadastrado")

    st.subheader("Membros cadastrados")

    for i,m in enumerate(dados["membros"]):

        col1,col2=st.columns([4,1])

        col1.write(m)

        if col2.button("Excluir",key=f"m{i}"):
            dados["membros"].pop(i)
            salvar(dados)
            st.experimental_rerun()

# ---------------- CLIENTES ----------------

if menu=="Adicionar cliente":

    st.header("Cadastrar cliente")

    cliente=st.text_input("Nome do cliente")
    valor=st.number_input("Valor recebido",0.0)

    if len(dados["membros"])>0:
        membro=st.selectbox("Quem recebeu",dados["membros"])
    else:
        st.warning("Cadastre um membro primeiro")
        membro=None

    if st.button("Adicionar cliente"):
        if cliente and membro:
            dados["clientes"].append({
                "cliente":cliente,
                "valor":valor,
                "membro":membro
            })
            salvar(dados)
            st.success("Cliente registrado")

    st.subheader("Clientes registrados")

    for i,c in enumerate(dados["clientes"]):

        col1,col2=st.columns([5,1])

        col1.write(f'{c["cliente"]} - R${c["valor"]} - {c["membro"]}')

        if col2.button("Excluir",key=f"c{i}"):
            dados["clientes"].pop(i)
            salvar(dados)
            st.experimental_rerun()

# ---------------- DESPESAS ----------------

if menu=="Adicionar despesa":

    st.header("Registrar despesa")

    descricao=st.text_input("Descrição da despesa")
    valor=st.number_input("Valor da despesa",0.0)

    if len(dados["membros"])>0:
        membro=st.selectbox("Quem pagou",dados["membros"])
    else:
        st.warning("Cadastre um membro primeiro")
        membro=None

    if st.button("Registrar despesa"):
        if descricao and membro:
            dados["despesas"].append({
                "descricao":descricao,
                "valor":valor,
                "membro":membro
            })
            salvar(dados)
            st.success("Despesa registrada")

    st.subheader("Despesas registradas")

    for i,d in enumerate(dados["despesas"]):

        col1,col2=st.columns([5,1])

        col1.write(f'{d["descricao"]} - R${d["valor"]} - pago por {d["membro"]}')

        if col2.button("Excluir",key=f"d{i}"):
            dados["despesas"].pop(i)
            salvar(dados)
            st.experimental_rerun()

# ---------------- RELATÓRIO ----------------

if menu=="Relatório financeiro":

    total=0
    recebido={m:0 for m in dados["membros"]}
    despesas={m:0 for m in dados["membros"]}

    for c in dados["clientes"]:
        total+=c["valor"]
        recebido[c["membro"]]+=c["valor"]

    total_despesas=0

    for d in dados["despesas"]:
        total_despesas+=d["valor"]
        despesas[d["membro"]]+=d["valor"]

    lucro=total-total_despesas

    st.header("Resumo financeiro")

    st.write("Total arrecadado:",total)
    st.write("Total despesas:",total_despesas)
    st.write("Lucro:",lucro)

    if len(dados["membros"])>0:

        divisao=lucro/len(dados["membros"])

        st.subheader("Divisão por membro")

        tabela=[]

        for m in dados["membros"]:

            saldo=recebido[m]-despesas[m]

            diferenca=saldo-divisao

            st.write("-----")
            st.write("Membro:",m)
            st.write("Recebeu:",recebido[m])
            st.write("Pagou despesas:",despesas[m])
            st.write("Saldo:",saldo)
            st.write("Deveria receber:",divisao)

            if diferenca>0:
                st.write("Deve pagar:",diferenca)
            else:
                st.write("Deve receber:",abs(diferenca))

            tabela.append({
                "Membro":m,
                "Recebeu":recebido[m],
                "Pagou despesas":despesas[m],
                "Saldo":saldo
            })

        # -------- GRAFICO --------

        if len(dados["clientes"])>0:

            nomes=[c["cliente"] for c in dados["clientes"]]
            valores=[c["valor"] for c in dados["clientes"]]

            fig,ax=plt.subplots()

            ax.bar(nomes,valores)

            ax.set_title("Faturamento por cliente")

            st.pyplot(fig)

        # -------- EXCEL --------

        if st.button("Exportar Excel"):

            df=pd.DataFrame(tabela)

            df.to_excel("relatorio_financeiro.xlsx",index=False)

            st.success("Arquivo Excel gerado")

        # -------- PDF --------

        if st.button("Gerar PDF"):

            pdf=FPDF()

            pdf.add_page()

            pdf.set_font("Arial",size=12)

            pdf.cell(200,10,"Sistema Financeiro",ln=True)
            pdf.cell(200,10,"Guia Online Parapua",ln=True)
            pdf.cell(200,10,"Direitos reservados a Kaio Marin",ln=True)

            pdf.cell(200,10,f"Total arrecadado: {total}",ln=True)
            pdf.cell(200,10,f"Total despesas: {total_despesas}",ln=True)
            pdf.cell(200,10,f"Lucro: {lucro}",ln=True)

            pdf.output("relatorio_financeiro.pdf")

            st.success("PDF gerado")
