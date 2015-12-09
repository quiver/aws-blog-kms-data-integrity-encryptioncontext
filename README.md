# How to Protect the Integrity of Your Encrypted Data by Using AWS Key Management Service and EncryptionContext

This is the code repository for Python-port code sample used in AWS Security Blog [How to Protect the Integrity of Your Encrypted Data by Using AWS Key Management Service and EncryptionContext]

## Prerequisites 
  - Amazon Web Services account
  - Python installed
  - Python boto3 installed
 
## Setting Up AWS Services

### KMS

Create a customer master key.

### DynamoDB

Create a table `EcDemoAddresses` with a string-type key `EmailAddress`.

Or you can run the following command:

```
$ cd encryption-context-python
$ python create_dynamodb_table.py
```

## Running Examples

There are three sample codes in the blog.
All sample codes are located at `encryption-context-python` directory.

### example1.py

KMS throws an InvalidCiphertextException upon receiving ciphertext that has been tampered with.

### example2.py

This is an insecure KMS encryption implementation.

If a malicious user(Mallory) can modify the DynamoDB table, she can replace data. Mallory can do this even without access to the encryption keys by simply swapping the encrypted data between the records, which doesn't require her to encrypt or decrypt anything. 

### example3.py

When you provide `EncryptionContext` at encryption, the system throws an `InvalidCiphertextException` when the system attemps to decrypt the record that has been tampered with.
This code improves the security of KMS encryption.
