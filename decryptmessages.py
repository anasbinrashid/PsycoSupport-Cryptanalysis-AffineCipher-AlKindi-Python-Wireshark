# Import pandas library for CSV file handling and data manipulation
import pandas as pd
# Import os module for operating system operations like creating directories
import os

# Create the output directory structure for storing decrypted files
# exist_ok=True means don't raise an error if the directory already exists
os.makedirs('output/decrypted', exist_ok=True)

def mod_inverse(a, m=26):
    """Find modular multiplicative inverse of a mod m"""
    # Loop through all possible values from 1 to m-1 (1 to 25 for alphabet)
    for i in range(1, m):
        # Check if (a * i) mod m equals 1, which means i is the modular inverse
        # The modular inverse a^(-1) satisfies: (a * a^(-1)) mod 26 = 1
        if (a * i) % m == 1:
            # Return the modular inverse if found
            return i
    # Return None if no modular inverse exists (happens when a is not coprime with m)
    return None

def affine_decrypt_char(c, a, b):
    """Decrypt a single character using affine cipher"""
    # Check if the character is not a letter (like space, punctuation, numbers)
    if not c.isalpha():
        # Return non-alphabetic characters unchanged
        return c
    
    # Calculate the modular multiplicative inverse of 'a' using our function
    a_inv = mod_inverse(a)
    # If no inverse exists, 'a' is not valid for affine cipher
    if a_inv is None:
        # Return None to indicate decryption failure
        return None
    
    # Check if the character is uppercase and store this information
    is_upper = c.isupper()
    # Convert the character to uppercase for processing
    c = c.upper()
    
    # Apply affine cipher decryption formula: P = a^(-1) * (C - b) mod 26
    # ord(c) - ord('A') converts letter to number (A=0, B=1, ..., Z=25)
    # Subtract b (the shift parameter), multiply by a_inv, then mod 26
    decrypted = (a_inv * (ord(c) - ord('A') - b)) % 26
    # Convert the decrypted number back to a letter by adding to ord('A')
    result = chr(decrypted + ord('A'))
    
    # Return the result in its original case (uppercase if was uppercase, else lowercase)
    return result if is_upper else result.lower()

def affine_decrypt(ciphertext, a, b):
    """Decrypt entire text using affine cipher"""
    # Use list comprehension to decrypt each character
    # If character is alphabetic, decrypt it; otherwise keep it as is
    # Join all characters back into a single string
    return ''.join(affine_decrypt_char(c, a, b) if c.isalpha() else c for c in ciphertext)

def decrypt_all_fields(row, a, b):
    """Decrypt all encrypted fields in a row"""
    # Create a dictionary to store all decrypted data from the CSV row
    decrypted_data = {
        # Decrypt the encrypted username field using affine cipher
        'username': affine_decrypt(row['username_enc'], a, b),
        # Decrypt the encrypted message field using affine cipher
        'message': affine_decrypt(row['message_enc'], a, b),
        # Decrypt the encrypted API key field using affine cipher
        'api_key': affine_decrypt(row['api_key_enc'], a, b),
        # Decrypt the ciphertext (the main encrypted response) using affine cipher
        'ciphertext': affine_decrypt(row['ciphertext'], a, b)
    }
    # Return the dictionary containing all decrypted fields
    return decrypted_data


# KEY_MAP: Dictionary mapping mood values to their corresponding affine cipher keys
# Format: mood_value: (a_parameter, b_parameter)
# These keys follow the pattern a = 2*mood + 1, b = 2*mood
KEY_MAP = {
    3: (7, 6),    # Mood 3: a=7, b=6
    5: (11, 10),  # Mood 5: a=11, b=10
    7: (15, 14),  # Mood 7: a=15, b=14
    10: (21, 20)  # Mood 10: a=21, b=20
}


