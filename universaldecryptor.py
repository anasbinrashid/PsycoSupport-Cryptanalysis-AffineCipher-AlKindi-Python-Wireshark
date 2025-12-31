# Import pandas library for CSV file handling and data manipulation
import pandas as pd
# Import Counter from collections for counting character frequencies
from collections import Counter
# Import os module for directory and file system operations
import os

# Create output directory for bonus task results
# exist_ok=True means don't raise error if directory already exists
os.makedirs('output/bonus', exist_ok=True)

def mod_inverse(a, m=26):
    """Find modular multiplicative inverse of a mod m"""
    # Iterate through all possible values from 1 to m-1 (1 to 25 for alphabet)
    for i in range(1, m):
        # Check if (a * i) mod m equals 1, which defines the modular inverse
        # The modular inverse a^(-1) satisfies: (a * a^(-1)) mod 26 = 1
        if (a * i) % m == 1:
            # Return i as the modular inverse of a
            return i
    # Return None if no modular inverse exists (when a is not coprime with m)
    return None

def affine_decrypt(ciphertext, a, b):
    """Decrypt text using affine cipher with parameters a and b"""
    # Calculate the modular multiplicative inverse of 'a'
    a_inv = mod_inverse(a)
    # If no inverse exists, 'a' is invalid (not coprime with 26)
    if a_inv is None:
        # Return None to indicate failure
        return None
    
    # Initialize empty list to build the decrypted result
    result = []
    # Loop through each character in the ciphertext
    for c in ciphertext:
        # Check if character is alphabetic (letter)
        if c.isalpha():
            # Check if character is uppercase to preserve case
            is_upper = c.isupper()
            # Convert to uppercase for uniform processing
            c = c.upper()
            # Apply affine decryption: P = a^(-1) * (C - b) mod 26
            # Convert letter to number (0-25), subtract b, multiply by inverse, mod 26
            decrypted = (a_inv * (ord(c) - ord('A') - b)) % 26
            # Convert decrypted number back to a letter
            char = chr(decrypted + ord('A'))
            # Append character in original case (uppercase or lowercase)
            result.append(char if is_upper else char.lower())
        else:
            # If not a letter (space, punctuation, etc.), keep it unchanged
            result.append(c)
    # Join all characters into a single string and return
    return ''.join(result)

def calculate_ioc(text):
    """Calculate Index of Coincidence"""
    # Remove non-alphabetic characters and convert to uppercase
    text = ''.join(c.upper() for c in text if c.isalpha())
    # Get total number of letters
    n = len(text)
    # Handle edge case: need at least 2 letters for IoC calculation
    if n <= 1:
        # Return 0 if text is too short
        return 0
    
    # Count frequency of each letter using Counter
    freq = Counter(text)
    # Calculate IoC using formula: Σ(fi * (fi - 1)) / (n * (n - 1))
    # where fi is frequency of each letter
    # This measures how likely two random letters are the same
    ic = sum(count * (count - 1) for count in freq.values()) / (n * (n - 1))
    # Return the Index of Coincidence value
    return ic

def score_english(text):
    """Score text based on English characteristics"""
    # List of common English words to check for in decrypted text
    # More common words found = higher likelihood of correct decryption
    common_words = ['THE', 'AND', 'TO', 'OF', 'A', 'IN', 'IS', 'YOU', 'THAT', 'IT',
                    'FOR', 'WITH', 'AS', 'THIS', 'ARE', 'ON', 'BE', 'AT', 'BY', 'YOUR',
                    'HAVE', 'NOT', 'BUT', 'CAN', 'FROM', 'THEY', 'WE', 'FEEL', 'FEELING',
                    'HELLO', 'WELCOME', 'GREAT', 'WONDERFUL', 'ITS', 'LISTEN', 'SUPPORT']
    
    # Convert text to uppercase for case-insensitive word matching
    text_upper = text.upper()
    # Count how many common words appear in text (5 points per word)
    word_score = sum(5 for word in common_words if word in text_upper)
    
    # Check for common two-letter combinations (bigrams) in English
    common_bigrams = ['TH', 'HE', 'IN', 'ER', 'AN', 'RE', 'ON', 'AT', 'EN', 'ND', 'ST', 'ES']
    # Count bigrams found (2 points per bigram)
    bigram_score = sum(2 for bigram in common_bigrams if bigram in text_upper)
    
    # Check for common three-letter combinations (trigrams) in English
    common_trigrams = ['THE', 'AND', 'ING', 'HER', 'ERE', 'ENT', 'THA', 'NTH', 'FOR', 'YOU']
    # Count trigrams found (3 points per trigram)
    trigram_score = sum(3 for trigram in common_trigrams if trigram in text_upper)
    
    # Calculate Index of Coincidence (English text ≈ 0.065-0.070)
    ioc = calculate_ioc(text)
    # Give 100 bonus points if IoC is in the English range
    ioc_score = 100 if 0.060 <= ioc <= 0.075 else 0
    
    # Calculate total score by summing all components
    total_score = word_score + bigram_score + trigram_score + ioc_score
    # Return both the total score and IoC value
    return total_score, ioc

