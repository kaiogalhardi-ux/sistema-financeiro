import streamlit as st
import json
import os

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

if menu=="Adicionar membro":

    nome=st.text_input("Nome do membro")

    if st.button("Cadastrar membro"):
        dados["membros"].append(nome)
        salvar(dados)
        st.success("Membro cadastrado")

    st.subheader("Membros cadastrados")

    for m in dados["membros"]:
        st.write(m)


if menu=="Adicionar cliente":

    cliente=st.text_input("Nome do cliente")
    valor=st.number_input("Valor recebido",0.0)
    membro=st.selectbox("Quem recebeu",dados["membros"])

    if st.button("Adicionar cliente"):
        dados["clientes"].append({
        "cliente":cliente,
        "valor":valor,
        "membro":membro
        })
        salvar(dados)
        st.success("Cliente registrado")

    st.subheader("Clientes registrados")

    for c in dados["clientes"]:
        st.write(c["cliente"],"R$",c["valor"],"-",c["membro"])


if menu=="Adicionar despesa":

    descricao=st.text_input("Descrição da despesa")
    valor=st.number_input("Valor da despesa",0.0)
    membro=st.selectbox("Quem pagou",dados["membros"])

    if st.button("Registrar despesa"):
        dados["despesas"].append({
        "descricao":descricao,
        "valor":valor,
        "membro":membro
        })
        salvar(dados)
        st.success("Despesa registrada")

    st.subheader("Despesas registradas")

    for d in dados["despesas"]:
        st.write(d["descricao"],"R$",d["valor"],"- pago por",d["membro"])


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

        for m in dados["membros"]:

            saldo=recebido[m]-despesas[m]

            st.write("-----")
            st.write("Membro:",m)
            st.write("Recebeu:",recebido[m])
            st.write("Pagou despesas:",despesas[m])
            st.write("Saldo:",saldo)
            st.write("Deveria receber:",divisao)

            diferenca=saldo-divisao

            if diferenca>0:
                st.write("Deve pagar:",diferenca)

            else:
                st.write("Deve receber:",abs(diferenca))