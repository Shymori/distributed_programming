import argparse
import sys
import xmlrpc.client
import xmlrpc.server

# ArgParse auxilia a interpretar a linha de comando facilmente
parser = argparse.ArgumentParser()
parser.add_argument('--server', action='store_true', help='Usado para iniciar a aplicação como servidor')
parser.add_argument('--host', default='localhost', help='Nome ou endereço do servidor')
parser.add_argument('--port', type=int, default=50007, help='Porta do servidor')
args = parser.parse_args()

Address = args.host
Port = args.port

if args.server:
    # Função para somar inteiros
    def fn_add_integers(a, b):
        return a + b

    # Função para somar números de ponto flutuante
    def fn_add_floats(a, b):
        return a + b

    # Função para somar arrays
    def fn_add_arrays(a, b):
        if not (isinstance(a, list) and isinstance(b, list)):
            raise TypeError("Ambos os parâmetros devem ser listas")
        if len(a) != len(b):
            raise ValueError("As listas devem ter o mesmo comprimento")
        return [x + y for x, y in zip(a, b)]

    with xmlrpc.server.SimpleXMLRPCServer((Address, Port)) as server:
        server.register_introspection_functions()
        server.register_multicall_functions()

        # Registrar funções
        server.register_function(fn_add_integers, 'fn_add_integers')
        server.register_function(fn_add_floats, 'fn_add_floats')
        server.register_function(fn_add_arrays, 'fn_add_arrays')

        print(f"Servidor rodando em http://{Address}:{Port}/")
        try:
            server.serve_forever()
        except KeyboardInterrupt:
            sys.exit(0)
else:
    with xmlrpc.client.ServerProxy(f'http://{Address}:{Port}', verbose=True) as proxy:
        # Testar as funções
        print("Soma de inteiros:", proxy.fn_add_integers(5, 4))
        print("Soma de floats:", proxy.fn_add_floats(5.5, 4.2))
        print("Soma de arrays:", proxy.fn_add_arrays([1, 2, 3], [4, 5, 6]))
