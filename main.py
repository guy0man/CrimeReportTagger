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
root.geometry("1000x800")
root.title("Crime Report NER Extraction")

root.grid_rowconfigure(1, weight=1)
root.grid_columnconfigure(1, weight=1)
root.grid_columnconfigure(0, weight=1)

label1 = tk.Label(root, text="Enter Crime Report:",font=("Arial", 16, "bold"))
label1.grid(row=0, column=0, padx=5, pady=5)

text_input = scrolledtext.ScrolledText(root)
text_input.grid(row=1,column=0,sticky="nsew", padx=10)

process_button = tk.Button(root, text="Extract Entities",font=("Arial", 10) , command=extract_entities)
process_button.grid(row=2,column=0, padx=10, pady=5, sticky="ew")

label2 = tk.Label(root, text="Entities",font=("Arial", 16, "bold"))
label2.grid(row=0, column=1, padx=5, pady=5)

output_display = scrolledtext.ScrolledText(root)
output_display.grid(row=1,column=1,rowspan=2, sticky="nsew", padx=10)
output_display.config(state="disabled") 

root.mainloop()