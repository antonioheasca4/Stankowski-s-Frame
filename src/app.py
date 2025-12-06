"""
Stankowski's Frame - Demo Application
Visual Steganography & AI-Assisted Authentication for Deutsche Bank
"""

import streamlit as st
import os
import json
import sys
from PIL import Image
import io

# Add parent directory to path for imports
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from src.steganography import StankowskiEncoder, StankowskiDecoder, create_demo_data

# Page configuration
st.set_page_config(
    page_title="Stankowski's Frame",
    page_icon="🔒",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        font-weight: 700;
        color: #0018A8;
        text-align: center;
        margin-bottom: 1rem;
    }
    .sub-header {
        font-size: 1.2rem;
        color: #666;
        text-align: center;
        margin-bottom: 2rem;
    }
    .story-box {
        background-color: #f0f2f6;
        padding: 2rem;
        border-radius: 10px;
        border-left: 5px solid #0018A8;
        margin: 2rem 0;
    }
    .success-box {
        background-color: #d4edda;
        padding: 1.5rem;
        border-radius: 10px;
        border-left: 5px solid #28a745;
        margin: 1rem 0;
    }
    .fraud-alert {
        background-color: #f8d7da;
        padding: 2rem;
        border-radius: 10px;
        border-left: 5px solid #dc3545;
        margin: 1rem 0;
        font-size: 1.3rem;
        font-weight: bold;
        text-align: center;
    }
    .data-comparison {
        background-color: #fff3cd;
        padding: 1.5rem;
        border-radius: 10px;
        border-left: 5px solid #ffc107;
        margin: 1rem 0;
    }
