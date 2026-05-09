import streamlit as st
import string
from collections import Counter
import io

# --- LOGIC LAYER (Keeping your original logic intact) ---

def analyze_text_data(text_content):
    """Analyzes text string and returns counts and word frequency."""
    
    # basic string counts
    character_count = len(text_content)
    # Line counting
    line_count = text_content.count('\n') + 1 if text_content else 0

    # String cleaning for accurate word frequency.
    lower_text = text_content.lower()
    
    # Create a punctuation removal translator
    translator = str.maketrans('', '', string.punctuation)
    clean_text = lower_text.translate(translator)
    
    # Create the word list 
    word_list = clean_text.split()
    word_count = len(word_list)

    # DATA ANALYSIS
    word_frequencies = Counter(word_list)
    most_common_words = word_frequencies.most_common(10)
    
    # Pack the results
    analysis_results = {
        'lines': line_count,
        'words': word_count,
        'characters': character_count,
        'frequency_distribution': most_common_words,
        'unique_words_count': len(word_frequencies)
    }
    
    return analysis_results

# --- UI LAYER (Streamlit version of index.html) ---

st.title("Text File Analyzer")
st.write("Upload a plain text file to see its statistics.")

# Streamlit's native file uploader (Replaces Flask's <form>)
uploaded_file = st.file_uploader("Choose a file to analyze", type=['txt'])

if uploaded_file is not None:
    try:
        # Read the file directly from memory (no need for os.path or saving to /uploads)
        stringio = io.StringIO(uploaded_file.getvalue().decode("utf-8"))
        text_content = stringio.read()

        # Run Analysis
        analysis = analyze_text_data(text_content)

        # --- Display Results ---
        st.subheader("Analysis Results")
        
        # Displaying metrics in columns for a clean look
        col1, col2, col3 = st.columns(3)
        col1.metric("Lines", analysis['lines'])
        col2.metric("Words", analysis['words'])
        col3.metric("Characters", analysis['characters'])
        
        st.write(f"**Unique Words:** {analysis['unique_words_count']}")

        # Display Frequency Table
        st.write("### Top 10 Most Common Words")
        for word, count in analysis['frequency_distribution']:
            st.text(f"{word}: {count}")

    except UnicodeDecodeError:
        st.error("Error: The file does not appear to be a simple plain text (.txt) file.")
    except Exception as e:
        st.error(f"An error occurred while reading the file: {e}")

elif uploaded_file is None:
    st.info("Please select a file to analyze.")