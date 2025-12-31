# Import pandas library for data manipulation and CSV operations
import pandas as pd
# Import matplotlib.pyplot for creating charts and visualizations
import matplotlib.pyplot as plt
# Import seaborn for enhanced statistical visualizations (imported but not used in this code)
import seaborn as sns
# Import Counter from collections for counting letter frequencies
from collections import Counter
# Import os module for file system operations
import os

# Create output directory for frequency analysis tables
# exist_ok=True prevents error if directory already exists
os.makedirs('output/frequency_tables', exist_ok=True)
# Create output directory for visualization charts
os.makedirs('output/charts', exist_ok=True)

# Standard English letter frequencies as percentages
# These are well-established frequencies for English text
# E is most common at 12.70%, Z is least common at 0.07%
ENGLISH_FREQ = {
    'E': 12.70, 'T': 9.06, 'A': 8.17, 'O': 7.51, 'I': 6.97,
    'N': 6.75, 'S': 6.33, 'H': 6.09, 'R': 5.99, 'D': 4.25,
    'L': 4.03, 'C': 2.78, 'U': 2.76, 'M': 2.41, 'W': 2.36,
    'F': 2.23, 'G': 2.02, 'Y': 1.97, 'P': 1.93, 'B': 1.29,
    'V': 0.98, 'K': 0.77, 'J': 0.15, 'X': 0.15, 'Q': 0.10, 'Z': 0.07
}

def analyze_ciphertext(ciphertext, idx):
    """Analyze frequency of letters in ciphertext"""
    # Remove all non-alphabetic characters and convert to uppercase
    # This creates a clean string with only letters for analysis
    clean_text = ''.join(c.upper() for c in ciphertext if c.isalpha())
    
    # Use Counter to count occurrences of each letter in the clean text
    letter_counts = Counter(clean_text)
    # Calculate total number of letters for percentage calculations
    total_letters = len(clean_text)
    
    # Initialize empty dictionary to store frequency information
    freq_dict = {}
    # Iterate through all 26 letters of the alphabet
    for letter in 'ABCDEFGHIJKLMNOPQRSTUVWXYZ':
        # Get the count for this letter (0 if letter doesn't appear)
        count = letter_counts.get(letter, 0)
        # Store both raw count and percentage frequency for this letter
        freq_dict[letter] = {
            # Raw count of how many times this letter appears
            'count': count,
            # Calculate percentage: (count / total) * 100, handle division by zero
            'frequency': (count / total_letters * 100) if total_letters > 0 else 0
        }
    
    # Return the frequency dictionary and total letter count
    return freq_dict, total_letters

def create_frequency_table(freq_dict, idx, mood):
    """Create and save frequency table"""
    # Convert frequency dictionary to pandas DataFrame
    # orient='index' means dictionary keys become row indices
    df = pd.DataFrame.from_dict(freq_dict, orient='index')
    # Sort DataFrame by frequency column in descending order (most frequent first)
    df = df.sort_values('frequency', ascending=False)
    # Add a column with standard English frequencies for comparison
    # Map each letter (index) to its English frequency from ENGLISH_FREQ dict
    df['english_freq'] = df.index.map(lambda x: ENGLISH_FREQ.get(x, 0))
    # Calculate difference between ciphertext frequency and English frequency
    # Positive = more common in ciphertext, negative = less common
    df['difference'] = df['frequency'] - df['english_freq']
    
    # Construct output filename with ciphertext number and mood
    output_file = f'output/frequency_tables/ciphertext_{idx}_mood_{mood}_frequency.csv'
    # Save the DataFrame to CSV file
    df.to_csv(output_file)
    # Print confirmation message with filename
    print(f"Saved frequency table: {output_file}")
    
    # Return the DataFrame for further use
    return df