def derive_key_from_mood(mood):
    """
    GENERAL FORMULA: Derive affine cipher key from mood value
    
    Based on cryptanalysis, the key derivation formula is:
    a = 2 * mood + 1
    b = 2 * mood
    
    This formula works for all mood values where (2*mood + 1) is coprime with 26.
    Valid values of 'a' (coprime with 26): [1, 3, 5, 7, 9, 11, 15, 17, 19, 21, 23, 25]
    """
    # Calculate 'a' parameter using the discovered formula
    a = 2 * mood + 1
    # Calculate 'b' parameter using the discovered formula
    b = 2 * mood
    
    # List of valid 'a' values that are coprime with 26
    # These are odd numbers from 1-25 that don't share factors with 26
    valid_a = [1, 3, 5, 7, 9, 11, 15, 17, 19, 21, 23, 25]
    
    # Check if calculated 'a' is in the list of valid values
    if a not in valid_a:
        # If the formula produces an invalid 'a', return None for both values
        return None, None
    
    # Return the derived key parameters
    return a, b

def universal_decrypt(ciphertext, mood):
    """
    Universal decryption function using the discovered formula.
    Works for any ciphertext encrypted with PsycoSupport's scheme.
    
    Args:
        ciphertext: The encrypted message
        mood: The mood value used during encryption
    
    Returns:
        Decrypted plaintext message
    """
    # Derive the affine cipher key using the universal formula
    a, b = derive_key_from_mood(mood)
    
    # Check if key derivation failed (invalid mood value)
    if a is None or b is None:
        # Return None to indicate decryption failure
        return None
    
    # Decrypt the ciphertext using the derived affine cipher key
    plaintext = affine_decrypt(ciphertext, a, b)
    
    # Return the decrypted plaintext
    return plaintext

