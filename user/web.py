from cryptography.hazmat.primitives.asymmetric import ec
from cryptography.hazmat.primitives import serialization
import base64

# Generate a new EC key (P-256 curve)
private_key = ec.generate_private_key(ec.SECP256R1())

# Export private key in PEM format
private_pem = private_key.private_bytes(
    encoding=serialization.Encoding.PEM,
    format=serialization.PrivateFormat.PKCS8,
    encryption_algorithm=serialization.NoEncryption()
)

# Export public key in uncompressed point format (for VAPID)
public_key = private_key.public_key()
public_bytes = public_key.public_bytes(
    encoding=serialization.Encoding.X962,
    format=serialization.PublicFormat.UncompressedPoint
)

# Base64-url encode the keys
vapid_private_key = base64.urlsafe_b64encode(private_pem).decode('utf-8')
vapid_public_key = base64.urlsafe_b64encode(public_bytes).decode('utf-8')

print("Private Key:", vapid_private_key)
print("Public Key :", vapid_public_key)
