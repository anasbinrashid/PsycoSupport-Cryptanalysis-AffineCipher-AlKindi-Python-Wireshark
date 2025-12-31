# PsycoSupport Cryptanalysis

> **Breaking the Affine Cipher: A Complete Cryptanalysis of PsycoSupport's Encryption Scheme**

This project demonstrates the successful cryptanalysis of encrypted communications from **PsycoSupport**, a mental health chatbot application. Using classical cryptanalysis techniques including **Al-Kindi's frequency analysis algorithm**, we discovered the key derivation formula and successfully decrypted all intercepted messages.

---

## Overview

This repository contains a complete cryptanalysis toolkit for breaking the **Affine Cipher** encryption used by PsycoSupport. The project was developed as part of an Information Security course assignment to demonstrate practical cryptanalysis skills.

### Key Achievements:
- Intercepted encrypted communications using **Wireshark**
- Performed **Al-Kindi frequency analysis** on ciphertexts
- Derived Affine cipher keys through mathematical analysis
- Discovered universal key derivation formula: `a = 2×mood + 1, b = 2×mood`
- Successfully decrypted all 5 intercepted user sessions

---

## The Target: PsycoSupport

**PsycoSupport** is an AI-powered mental health chatbot available at:

🔗 **https://github.com/maadilrehman/PsycoSupport**

### How PsycoSupport Works:

1. The application consists of a **Server** and **Client** architecture
2. Users connect to the client and enter their **Groq API key** for LLM access
3. Users input their **mood value** (1-10 scale) and send messages
4. The AI psychologist responds with therapeutic guidance
5. All communications are **encrypted using an Affine Cipher**

### The Vulnerability:

The encryption scheme ties the cipher key directly to the user's mood value, creating a predictable and breakable encryption pattern. By intercepting network traffic, an attacker can:
- Capture encrypted messages
- Determine the mood value from packet metadata
- Derive the decryption key using the discovered formula

---

## Attack Methodology

### Phase 1: Traffic Interception

Using **Wireshark** with promiscuous mode enabled on the loopback interface, I intercepted HTTP traffic between the PsycoSupport client and server. The captured packets contained:
- Encrypted usernames
- Encrypted user messages
- Mood values (in plaintext)
- Encrypted API keys
- Encrypted AI responses (ciphertexts)

The intercepted data was compiled into `messages.csv` for analysis.

### Phase 2: Al-Kindi Frequency Analysis

Applying **Al-Kindi's frequency analysis** algorithm (developed by the 9th-century Arab polymath Abu Yusuf Ya'qub ibn Is-haq al-Kindi), I analyzed the letter frequency distribution of each ciphertext and compared it to standard English letter frequencies:

| Letter | English Frequency |
|--------|------------------|
| E | 12.70% |
| T | 9.06% |
| A | 8.17% |
| O | 7.51% |
| I | 6.97% |
| N | 6.75% |

### Phase 3: Key Derivation

By mapping the most frequent ciphertext letters to common English letters and solving the resulting system of equations, I derived the Affine cipher parameters (a, b) for each mood value.

### Phase 4: Formula Discovery

After analyzing the pattern across all mood values, I discovered the **universal key derivation formula**:

```
a = 2 × mood + 1
b = 2 × mood
```

This formula allows instant decryption of any PsycoSupport ciphertext without needing frequency analysis.

---

## Project Structure

```
PsycoSupport-Cryptanalysis/
│
├── messages.csv              # Intercepted encrypted data
├── decryptmessages.py        # Decrypt using known keys
├── frequencyanalysis.py      # Al-Kindi frequency analysis
├── keyderivation.py          # Derive keys via cryptanalysis
├── universaldecryptor.py     # Universal decryption algorithm
├── README.md                 # This file
├── Report.docx               # Detailed analysis report
│
├── Screenshots/              # Documentation screenshots
│   ├── wireshark captures
│   ├── decryption outputs
│   └── frequency charts
│
└── Outputs/                  # Generated analysis files
    ├── bonus/                # Universal decryptor results
    ├── charts/               # Frequency visualization charts
    ├── decrypted/            # Decrypted messages
    ├── frequency_tables/     # Letter frequency CSVs
    └── key_analysis/         # Key derivation results
```

---

## Installation

### Prerequisites

- Python 3.8 or higher
- pip (Python package manager)

### Setup

1. **Clone the repository**
   ```bash
   git clone https://github.com/anasbinrashid/PsycoSupport-Cryptanalysis-AffineCipher-Alkindi-Python-Wireshark.git
   cd PsycoSupport-Cryptanalysis-AffineCipher-Alkindi-Python-Wireshark
   ```

2. **Install dependencies**
   ```bash
   pip install pandas matplotlib seaborn
   ```

---

## Usage

### 1. Frequency Analysis (Al-Kindi Algorithm)

Analyze letter frequencies in the intercepted ciphertexts:

```bash
python frequencyanalysis.py
```

