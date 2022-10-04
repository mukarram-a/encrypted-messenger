'''

Sends and recieves messages to communicate with the server.
Allows user to upload public posts or change their biography.
"send()" function called from 'a5.py' 

'''


# Mukarram A.
# Ds_client.py

#IP Address// Server : 168.235.86.101
#Port: 3021

import socket, json, time
from unittest.mock import NonCallableMagicMock
from Ds_protocol import join, posting, bio1, extract_json


def send(server:str, port:int, username:str, password:str, message:str, bio:str=None, param_pub_key:str=None, nap=None):        #function that allows a username, password, message, and bio to be sent to a server and process the responses
  '''
  The send function joins a ds server and sends a message, bio, or both

  :param server: The ip address for the ICS 32 DS server.
  :param port: The port where the ICS 32 DS server is accepting connections.
  :param username: The user name to be assigned to the message.
  :param password: The password associated with the username.
  :param message: The message to be sent to the server.
  :param bio: Optional, a bio for the user.
  '''
  if type(server) != str:                                               #error checking for invalid inputs and input type. Returns False if type/input is invalid
    print('TypeError. Server should be a string. Returning...')
    return False

  if type(port) != int:
    print('TypeError. Port should be an int. Returning...')
    return False

  if type(username) != str:
    print('TypeError. Username should be a string. Returning...')
    return False

  if username == '':
    print('Username can not be empty. Returning...')
    return False

  if ' ' in username:
    print('Username can not contain whitespace. Returning...')
    return False

  if type(password) != str:
    print('TypeError. Password should be a string. Returning...')
    return False

  if password == '':
    print('Password can not be empty. Returning...')
    return False

  if ' ' in password:
    print('Password can not contain whitespace. Returning...')
    return False

  if bio.strip() == '':
    print('Bio cannot be empty. Returning...')
    return False

  if bio is not None:
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client:   #establishes the connection between the program and the server
      try:
        client.connect((server, port))                                  #connects to the server using the server and port input parameterss
      except (socket.gaierror, OSError):
        print('Connection refused, check ip and port. Returning...')    #if the connection is refused, the program will return False and print out an error message
        return False
      send = client.makefile('w')                                       #enables the program connection to send data to the server
      recv = client.makefile('r')                                       #enables the program connection to recieve data from the server
      print('--------------start--------------')                        #formatting to make readability of output easier
      print()
      print('( Client has connected to', server, 'on', port, ')')       #prints a message to the user once the program has successfully connected to the server

      
      send.write(join(username, password, param_pub_key) + '\r\n')      #send the username and password to the server
      send.flush()                                                      #ensures that all data is passed to the server
      json_msg = recv.readline()                                        #recieves message from the server and stores it as a variable
      x = extract_json(json_msg)                                        #takes the variable for the server response and uses a function in ds_protocol to covert it to a namedtuple
      invalid_search = x[0]
      print(x[0])                                                       #prints server message to user
      
      if invalid_search == 'Invalid join message. Username or password does not meet server requirements.':     #if an error message is detected from the server, return False
        print()
        print('--------------end--------------')
        print()
        return False
      
      server_pub_key = x.token                                           #stores the server-sent token as variable for reuse later in code


      if message != '':                                                 #if the message parameter is empty, the program will connect to the server and only update the user's bio
        send.write(posting(param_pub_key, nap.encrypt_entry(message, server_pub_key))  + '\r\n')                    #uses the posting function to create a post in json format and sends the post and token to the server
        send.flush()                                                    
        json_msg = recv.readline()                                      #recieves message from the server and stores it as a variable
        x = extract_json(json_msg)                                      #takes the variable for the server response and uses a function in ds_protocol to covert it to a namedtuple
        print(x[0])                                                     #prints server message to user


      send.write(bio1(param_pub_key, nap.encrypt_entry(bio, server_pub_key)) + '\r\n')                             #uses the bio1 function to create a bio in json format and sends the bio and token to the server
      send.flush()                                                      #ensures that all data is passed to the server
      json_msg = recv.readline()                                        #recieves message from the server and stores it as a variable
      x = extract_json(json_msg)                                        #takes the variable for the server response and uses a function in ds_protocol to covert it to a namedtuple
      print(x[0])                                                       #prints server message to user
      print()
      print('--------------end--------------')                          #formatting to make readability of output easier
      print()
      return True
  else:
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client:   #establishes the connection between the program and the server
      try:
        client.connect((server, port))                                  #connects to the server using the server and port input parameters
      except (socket.gaierror, OSError):
          print('Connection refused, check ip and port. Returning...')  #if the connection is refused, the program will return False and print out an error message
          return False

      send = client.makefile('w')                                       #enables the program connection to send data to the server
      recv = client.makefile('r')                                       #enables the program connection to recieve data from the server

      print('--------------start--------------')                        #formatting to make readability of output easier
      print()
      print('( Client has connected to', server, 'on', port, ')')

      send.write(join(username, password, param_pub_key) + '\r\n')                     #uses the join function to send the username and password to the server
      send.flush()                                                      #ensures that all data is passed to the server
      json_msg = recv.readline()                                        #recieves message from the server and stores it as a variable
      x = extract_json(json_msg)                                        #takes the variable for the server response and uses a function in ds_protocol to covert it to a namedtuple
      invalid_search = x[0]
      print(x[0])                                                       #prints server message to user
      
      if invalid_search == 'Invalid join message. Username or password does not meet server requirements.':      #if an error message is detected from the server, return False
        print()
        print('--------------end--------------')                          #formatting to make readability of output easier
        print()
        return False
      
      server_pub_key = x.token                                                      #stores the server-sent token as variable for reuse later in code
      
      send.write(posting(param_pub_key, nap.encrypt_entry(message, server_pub_key)) + '\r\n')                      #uses the posting function to create a post in json format and sends the post and token to the server
      send.flush()                                                      #ensures that all data is passed to the server
      json_msg = recv.readline()                                        #recieves message from the server and stores it as a variable
      x = extract_json(json_msg)                                        #takes the variable for the server response and uses a function in ds_protocol to covert it to a namedtuple
      print(x[0])                                                       #prints server message to user
      print()
      print('---------------end---------------')                        #formatting to make readability of output easier
      print()
      return True
  