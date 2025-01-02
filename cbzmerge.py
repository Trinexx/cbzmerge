import os
import zipfile
import shutil
import tempfile
import argparse
import re
from tqdm import tqdm
from PIL import Image

def is_double_page(filename):
    """Check if the filename indicates a double-page image."""
    return bool(re.match(r'^\d{2,4}-\d{2,4}\.jpg$', filename))

def unpack_cbz(inputdir, cbz_filename, tempdir):
    """Unpack a CBZ into its own subdirectory."""
    cbz_path = os.path.join(inputdir, cbz_filename)
    cbz_subdir = os.path.join(tempdir, os.path.splitext(cbz_filename)[0])
    os.makedirs(cbz_subdir, exist_ok=True)

    with zipfile.ZipFile(cbz_path, 'r') as zip_ref:
        zip_ref.extractall(cbz_subdir)
    
    return cbz_subdir

def export_to_pdf(files, output_pdf):
    """Export the files to a PDF using Pillow, with progress indication."""
    images = []
    for file in tqdm(files, desc="Exporting to PDF", unit="page"):
        img = Image.open(file)
        images.append(img.convert('RGB'))  # Convert to RGB if not already

    images[0].save(output_pdf, save_all=True, append_images=images[1:], resolution=100.0, quality=95)

def merge_cbz_files(inputdir, output_file, is_pdf=False):
    # Step 1: Create temporary directory
    tempdir = tempfile.mkdtemp()
    mergedir = os.path.join(tempdir, 'mergedir')
    os.makedirs(mergedir, exist_ok=True)

    # Step 2: Get a sorted list of CBZ files from the input directory
    cbz_files = sorted([f for f in os.listdir(inputdir) if f.endswith(".cbz")])

    # Step 3: Extract files from each CBZ into its own subdirectory
    subdirs = []
    for cbz_filename in tqdm(cbz_files, desc="Unpacking CBZ files"):
        subdir = unpack_cbz(inputdir, cbz_filename, tempdir)
        subdirs.append(subdir)

    # Step 4: Go through each subdirectory and copy files to the mergedir, renaming sequentially
    page_counter = 1
    files_to_export = []

    for subdir in tqdm(subdirs, desc="Renumbering and copying pages"):
        # Sort the files in the current subdirectory
        image_files = sorted([f for f in os.listdir(subdir) if f.lower().endswith(('.jpg', '.jpeg', '.png', '.gif'))])

        for filename in image_files:
            original_page = os.path.join(subdir, filename)

            # Check if the file is a double-page image (e.g., 18-19.jpg)
            if is_double_page(filename):
                # Preserve double-page structure and update the numbers
                base_name, ext = os.path.splitext(filename)
                new_base_name = f"{page_counter:02d}-{page_counter+1:02d}{ext}"
                new_page_path = os.path.join(mergedir, new_base_name)

                shutil.copy(original_page, new_page_path)
                files_to_export.append(new_page_path)
                page_counter += 2  # Skip two numbers for double-page
            else:
                # Single-page image: just renumber it
                base_name, ext = os.path.splitext(filename)
                new_page_name = f"{page_counter:02d}{ext}"
                new_page_path = os.path.join(mergedir, new_page_name)

                shutil.copy(original_page, new_page_path)
                files_to_export.append(new_page_path)
                page_counter += 1

    # Step 5: Create the output file (CBZ or PDF)
    if is_pdf:
        export_to_pdf(files_to_export, output_file)
    else:
        with zipfile.ZipFile(output_file, 'w', zipfile.ZIP_DEFLATED) as zip_out:
            for file_path in tqdm(files_to_export, desc="Creating output CBZ"):
                zip_out.write(file_path, arcname=os.path.basename(file_path))

    # Step 6: Clean up the temporary directory
    shutil.rmtree(tempdir)

    # Final message after completion
    print(f"Files have been successfully merged into {output_file}")

def main():
    # Set up command-line argument parsing with help descriptions
    parser = argparse.ArgumentParser(
        description="Merge multiple CBZ files into a single CBZ or PDF file. The program extracts all the pages from "
                    "the specified CBZ files, renumbers them sequentially, preserves double-page naming, "
                    "and creates a merged output file."
    )
    parser.add_argument(
        "inputdir", 
        help="Directory containing CBZ files to concatenate. All CBZ files in this directory will be unpacked and merged."
    )
    parser.add_argument(
        "output_file", 
        help="Output file name. This can be a CBZ file (with .cbz extension) or a PDF file (with .pdf extension)."
    )
    parser.add_argument(
        "--pdf", 
        action="store_true",
        help="If specified, the output file will be a PDF instead of a CBZ."
    )

    # Parse the arguments
    args = parser.parse_args()

    # Call the merge function
    merge_cbz_files(args.inputdir, args.output_file, is_pdf=args.pdf)

if __name__ == "__main__":
    main()
