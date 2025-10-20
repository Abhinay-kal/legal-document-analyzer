# -*- coding: utf-8 -*-
"""
Main application file for the PlainSpeak Legal Analyzer.

This script builds and launches the Gradio web interface, and it
orchestrates the simplification process by calling functions from the
simplifier module.
"""

import gradio as gr
from simplifier import simplify_lexically, simplify_syntactically

def analyze_and_simplify_text(legal_text: str) -> (str, str, str):
    """
    The main function called by the Gradio interface. It runs the full
    simplification pipeline and formats the results for display.

    Args:
        legal_text (str): The input text from the user.

    Returns:
        tuple: A tuple containing the original text, the fully simplified
               text, and a formatted string explaining the changes.
    """
    if not legal_text or not legal_text.strip():
        return "", "", "Please enter some text to analyze."

    changes_log = []

    # --- Step 1: Perform Lexical Simplification (Jargon Replacement) ---
    lexically_simplified_text = simplify_lexically(legal_text, changes_log)

    # --- Step 2: Perform Syntactic Simplification (Sentence Splitting) ---
    fully_simplified_text = simplify_syntactically(lexically_simplified_text, changes_log)

    # --- Step 3: Format the Explanation Log for Display ---
    explanation_output = "✅ Simplification Report:\n" + "="*25 + "\n"
    if not changes_log:
        explanation_output += "No simplifications were applied based on the current rules.\n"
    else:
        # Group changes by type for better readability
        lexical_changes = [c for c in changes_log if c['type'] == 'lexical']
        syntactic_changes = [c for c in changes_log if c['type'] == 'syntactic']

        if lexical_changes:
            explanation_output += "\n--- Jargon Replaced ---\n"
            for change in lexical_changes:
                explanation_output += f"• Replaced '{change['original']}' with '{change['simplified']}'.\n"
        
        if syntactic_changes:
            explanation_output += "\n--- Sentences Simplified ---\n"
            for change in syntactic_changes:
                explanation_output += f"• {change['reason']}\n"
        
        if not lexical_changes and not syntactic_changes:
             explanation_output += "No specific simplifications were applied.\n"


    return legal_text, fully_simplified_text, explanation_output

# --- Main execution block to launch the Gradio app ---
if __name__ == "__main__":
    iface = gr.Interface(
        fn=analyze_and_simplify_text,
        inputs=gr.Textbox(
            lines=15,
            label="📝 Paste Legal Text Here",
            placeholder="e.g., 'Whereas, pursuant to the agreement, the parties shall commence work...'"
        ),
        outputs=[
            gr.Textbox(label="📜 Original Text"),
            gr.Textbox(label="✨ Simplified Text"),
            gr.Textbox(label="🔍 Explanation of Changes")
        ],
        title="PlainSpeak Legal Analyzer",
        description="A tool to demystify complex legal text. It replaces jargon with plain English and simplifies complex sentences. The report below explains every change made.",
        allow_flagging='never',
        examples=[
            ["This agreement shall be governed by and construed in accordance with the laws of the aforementioned state, notwithstanding any conflict of law principles. The parties hereby consent to the exclusive jurisdiction of the courts located therein; furthermore, any failure to enforce a provision shall not constitute a waiver of said provision."],
            ["Pursuant to the terms stipulated herein, the lessee shall remit payment to the lessor forthwith."]
        ]
    )

    print("Launching the PlainSpeak Legal Analyzer...")
    iface.launch()
