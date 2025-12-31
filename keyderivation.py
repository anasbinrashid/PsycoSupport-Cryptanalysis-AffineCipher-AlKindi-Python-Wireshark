# Import pandas for CSV file handling and data manipulation
import pandas as pd
# Import Counter from collections for counting letter occurrences
from collections import Counter
# Import os module for directory and file operations
import os

# Create output directory for key analysis results
# exist_ok=True prevents error if directory already exists
os.makedirs('output/key_analysis', exist_ok=True)

def mod_inverse(a, m=26):
    """Find modular multiplicative inverse of a mod m"""
    # Loop through all possible inverse values from 1 to m-1
    for i in range(1, m):
        # Check if (a * i) mod m equals 1
        # If true, i is the modular inverse of a
        if (a * i) % m == 1:
            # Return the modular inverse
            return i
    # Return None if no modular inverse exists
    return None

def affine_decrypt_char(c, a, b):
    """Decrypt a single character using affine cipher"""
    # Check if character is not alphabetic (space, punctuation, etc.)
    if not c.isalpha():
        # Return non-alphabetic characters unchanged
        return c
    
    # Calculate modular multiplicative inverse of 'a'
    a_inv = mod_inverse(a)
    # If inverse doesn't exist, return None (invalid key)
    if a_inv is None:
        return None
    
    # Check if character is uppercase for case preservation
    is_upper = c.isupper()
    # Convert to uppercase for uniform processing
    c = c.upper()
    
    # Apply affine cipher decryption formula: P = a^(-1) * (C - b) mod 26
    # Convert letter to number (0-25), subtract b, multiply by inverse, mod 26
    decrypted = (a_inv * (ord(c) - ord('A') - b)) % 26
    # Convert decrypted number back to letter
    result = chr(decrypted + ord('A'))
    
    # Return result in original case (uppercase or lowercase)
    return result if is_upper else result.lower()

def affine_decrypt(ciphertext, a, b):
    """Decrypt entire text using affine cipher"""
    # Decrypt each character if alphabetic, otherwise keep as is
    # Join all characters back into a single string
    return ''.join(affine_decrypt_char(c, a, b) if c.isalpha() else c for c in ciphertext)

def get_most_frequent_letters(ciphertext, n=5):
    """Get n most frequent letters in ciphertext"""
    # Remove non-alphabetic characters and convert to uppercase
    clean_text = ''.join(c.upper() for c in ciphertext if c.isalpha())
    # Count frequency of each letter using Counter
    counter = Counter(clean_text)
    # Return list of n most common letters (without counts)
    return [letter for letter, _ in counter.most_common(n)]

def test_key_hypothesis(ciphertext, a, b):
    """Test a key hypothesis and return decrypted text with score"""
    # Decrypt the ciphertext using provided key (a, b)
    decrypted = affine_decrypt(ciphertext, a, b)
    
    # List of common English words to check in decrypted text
    # Higher score = more common words found = more likely correct decryption
    common_words = ['THE', 'AND', 'FOR', 'ARE', 'BUT', 'NOT', 'YOU', 'WITH', 'HER', 'WAS', 
                    'ONE', 'OUR', 'OUT', 'CAN', 'WHO', 'THAT', 'THIS', 'HAVE', 'FROM', 'THEY',
                    'BEEN', 'YOUR', 'FEEL', 'FEELING', 'KNOW']
    
    # Convert decrypted text to uppercase for word matching
    decrypted_upper = decrypted.upper()
    # Count how many common words appear in the decrypted text
    # sum() counts True values (when word is found in text)
    score = sum(word in decrypted_upper for word in common_words)
    
    # Return both the decrypted text and its quality score
    return decrypted, score

