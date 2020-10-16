import socket
import DH as dh
from pyDes import *
import binascii


def Encriptado(texto):
   llave = '11223344'
   cipher = des(llave, CBC, "\0\0\0\0\0\0\0\0", pad=None, padmode=PAD_PKCS5)
   textoCifrado = cipher.encrypt(texto)
   text = binascii.hexlify(textoCifrado).decode()
   array = [textoCifrado, text]
   return array

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
arrayCifrado = Encriptado(texto)
archivo = open("mensajeentrada.txt","w")
archivo.write(arrayCifrado[1])
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
      cliente.send(arrayCifrado[1].encode('ascii'))
      break

cliente.close()
servidor.close()

print("Conexiones cerradas")
