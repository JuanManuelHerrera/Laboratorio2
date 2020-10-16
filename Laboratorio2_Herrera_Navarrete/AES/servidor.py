import socket
import DH as dh
from Cryptodome.Cipher import AES
from Cryptodome.Util.Padding import pad
import binascii


def Encriptado(texto):
   texto = texto.encode()
   key =  b'Sixteen byte key'
   cipher = AES.new(key, AES.MODE_CBC, iv=b'0123456789abcdef')
   padded_data = pad(texto, cipher.block_size)
   data = cipher.encrypt(padded_data)
   return data

servidor = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
servidor.bind(('',8050))
servidor.listen(1)
cliente, addr = servidor.accept()

#Llaves Publicas
array = [2305843009213693951,5614156465]

privateKey = 31 #Private-key

server = dh.DH_Endpoint(array[1], array[0], privateKey)
llaveParcial = str(server.generate_partial_key())

cont = 1 #Inicio de sesión

#Mensaje encriptado

archivo = open("mensajeentrada.txt","r")
texto = archivo.read()
archivo.close()

#3Des
data = Encriptado(texto)
dataE = binascii.hexlify(data).decode()
archivo = open("mensajeentrada.txt","w")
archivo.write(dataE)
archivo.close()

while True:
   if cont == 1:
      recibido = cliente.recv(1024)
      llaveParcialCliente = recibido.decode('utf-8')
      array.append(int(llaveParcialCliente))
      mensaje = llaveParcial
      cliente.send(mensaje.encode('ascii'))
      cont = 2

   elif cont == 2:
      recibido = cliente.recv(1024)
      fullKeyC = recibido.decode('utf-8')
      fullKeyS = str(server.generate_full_key(array[2]))
      if fullKeyS == fullKeyC:
         cont = 0
         mensaje = "Enlace conectado mediante Deffie Hellman's"
         cliente.send(mensaje.encode('ascii'))
      else:
         print("Error")
   else:
      cliente.send(dataE.encode('ascii'))
      break

cliente.close()
servidor.close()

print("Conexiones cerradas")