def find_affine_key(ciphertext, mood):
    """Find affine cipher parameters using frequency analysis"""
    # Print separator line for visual organization
    print(f"\n{'='*60}")
    # Print which mood value we're analyzing
    print(f"Analyzing Mood {mood}")
    # Print separator line
    print(f"{'='*60}")
    
    # Most common letters in standard English text (in frequency order)
    english_common = ['E', 'T', 'A', 'O', 'I', 'N']
    
    # Get the 6 most frequent letters in the ciphertext
    cipher_common = get_most_frequent_letters(ciphertext, 6)
    # Print the most frequent ciphertext letters for reference
    print(f"Most frequent letters in ciphertext: {', '.join(cipher_common)}")
    
    # Valid values for 'a' parameter - must be coprime with 26
    # These are all odd numbers from 1 to 25 that don't share factors with 26
    valid_a = [1, 3, 5, 7, 9, 11, 15, 17, 19, 21, 23, 25]
    
    # Initialize tracking variables for best key found
    best_score = 0  # Highest quality score found
    best_key = None  # Best (a, b) key pair
    best_decrypted = None  # Best decrypted text
    candidates = []  # List of all candidate keys with scores
    
    # Try mapping most frequent cipher letter to most frequent English letters
    # Loop through top 3 most frequent ciphertext letters
    for cipher_letter in cipher_common[:3]:
        # Loop through top 3 most frequent English letters
        for english_letter in english_common[:3]:
            # Convert letters to numbers (A=0, B=1, ..., Z=25)
            C1 = ord(cipher_letter) - ord('A')  # First ciphertext letter as number
            P1 = ord(english_letter) - ord('A')  # First plaintext letter as number
            
            # Try different second letter mappings to create system of equations
            # Loop through another cipher letter (excluding the first one)
            for cipher_letter2 in cipher_common[:3]:
                # Skip if it's the same letter as the first
                if cipher_letter2 == cipher_letter:
                    continue
                
                # Loop through another English letter (excluding the first one)
                for english_letter2 in english_common[:3]:
                    # Skip if it's the same letter as the first
                    if english_letter2 == english_letter:
                        continue
                    
                    # Convert second pair of letters to numbers
                    C2 = ord(cipher_letter2) - ord('A')  # Second ciphertext letter
                    P2 = ord(english_letter2) - ord('A')  # Second plaintext letter
                    
                    # Solve for affine cipher parameters a and b
                    # Affine encryption: C = a*P + b (mod 26)
                    # System of equations:
                    # C1 = a*P1 + b (mod 26)
                    # C2 = a*P2 + b (mod 26)
                    # Subtracting: C1 - C2 = a*(P1 - P2) (mod 26)
                    
                    # Try each valid 'a' value
                    for a in valid_a:
                        # Check if this 'a' satisfies the equation
                        if (a * (P1 - P2)) % 26 == (C1 - C2) % 26:
                            # Calculate 'b' using first equation: b = C1 - a*P1 (mod 26)
                            b = (C1 - a * P1) % 26
                            
                            # Test this key hypothesis by decrypting
                            decrypted, score = test_key_hypothesis(ciphertext, a, b)
                            
                            # Check if this is the best score so far
                            if score > best_score:
                                # Update best score
                                best_score = score
                                # Update best key
                                best_key = (a, b)
                                # Update best decrypted text
                                best_decrypted = decrypted
                            
                            # If this key produced any matches, save it as a candidate
                            if score > 0:
                                candidates.append({
                                    'a': a,  # The 'a' parameter
                                    'b': b,  # The 'b' parameter
                                    # Description of letter mappings used
                                    'mapping': f"{cipher_letter}→{english_letter}, {cipher_letter2}→{english_letter2}",
                                    'score': score,  # Quality score
                                    'preview': decrypted[:100]  # First 100 chars of decryption
                                })
    
    # Sort all candidate keys by score (best first)
    candidates.sort(key=lambda x: x['score'], reverse=True)
    
    # Print the top 5 candidate keys for review
    print(f"\nTop 5 key candidates:")
    # Enumerate through top 5 candidates with numbering starting at 1
    for i, cand in enumerate(candidates[:5], 1):
        # Print candidate number and its key parameters with score
        print(f"\n{i}. a={cand['a']}, b={cand['b']} (Score: {cand['score']})")
        # Print which letter mappings were used
        print(f"   Mapping: {cand['mapping']}")
        # Print preview of decrypted text (truncated with ellipsis)
        print(f"   Preview: {cand['preview']}...")
    
    # If a best key was found, print detailed results
    if best_key:
        # Print separator line
        print(f"\n{'='*60}")
        # Print the best key found with its score
        print(f"BEST KEY FOUND: a={best_key[0]}, b={best_key[1]} (Score: {best_score})")
        # Print separator line
        print(f"{'='*60}")
        # Print preview of best decryption (first 200 characters)
        print(f"Decrypted preview:\n{best_decrypted[:200]}...")
        
    # Return the best key, full decrypted text, and all candidates
    return best_key, best_decrypted, candidates