def plot_frequency_chart(freq_dict, idx, mood, total_letters):
    """Create frequency comparison chart"""
    # Extract all letters as a list (A-Z in order)
    letters = list(freq_dict.keys())
    # Extract ciphertext frequencies for all letters
    cipher_freqs = [freq_dict[l]['frequency'] for l in letters]
    # Extract standard English frequencies for all letters
    english_freqs = [ENGLISH_FREQ.get(l, 0) for l in letters]
    
    # Create figure with 2 subplots stacked vertically
    # figsize=(14, 10) sets the figure size in inches
    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(14, 10))
    
    # Create first chart: Side-by-side bar comparison
    # Create range of x-positions (0-25 for 26 letters)
    x = range(26)
    # Set bar width for side-by-side bars
    width = 0.35
    # Plot ciphertext frequencies (shifted left by width/2)
    ax1.bar([i - width/2 for i in x], cipher_freqs, width, label='Ciphertext', alpha=0.8)
    # Plot English frequencies (shifted right by width/2)
    ax1.bar([i + width/2 for i in x], english_freqs, width, label='English', alpha=0.8)
    # Set x-axis label with font size
    ax1.set_xlabel('Letters', fontsize=12)
    # Set y-axis label with font size
    ax1.set_ylabel('Frequency (%)', fontsize=12)
    # Set chart title with ciphertext number, mood, and total letters
    ax1.set_title(f'Ciphertext {idx} (Mood {mood}) - Frequency Comparison\nTotal Letters: {total_letters}', fontsize=14)
    # Set x-axis tick positions to match bar positions
    ax1.set_xticks(x)
    # Set x-axis tick labels to be the letters A-Z
    ax1.set_xticklabels(letters)
    # Add legend to distinguish ciphertext vs English bars
    ax1.legend()
    # Add horizontal grid lines with transparency
    ax1.grid(axis='y', alpha=0.3)
    
    # Create second chart: Sorted frequency distribution (ciphertext only)
    # Sort frequency dictionary items by frequency in descending order
    sorted_items = sorted(freq_dict.items(), key=lambda x: x[1]['frequency'], reverse=True)
    # Extract letters in sorted order (most frequent first)
    sorted_letters = [item[0] for item in sorted_items]
    # Extract frequencies in sorted order
    sorted_freqs = [item[1]['frequency'] for item in sorted_items]
    
    # Plot bars for sorted frequencies
    ax2.bar(range(26), sorted_freqs, alpha=0.8, color='steelblue')
    # Set x-axis label
    ax2.set_xlabel('Letters (sorted by frequency)', fontsize=12)
    # Set y-axis label
    ax2.set_ylabel('Frequency (%)', fontsize=12)
    # Set chart title
    ax2.set_title(f'Ciphertext {idx} - Sorted Frequency Distribution', fontsize=14)
    # Set x-axis tick positions (0-25)
    ax2.set_xticks(range(26))
    # Set x-axis labels to sorted letters
    ax2.set_xticklabels(sorted_letters)
    # Add horizontal grid lines
    ax2.grid(axis='y', alpha=0.3)
    
    # Adjust subplot spacing to prevent overlap
    plt.tight_layout()
    # Construct output filename for the chart
    output_file = f'output/charts/ciphertext_{idx}_mood_{mood}_frequency_chart.png'
    # Save the figure as PNG with high resolution (300 DPI)
    plt.savefig(output_file, dpi=300, bbox_inches='tight')
    # Close the figure to free memory
    plt.close()
    # Print confirmation message
    print(f"Saved chart: {output_file}")

def main():
    # Read the CSV file containing encrypted messages
    df = pd.read_csv('messages.csv')
    
    # Print how many ciphertexts were found in the CSV
    print(f"Found {len(df)} ciphertexts to analyze\n")
    
    # Process each ciphertext in the DataFrame
    # iterrows() returns index and row data for each row
    for idx, row in df.iterrows():
        # Extract the ciphertext column from current row
        ciphertext = row['ciphertext']
        # Extract the mood value from current row
        mood = row['mood']
        
        # Print progress message showing which ciphertext is being processed
        print(f"Processing Ciphertext {idx + 1} (Mood: {mood})...")
        
        # Perform frequency analysis on the ciphertext
        # Returns dictionary of frequencies and total letter count
        freq_dict, total_letters = analyze_ciphertext(ciphertext, idx + 1)
        
        # Create and save frequency table as CSV
        # Returns DataFrame for additional processing
        freq_df = create_frequency_table(freq_dict, idx + 1, mood)
        
        # Create and save visualization charts
        plot_frequency_chart(freq_dict, idx + 1, mood, total_letters)
        
        # Get the 5 most frequent letters by selecting top 5 from sorted DataFrame
        # nlargest() returns top N rows based on specified column
        top_5 = freq_df.nlargest(5, 'frequency').index.tolist()
        # Print the top 5 most frequent letters, joined with commas
        print(f"Top 5 most frequent letters: {', '.join(top_5)}")
        # Print the total number of letters analyzed
        print(f"Total letters analyzed: {total_letters}\n")
    
    # Print completion message
    print("Frequency analysis complete!")
    # Tell user where to find CSV output files
    print("Check 'output/frequency_tables/' for CSV files")
    # Tell user where to find chart files
    print("Check 'output/charts/' for visualization charts")

# Standard Python idiom: run main() only if script is executed directly
if __name__ == "__main__":
    main()