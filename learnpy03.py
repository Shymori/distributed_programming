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
    with xmlrpc.client.ServerProxy('http://127.0.0.1:50007', verbose=True) as proxy:

        print(proxy.fn_add(5, 4))
        print(proxy.fn_mul(5, 4))
        print(proxy.fn_sub(5, 4))
        print(proxy.fn_div(5, 4))

