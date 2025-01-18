import re
import os

class SubtitleProcessor:
    def __init__(self):
        self.reset_state()
    
    def reset_state(self):
        """Reset all internal state"""
        self.current_srt_file = None
        self.current_txt_file = None
        self.subtitle_entries = []  # List of (index, timestamp, content) tuples
        self.original_content = None
        self.start_line = None  # Starting line for translation
    
    def load_srt_file(self, file_path):
        """
        Load and parse .srt file
        Returns (success, message)
        """
        try:
            self.reset_state()
            self.current_srt_file = file_path
            
            with open(file_path, 'r', encoding='utf-8') as f:
                self.original_content = f.read()
                
            # Parse content into entries
            pattern = r'(\d+)\n(\d{2}:\d{2}:\d{2},\d{3} --> \d{2}:\d{2}:\d{2},\d{3})\n((?:.*\n)*?)\n'
            matches = re.finditer(pattern, self.original_content + '\n')
            
            for match in matches:
                index = int(match.group(1))
                timestamp = match.group(2)
                content = match.group(3).strip()
                self.subtitle_entries.append((index, timestamp, content))
            
            return True, len(self.subtitle_entries)
            
        except Exception as e:
            self.reset_state()
            return False, str(e)
    
    def extract_text_content(self, output_path=None):
        """
        Extract text content to .txt file
        Returns (success, message)
        """
        if not self.subtitle_entries:
            return False, "No subtitle loaded"
            
        try:
            if output_path is None:
                base_name = os.path.splitext(self.current_srt_file)[0]
                output_path = f"{base_name}_content.txt"
            
            with open(output_path, 'w', encoding='utf-8') as f:
                for _, _, content in self.subtitle_entries:
                    f.write(f"{content}\n")
            
            self.current_txt_file = output_path
            return True, output_path
            
        except Exception as e:
            return False, str(e)
    
    def import_translation(self, file_path, start_line=None):
        """
        Import translation from text file
        Returns (success, message)
        """
        if not self.subtitle_entries:
            return False, "No subtitle loaded"
            
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                translated_lines = [line.strip() for line in f.readlines()]
            
            return self.apply_translation(translated_lines, start_line)
            
        except Exception as e:
            return False, str(e)
    
    def apply_translation(self, translated_lines, start_line=None):
        """
        Apply translation lines starting from start_line
        Returns (success, message)
        """
        if start_line is None:
            start_line = self.start_line
            
        if start_line is None:
            return False, "No start line selected"
            
        if start_line >= len(self.subtitle_entries):
            return False, "Start line exceeds subtitle length"
            
        try:
            # Apply translations
            for i, new_content in enumerate(translated_lines):
                if start_line + i >= len(self.subtitle_entries):
                    break
                    
                if new_content.strip():  # Only update non-empty lines
                    self.update_content(start_line + i, new_content)
            
            return True, f"Updated {min(len(translated_lines), len(self.subtitle_entries) - start_line)} lines"
            
        except Exception as e:
            return False, str(e)
    
    def paste_translation(self, text, start_line=None):
        """
        Apply translation from pasted text
        Returns (success, message)
        """
        if not text.strip():
            return False, "No text to paste"
            
        translated_lines = text.strip().split('\n')
        return self.apply_translation(translated_lines, start_line)
    
    def set_start_line(self, line_number):
        """Set starting line for translation"""
        if 0 <= line_number < len(self.subtitle_entries):
            self.start_line = line_number
            return True
        return False
    
    def get_page_content(self, page, lines_per_page):
        """Get content for specified page"""
        if not self.subtitle_entries:
            return []
            
        start_idx = (page - 1) * lines_per_page
        end_idx = start_idx + lines_per_page
        
        # Return tuples of (index, timestamp, content)
        return [(index, timestamp, content) for index, timestamp, content in self.subtitle_entries[start_idx:end_idx]]
    
    def get_total_pages(self, lines_per_page):
        """Calculate total pages based on lines per page"""
        if not self.subtitle_entries:
            return 0
        return (len(self.subtitle_entries) + lines_per_page - 1) // lines_per_page
    
    def search_content(self, query):
        """
        Search for query in content
        Returns list of matching line indices
        """
        if not self.subtitle_entries:
            return []
            
        results = []
        for i, (_, _, content) in enumerate(self.subtitle_entries):
            if query.lower() in content.lower():
                results.append(i)
        return results
    
    def update_content(self, line_index, new_content):
        """Update content for specific line"""
        if 0 <= line_index < len(self.subtitle_entries):
            index, timestamp, _ = self.subtitle_entries[line_index]
            self.subtitle_entries[line_index] = (index, timestamp, new_content)
            return True
        return False
    
    def export_srt(self, output_path):
        """
        Export current state to .srt file
        Returns success boolean
        """
        if not self.subtitle_entries:
            return False
            
        try:
            with open(output_path, 'w', encoding='utf-8') as f:
                for index, timestamp, content in self.subtitle_entries:
                    f.write(f"{index}\n")
                    f.write(f"{timestamp}\n")
                    f.write(f"{content}\n\n")
            return True
            
        except Exception:
            return False 