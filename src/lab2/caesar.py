def encrypt_caesar(plaintext: str, shift: int = 3) -> str:
    """
    Encrypts plaintext using a Caesar cipher.
    >>> encrypt_caesar("PYTHON")
    'SBWKRQ'
    >>> encrypt_caesar("python")
    'sbwkrq'
    >>> encrypt_caesar("Python3.6")
    'Sbwkrq3.6'
    >>> encrypt_caesar("")
    ''
    """
    ciphertext = ""
    elements = [elem for elem in plaintext]
    for i in range(len(elements)):
        if elements[i].isalpha():
            n = ord(elements[i]) + shift
            if elements[i].isupper():
                if n > 90:
                    n = n - 26
            else:
                if n > 122:
                    n = n - 26
            ciphertext += chr(n)
        else:
            ciphertext += elements[i]
    return ciphertext


def decrypt_caesar(ciphertext: str, shift: int = 3) -> str:
    """
    Decrypts a ciphertext using a Caesar cipher.
    >>> decrypt_caesar("SBWKRQ")
    'PYTHON'
    >>> decrypt_caesar("sbwkrq")
    'python'
    >>> decrypt_caesar("Sbwkrq3.6")
    'Python3.6'
    >>> decrypt_caesar("")
    ''
    """
    plaintext = ""
    elements = [elem for elem in ciphertext]
    for i in range(len(elements)):
        if elements[i].isalpha():
            n = ord(elements[i]) - shift
            if elements[i].isupper():
                if n < 65:
                    n = n + 26
            else:
                if n < 97:
                    n = n + 26
            plaintext += chr(n)
        else:
            plaintext += elements[i]
    return plaintext
