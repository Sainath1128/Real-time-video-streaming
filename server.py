import socket, cv2, pickle, struct, imutils,os

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
interface_name = "wlp4s0"
host_ip = os.popen('ip addr show wlp4s0').read().split("inet ")[1].split("/")[0]
print('HOST IP:', host_ip)
port = 9999
socket_address = (host_ip, port)

server_socket.bind(socket_address)
server_socket.listen(5)
print("LISTENING AT:", socket_address)

while True:
    client_socket, addr = server_socket.accept()
    print('GOT CONNECTION FROM:', addr)
    if client_socket:
        vid = cv2.VideoCapture(0)

        while vid.isOpened():
            img, frame = vid.read()
            frame = imutils.resize(frame, width=320)
            a = pickle.dumps(frame)
            message = struct.pack("Q", len(a)) + a
            client_socket.sendall(message)

            cv2.imshow('TRANSMITTING VIDEO', frame)
            if cv2.waitKey(1) == '13':
                client_socket.close()
