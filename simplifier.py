# -*- coding: utf-8 -*-
"""
Core logic for the PlainSpeak Legal Analyzer.

This module contains the functions for performing lexical and syntactic
simplification of legal text.
"""

import re
import spacy
from jargon_map import LEGAL_JARGON_MAP

# Load the spaCy English model once when the module is imported for efficiency
try:
    nlp = spacy.load("en_core_web_sm")
except OSError:
    print("Downloading 'en_core_web_sm' model...")
    from spacy.cli import download
    download("en_core_web_sm")
    nlp = spacy.load("en_core_web_sm")


def simplify_lexically(text: str, changes_log: list) -> str:
    """
    Identifies and replaces words from the LEGAL_JARGON_MAP.

    Args:
        text (str): The original text to simplify.
        changes_log (list): A list to append change details to.

    Returns:
        str: The text with jargon terms replaced.
    """
    simplified_text = text
    
    # Sort keys by length, longest first, to avoid partial matches (e.g., matching "hereto" before "heretofore")
    sorted_jargon = sorted(LEGAL_JARGON_MAP.keys(), key=len, reverse=True)

    for jargon in sorted_jargon:
        simple_term = LEGAL_JARGON_MAP[jargon]
        # \b ensures we match whole words only, re.IGNORECASE for case-insensitivity
        pattern = r'\b' + re.escape(jargon) + r'\b'
        
        # Check if the term exists before trying to replace it
        if re.search(pattern, simplified_text, flags=re.IGNORECASE):
            changes_log.append({
                'type': 'lexical',
                'original': jargon,
                'simplified': simple_term,
            })
            simplified_text = re.sub(pattern, simple_term, simplified_text, flags=re.IGNORECASE)

    return simplified_text


def simplify_syntactically(text: str, changes_log: list) -> str:
    """
    Analyzes and simplifies sentence structure, primarily by splitting long sentences.

    Args:
        text (str): The text to process (ideally after lexical simplification).
        changes_log (list): A list to append change details to.

    Returns:
        str: The text with simplified sentence structures.
    """
    doc = nlp(text)
    simplified_sentences = []
    
    for sent in doc.sents:
        # Define criteria for a sentence that needs splitting
        is_long = len(sent) > 35  # Over 35 tokens is a good indicator
        has_semicolon = ';' in sent.text
        
        # --- SENTENCE SPLITTING LOGIC ---
        if is_long and has_semicolon:
            # Split the sentence by the first semicolon
            parts = sent.text.split(';', 1)
            
            if len(parts) == 2 and parts[0].strip() and parts[1].strip():
                new_sentence1 = parts[0].strip() + "."
                new_sentence2 = parts[1].strip().capitalize()
                
                simplified_sentences.append(new_sentence1)
                simplified_sentences.append(new_sentence2)
                
                changes_log.append({
                    'type': 'syntactic',
                    'original': sent.text,
                    'simplified': f"'{new_sentence1}' and '{new_sentence2}'",
                    'reason': f"Split a long sentence ({len(sent)} tokens) at a semicolon."
                })
                continue # Skip to the next sentence in the loop
        
        # If no split was made, add the original sentence back
        simplified_sentences.append(sent.text)

    return " ".join(simplified_sentences)
