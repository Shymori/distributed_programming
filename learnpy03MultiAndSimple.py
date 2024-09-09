import argparse
import sys
import xmlrpc.client
import xmlrpc.server

# ArgParse auxilia interpretar linha de comando facilemnte
parser = argparse.ArgumentParser()
parser.add_argument('--server', action='store_true', help='suado para inicia a aplicação como servidora')
parser.add_argument('--host', default='localhost', help='nome ou endereço do servidor')
parser.add_argument('--port', type=int, default=50007, help='porta do servidor')
args = parser.parse_args()

Address = args.host
Port = args.port

if args.server:
    
    with xmlrpc.server.SimpleXMLRPCServer((Address,Port)) as server:

            server.register_introspection_functions()
            server.register_multicall_functions()

            @server.register_function
            def fn_add(a,b):
                return a + b
            
            @server.register_function
            def fn_sub(a,b):
                return a - b

            @server.register_function
            def fn_mul(a,b):
                return a * b

            @server.register_function
            def fn_div(a,b):
                return a / b

            try:
                server.serve_forever()
            except KeyboardInterrupt:
                sys.Exit(0)
else:
    with xmlrpc.client.ServerProxy('http://127.0.0.1:50007',verbose=True) as proxy:
        a = proxy.fn_add(2, 3)
        b = proxy.fn_mul(a, 2)
        c = proxy.fn_sub(b, 5)
        d = proxy.fn_div(a, c)

        print("\nChamada simples:")
        print(f"a = {a}")
        print(f"b = {b}")
        print(f"c = {c}")
        print(f"d = {d}")

        multicall = xmlrpc.client.MultiCall(proxy)
        multicall.fn_add(2, 3)
        multicall.fn_mul(5, 5)
        multicall.fn_sub(7, 2)
        multicall.fn_div(40, 8)
        results = multicall()

        print("Multicall:")
        for result in results:
            print(result)

