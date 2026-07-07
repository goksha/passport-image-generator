import io
import streamlit as st
from PIL import Image, ImageOps

# Page Configuration
st.set_page_config(page_title="High-Res Passport Grid Generator", layout="centered")
st.title("📸 600 DPI Passport Photo $4 \\times 2$ Grid Generator")
st.write("Upload photos to generate grids of 4 columns and 2 rows dynamically arranged on a single A4 page.")

# Upload Multiple Files
uploaded_files = st.file_uploader("Choose photos...", type=["jpg", "jpeg", "png"], accept_multiple_files=True)

if uploaded_files:
    num_images = len(uploaded_files)
    
    # Standard A4 size at 600 DPI is 4960 x 7016 pixels
    A4_WIDTH = 4960
    A4_HEIGHT = 7016
    
    # Exact dimensions requested (35x45mm at 600 DPI)
    PASSPORT_W = 826  
    PASSPORT_H = 1063  
    
    # Corrected structure: 4 columns across, 2 rows down
    COLS, ROWS = 4, 2
    GAP_X, GAP_Y = 40, 40  # Gaps between individual photos
    
    # Calculate dimensions of a single 4x2 grid block
    BLOCK_W = (COLS * PASSPORT_W) + ((COLS - 1) * GAP_X)
    BLOCK_H = (ROWS * PASSPORT_H) + ((ROWS - 1) * GAP_Y)
    
    # 1. Determine dynamic multi-block layout on the single A4 page
    if num_images == 1:
        BLOCK_LAYOUT_COLS, BLOCK_LAYOUT_ROWS = 1, 1
    else:
        # Since a 4x2 horizontal block is quite wide, stacking them vertically 
        # (1 column of blocks, up to 3 blocks total) fits best on portrait A4.
        BLOCK_LAYOUT_COLS, BLOCK_LAYOUT_ROWS = 1, num_images
        if num_images > 3:
            st.warning("⚠️ Canvas limit: A portrait A4 sheet can comfortably hold up to 3 stacked horizontal blocks. Showing the first 3 photos.")
            uploaded_files = uploaded_files[:3]
            num_images = 3

    # Gaps between separate photo blocks
    BLOCK_GAP_Y = 250
    
    # Calculate overall layout size for center scaling
    TOTAL_LAYOUT_W = BLOCK_W
    TOTAL_LAYOUT_H = (BLOCK_LAYOUT_ROWS * BLOCK_H) + ((BLOCK_LAYOUT_ROWS - 1) * BLOCK_GAP_Y)
    
    PAGE_MARGIN_X = (A4_WIDTH - TOTAL_LAYOUT_W) // 2
    PAGE_MARGIN_Y = (A4_HEIGHT - TOTAL_LAYOUT_H) // 2

    # Create high-res white canvas
    a4_canvas = Image.new("RGB", (A4_WIDTH, A4_HEIGHT), "white")
    
    # 2. Distribute images into their respective blocks dynamically
    for idx, file in enumerate(uploaded_files):
        img = Image.open(file)
        img_cropped = ImageOps.fit(img, (PASSPORT_W, PASSPORT_H), Image.Resampling.LANCZOS)
        
        # Calculate vertical position for this block row
        block_start_x = PAGE_MARGIN_X
        block_start_y = PAGE_MARGIN_Y + idx * (BLOCK_H + BLOCK_GAP_Y)
        
        # Populate the 2 rows down x 4 columns across layout
        for row in range(ROWS):
            for col in range(COLS):
                x = block_start_x + col * (PASSPORT_W + GAP_X)
                y = block_start_y + row * (PASSPORT_H + GAP_Y)
                a4_canvas.paste(img_cropped, (x, y))

    # Preview Layout
    st.subheader("Preview (Single A4 Page)")
    st.image(a4_canvas, use_container_width=True)
        
    # PDF Compilation at 600 DPI
    pdf_buffer = io.BytesIO()
    a4_canvas.save(pdf_buffer, format="PDF", resolution=600.0)
    pdf_buffer.seek(0)
    
    st.download_button(
        label="📥 Download Printable 600 DPI PDF",
        data=pdf_buffer,
        file_name="passport_4x2_columns_collage.pdf",
        mime="application/pdf"
    )
