menu = '''
[u] Cadastrar Usuário
[c] Criar conta
[d] Depositar
[s] Sacar
[e] Extrato
[q] Sair
'''

saldo = 0
limite = 500
registro_extrato = ''
clientes = []
contas = []
numero_conta_atual = 1

num_saques = 1
LIMITE_SAQUES = 3

def obter_conta_do_usuario(cpf, contas):
    for conta in contas:
        if conta['usuario']['cpf'] == cpf:
            return conta
    return None

def criar_cliente(clientes):
    print('Cadastro de usuário')
    nome = input("Digite o seu nome completo: ")
    data_nascimento = input("Digite a data de nascimento (dd/mm/aaaa): ")
    endereco = input("Digite seu endereço (Logradouro, Número, Bairro, Cidade/Sigla Estado): ")
    cpf = input ("Digite apenas os números do seu CPF: ")

    for cliente in clientes:
        if cliente['cpf'] == cpf:
            print("Usuário já cadastrado")
            return clientes
        else:
            novo_cliente = {
                'nome' : nome,
                'data_nascimento': data_nascimento,
                'endereco': endereco,
                'cpf': cpf
            }

            clientes.append(novo_cliente)
            print("Cliente cadastrado com sucesso")
            return clientes

def criar_conta(usuarios, contas, numero_conta_atual):
    print('Criação de conta')
    cpf = input("Digite apenas os números do CPF")
    usuario_encontrado = None

    for cliente in clientes:
        if cliente['cpf'] == cpf:
            usuario_encontrado = cliente
            break
    if not usuario_encontrado:
        print('Cliente não encontrado. Crie seu usuário para criar sua conta bancária.')
        return contas, numero_conta_atual

    nova_conta = {
        'agencia': '0001',
        'numero_conta': numero_conta_atual+1,
        'usuario': usuario_encontrado
    }

    contas.append(nova_conta)
    print(f'Sua conta foi criada com sucesso. Numero da conta: {numero_conta_atual}.')
    return contas, numero_conta_atual

def deposito(saldo, registro_extrato, contas, /):
    print('Depósito')
    cpf = input("Digite apenas os números do CPF: ")
    conta = obter_conta_do_usuario(cpf, contas)
    if conta is None:
        print("Você precisa ter uma conta para realizar um depósito.")
        return saldo, registro_extrato
    valor_deposito = float(input('Digite o valor do depósito: '))
    if valor_deposito > 0:
        saldo += valor_deposito
        print(f'R${valor_deposito} foi adicionado à conta.')
        registro_extrato += f'Foi adicionado R${valor_deposito} à conta.\n'
    else:
        print("Valor Inválido.")
    return saldo, registro_extrato

def saque(*, num_saques, saldo, registro_extrato, contas):
    print('Saque')
    cpf = input("Digite apenas os números do CPF: ")
    conta = obter_conta_do_usuario(cpf, contas)
    if conta is None:
        print("Você precisa ter uma conta para realizar um saque.")
        return num_saques, saldo, registro_extrato
    if num_saques <= LIMITE_SAQUES:
        valor_saque = float(input('Digite um valor para saque: '))
        if 0 < valor_saque <= saldo and valor_saque <= limite:
            saldo -= valor_saque
            print(f'R${valor_saque} foi sacado com sucesso.')
            registro_extrato += f'Foi realizado um saque de R${valor_saque} na conta.\n'
            num_saques += 1
        else:
            print('Valor inválido ou saldo indisponível.')
    else:
        print('Você atingiu o limite de saque.')
    return num_saques, saldo, registro_extrato

def extrato(saldo, /, *, registro_extrato, contas):
    print("Extrato:")
    cpf = input("Digite apenas os números do CPF: ")
    conta = obter_conta_do_usuario(cpf, contas)
    if conta is None:
        print("Você precisa ter uma conta para visualizar o extrato.")
        return saldo, registro_extrato
    print(f'O Saldo atual é R${saldo}\n')
    print(registro_extrato)
    return saldo, registro_extrato

while True:
    opcao = input(menu)
    if opcao == 'u':
        clientes = criar_cliente(clientes)
    if opcao == 'c':
        contas, numero_conta_atual = criar_conta(clientes, contas, numero_conta_atual)
    if opcao == 'd':
        saldo, registro_extrato = deposito(saldo, registro_extrato, contas)
    elif opcao == 's':
        num_saques, saldo, registro_extrato = saque(num_saques=num_saques, saldo=saldo, registro_extrato = registro_extrato, contas=contas)
    elif opcao == 'e':
        saldo, registro_extrato = extrato(saldo, registro_extrato=registro_extrato, contas=contas)
    elif opcao == 'q':
        print('Você escolheu sair do sistema.')
        break
    else:
        print('Operação Inválida. Por favor, selecione novamente a função desejada')
