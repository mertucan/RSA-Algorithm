
class RSA:
    def __init__(self):
        self.p = 3
        self.q = 11
        self.n = self.p * self.q
        self.phi = (self.p - 1) * (self.q - 1)
        self.e = 3
        self.d = 7
        
        # Custom alphabet mapping to ensure values < 33
        # 26 letters + space = 27 chars. 
        # 0=space, 1=a, ... 26=z
        self.alphabet = " abcdefghijklmnopqrstuvwxyz"
        self.char_to_int = {c: i for i, c in enumerate(self.alphabet)}
        self.int_to_char = {i: c for i, c in enumerate(self.alphabet)}

    def encrypt_num(self, m):
        return pow(m, self.e, self.n)

    def decrypt_num(self, c):
        return pow(c, self.d, self.n)

    def sign_num(self, m):
        # Signature is encrypting with private key
        return pow(m, self.d, self.n)

    def verify_num(self, s):
        # Verification is decrypting with public key (mathematically same as encrypting with e)
        return pow(s, self.e, self.n)

    def text_to_nums(self, text):
        nums = []
        for char in text.lower():
            if char in self.char_to_int:
                nums.append(self.char_to_int[char])
            else:
                # Handle unknown chars (maybe skip or map to space)
                nums.append(0) 
        return nums

    def nums_to_text(self, nums):
        text = []
        for n in nums:
            if n in self.int_to_char:
                text.append(self.int_to_char[n])
            else:
                text.append('?')
        return "".join(text)

    def encrypt_message(self, message):
        nums = self.text_to_nums(message)
        cipher_nums = [self.encrypt_num(m) for m in nums]
        return cipher_nums

    def decrypt_message(self, cipher_nums):
        # cipher_nums can be a list of ints or string of space-separated ints
        if isinstance(cipher_nums, str):
            try:
                cipher_nums = [int(x) for x in cipher_nums.split()]
            except ValueError:
                return "Error: Invalid ciphertext format"
        
        decrypted_nums = [self.decrypt_num(c) for c in cipher_nums]
        return self.nums_to_text(decrypted_nums)

    def sign_message(self, message):
        nums = self.text_to_nums(message)
        signature_nums = [self.sign_num(m) for m in nums]
        return signature_nums

    def verify_message(self, signature_nums):
        if isinstance(signature_nums, str):
             try:
                signature_nums = [int(x) for x in signature_nums.split()]
             except ValueError:
                return "Error: Invalid signature format"

        verified_nums = [self.verify_num(s) for s in signature_nums]
        return self.nums_to_text(verified_nums)

