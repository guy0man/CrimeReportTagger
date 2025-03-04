import tkinter as tk
import spacy
import re
from tkinter import scrolledtext
from spacy.lang.en.stop_words import STOP_WORDS
from string import punctuation

# Load spaCy model
nlp = spacy.load("custom_ner_model")

# Add Sentencizer if missing
if "sentencizer" not in nlp.pipe_names:
    nlp.add_pipe("sentencizer", before="ner")

def preprocess_text(text):
    """Preprocess text: lowercasing, removing URLs, punctuation, stopwords, and extra spaces."""
    text = text.lower()  # Convert to lowercase
    text = re.sub(r"http\S+|www\S+|https\S+", "", text, flags=re.MULTILINE)  # Remove URLs
    text = re.sub(r"[^\w\s]", "", text)  # Remove special characters & punctuation
    text = " ".join([word for word in text.split() if word not in STOP_WORDS])  # Remove stopwords
    text = " ".join(text.split())  # Remove extra spaces
    return text

def extract_entities():
    """Extract named entities after preprocessing the input text."""
    raw_text = text_input.get("1.0", tk.END).strip()
    cleaned_text = preprocess_text(raw_text)

    if not cleaned_text:
        output_display.config(state="normal")  # Enable editing before inserting
        output_display.delete("1.0", tk.END)
        output_display.insert(tk.END, "No valid text provided.")
        output_display.config(state="disabled")  # Make it read-only
        return

    doc = nlp(cleaned_text)

    # Sentence tokenization
    sentences = "\n".join([sent.text for sent in doc.sents])

    # Extract entities
    entities = "\n".join([f"{ent.text} ({ent.label_})" for ent in doc.ents])

    output_display.config(state="normal")  # Enable editing
    output_display.delete("1.0", tk.END)
    output_display.insert(tk.END, f"Entities:\n{entities if entities else 'No entities found.'}")
    output_display.config(state="disabled")  # Make it read-only

# UI setup
root = tk.Tk()
root.title("NER Extraction")

text_input = scrolledtext.ScrolledText(root, width=50, height=10)
text_input.pack()

process_button = tk.Button(root, text="Extract Entities", command=extract_entities)
process_button.pack()

output_display = scrolledtext.ScrolledText(root, width=50, height=10)
output_display.pack()
output_display.config(state="disabled") 

root.mainloop()