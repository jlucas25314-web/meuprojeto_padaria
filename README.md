# Pão de Casa

Aplicação Django para uma padaria artesanal. O site público apresenta o cardápio e os detalhes de cada produto. A equipe autenticada pode cadastrar, editar e remover produtos; o painel administrativo do Django também está configurado.

## Funcionalidades

- Home responsiva com catálogo carregado do banco de dados.
- Listagem e página de detalhes dos produtos.
- Cadastro, edição e exclusão protegidos por login.
- Exclusão confirmada por formulário POST com proteção CSRF.
- Login nativo do Django e cadastro de produtos pelo admin.
- Seis produtos de demonstração adicionados pelas migrações iniciais.

## Executar localmente

No Windows PowerShell:

```powershell
python -m venv venv
venv\Scripts\Activate.ps1
pip install -r requirements.txt
$env:DJANGO_SECRET_KEY = (python -c "import secrets; print(secrets.token_urlsafe(50))").Trim()
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
```

Abra `http://127.0.0.1:8000/` para acessar o site. Entre em `/accounts/login/` para gerenciar o cardápio ou em `/admin/` para usar o painel administrativo. Os produtos de demonstração podem ser alterados ou removidos pela equipe.

## Personalização

Atualize nomes, descrições, preços e imagens dos produtos pelo site autenticado ou pelo admin. Endereço, horários e contato da padaria devem ser configurados com as informações reais antes da publicação. O Bootstrap e as fontes são carregados por CDN.

## Testes

```powershell
python manage.py test app
```

O servidor de desenvolvimento e as configurações padrão do projeto são para uso local; revise as configurações de segurança antes de publicar em produção.

`DJANGO_SECRET_KEY` é lida do ambiente e não deve ser enviada ao GitHub. Em produção, configure também `DJANGO_DEBUG=False` e `DJANGO_ALLOWED_HOSTS` com os domínios permitidos. Sem uma chave de ambiente, o modo local gera uma chave temporária; ela muda ao reiniciar o processo.