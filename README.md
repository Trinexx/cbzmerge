# CBZ Merger

This program allows you to merge multiple CBZ files into a single CBZ or PDF file. It extracts the pages from each CBZ, renumbers them sequentially, preserves double-page spreads (e.g., "18-19.jpg"), and creates an output file. You can use it to merge comic book archives, ensuring proper sequencing and presentation.

## Features

- **Merge multiple CBZ files**: The program extracts the pages from all CBZ files in the specified directory.
- **Sequential renumbering**: It renumbers the pages starting from `01`, picking up from where the previous file's pages left off.
- **Preserve double-page spreads**: Pages like `18-19.jpg` are preserved and renumbered properly.
- **Export to CBZ or PDF**: You can choose whether to output the merged content as a CBZ archive or a PDF.
- **Progress monitoring**: The program shows progress during the unpacking, renumbering, and export stages.
- **Command-line arguments**: Configure the input and output directories and select the format (CBZ or PDF) via command-line flags.

## Requirements

- Python 3.x
- Pillow
- tqdm

You can install the required dependencies using `pip`:

```
pip install Pillow tqdm
```

## Usage

### Merge CBZ files into a single CBZ

```bash
python cbzmerge.py /path/to/input/cbz/directory output.cbz
```

### Merge CBZ files into a single PDF

```bash
python cbzmerge.py /path/to/input/cbz/directory output.pdf --pdf
```

### Command-Line Arguments

- `inputdir`: The directory containing the CBZ files to be merged.
- `output_file`: The name of the output file (either `.cbz` or `.pdf`).
- `--pdf`: Optional flag to specify that the output should be a PDF instead of a CBZ.

## Example

Suppose you have three CBZ files:

- `comic1.cbz`
- `comic2.cbz`
- `comic3.cbz`

If you want to merge these into a single CBZ, put them into a directory named "comics" and then run the following:

```bash
python cbzmerge.py comics/ merged_comic.cbz
```

Or, to merge them into a PDF:

```bash
python cbzmerge.py comics/ merged_comic.pdf --pdf
```

The program will create an output file with properly sequentially numbered pages and preserve any double-page spreads.
  
## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
