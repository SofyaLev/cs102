def encrypt_vigenere(plaintext: str, keyword: str) -> str:
    """
    Encrypts plaintext using a Vigenere cipher.
    >>> encrypt_vigenere("PYTHON", "A")
    'PYTHON'
    >>> encrypt_vigenere("python", "a")
    'python'
    >>> encrypt_vigenere("ATTACKATDAWN", "LEMON")
    'LXFOPVEFRNHR'
    """
    ciphertext = ""
    keyword_len = len(keyword)
    plaintext_len = len(plaintext)
    if keyword_len < plaintext_len:
        new_key = keyword*(plaintext_len // keyword_len)
        i = 0
        while len(new_key) < plaintext_len:
            new_key += keyword[i]
            i += 1
    else:
        new_key = keyword

    plaintext_ord = [ord(i) for i in plaintext]
    key_ord = [ord(i.upper())-65 for i in new_key]

    for i in range(plaintext_len):
        if plaintext[i].isupper():
            ciphertext += chr((plaintext_ord[i] + key_ord[i] - 65) % 26 + 65)
        else:
            ciphertext += chr((plaintext_ord[i] + key_ord[i] - 97) % 26 + 97)
    return ciphertext


def decrypt_vigenere(ciphertext: str, keyword: str) -> str:
    """
    Decrypts a ciphertext using a Vigenere cipher.
    >>> decrypt_vigenere("PYTHON", "A")
    'PYTHON'
    >>> decrypt_vigenere("python", "a")
    'python'
    >>> decrypt_vigenere("LXFOPVEFRNHR", "LEMON")
    'ATTACKATDAWN'
    """
    plaintext = ""
    keyword_len = len(keyword)
    ciphertext_len = len(ciphertext)
    if keyword_len < ciphertext_len:
        new_key = keyword * (ciphertext_len // keyword_len)
        i = 0
        while len(new_key) < ciphertext_len:
            new_key += keyword[i]
            i += 1
    else:
        new_key = keyword
    ciphertext_ord = [ord(i) for i in ciphertext]
    key_ord = [ord(i.upper())-65 for i in new_key]
    for i in range(ciphertext_len):
        if ciphertext[i].isupper():
            plaintext += chr((ciphertext_ord[i] - key_ord[i] - 65) % 26 + 65)
        else:
            plaintext += chr((ciphertext_ord[i] - key_ord[i] - 97) % 26 + 97)
    return plaintext