def main():
    # Read the CSV file containing encrypted messages into a pandas DataFrame
    df = pd.read_csv('messages.csv')
    
    # Print a header separator line (70 equals signs)
    print(f"{'='*70}")
    # Print the main title of the decryption process
    print("DECRYPTING ALL MESSAGES")
    # Print another separator line
    print(f"{'='*70}\n")
    
    # Initialize an empty list to store results from all decryptions
    decrypted_results = []
    
    # Iterate through each row in the DataFrame using iterrows()
    # idx is the row index, row is the actual row data
    for idx, row in df.iterrows():
        # Extract the mood value from the current row
        mood = row['mood']
        
        # Print a separator line for this specific ciphertext
        print(f"\n{'='*70}")
        # Print which ciphertext we're working on (idx+1 for human-readable numbering)
        print(f"Ciphertext {idx + 1} - Mood: {mood}")
        # Print another separator line
        print(f"{'='*70}")
        
        # Check if the current mood value exists in our KEY_MAP dictionary
        if mood not in KEY_MAP:
            # Print a warning if no key exists for this mood
            print(f"WARNING: No key found for mood {mood}. Skipping...")
            # Skip to the next iteration of the loop
            continue
        
        # Retrieve the affine cipher parameters (a, b) for this mood from KEY_MAP
        a, b = KEY_MAP[mood]
        # Print which key we're using for decryption
        print(f"Using key: a={a}, b={b}")
        
        # Decrypt all fields in the current row using the retrieved key
        decrypted = decrypt_all_fields(row, a, b)
        
        # Print the fully decrypted ciphertext (the psychologist's response)
        print(f"\nDecrypted Ciphertext (full response):\n{decrypted['ciphertext']}\n")
        
        # Open a new file to save this individual decryption result
        # File naming pattern: ciphertext_{number}_mood_{mood_value}_decrypted.txt
        # 'w' mode means write (create new or overwrite), encoding='utf-8' for Unicode support
        with open(f'output/decrypted/ciphertext_{idx+1}_mood_{mood}_decrypted.txt', 'w', encoding='utf-8') as f:
            # Write the ciphertext number identifier
            f.write(f"Ciphertext Number: {idx + 1}\n")
            # Write the mood value used
            f.write(f"Mood: {mood}\n")
            # Write the key parameters used for decryption
            f.write(f"Key Used: a={a}, b={b}\n")
            # Write a separator line
            f.write(f"{'='*70}\n\n")
            # Write the original encrypted username
            f.write(f"Encrypted Username: {row['username_enc']}\n")
            # Write the original encrypted message
            f.write(f"Encrypted Message: {row['message_enc']}\n")
            # Write another separator line
            f.write(f"{'='*70}\n")
            # Write a header for the decrypted response section
            f.write(f"PSYCHOLOGIST'S RESPONSE (DECRYPTED):\n")
            # Write another separator line
            f.write(f"{'='*70}\n\n")
            # Write the fully decrypted response text
            f.write(decrypted['ciphertext'])
        
        # Append a summary of this decryption to our results list
        decrypted_results.append({
            # Store the ciphertext number
            'ciphertext_num': idx + 1,
            # Store the mood value
            'mood': mood,
            # Store the 'a' parameter of the key
            'key_a': a,
            # Store the 'b' parameter of the key
            'key_b': b,
            # Store the encrypted username
            'username_encrypted': row['username_enc'],
            # Store first 50 characters of encrypted message plus ellipsis
            'message_encrypted': row['message_enc'][:50] + '...',
            # Store first 100 characters of decrypted response plus ellipsis
            'response_decrypted': decrypted['ciphertext'][:100] + '...'
        })
    
    # Convert the results list into a DataFrame for easy CSV export
    results_df = pd.DataFrame(decrypted_results)
    # Save the full summary DataFrame to CSV (without row indices)
    results_df.to_csv('output/decrypted/decryption_summary.csv', index=False)
    
    # Create a cleaner summary with only the essential columns
    summary_df = results_df[['ciphertext_num', 'mood', 'key_a', 'key_b']]
    # Save the clean summary to a separate CSV file
    summary_df.to_csv('output/decrypted/keys_used_summary.csv', index=False)
    
    # Print final completion message with separator
    print(f"\n{'='*70}")
    print("DECRYPTION COMPLETE!")
    print(f"{'='*70}")
    # Inform user where the decrypted files are saved
    print(f"\nAll decrypted files saved to 'output/decrypted/'")
    # Inform user where the summary file is saved
    print(f"Summary saved to 'output/decrypted/decryption_summary.csv'")
    
    # Print a header for the keys summary table
    print("\n\nKEYS USED FOR EACH MOOD:")
    # Print the summary DataFrame as a formatted string table (without indices)
    print(summary_df.to_string(index=False))

# Standard Python idiom: only run main() if this script is executed directly
# (not when imported as a module)
if __name__ == "__main__":
    main()