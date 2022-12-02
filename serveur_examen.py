import socket

host = "localhost" # "", "127.0.0.1
port = 10003

server_socket = socket.socket()
server_socket.bind((host, port))
server_socket.listen(1)

print('En attente du client')
conn, address = server_socket.accept()
print(f'Client connecté {address}')

msg = ""
while msg != "bye":
    # Réception du message du client
    msg = conn.recv(1024).decode() # message en by
    print(f"Message du chronomètre : {msg}")

# Fermeture
conn.close()
print("Fermeture de la socket client")
server_socket.close()
print("Fermeture de la socket serveur")
