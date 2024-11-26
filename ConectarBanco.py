from sshtunnel import SSHTunnelForwarder
import paramiko
import time

class ConectarBanco:
    def __init__(self, ssh_host, ssh_port, ssh_username, ssh_key_path):
        self.ssh_host = ssh_host
        self.ssh_port = ssh_port
        self.ssh_username = ssh_username
        self.ssh_key_path = ssh_key_path
        self.tunnel = None
        self.key = paramiko.RSAKey.from_private_key_file(self.ssh_key_path)
        self.hostBanco1 = 'host'
        self.hostBanco2 = 'host'
        self.hostBanco3 = 'host'
        self.hostBanco4 = 'host'

    def conectar(self):
        while True:
            try:
                print("Conectando...")
                self.tunnel = SSHTunnelForwarder(
                    (self.ssh_host, self.ssh_port),
                    ssh_username=self.ssh_username,
                    ssh_pkey=self.key,
                    remote_bind_addresses=[
                        (self.hostBanco1, 3306), 
                        (self.hostBanco2, 3306), 
                        (self.hostBanco3, 3306), 
                        (self.hostBanco4, 3306)
                    ],
                    local_bind_addresses=[
                        ('127.0.0.1', 4400), 
                        ('127.0.0.1', 4500), 
                        ('127.0.0.1', 4600), 
                        ('127.0.0.1', 4700)
                    ]
                )
                self.tunnel.start()
                print("Conectou.")
                return
            except Exception as e:
                print(f"Deu ruim piazão: {e}. Reset em 5 segundos...")
                time.sleep(5)

    def manter_conexao(self):
        while True:
            try:
                if self.tunnel and self.tunnel.is_active:
                    print("Conexão está ativa.")
                else:
                    print("Conexão perdida. Tentando reconectar...")
                    self.conectar_tunel()
                time.sleep(10)
            except KeyboardInterrupt:
                print("Deu ruim piazão. Tunel sendo fechado...")
                self.fechar_conexao()
                break

    def fechar_conexao(self):
        if self.tunnel:
            self.tunnel.stop()
            print("Conexão fechada.")

if __name__ == "__main__":
    ssh_host = ''       # Host do SSH
    ssh_port = 22       # Porta do SSH
    ssh_username = ''   # user do SSH
    ssh_key_path = ''   # Caminho para a chave SSH (formato .pem)

    manager = ConectarBanco(ssh_host, ssh_port, ssh_username, ssh_key_path)
    manager.conectar()
    manager.manter_conexao()
