### Patching note

- Only patch files in `providers/mac`
- Submit a patch as a ZIP file in the following structure (unmodified files can be omitted):

  ```
  ---patch.zip
     |---providers
         |---mac
             |---aes256_xor.py
             |---crc32.py
             |---dsa512.py
             |---rsa1024.py
             |---sha256.py
  ```

- A patch file is invalid if one of the following occurs (including but not limited to):
    - The intended functionality or behaviour is changed. For example, the `get_public_info` method does not give enough
      information to verify generated MAC(s).
    - The associated Cryptographic algorithms are changed.
    - The associated MAC size is changed.
    - The Levenshtein distance (from the original source file) exceeds the required limit (see the table below).

      |Filename       |Required Levenshtein distance|
      |---------------|-----------------------------|
      |`aes256_xor.py`|≤ 15                         |
      |`crc32.py`     |≤ 20                         |
      |`dsa512.py`    |≤ 25                         |
      |`rsa1024.py`   |≤ 15                         |
      |`sha256.py`    |≤ 5                          |

    - The probability that a crash occurs on a random call to any method is higher than 1/1,000,000.


- Automatic checks can not be perfect. If you find out that a deployed patch is invalid, please report to us so that the 
patch can be manually taken down.

_Good luck and have fun!_