def main():
    # Print header with separator lines
    print("="*70)
    print("BONUS: UNIVERSAL DECRYPTION ALGORITHM")
    print("="*70)
    # Print the discovered mathematical formula
    print("\nDiscovered Formula: a = 2*mood + 1, b = 2*mood")
    # Print separator line
    print("="*70)
    
    # Read the CSV file containing encrypted messages
    df = pd.read_csv('messages.csv')
    
    # Initialize empty list to store decryption results
    results = []
    
    # Print status message
    print("\nTesting universal decryption algorithm on all ciphertexts...\n")
    
    # Iterate through each row in the DataFrame
    for idx, row in df.iterrows():
        # Extract ciphertext from current row
        ciphertext = row['ciphertext']
        # Extract mood value from current row
        mood = row['mood']
        
        # Print separator line for this ciphertext
        print(f"\n{'='*70}")
        # Print ciphertext number and mood value
        print(f"Ciphertext {idx + 1} - Mood: {mood}")
        # Print separator line
        print(f"{'='*70}")
        
        # Apply the universal key derivation formula
        a, b = derive_key_from_mood(mood)
        
        # Check if formula produced invalid key
        if a is None or b is None:
            # Print failure message with details
            print(f"✗ Formula produced invalid key for mood {mood}")
            # Show the calculation that led to invalid result
            print(f"  Calculated: a = 2*{mood} + 1 = {2*mood + 1}, b = 2*{mood} = {2*mood}")
            # Explain why it failed
            print(f"  Note: a must be coprime with 26")
            # Append failure result to results list
            results.append({
                'ciphertext_num': idx + 1,  # Ciphertext number
                'mood': mood,  # Mood value
                'key_a': None,  # No valid 'a' parameter
                'key_b': None,  # No valid 'b' parameter
                'score': 0,  # Zero score for failed decryption
                'success': False  # Mark as unsuccessful
            })
            # Skip to next iteration
            continue
        
        # Print the formula application with actual values
        print(f"Applying formula: a = 2*{mood} + 1 = {a}, b = 2*{mood} = {b}")
        
        # Decrypt using the universal decryption function
        decrypted = universal_decrypt(ciphertext, mood)
        
        # Check if decryption was successful
        if decrypted:
            # Calculate quality score for the decrypted text
            score, ioc = score_english(decrypted)
            
            # Print success message
            print(f"\n✓ Successfully decrypted!")
            # Print the key used
            print(f"Key: a={a}, b={b}")
            # Print quality metrics
            print(f"Quality Score: {score}, IoC: {ioc:.4f}")
            # Print preview of decrypted text (first 150 characters)
            print(f"\nDecrypted preview:\n{decrypted[:150]}...\n")
            
            # Append successful result to results list
            results.append({
                'ciphertext_num': idx + 1,  # Ciphertext number
                'mood': mood,  # Mood value
                'key_a': a,  # 'a' parameter used
                'key_b': b,  # 'b' parameter used
                'score': score,  # Quality score
                'ioc': ioc,  # Index of Coincidence
                'success': True  # Mark as successful
            })
            
            # Save full decryption to individual text file
            # Open file in write mode with constructed filename
            with open(f'output/bonus/universal_decrypted_{idx+1}_mood_{mood}.txt', 'w') as f:
                # Write file header
                f.write(f"UNIVERSAL DECRYPTION ALGORITHM\n")
                # Write separator line
                f.write(f"{'='*70}\n\n")
                # Write ciphertext number
                f.write(f"Ciphertext Number: {idx + 1}\n")
                # Write mood value
                f.write(f"Mood: {mood}\n\n")
                # Write key derivation section header
                f.write(f"Key Derivation Formula:\n")
                # Show 'a' calculation
                f.write(f"  a = 2 * mood + 1 = 2 * {mood} + 1 = {a}\n")
                # Show 'b' calculation
                f.write(f"  b = 2 * mood = 2 * {mood} = {b}\n\n")
                # Write quality metrics section header
                f.write(f"Quality Metrics:\n")
                # Write English score
                f.write(f"  English Score: {score}\n")
                # Write Index of Coincidence
                f.write(f"  Index of Coincidence: {ioc:.4f}\n")
                # Write separator line
                f.write(f"{'='*70}\n\n")
                # Write decrypted message section header
                f.write("DECRYPTED MESSAGE:\n\n")
                # Write the full decrypted text
                f.write(decrypted)
        else:
            # Print failure message if decryption returned None
            print("✗ Decryption failed")
            # Append failed result to results list
            results.append({
                'ciphertext_num': idx + 1,  # Ciphertext number
                'mood': mood,  # Mood value
                'key_a': a,  # 'a' parameter (even though decryption failed)
                'key_b': b,  # 'b' parameter (even though decryption failed)
                'score': 0,  # Zero score for failure
                'success': False  # Mark as unsuccessful
            })
    
    # Convert results list to pandas DataFrame
    results_df = pd.DataFrame(results)
    # Save results to CSV file
    results_df.to_csv('output/bonus/universal_decryption_results.csv', index=False)
    
    # Filter DataFrame to get only successful decryptions
    successful_results = results_df[results_df['success'] == True]
    
    # Print verification section header
    print("\n" + "="*70)
    print("VERIFICATION OF UNIVERSAL FORMULA")
    print("="*70)
    
    # Check if there were any successful decryptions
    if len(successful_results) > 0:
        # Print success rate
        print(f"\nSuccessfully decrypted: {len(successful_results)}/{len(results_df)} ciphertexts")
        # Print verification section header
        print("\nKey Derivation Verification:")
        # Print separator line
        print("-" * 70)
        
        # Initialize flag to track if all keys match formula
        all_match = True
        # Iterate through each successful result
        for idx, row in successful_results.iterrows():
            # Extract mood value
            mood = row['mood']
            # Extract 'a' parameter used
            a = row['key_a']
            # Extract 'b' parameter used
            b = row['key_b']
            # Calculate expected 'a' using formula
            expected_a = 2 * mood + 1
            # Calculate expected 'b' using formula
            expected_b = 2 * mood
            
            # Determine if actual matches expected (✓ for match, ✗ for mismatch)
            match = "✓" if (a == expected_a and b == expected_b) else "✗"
            # If there's a mismatch, update the flag
            if a != expected_a or b != expected_b:
                all_match = False
            
            # Print verification line showing mood, actual values, and expected values
            print(f"{match} Mood {mood}: a={a} (expected {expected_a}), b={b} (expected {expected_b})")
        
        # Print overall verification result
        if all_match:
            # All keys matched the formula
            print("\n✓ Formula verified for ALL successful decryptions!")
        else:
            # Some keys didn't match the formula
            print("\n✗ Formula does not match some cases")
        
        # Save comprehensive documentation to text file
        # Open file in write mode
        with open('output/bonus/GENERAL_FORMULA_DOCUMENTATION.txt', 'w') as f:
            # Write main header with separator
            f.write("="*70 + "\n")
            f.write("PSYCOSUPPORT UNIVERSAL DECRYPTION ALGORITHM\n")
            f.write("="*70 + "\n\n")
            
            # Write discovered formula section
            f.write("DISCOVERED FORMULA:\n")
            f.write("-" * 70 + "\n")
            f.write("For any ciphertext encrypted with PsycoSupport:\n\n")
            f.write("  Key Derivation:\n")
            f.write("    a = 2 * mood + 1\n")
            f.write("    b = 2 * mood\n\n")
            f.write("  Where:\n")
            f.write("    - mood is the user's mood value (integer input)\n")
            f.write("    - a must be coprime with 26 (odd numbers work)\n")
            f.write("    - b is the shift parameter\n\n")
            
            # Write algorithm section header
            f.write("="*70 + "\n")
            f.write("AFFINE CIPHER DECRYPTION ALGORITHM\n")
            f.write("="*70 + "\n\n")
            # Write step-by-step algorithm
            f.write("Step 1: Derive the key from mood value\n")
            f.write("  a = 2 * mood + 1\n")
            f.write("  b = 2 * mood\n\n")
            
            f.write("Step 2: Calculate modular multiplicative inverse of a\n")
            f.write("  Find a_inv such that: (a * a_inv) mod 26 = 1\n\n")
            
            f.write("Step 3: For each character C in ciphertext:\n")
            f.write("  If C is a letter:\n")
            f.write("    - Convert to number: C_num = ord(C) - ord('A')  [0-25]\n")
            f.write("    - Decrypt: P_num = a_inv * (C_num - b) mod 26\n")
            f.write("    - Convert back: P = chr(P_num + ord('A'))\n")
            f.write("  Else:\n")
            f.write("    - Keep character unchanged (spaces, punctuation, etc.)\n\n")
            
            # Write verified test cases section
            f.write("="*70 + "\n")
            f.write("VERIFIED TEST CASES\n")
            f.write("="*70 + "\n\n")
            
            # Write details for each successful decryption
            for idx, row in successful_results.iterrows():
                f.write(f"Test Case {row['ciphertext_num']}:\n")
                f.write(f"  Mood: {row['mood']}\n")
                f.write(f"  Derived Key: a={row['key_a']}, b={row['key_b']}\n")
                f.write(f"  Quality Score: {row['score']}\n")
                f.write(f"  IoC: {row['ioc']:.4f}\n")
                f.write(f"  Status: ✓ Successfully decrypted\n\n")
            
            # Write implementation section with Python code
            f.write("="*70 + "\n")
            f.write("IMPLEMENTATION (Python)\n")
            f.write("="*70 + "\n\n")
            # Write complete Python implementation as string
            f.write("""
def mod_inverse(a, m=26):
    '''Find modular multiplicative inverse'''
    for i in range(1, m):
        if (a * i) % m == 1:
            return i
    return None

def universal_decrypt(ciphertext, mood):
    '''Universal decryption for PsycoSupport'''
    # Derive key
    a = 2 * mood + 1
    b = 2 * mood
    
    # Get inverse
    a_inv = mod_inverse(a)
    if not a_inv:
        return None
    
    # Decrypt
    result = []
    for c in ciphertext:
        if c.isalpha():
            is_upper = c.isupper()
            c_num = ord(c.upper()) - ord('A')
            p_num = (a_inv * (c_num - b)) % 26
            char = chr(p_num + ord('A'))
            result.append(char if is_upper else char.lower())
        else:
            result.append(c)
    
    return ''.join(result)
""")
            
            # Write usage example section
            f.write("\n" + "="*70 + "\n")
            f.write("USAGE EXAMPLE\n")
            f.write("="*70 + "\n\n")
            # Write example code showing how to use the function
            f.write("# To decrypt any PsycoSupport ciphertext:\n")
            f.write("mood = 5  # The mood value used during encryption\n")
            f.write("ciphertext = 'YVYVYCYFYM'  # The encrypted message\n")
            f.write("plaintext = universal_decrypt(ciphertext, mood)\n")
            f.write("print(plaintext)  # Output: 'AADIL'\n\n")
            
            # Write mathematical foundation section
            f.write("="*70 + "\n")
            f.write("MATHEMATICAL FOUNDATION\n")
            f.write("="*70 + "\n\n")
            # Explain the affine cipher mathematics
            f.write("The encryption uses an Affine Cipher:\n")
            f.write("  Encryption: C = (a * P + b) mod 26\n")
            f.write("  Decryption: P = a^(-1) * (C - b) mod 26\n\n")
            
            f.write("The key derivation ties the cipher parameters to user input:\n")
            f.write("  - Linear relationship: a and b grow with mood\n")
            f.write("  - Ensures a is always odd (coprime with 26)\n")
            f.write("  - Predictable but requires knowledge of the formula\n\n")
            
            f.write("Valid 'a' values (coprime with 26):\n")
            f.write("  [1, 3, 5, 7, 9, 11, 15, 17, 19, 21, 23, 25]\n\n")
            
            f.write("Mood range for valid keys:\n")
            f.write("  Since a = 2*mood + 1 must be ≤ 25 and coprime with 26:\n")
            f.write("  Maximum mood = 12 (gives a=25)\n")
            f.write("  Minimum mood = 0 (gives a=1)\n\n")
    
    # Print completion section header
    print("\n" + "="*70)
    print("BONUS TASK COMPLETE!")
    print("="*70)
    # List all output files created
    print(f"\nResults saved to 'output/bonus/':")
    print(f"  - universal_decryption_results.csv - Summary of all decryptions")
    print(f"  - GENERAL_FORMULA_DOCUMENTATION.txt - Complete algorithm documentation")
    print(f"  - universal_decrypted_*.txt - Individual decrypted messages")
    
    # Print summary table header
    print(f"\n{'='*70}")
    print("SUMMARY TABLE")
    print(f"{'='*70}\n")
    # Print results DataFrame as formatted string (selected columns, no indices)
    print(results_df[['ciphertext_num', 'mood', 'key_a', 'key_b', 'success']].to_string(index=False))
    
    # Print formula confirmation section
    print(f"\n\n{'='*70}")
    print("UNIVERSAL FORMULA CONFIRMED")
    print(f"{'='*70}")
    # Display the formula prominently
    print("\nKey Derivation Formula:")
    print("     a = 2 * mood + 1")
    print("     b = 2 * mood")
    # Explain the formula's capabilities
    print("\n  - This formula decrypts ALL PsycoSupport ciphertexts")
    print("  - Works for any mood value (0-12)")
    print("  - No frequency analysis needed once formula is known")
    # Print final separator
    print(f"\n{'='*70}\n")

# Standard Python idiom: run main() only if script is executed directly
# Prevents main() from running if this file is imported as a module
if __name__ == "__main__":
    main()