from flask import Flask, render_template, request
from rsa_logic import RSA

app = Flask(__name__)
rsa = RSA()

@app.route('/')
def index():
    # Default to 'encrypt' tab
    return render_template('index.html', 
                           p=rsa.p, q=rsa.q, n=rsa.n, 
                           phi=rsa.phi, e=rsa.e, d=rsa.d,
                           active_tab='encrypt')

@app.route('/encrypt', methods=['POST'])
def encrypt():
    message = request.form.get('message', '')
    ciphertext = rsa.encrypt_message(message)
    return render_template('index.html', 
                           p=rsa.p, q=rsa.q, n=rsa.n, phi=rsa.phi, e=rsa.e, d=rsa.d,
                           encrypt_result=ciphertext,
                           original_message_enc=message,
                           active_tab='encrypt')

@app.route('/decrypt', methods=['POST'])
def decrypt():
    ciphertext = request.form.get('ciphertext', '')
    message = rsa.decrypt_message(ciphertext)
    return render_template('index.html', 
                           p=rsa.p, q=rsa.q, n=rsa.n, phi=rsa.phi, e=rsa.e, d=rsa.d,
                           decrypt_result=message,
                           original_ciphertext_dec=ciphertext,
                           active_tab='decrypt')

@app.route('/sign', methods=['POST'])
def sign():
    message = request.form.get('message', '')
    signature = rsa.sign_message(message)
    return render_template('index.html', 
                           p=rsa.p, q=rsa.q, n=rsa.n, phi=rsa.phi, e=rsa.e, d=rsa.d,
                           sign_result=signature,
                           original_message_sign=message,
                           active_tab='sign')

@app.route('/verify', methods=['POST'])
def verify():
    signature = request.form.get('signature', '')
    message = rsa.verify_message(signature)
    return render_template('index.html', 
                           p=rsa.p, q=rsa.q, n=rsa.n, phi=rsa.phi, e=rsa.e, d=rsa.d,
                           verify_result=message,
                           original_signature_ver=signature,
                           active_tab='sign') # Keep user on 'sign' tab which will include verify

@app.route('/exchange', methods=['POST'])
def exchange():
    # Scenario: Alice sends a secret key (number) to Bob
    # Secret Key K = 5 (example, must be < n=33)
    K = 5
    
    # Bob's Public Key (from our system)
    # e = 3, n = 33
    
    # Encryption: C = K^e mod n
    C = rsa.encrypt_num(K)
    
    # Decryption (Bob): K' = C^d mod n
    decrypted_K = rsa.decrypt_num(C)
    
    scenario_log = [
        f"1. Alice chooses a secret key K = {K}.",
        f"2. Alice uses Bob's Public Key (e={rsa.e}, n={rsa.n}) to encrypt K.",
        f"3. Ciphertext C = {K}^{rsa.e} mod {rsa.n} = {C}.",
        f"4. Alice sends C = {C} to Bob.",
        f"5. Bob receives C = {C}.",
        f"6. Bob uses his Private Key (d={rsa.d}, n={rsa.n}) to decrypt C.",
        f"7. Decrypted Key K' = {C}^{rsa.d} mod {rsa.n} = {decrypted_K}.",
        f"8. Key Exchange Successful: {K} == {decrypted_K}"
    ]
    
    return render_template('index.html', 
                           p=rsa.p, q=rsa.q, n=rsa.n, phi=rsa.phi, e=rsa.e, d=rsa.d,
                           exchange_result=scenario_log,
                           active_tab='exchange')

if __name__ == '__main__':
    app.run(debug=True)