**Output:**
- CSV files with frequency tables in `Outputs/frequency_tables/`
- Visualization charts in `Outputs/charts/`

### 2. Key Derivation

Derive Affine cipher keys using cryptanalysis:

```bash
python keyderivation.py
```

**Output:**
- Derived keys and decrypted texts in `Outputs/key_analysis/`

### 3. Decrypt Messages (Known Keys)

Decrypt all messages using the discovered keys:

```bash
python decryptmessages.py
```

**Output:**
- Individual decrypted files in `Outputs/decrypted/`
- Summary CSV with all results

### 4. Universal Decryptor (Bonus)

Use the discovered formula to decrypt any PsycoSupport ciphertext:

```bash
python universaldecryptor.py
```

**Output:**
- Complete algorithm documentation in `Outputs/bonus/`
- Universal decryption results

---

## The Discovery

### The Universal Key Derivation Formula

After extensive cryptanalysis, I discovered that PsycoSupport uses a deterministic key derivation scheme:

```python
def derive_key(mood):
    a = 2 * mood + 1  # Multiplicative key
    b = 2 * mood      # Additive key (shift)
    return a, b
```

### Verified Key Mappings

| Mood | a | b | a⁻¹ (mod 26) |
|------|---|---|--------------|
| 3 | 7 | 6 | 15 |
| 5 | 11 | 10 | 19 |
| 7 | 15 | 14 | 7 |
| 10 | 21 | 20 | 5 |

### Universal Decryption Function

```python
def universal_decrypt(ciphertext, mood):
    """Decrypt any PsycoSupport ciphertext instantly"""
    a = 2 * mood + 1
    b = 2 * mood
    a_inv = mod_inverse(a, 26)
    
    result = []
    for c in ciphertext:
        if c.isalpha():
            c_num = ord(c.upper()) - ord('A')
            p_num = (a_inv * (c_num - b)) % 26
            result.append(chr(p_num + ord('A')))
        else:
            result.append(c)
    
    return ''.join(result)
```

---

## Technical Details

### The Affine Cipher

The Affine cipher is a monoalphabetic substitution cipher that uses modular arithmetic:

**Encryption:** `C = (aP + b) mod 26`

**Decryption:** `P = a⁻¹(C - b) mod 26`

Where:
- `P` = Plaintext letter (0-25)
- `C` = Ciphertext letter (0-25)
- `a` = Multiplicative key (must be coprime with 26)
- `b` = Additive key (shift)
- `a⁻¹` = Modular multiplicative inverse of a

### Valid 'a' Values

For the cipher to be reversible, `a` must be coprime with 26:

```
Valid a values: [1, 3, 5, 7, 9, 11, 15, 17, 19, 21, 23, 25]
```

### Index of Coincidence (IoC)

To verify successful decryption, I used the **Index of Coincidence**:

```
IoC = Σ(fᵢ × (fᵢ - 1)) / (N × (N - 1))
```

English text has an IoC of approximately **0.065-0.070**. All decrypted texts showed IoC values within this range, confirming successful decryption.

---

## Results

### Decryption Success Rate: 100%

| Ciphertext | Mood | Key (a, b) | Quality Score | IoC |
|------------|------|------------|---------------|-----|
| 1 (ANAS) | 3 | (7, 6) | 281 | 0.0652 |
| 2 (AADIL) | 5 | (11, 10) | 291 | 0.0639 |
| 3 (UROOJ) | 7 | (15, 14) | 281 | 0.0649 |
| 4 (KHAN) | 10 | (21, 20) | 291 | 0.0663 |
| 5 (RASHID) | 3 | (7, 6) | 278 | 0.0658 |

### Sample Decrypted Output

**Original Ciphertext (Mood 3):**
```
KJC EATBIVPQF JDGJ SAQXI JGYIT JDI PKVCJ CJIH NS VIGUDKTW AQJ...
```

**Decrypted Plaintext:**
```
ITS WONDERFUL THAT YOUVE TAKEN THE FIRST STEP BY REACHING OUT...
```

---

## Screenshots

The `Screenshots/` folder contains documentation of:

- Wireshark packet capture setup
- Promiscuous mode configuration
- Server and client execution
- Frequency analysis output
- Key derivation process
- Final decryption results

---

## Cryptographic Concepts Used

| Concept | Application |
|---------|-------------|
| **Al-Kindi Frequency Analysis** | Breaking monoalphabetic substitution ciphers by analyzing letter frequencies |
| **Modular Arithmetic** | Computing a⁻¹ mod 26 for decryption |
| **Index of Coincidence** | Verifying decryption quality matches English text patterns |
| **Affine Cipher** | The target encryption algorithm |
| **Known-Plaintext Attack** | Using known English patterns to derive keys |

---

## References

1. **Al-Kindi** - "A Manuscript on Deciphering Cryptographic Messages" (9th Century)
2. **William F. Friedman** - "The Index of Coincidence and Its Applications" (1922)
3. **Bruce Schneier** - "Applied Cryptography" (1996)
