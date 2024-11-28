import random
from sympy import mod_inverse

# Fonction pour vérifier si un nombre est premier
def is_prime(num):
    if num < 2:
        return False
    for i in range(2, int(num**0.5) + 1):
        if num % i == 0:
            return False
    return True

# Génère un candidat nombre premier
def generate_prime_candidate(length):
    # Génère un nombre impair aléatoire
    p = random.getrandbits(length)
    # Assure que p est impair
    if p % 2 == 0:
        p += 1
    return p

# Génère un nombre premier de la longueur spécifiée
def generate_prime_number(length=10):
    p = 0
    # Continue à générer des nombres jusqu'à ce qu'un nombre premier soit trouvé
    while not is_prime(p):
        p = generate_prime_candidate(length)
    return p

# Calcul du PGCD
def gcd(a, b):
    while b != 0:
        a, b = b, a % b
    return a

# Génération des clés publiques et privées RSA
def generate_keys():
    # Choisir deux nombres premiers distincts p et q
    p = generate_prime_number(8)  # Vous pouvez ajuster la longueur pour des nombres plus grands
    q = generate_prime_number(8)
    
    # Assurer que p et q sont différents
    while q == p:
        q = generate_prime_number(8)
    
    # Calculer n
    n = p * q
    
    # Calculer phi(n)
    phi_n = (p - 1) * (q - 1)
    
    # Choisir e tel que 1 < e < phi(n) et gcd(e, phi_n) = 1
    e = random.randrange(1, phi_n)
    g = gcd(e, phi_n)
    while g != 1:
        e = random.randrange(1, phi_n)
        g = gcd(e, phi_n)
    
    # Calculer d tel que (d * e) % phi(n) = 1
    d = mod_inverse(e, phi_n)
    
    # Clé publique (e, n)
    public_key = (e, n)
    
    # Clé privée (d, n)
    private_key = (d, n)
    
    return public_key, private_key

# Chiffrement du message
def encrypt(public_key, plaintext):
    e, n = public_key
    # Convertir chaque byte du message en son code entier, puis chiffrer avec RSA
    cipher_nums = [pow(byte, e, n) for byte in plaintext]
    # Convertir les nombres chiffrés en une chaîne de caractères pour l'envoi
    ciphertext = ' '.join(map(str, cipher_nums))
    return ciphertext

# Déchiffrement du message
def decrypt(private_key, ciphertext):
    d, n = private_key
    # Convertir la chaîne de caractères chiffrés en une liste de nombres
    cipher_nums = list(map(int, ciphertext.split()))
    # Déchiffrer chaque nombre et convertir en bytes
    plaintext = bytes([pow(char, d, n) for char in cipher_nums])
    return plaintext

# Génération des clés
public_key, private_key = generate_keys()

print("Clé publique:", public_key)
print("Clé privée:", private_key)

# Message à chiffrer (doit être en bytes)
message = b"Hello, RSA!"

# Chiffrer le message
encrypted_message = encrypt(public_key, message)
print("Message chiffré:", encrypted_message)

# Déchiffrer le message
decrypted_message = decrypt(private_key, encrypted_message)
print("Message déchiffré:", decrypted_message.decode())