def main():
    # Read the CSV file containing encrypted messages
    df = pd.read_csv('messages.csv')
    
    # Initialize empty list to store analysis results
    results = []
    
    # Analyze each ciphertext in the DataFrame
    # iterrows() gives us index and row data
    for idx, row in df.iterrows():
        # Extract ciphertext from current row
        ciphertext = row['ciphertext']
        # Extract mood value from current row
        mood = row['mood']
        # Extract encrypted username from current row
        username_enc = row['username_enc']
        
        # Print major separator for new ciphertext analysis
        print(f"\n\n{'#'*70}")
        # Print ciphertext number (human-readable, starting from 1)
        print(f"CIPHERTEXT {idx + 1}")
        # Print the encrypted username for reference
        print(f"Username (encrypted): {username_enc}")
        # Print separator line
        print(f"{'#'*70}")
        
        # Perform frequency analysis to find the best affine cipher key
        best_key, best_decrypted, candidates = find_affine_key(ciphertext, mood)
        
        # If a valid key was found, save the results
        if best_key:
            # Append result dictionary to results list
            results.append({
                'ciphertext_num': idx + 1,  # Ciphertext number
                'mood': mood,  # Mood value
                'username_enc': username_enc,  # Encrypted username
                'a': best_key[0],  # 'a' parameter of best key
                'b': best_key[1],  # 'b' parameter of best key
                # Preview of decrypted text (first 150 chars) or None if no decryption
                'decrypted_preview': best_decrypted[:150] if best_decrypted else None
            })
            
            # Save full decryption to individual text file
            # Open file in write mode with constructed filename
            with open(f'output/key_analysis/decrypted_{idx+1}_mood_{mood}.txt', 'w') as f:
                # Write ciphertext number header
                f.write(f"Ciphertext {idx + 1}\n")
                # Write mood value
                f.write(f"Mood: {mood}\n")
                # Write the derived key parameters
                f.write(f"Key: a={best_key[0]}, b={best_key[1]}\n")
                # Write separator line
                f.write(f"{'='*60}\n\n")
                # Write the complete decrypted text
                f.write(best_decrypted)
    
    # Convert results list to pandas DataFrame for easy export
    results_df = pd.DataFrame(results)
    # Save results summary to CSV file
    results_df.to_csv('output/key_analysis/key_derivation_summary.csv', index=False)
    # Print completion message with separator
    print(f"\n\n{'='*70}")
    print("Key derivation complete!")
    # Tell user where results are saved
    print("Results saved to 'output/key_analysis/'")
    # Print separator line
    print(f"{'='*70}")
    
    # Print summary table header
    print("\n\nSUMMARY OF KEYS FOUND:")
    # Print selected columns as formatted string table (no row indices)
    # Shows ciphertext number, mood, and derived key parameters
    print(results_df[['ciphertext_num', 'mood', 'a', 'b']].to_string(index=False))

# Standard Python idiom: run main() only if script is executed directly
if __name__ == "__main__":
    main()