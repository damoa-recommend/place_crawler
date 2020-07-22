import hashlib

def encode_sha2(data): 
  data = data or ''
  encoded_string = data.replace('\n', ' ').replace('\t', ' ').replace('\r', '').strip().encode()
  return hashlib.sha256(encoded_string).hexdigest()