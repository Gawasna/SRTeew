# SRTeew

SRT Subtitle Editor with Easy Workflow - Version 1.0

## Features

- Download and process .srt subtitle files
- Separate metadata and text content
- Support importing translations from .txt files or pasting directly
- Tabular interface displays ID, timestamp and content
- Pagination and content search
- Export .srt file with translated content

## Cài đặt

### From Source Code

1. Clone repository:
```bash
git clone https://github.com/Gawasna/SRTeew.git
cd SRTeew
```

2. Cài đặt dependencies:
```bash
pip install -r requirements.txt
```

3. Chạy ứng dụng:
```bash
python main.py
```

### From Executable File

1. Download the file SRTeew.exe from [Releases](https://github.com/Gawasna/SRTeew/releases)
2. Run the executable file

## Build

To create executable file:

```bash
python setup.py build
```

The executable file will be created in the `build` directory.

## Use

1. Download the .srt file to be processed
2. Export content to .txt file (if necessary)
3. Select the starting line by clicking
4. Import translation:
   - From .txt file: Click "Import translation"
   - Or paste directly (Ctrl+V)
5. Export the translated .srt file

## Shortcut key

- Ctrl + V: Paste the translation content
- Ctrl + Mouse wheel: Zoom in/out
- Ctrl + Plus/Minus: Change font size

## License

Distributed under the MIT License. See `LICENSE` for more information.

## Contact

Project Link: [https://github.com/your-username/SRTeew](https://github.com/Gawasna/SRTeew)
