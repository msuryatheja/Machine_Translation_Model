import streamlit as st
import time
from transformers import pipeline

# Initialize translation history, file upload history, and user input in session state if not already present
if "translation_history" not in st.session_state:
    st.session_state["translation_history"] = []
if "file_history" not in st.session_state:
    st.session_state["file_history"] = []
if "user_input" not in st.session_state:
    st.session_state["user_input"] = ""

st.title("Machine Translation Model")

# Choose the translation models from Hugging Face
translation_models = {
    "English to German": "Helsinki-NLP/opus-mt-en-de",
    "German to English": "Helsinki-NLP/opus-mt-de-en",
    "English to French": "Helsinki-NLP/opus-mt-en-fr",
    "French to English": "Helsinki-NLP/opus-mt-fr-en",
    "English to Urdu": "Helsinki-NLP/opus-mt-en-ur",
    "Urdu to English": "Helsinki-NLP/opus-mt-ur-en",
    "English to Spanish": "Helsinki-NLP/opus-mt-en-es",
    "Spanish to English": "Helsinki-NLP/opus-mt-es-en",
    "English to Chinese": "Helsinki-NLP/opus-mt-en-zh",
    "Chinese to English": "Helsinki-NLP/opus-mt-zh-en",
    "English to Telugu": "Helsinki-NLP/opus-mt-en-tl",
}

selected_translation = st.selectbox("Select translation model", list(translation_models.keys()))
translator = pipeline(task="translation", model=translation_models[selected_translation])

# Add file uploader for text file input
uploaded_file = st.file_uploader("Upload a text file for translation", type=["txt"])
if uploaded_file is not None:
    # Read the file content and store it in session state
    file_content = uploaded_file.read().decode("utf-8")
    st.session_state.file_history.append({"file_name": uploaded_file.name, "content": file_content})
    st.session_state.user_input = file_content

# Display text area for user input or pre-fill it with file content if available
user_input = st.text_area("Enter the text for translation:", st.session_state.user_input)

# Create the "Translate" button
translate_button_clicked = st.button("Translate")

# Handle translation
if translate_button_clicked:
    with st.spinner("Translating..."):
        time.sleep(2)
        if user_input:
            # Perform translation
            translated_text = translator(user_input, max_length=500)[0]['translation_text']
            # Add the translation to history
            st.session_state.translation_history.append({
                "Input": user_input,
                "Output": translated_text,
                "Configuration": selected_translation
            })
            # Display the result
            st.success(f"Translated Text: {translated_text}")
        else:
            st.warning("Please enter text for translation.")

# Clear button (placed outside the translation logic)
clear_button_clicked = st.button("Clear All History")

if clear_button_clicked:
    st.session_state.translation_history.clear()
    st.session_state.file_history.clear()
    st.session_state.user_input = ""
      # Reload the app to clear fields

# Display translation history and file upload history in the sidebar
with st.sidebar:
    st.header("Translation History")
    if st.session_state.translation_history:
        for i, entry in enumerate(st.session_state.translation_history[::-1]):
            st.write(f"**Translation {len(st.session_state.translation_history) - i}:**")
            st.write(f"**Configuration:** {entry['Configuration']}")
            st.write(f"**Input:** {entry['Input']}")
            st.write(f"**Output:** {entry['Output']}")
            st.markdown("---")
    else:
        st.write("No translations yet.")

    # File Upload History
    st.header("File Upload History")
    if st.session_state.file_history:
        for i, file_entry in enumerate(st.session_state.file_history[::-1]):
            st.write(f"**File {len(st.session_state.file_history) - i}:** {file_entry['file_name']}")
            st.text_area("File Content", value=file_entry['content'], height=100, key=f"file_{i}")
            st.markdown("---")
    else:
        st.write("No files uploaded yet.")

# About section
st.markdown("---")
st.subheader("About")
st.write("This is a Machine Translation Model, developed by M.Surya Theja, Rohini Reddy, and Yashakeerthi Lasya as a team.")
st.subheader('Work Process')
st.write("Select a translation model from the dropdown, upload a text file, or enter text, and click 'Translate' to see the translation.")
