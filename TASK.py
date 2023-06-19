import random

def generate_prime(min_value, max_value, k=10):# Генерація випадкового простого числа у заданому діапазоні
    while True:
        p = random.randint(min_value, max_value)
        if is_prime(p, k):
            return p

def is_prime(n, k):# Перевірка, чи є число простим
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

def generate_primitive_root(p):# Генерація примітивного кореня залишкового поля p
    phi = p - 1
    factors = prime_factors(phi)
    for g in range(2, p):
        if all(pow(g, phi // factor, p) != 1 for factor in factors):
            return g

def prime_factors(n):# Знаходження простих множників числа n
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

def mod_inverse(a, m):# Обчислення оберненого елемента a відносно модуля m
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

def generate_keys(p, g):# Генерація приватного та публічного ключів
    a = random.randint(1, p - 1)
    b = pow(g, a, p)
    return a, b

def decrypt_message(encrypted_blocks, p, a):# Розшифрування повідомлення
    block_size = (len(str(p)) - 1) // 3

    decrypted_message = ""
    for block in encrypted_blocks:
        x, y = block

        s = pow(x, a, p)
        m = (y * mod_inverse(s, p)) % p

        block_str = str(m).zfill(block_size * 3)
        for i in range(0, len(block_str), 3):
            code = int(block_str[i:i+3])
            if code != 0:
                decrypted_message += chr(code)

    return decrypted_message

def encrypt_message(message, p, g, b):# Зашифрування повідомлення
    block_size = (len(str(p)) - 1) // 3

    encrypted_blocks = []
    for i in range(0, len(message), block_size):
        block = message[i:i+block_size]

        m = 0
        for c in block:
            m = m * 1000 + ord(c)

        k = random.randint(1, p - 1)
        x = pow(g, k, p)
        y = (pow(b, k, p) * m) % p

        encrypted_blocks.append((x, y))

    return encrypted_blocks

def sign_message(message, p, g, a):# Розмір блоку для коректного підписування
    block_size = (len(str(p)) - 1) // 3

    signed_blocks = []
    for i in range(0, len(message), block_size):
        block = message[i:i+block_size]

        m = 0
        for c in block:
            m = m * 1000 + ord(c)

        k = random.randint(1, p - 1)
        x = pow(g, k, p)
        y = (pow(a, k, p) * m) % p

        signed_blocks.append((x, y))

    return signed_blocks

# Генерація простого числа p та примітивного кореня g
p = generate_prime(2048, 4096)
g = generate_primitive_root(p)

# Генерація ключів
a, b = generate_keys(p, g)
print("Private Key (a):", a)
print("Public Key (b):", b)

message = "Hello, world! This is a test message."

# Шифрування повідомлення
encrypted_blocks = encrypt_message(message, p, g, b)
print("Encrypted Blocks:", encrypted_blocks)

# Розшифрування повідомлення
decrypted_message = decrypt_message(encrypted_blocks, p, a)
print("Decrypted Message:", decrypted_message)
print("Decrypted Message is correct:", decrypted_message == message)

# Підписування повідомлення
signed_blocks = sign_message(message, p, g, a)
print("Signed Blocks:", signed_blocks)

# Спроба змінити шифрований блок
corrupted_blocks = encrypted_blocks.copy()
corrupted_blocks[0] = (corrupted_blocks[0][0], corrupted_blocks[0][1] + 1)

# Розшифрування пошкодженого повідомлення
corrupted_decrypted_message = decrypt_message(corrupted_blocks, p, a)
print("Corrupted Decrypted Message:", corrupted_decrypted_message)

# Перевірка повернення "false" при пошкодженні даних
print("Signature verification failed:", corrupted_decrypted_message != message)
