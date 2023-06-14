import random
import hashlib

def generate_prime(min_value, max_value, k=10):# Використовується алгоритм перевірки простоти Міллера-Рабіна з параметром k
    while True:
        p = random.randint(min_value, max_value)
        if is_prime(p, k):
            return p

def is_prime(n, k):# Функція для перевірки, чи є число простим
    if n == 2 or n == 3:
        return True
    if n <= 1 or n % 2 == 0:
        return False

    r, s = 0, n - 1
    while s % 2 == 0:
        r += 1
        s //= 2

    for _ in range(k):
        a = random.randint(2, n - 2)
        x = pow(a, s, n)
        if x == 1 or x == n - 1:
            continue
        for _ in range(r - 1):
            x = pow(x, 2, n)
            if x == n - 1:
                break
        else:
            return False

    return True

def generate_primitive_root(p):# Функція для генерації примітивного кореня по модулю p
    phi = p - 1
    factors = prime_factors(phi)
    for g in range(2, p):
        if all(pow(g, phi // factor, p) != 1 for factor in factors):
            return g

def prime_factors(n):# Функція для знаходження простих множників числа n
    factors = []
    while n % 2 == 0:
        factors.append(2)
        n = n // 2
    i = 3
    while i * i <= n:
        if n % i == 0:
            factors.append(i)
            n = n // i
        else:
            i += 2
    if n > 2:
        factors.append(n)
    return factors


def mod_inverse(a, m):# Функція для обчислення оберненого за модулем числа a
    if m == 1:
        return 0
    original_m = m
    x, y = 1, 0
    while a > 1:
        q = a // m
        a, m = m, a % m
        x, y = y, x - q * y
    if x < 0:
        x += original_m
    return x

def generate_keys(p, g):# Функція для генерації приватного та публічного ключів
    a = random.randint(1, p - 1)
    b = pow(g, a, p)
    return a, b

def decrypt_message(encrypted_blocks, p, a):# Функція для розшифрування повідомлення
    block_size = len(str(p)) - 1

    decrypted_message = ""
    for block in encrypted_blocks:
        x, y = block

        s = pow(x, a, p)
        m = (y * mod_inverse(s, p)) % p

        decrypted_message += str(m).zfill(block_size)

    return decrypted_message

# Вибір загальносистемних параметрів
def encrypt_message(message, p, g, b):
    block_size = len(str(p)) - 1

    encrypted_blocks = []
    for i in range(0, len(message), block_size):
        block = message[i:i+block_size]

        # Хешування блоку
        block_hash = hashlib.sha256(block.encode()).hexdigest()

        m = int(block_hash, 16)

        k = random.randint(1, p - 1)
        x = pow(g, k, p)
        y = (pow(b, k, p) * m) % p

        encrypted_blocks.append((x, y))

    return encrypted_blocks

# Вибір загальносистемних параметрів
p = generate_prime(2048, 4096)
g = generate_primitive_root(p)

# Генерація ключів
a, b = generate_keys(p, g)
print("Private Key (a):", a)
print("Public Key (b):", b)

# Зашифрування повідомлення
message = "Hello, world! This is a test message."
encrypted_blocks = encrypt_message(message, p, g, b)
print("Encrypted Blocks:", encrypted_blocks)

# Розшифрування повідомлення
decrypted_message = decrypt_message(encrypted_blocks, p, a)
print("Decrypted Message:", decrypted_message)

# Перевірка коректності розшифрованого повідомлення
print("Decrypted Message is correct:", decrypted_message == message)

# Переконання в правильності розшифрованого повідомлення при пошкодженні даних
corrupted_blocks = encrypted_blocks.copy()
corrupted_blocks[0] = (corrupted_blocks[0][0], corrupted_blocks[0][1] + 1)

corrupted_decrypted_message = decrypt_message(corrupted_blocks, p, a)
print("Corrupted Decrypted Message:", corrupted_decrypted_message)

# Перевірка повернення "false" при пошкодженні даних
print("Signature verification failed:", corrupted_decrypted_message != message)
