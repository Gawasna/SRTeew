import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import customtkinter as ctk
import os
from subtitle_processor import SubtitleProcessor
from update_checker import UpdateChecker

APP_NAME = "SRTeew"
APP_VERSION = "1.0"

class SubtitleApp:
    def __init__(self, root):
        self.root = root
        self.processor = SubtitleProcessor()
        self.selected_line = None
        self.update_checker = UpdateChecker(APP_VERSION)
        self.setup_gui()
        self.setup_bindings()
        self.check_for_updates()
        
    def check_for_updates(self):
        """Kiểm tra cập nhật khi khởi động"""
        has_update, latest_version, notes = self.update_checker.check_for_updates()
        if has_update:
            if messagebox.askyesno(
                "Cập nhật mới",
                f"Đã có phiên bản mới: v{latest_version}\n\nBạn có muốn xem changelog không?"
            ):
                self.show_changelog()
                
    def show_changelog(self):
        """Hiển thị changelog trong cửa sổ mới"""
        changelog_window = tk.Toplevel(self.root)
        changelog_window.title("Changelog")
        changelog_window.geometry("600x400")
        
        # Tạo text area để hiển thị changelog
        text_area = tk.Text(changelog_window, wrap=tk.WORD, padx=10, pady=10)
        text_area.pack(fill=tk.BOTH, expand=True)
        text_area.insert("1.0", self.update_checker.get_changelog())
        text_area.configure(state='disabled')
        
        # Thêm scrollbar
        scrollbar = ttk.Scrollbar(changelog_window, command=text_area.yview)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        text_area.configure(yscrollcommand=scrollbar.set)
        
        # Nút Download
        download_btn = ctk.CTkButton(
            changelog_window,
            text="Tải phiên bản mới",
            command=self.update_checker.open_download_page
        )
        download_btn.pack(pady=10)
    
    def setup_bindings(self):
        """Setup keyboard shortcuts"""
        self.root.bind('<Control-v>', self.handle_paste)
        self.root.bind('<Control-plus>', self.increase_font_size)
        self.root.bind('<Control-minus>', self.decrease_font_size)
        self.text_area.bind('<Control-MouseWheel>', self.zoom)
        
    def setup_gui(self):
        # Configure window
        self.root.title(f"{APP_NAME} v{APP_VERSION}")
        self.root.geometry("1920x1080")
        
        # Create main frames
        self.create_header()
        self.create_content_area()
        self.create_sidebar()
        self.create_footer()
    
    def create_header(self):
        """Create header with tools"""
        header = ttk.Frame(self.root)
        header.pack(fill=tk.X, padx=5, pady=5)
        
        # App info
        app_label = ttk.Label(
            header,
            text=f"{APP_NAME} v{APP_VERSION}",
            font=("Helvetica", 12, "bold")
        )
        app_label.pack(side=tk.LEFT, padx=10)
        
        # Check update button
        update_btn = ctk.CTkButton(
            header,
            text="Kiểm tra cập nhật",
            command=self.check_for_updates
        )
        update_btn.pack(side=tk.LEFT, padx=5)
        
        # Separator
        ttk.Separator(header, orient="vertical").pack(side=tk.LEFT, fill="y", padx=10, pady=5)
        
        # Load file button
        load_btn = ctk.CTkButton(
            header, 
            text="Tải file SRT",
            command=self.load_file
        )
        load_btn.pack(side=tk.LEFT, padx=5)
        
        # Import translation button
        import_btn = ctk.CTkButton(
            header,
            text="Nhập bản dịch",
            command=self.import_translation
        )
        import_btn.pack(side=tk.LEFT, padx=5)
        
        # Page size configuration
        ttk.Label(header, text="Số dòng/trang:").pack(side=tk.LEFT, padx=5)
        self.page_size_var = tk.StringVar(value="30")
        self.page_size_var.trace_add("write", self.on_page_size_change)
        page_size = ttk.Spinbox(
            header,
            from_=10,
            to=50,
            textvariable=self.page_size_var,
            width=10
        )
        page_size.pack(side=tk.LEFT, padx=5)
        
        # Current page display
        self.page_display_var = tk.StringVar(value="Trang: 0/0")
        ttk.Label(header, textvariable=self.page_display_var).pack(side=tk.LEFT, padx=20)
        
        # Font size controls
        font_frame = ttk.Frame(header)
        font_frame.pack(side=tk.LEFT, padx=20)
        
        ttk.Label(font_frame, text="Cỡ chữ:").pack(side=tk.LEFT)
        self.font_size = 11
        font_minus = ctk.CTkButton(
            font_frame,
            text="-",
            width=30,
            command=self.decrease_font_size
        )
        font_minus.pack(side=tk.LEFT, padx=2)
        
        font_plus = ctk.CTkButton(
            font_frame,
            text="+",
            width=30,
            command=self.increase_font_size
        )
        font_plus.pack(side=tk.LEFT, padx=2)
        
        # Status bar
        self.status_var = tk.StringVar(value="Chưa tải file")
        status = ttk.Label(header, textvariable=self.status_var)
        status.pack(side=tk.RIGHT, padx=5)
    
    def create_content_area(self):
        """Create main content area"""
        content = ttk.Frame(self.root)
        content.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # Create ID display area
        self.id_area = tk.Text(content, wrap=tk.WORD, font=("Courier New", self.font_size),
                              width=6, bg='lightgray')
        self.id_area.pack(side=tk.LEFT, fill=tk.Y)
        self.id_area.configure(state='disabled')  # Make it read-only
        
        # Create timestamp display area
        self.timestamp_area = tk.Text(content, wrap=tk.WORD, font=("Courier New", self.font_size),
                                    width=30, bg='#f0f0f0')
        self.timestamp_area.pack(side=tk.LEFT, fill=tk.Y)
        self.timestamp_area.configure(state='disabled')
        
        # Create text display area with scrollbar
        self.text_area = tk.Text(content, wrap=tk.WORD, font=("Courier New", self.font_size))
        self.text_area.tag_configure("selected_line", background="yellow")
        self.text_area.bind("<ButtonRelease-1>", self.on_text_click)
        
        # Sync scrolling between all areas
        def on_text_scroll(*args):
            self.id_area.yview_moveto(args[0])
            self.timestamp_area.yview_moveto(args[0])
            
        def on_mousewheel(event):
            self.id_area.yview_scroll(int(-1*(event.delta/120)), "units")
            self.timestamp_area.yview_scroll(int(-1*(event.delta/120)), "units")
            return "break"
        
        scrollbar = ttk.Scrollbar(content, command=self.text_area.yview)
        self.text_area.configure(yscrollcommand=lambda *args: (
            scrollbar.set(*args), 
            on_text_scroll(args[0])
        ))
        self.text_area.bind("<MouseWheel>", on_mousewheel)
        
        self.text_area.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Add column headers
        header_frame = ttk.Frame(content)
        header_frame.pack(fill=tk.X, before=self.id_area)
        
        ttk.Label(header_frame, text="ID", width=6, anchor="center",
                 background="lightgray").pack(side=tk.LEFT)
        ttk.Label(header_frame, text="Timestamp", width=30, anchor="center",
                 background="#f0f0f0").pack(side=tk.LEFT)
        ttk.Label(header_frame, text="Content", anchor="w").pack(side=tk.LEFT, fill=tk.X, expand=True)
    
    def create_sidebar(self):
        """Create sidebar with navigation"""
        sidebar = ttk.Frame(self.root)
        sidebar.pack(side=tk.RIGHT, fill=tk.Y, padx=5, pady=5)
        
        # Navigation buttons
        prev_btn = ctk.CTkButton(
            sidebar,
            text="Trang trước",
            command=self.prev_page
        )
        prev_btn.pack(pady=5)
        
        next_btn = ctk.CTkButton(
            sidebar,
            text="Trang sau",
            command=self.next_page
        )
        next_btn.pack(pady=5)
        
        # Search box
        ttk.Label(sidebar, text="Tìm kiếm:").pack(pady=5)
        self.search_var = tk.StringVar()
        search_entry = ttk.Entry(
            sidebar,
            textvariable=self.search_var
        )
        search_entry.pack(pady=5)
        
        search_btn = ctk.CTkButton(
            sidebar,
            text="Tìm",
            command=self.search_content
        )
        search_btn.pack(pady=5)
        
        # Extract text button
        extract_btn = ctk.CTkButton(
            sidebar,
            text="Xuất text",
            command=self.extract_text
        )
        extract_btn.pack(pady=20)
    
    def create_footer(self):
        """Create footer with action buttons"""
        footer = ttk.Frame(self.root)
        footer.pack(fill=tk.X, padx=5, pady=5)
        
        # Action buttons
        select_btn = ctk.CTkButton(
            footer,
            text="Chọn dòng bắt đầu",
            command=self.select_start_line
        )
        select_btn.pack(side=tk.LEFT, padx=5)
        
        revert_btn = ctk.CTkButton(
            footer,
            text="Hoàn tác",
            command=self.revert_changes
        )
        revert_btn.pack(side=tk.LEFT, padx=5)
        
        export_btn = ctk.CTkButton(
            footer,
            text="Xuất file",
            command=self.export_file
        )
        export_btn.pack(side=tk.RIGHT, padx=5)
    
    def load_file(self):
        """Handle file loading"""
        file_path = filedialog.askopenfilename(
            filetypes=[("Subtitle files", "*.srt")]
        )
        if file_path:
            success, result = self.processor.load_srt_file(file_path)
            if success:
                self.update_status(f"Đã tải file: {os.path.basename(file_path)} ({result} dòng)")
                self.current_page = 1
                self.update_page_display()
                self.update_content_display()
            else:
                messagebox.showerror("Lỗi", f"Không thể tải file: {result}")
    
    def on_page_size_change(self, *args):
        """Handle page size change"""
        try:
            page_size = int(self.page_size_var.get())
            if self.processor.current_srt_file:
                self.current_page = 1
                self.update_page_display()
                self.update_content_display()
        except ValueError:
            pass
    
    def update_page_display(self):
        """Update page navigation display"""
        total_pages = self.processor.get_total_pages(int(self.page_size_var.get()))
        self.page_display_var.set(f"Trang: {self.current_page}/{total_pages}")
    
    def update_content_display(self):
        """Update content display"""
        self.text_area.delete("1.0", tk.END)
        self.id_area.configure(state='normal')
        self.id_area.delete("1.0", tk.END)
        self.timestamp_area.configure(state='normal')
        self.timestamp_area.delete("1.0", tk.END)
        
        content = self.processor.get_page_content(
            self.current_page,
            int(self.page_size_var.get())
        )
        
        for index, timestamp, text in content:
            # Display ID
            self.id_area.insert(tk.END, f"{index:4d}\n")
            # Display timestamp
            self.timestamp_area.insert(tk.END, f"{timestamp}\n")
            # Display content
            self.text_area.insert(tk.END, f"{text}\n")
        
        self.id_area.configure(state='disabled')
        self.timestamp_area.configure(state='disabled')
    
    def prev_page(self):
        """Navigate to previous page"""
        if self.current_page > 1:
            self.current_page -= 1
            self.update_page_display()
            self.update_content_display()
    
    def next_page(self):
        """Navigate to next page"""
        total_pages = self.processor.get_total_pages(int(self.page_size_var.get()))
        if self.current_page < total_pages:
            self.current_page += 1
            self.update_page_display()
            self.update_content_display()
    
    def on_text_click(self, event):
        """Handle text click for line selection"""
        if not self.processor.current_srt_file:
            return
            
        # Get clicked line
        index = self.text_area.index(f"@{event.x},{event.y}")
        line_num = int(float(index))
        
        # Calculate actual line number
        page_size = int(self.page_size_var.get())
        start_idx = (self.current_page - 1) * page_size
        self.selected_line = start_idx + line_num - 1
        
        # Update highlight
        self.text_area.tag_remove("selected_line", "1.0", tk.END)
        self.text_area.tag_add("selected_line", f"{line_num}.0", f"{line_num + 1}.0")
    
    def search_content(self):
        """Search content"""
        if not self.processor.current_srt_file:
            return
            
        query = self.search_var.get()
        if not query:
            return
            
        results = self.processor.search_content(query)
        if results:
            # Go to first result
            page_size = int(self.page_size_var.get())
            result_page = (results[0] // page_size) + 1
            self.current_page = result_page
            self.update_page_display()
            self.update_content_display()
            
            # Highlight result
            line_in_page = results[0] % page_size + 1
            self.text_area.tag_remove("selected_line", "1.0", tk.END)
            self.text_area.tag_add("selected_line", f"{line_in_page}.0", f"{line_in_page + 1}.0")
            self.selected_line = results[0]
        else:
            messagebox.showinfo("Tìm kiếm", "Không tìm thấy kết quả")
    
    def select_start_line(self):
        """Handle start line selection"""
        if self.selected_line is None:
            messagebox.showwarning("Chọn dòng", "Vui lòng chọn dòng bắt đầu")
            return
        
        if self.processor.set_start_line(self.selected_line):
            messagebox.showinfo("Đã chọn", f"Đã chọn dòng bắt đầu: {self.selected_line + 1}")
        else:
            messagebox.showerror("Lỗi", "Không thể chọn dòng này")
    
    def extract_text(self):
        """Extract text content to file"""
        if not self.processor.current_srt_file:
            messagebox.showwarning("Xuất text", "Vui lòng tải file SRT trước")
            return
            
        success, result = self.processor.extract_text_content()
        if success:
            messagebox.showinfo("Xuất text", f"Đã xuất nội dung ra file:\n{result}")
        else:
            messagebox.showerror("Lỗi", f"Không thể xuất text: {result}")
    
    def revert_changes(self):
        """Revert changes"""
        if not self.processor.current_srt_file:
            return
            
        if messagebox.askyesno("Xác nhận", "Bạn có chắc muốn hoàn tác các thay đổi?"):
            success, _ = self.processor.load_srt_file(self.processor.current_srt_file)
            if success:
                self.update_content_display()
                messagebox.showinfo("Hoàn tác", "Đã hoàn tác về trạng thái ban đầu")
    
    def export_file(self):
        """Export processed file"""
        if not self.processor.current_srt_file:
            messagebox.showwarning("Xuất file", "Vui lòng tải file SRT trước")
            return
            
        file_path = filedialog.asksaveasfilename(
            defaultextension=".srt",
            filetypes=[("Subtitle files", "*.srt")],
            initialfile=f"translated_{os.path.basename(self.processor.current_srt_file)}"
        )
        
        if file_path:
            if self.processor.export_srt(file_path):
                messagebox.showinfo("Xuất file", "Đã xuất file thành công")
            else:
                messagebox.showerror("Lỗi", "Không thể xuất file")
    
    def update_status(self, message):
        """Update status bar"""
        self.status_var.set(message)
    
    def handle_paste(self, event=None):
        """Handle paste event"""
        if self.selected_line is None:
            messagebox.showwarning("Paste", "Vui lòng chọn dòng bắt đầu trước khi paste")
            return
            
        try:
            text = self.root.clipboard_get()
            success, message = self.processor.paste_translation(text, self.selected_line)
            
            if success:
                self.update_content_display()
                messagebox.showinfo("Paste", message)
            else:
                messagebox.showerror("Lỗi", f"Không thể paste: {message}")
                
        except tk.TclError:
            messagebox.showerror("Lỗi", "Không có nội dung trong clipboard")
    
    def import_translation(self):
        """Import translation from file"""
        if not self.processor.current_srt_file:
            messagebox.showwarning("Nhập bản dịch", "Vui lòng tải file SRT trước")
            return
            
        if self.selected_line is None:
            messagebox.showwarning("Nhập bản dịch", "Vui lòng chọn dòng bắt đầu")
            return
            
        file_path = filedialog.askopenfilename(
            filetypes=[("Text files", "*.txt")]
        )
        
        if file_path:
            success, message = self.processor.import_translation(file_path, self.selected_line)
            if success:
                self.update_content_display()
                messagebox.showinfo("Nhập bản dịch", message)
            else:
                messagebox.showerror("Lỗi", f"Không thể nhập bản dịch: {message}")
    
    def increase_font_size(self, event=None):
        """Increase font size"""
        self.font_size = min(self.font_size + 1, 20)
        self.text_area.configure(font=("Courier New", self.font_size))
        self.id_area.configure(font=("Courier New", self.font_size))
        self.timestamp_area.configure(font=("Courier New", self.font_size))
    
    def decrease_font_size(self, event=None):
        """Decrease font size"""
        self.font_size = max(self.font_size - 1, 8)
        self.text_area.configure(font=("Courier New", self.font_size))
        self.id_area.configure(font=("Courier New", self.font_size))
        self.timestamp_area.configure(font=("Courier New", self.font_size))
    
    def zoom(self, event):
        """Handle zoom with mouse wheel"""
        if event.state == 4:  # Ctrl
            if event.delta > 0:
                self.increase_font_size()
            else:
                self.decrease_font_size()
            return "break"

if __name__ == "__main__":
    root = tk.Tk()
    app = SubtitleApp(root)
    root.mainloop() 