# Sistema de Planos de Negócio para Óticas

## Deployment no Hostinger - 18/06/2025 19:35

### Opção 1: Streamlit Cloud (Recomendada)
1. Criar repositório GitHub público
2. Upload destes arquivos
3. Deploy via https://share.streamlit.io/
4. Integrar no site via iframe

### Opção 2: VPS Hostinger
```bash
# Instalar Python e dependências
sudo apt update
sudo apt install python3 python3-pip
pip3 install -r requirements.txt

# Executar aplicação
streamlit run main.py --server.port 8501 --server.address 0.0.0.0
```

### Integração no Site WordPress/HTML
```html
<iframe 
    src="https://sua-app.streamlit.app" 
    width="100%" 
    height="800px" 
    frameborder="0"
    style="border: none; box-shadow: 0 4px 8px rgba(0,0,0,0.1);">
</iframe>
```

### Sistema Incluído
- Autenticação multi-usuário
- 12 etapas de plano de negócio
- Análise financeira completa
- Geração de relatórios PDF
- Sistema de precificação
- Calculadoras tributárias e trabalhistas

### Usuário Padrão
- Login: Rômulo
- Senha: 965874+Rr
- Pergunta de Segurança: "Qual sua primeira ótica de referência?"
- Resposta: "brasil ocular"

### Suporte
Para dúvidas sobre deployment, consultar deployment_guide.md
