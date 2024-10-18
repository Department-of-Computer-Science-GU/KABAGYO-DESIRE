# Import necessary libraries
import socketio
import hashlib
import base64
from cryptography.hazmat.primitives.ciphers.aes import AES256_CBC
from cryptography.hazmat.primitives import padding
from cryptography.hazmat.backends import default_backend

# Client-side implementation of a secure messaging system
class SecureMessagingClient(socketio.Client):
    def __init__(self, username, server_url):
        super().__init__()
        self.username = username
        self.server_url = server_url
        self.shared_secrets = {}  # Dictionary to store shared secrets for each user pair

    def connect(self):
        print(f"Connecting client {self.username} to {self.server_url}")
        self.connect(self.server_url)

    def handle_connect(self):
        print(f"Client {self.username} connected to the server")

    def handle_authenticate(self, data):
        if data["status"] == "success":
            print(f"Authentication successful for {self.username}")
            self.shared_secrets[data["recipient"]] = generate_shared_secret(self.username, data["recipient"])
            self.send({"type": "start_conversation", "recipient": data["recipient"]})
        else:
            print(f"Authentication failed for {self.username}")

    def handle_start_conversation(self, data):
        print(f"Starting conversation with {data['recipient']} for {self.username}")
        self.send({"type": "send_message", "message": f"Hello from {self.username}!"})

    def handle_send_message(self, data):
        message = data["message"]
        encrypted_msg = encrypt_message(self.shared_secrets[data["recipient"]], message)
        self.emit("receive_message", {"sender": self.username, "message": encrypted_msg}, broadcast=True)

    def handle_receive_message(self, data):
        sender = data["sender"]
        encrypted_msg = data["message"]
        decrypted_msg = decrypt_message(self.shared_secrets[sender], encrypted_msg)
        print(f"Received message from {sender}: {decrypted_msg}")

# Helper functions
def generate_shared_secret(username1, username2):
    # Generate a shared secret based on usernames
    combined_username = username1 + username2
    return hashlib.sha256(combined_username.encode()).digest()

def encrypt_message(shared_secret, plaintext):
    # Encrypt message using AES-256-CBC
    key = shared_secret[:16]  # First 128 bits for CBC mode
    iv = shared_secret[16:32]  # Next 128 bits for IV
    cipher = AES256_CBC(key, iv)
    
    padder = padding.PKCS7(128).padder()
    padded_data = padder.update(plaintext.encode())
    padded_data += padder.finalize()
    
    return base64.b64encode(iv + cipher.encrypt(padded_data))

def decrypt_message(shared_secret, ciphertext):
    # Decrypt message using AES-256-CBC
    encrypted_data = base64.b64decode(ciphertext)
    iv = encrypted_data[:16]
    cipher = AES256_CBC(shared_secret[:16], iv)
    decrypted_padded = cipher.decrypt(encrypted_data[16:])
    unpadder = padding.PKCS7(128).unpadder()
    return unpadder.update(decrypted_padded).decode()

if __name__ == "__main__":
    username = input("Enter your username: ")
    server_url = "http://localhost:5000"
    
    client = SecureMessagingClient(username, server_url)
    client.connect()
    
    # Handle events
    client.on('connect', client.handle_connect)
    client.on('authenticate', client.handle_authenticate)
    client.on('start_conversation', client.handle_start_conversation)
    client.on('send_message', client.handle_send_message)
    client.on('receive_message', client.handle_receive_message)

    # Run the event loop
    client.wait()
