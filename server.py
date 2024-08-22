import socket
import threading
import time

# Create a connection
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
#AF_NET is for ipv4 and SOCK_STREAM is for TCP connection

# Define the server address and port
server_address = ('LocalHost', 12345)

# Bind the socket to the server address
server_socket.bind(server_address)
#bind accepts 2 params as a tuple, i.e., host and port number
#we use bind bcoz we want the server to listen to the client


# Listen for incoming connections
server_socket.listen(2)  # Two players will connect
#queue will be created 
#listen is like a queue where all the requests will go on getting added and when the queue is full then we give message to the client


print('Waiting for 2 players to connect...')

# these are the quiz questions
questions = [
    "How many layers does the OSI model have?\na) 7\nb) 5\nc) 4\n",
    "What does status code 301 mean?\na) Moved permanently\nb) Bad Request\nc) OK\n",
    "TCP is \na) Connection-Oriented\nb) Connectionless\nc) None of these\n"
]

answers = ['a', 'a', 'a']  # Correct answers for each question

# Function to handle a client connection
def handle_client(client_socket, player_id):
    print(f'Player {player_id} connected.')

    player_score = 0 #initially score is initialzied to 0

    for question in questions:
        client_socket.sendall(question.encode()) #questions are sent to the client
        response = client_socket.recv(1024).decode().strip().lower() #we recieve answer from the client

        if response == answers[questions.index(question)]:  #if answer is correct then player gets 1 point
            player_score += 1
            client_socket.sendall("Correct Answer!\n".encode())
        else: #For wrong answer
            client_socket.sendall(f"Wrong Answer!\n Correct answer is {answers[questions.index(question)]}\n".encode())

    client_socket.sendall(f"Your final score: {player_score}\n".encode())# Displays the final score.
    #client_socket.close()
    print(f'Player {player_id} disconnected.')

    return player_score

# Function to accept incoming connections and start a new thread for each client
def accept_connections():
    player_scores = []
    clients = []

    while len(clients) < 2:
        client_socket, client_address = server_socket.accept()
        clients.append((client_socket, client_address))
        print(f'Player {len(clients)} connected.')

    start_time = time.time()

    for player_id, (client_socket, _) in enumerate(clients, 1):
        thread = threading.Thread(target=handle_client, args=(client_socket, player_id))
        thread.start()
        player_scores.append(thread)

    # Wait for all threads to finish or until one minute is up
    for thread in player_scores:
        thread.join()

    '''end_time = time.time()
    elapsed_time = end_time - start_time

    # Determine the winner or if it's a tie
    if elapsed_time >= 60:
        print("Time's up! Quiz ended.")
    else:
        if player_scores[0] > player_scores[1]:
            print(f"Player 1 wins with {player_scores[0]} points!")
        elif player_scores[1] > player_scores[0]:
            print(f"Player 2 wins with {player_scores[1]} points!")
        else:
            print("It's a tie!")'''
    

# Start accepting connections
accept_connections()