</style>
""", unsafe_allow_html=True)


def show_narrative():
    """Display the narrative story"""
    st.markdown('<div class="story-box">', unsafe_allow_html=True)
    st.markdown("""
    ### 📖 The Story
    
    *"In 1974, Anton Stankowski created the Deutsche Bank symbol: a square and a diagonal line. 
    He called it 'Growth within a stable framework'. For 50 years, this 'frame' was just ink on paper. 
    Today, in the era of DeepFakes and document fraud, we activate Version 10.0. We transform Stankowski's 
    logo from a drawing into an invisible digital safe. We propose Stankowski's Frame: the physical document 
    becomes its own digital guarantee."*
    """)
    st.markdown('</div>', unsafe_allow_html=True)


def encoder_page():
    """Encoder interface"""
    st.markdown('<h2 style="color: #0018A8;">🔐 Document Encoder</h2>', unsafe_allow_html=True)
    st.markdown("Embed encrypted authentication data into your document's Deutsche Bank logo.")
    
    col1, col2 = st.columns([1, 1])
    
    with col1:
        st.subheader("Upload Document")
        uploaded_file = st.file_uploader(
            "Upload document with Deutsche Bank logo",
            type=['png', 'jpg', 'jpeg'],
            key="encoder_upload"
        )
        
        if uploaded_file:
            image = Image.open(uploaded_file)
            st.image(image, caption="Original Document", width="stretch")
    
    with col2:
        st.subheader("Secret Data to Embed")
        
        amount = st.text_input("Amount", value="10000", key="enc_amount")
        currency = st.text_input("Currency", value="EUR", key="enc_currency")
        iban = st.text_input("IBAN", value="DE89370400440532013000", key="enc_iban")
        date = st.date_input("Date", key="enc_date")
        doc_type = st.selectbox("Document Type", ["contract", "invoice", "statement"], key="enc_type")
        
        if st.button("🔒 Encode Document", type="primary"):
            if uploaded_file:
                with st.spinner("Embedding encrypted data..."):
                    # Prepare data
                    secret_data = {
                        "amount": amount,
                        "currency": currency,
                        "iban": iban,
                        "date": str(date),
                        "document_type": doc_type,
                        "secure_hash": "a7f3d9e2c1b4"
                    }
                    
                    # Save uploaded file temporarily
                    output_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), "output")
                    os.makedirs(output_dir, exist_ok=True)
                    temp_input = os.path.join(output_dir, "temp_input.png")
                    image.save(temp_input)
                    
                    # Encode
                    encoder = StankowskiEncoder()
                    output_path = os.path.join(output_dir, "encoded_document.png")
                    
                    if encoder.embed_data(temp_input, secret_data, output_path):
                        st.success("✅ Document encoded successfully!")
                        
                        # Show encoded image
                        encoded_img = Image.open(output_path)
                        st.image(encoded_img, caption="Encoded Document (with hidden data)", width="stretch")
                        
                        # Download button
                        with open(output_path, "rb") as f:
                            st.download_button(
                                "📥 Download Encoded Document",
                                data=f,
                                file_name="stankowski_secured_document.png",
                                mime="image/png"
                            )
                        
                        # Show embedded data
                        st.json(secret_data)
                        
                        # Cleanup
                        if os.path.exists(temp_input):
                            os.remove(temp_input)
                    else:
                        st.error("❌ Encoding failed. Please ensure the image is large enough.")
            else:
                st.warning("⚠️ Please upload a document first.")


def decoder_page():
    """Decoder and fraud detection interface"""
    st.markdown('<h2 style="color: #0018A8;">🔍 Document Validator & Fraud Detector</h2>', unsafe_allow_html=True)
    st.markdown("Upload a document to extract and verify its hidden authentication data.")
    
    col1, col2 = st.columns([1, 1])
    
    with col1:
        st.subheader("Upload Document to Verify")
        uploaded_file = st.file_uploader(
            "Upload document to validate",
            type=['png', 'jpg', 'jpeg'],
            key="decoder_upload"
        )
        
        if uploaded_file:
            image = Image.open(uploaded_file)
            st.image(image, caption="Document to Verify", width="stretch")
    
    with col2:
        st.subheader("Visible Data (Manual Entry)")
        st.markdown("*Enter what you see on the document:*")
        
        visible_amount = st.text_input("Visible Amount", value="50000", key="dec_amount")
        visible_currency = st.text_input("Visible Currency", value="EUR", key="dec_currency")
        visible_iban = st.text_input("Visible IBAN", value="DE89370400440532013000", key="dec_iban")
    
    if st.button("🔓 Validate Document", type="primary"):
        if uploaded_file:
            with st.spinner("Extracting hidden data from Stankowski's Frame..."):
                # Save uploaded file temporarily
                output_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), "output")
                os.makedirs(output_dir, exist_ok=True)
                temp_file = os.path.join(output_dir, "temp_decode.png")
                image.save(temp_file)
                
                # Decode
                decoder = StankowskiDecoder()
                hidden_data = decoder.extract_data(temp_file)
                
                if hidden_data:
                    st.success("✅ Hidden data extracted successfully!")
                    
                    # Compare data
                    st.markdown("---")
                    st.markdown("### 📊 Data Comparison")
                    
                    hidden_amount = hidden_data.get("amount", "N/A")
                    is_fraud = str(visible_amount) != str(hidden_amount)
                    
                    if is_fraud:
                        # FRAUD DETECTED - The WOW moment!
                        st.markdown('<div class="fraud-alert">⚠️ FRAUD DETECTED!</div>', unsafe_allow_html=True)
                        
                        col_a, col_b = st.columns(2)
                        
                        with col_a:
                            st.markdown("#### 👁️ Visible on Document")
                            st.markdown(f"**Amount:** {visible_amount} {visible_currency}")
                            st.markdown(f"**IBAN:** {visible_iban}")
                        
                        with col_b:
                            st.markdown("#### 🔒 Stankowski Secure Layer")
                            st.markdown(f"**Amount:** {hidden_amount} {hidden_data.get('currency', 'EUR')}")
                            st.markdown(f"**IBAN:** {hidden_data.get('iban', 'N/A')}")
                        
                        st.markdown('<div class="data-comparison">', unsafe_allow_html=True)
                        st.markdown("""
                        ### 🎯 Analysis
                        The hacker modified the visible text from **10,000 EUR** to **50,000 EUR**, 
                        but they forgot one crucial detail: **the logo is watching!** 
                        
                        Stankowski's Frame detected that the Deutsche Bank logo still contains 
                        the original encrypted data, proving this document has been tampered with.
                        """)
                        st.markdown('</div>', unsafe_allow_html=True)
                        
                    else:
                        # AUTHENTIC DOCUMENT
                        st.markdown('<div class="success-box">', unsafe_allow_html=True)
                        st.markdown("### ✅ AUTHENTIC DOCUMENT")
                        st.markdown("All data matches. This document is verified authentic.")
                        st.markdown('</div>', unsafe_allow_html=True)
                    
                    # Show full hidden data
                    st.markdown("---")
                    st.markdown("### 📄 Complete Hidden Data")
                    st.json(hidden_data)
                    
                    # Cleanup
                    if os.path.exists(temp_file):
                        os.remove(temp_file)
                else:
                    st.error("❌ No hidden data found. This document may not be Stankowski-secured.")
        else:
            st.warning("⚠️ Please upload a document first.")


def demo_scenario_page():
    """Pre-configured demo scenario"""
    st.markdown('<h2 style="color: #0018A8;">🎬 Live Demo Scenario</h2>', unsafe_allow_html=True)
    
    show_narrative()
    
    st.markdown("---")
    st.markdown("### 🎯 The WOW Moment")
    
    st.markdown("""
    This is the scenario you present to the judges:
    
    1. **The Setup**: A fraudster has modified a Deutsche Bank contract, changing 10,000 EUR to 50,000 EUR using Photoshop
    2. **The Trap**: They modified the visible text, but forgot about the logo
    3. **The Reveal**: Stankowski's Frame detects the fraud instantly
    """)
    
    st.info("💡 **Tip**: Use the 'Encoder' tab to create authentic documents, then the 'Decoder' tab to detect fraudulent ones!")
    
    # Instructions
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("#### 📝 Step 1: Create Authentic Document")
        st.markdown("""
        1. Go to **Encoder** tab
        2. Upload your `deutsche_bank_logo.png`
        3. Set Amount: **10000 EUR**
        4. Click "Encode Document"
        5. Download the secured document
        """)
    
    with col2:
        st.markdown("#### 🎭 Step 2: Simulate Fraud Detection")
        st.markdown("""
        1. Go to **Decoder** tab
        2. Upload the encoded document
        3. Enter Visible Amount: **50000 EUR** (fraudulent)
        4. Click "Validate Document"
        5. **FRAUD DETECTED!** 🚨
        """)


def main():
    """Main application"""
    
    # Header
    st.markdown('<div class="main-header">🔒 Stankowski\'s Frame</div>', unsafe_allow_html=True)
    st.markdown('<div class="sub-header">Visual Steganography & AI-Assisted Authentication</div>', unsafe_allow_html=True)
    
    # Sidebar
    with st.sidebar:
        st.image("https://upload.wikimedia.org/wikipedia/commons/thumb/7/7b/Deutsche_Bank_logo_without_wordmark.svg/240px-Deutsche_Bank_logo_without_wordmark.svg.png", width=150)
        
        st.markdown("### Navigation")
        page = st.radio(
            "Select Mode:",
            ["🎬 Demo Scenario", "🔐 Encoder", "🔍 Fraud Detector"],
            label_visibility="collapsed"
        )
        
        st.markdown("---")
        st.markdown("### About")
        st.markdown("""
        **Stankowski's Frame** transforms the 50-year-old Deutsche Bank logo 
        into an invisible digital safe using LSB steganography and AES-256 encryption.
        
        **Tech Stack:**
        - LSB Steganography
        - AES-256 Encryption
        - Python + Streamlit
        """)
        
        st.markdown("---")
        st.markdown("*Deutsche Bank Hackathon 5*")
    
    # Main content
    if page == "🎬 Demo Scenario":
        demo_scenario_page()
    elif page == "🔐 Encoder":
        encoder_page()
    elif page == "🔍 Fraud Detector":
        decoder_page()


if __name__ == "__main__":
    main()
