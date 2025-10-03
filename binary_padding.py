#!/usr/bin/env python3
"""
PadZip-Evader - Binary Padding & ZIP Oversize Tool 
Created by Joas A Santos
"""

import struct
import os
import zipfile
import hashlib
import argparse
from pathlib import Path

class BinaryPaddingTool:
    def __init__(self):
        self.version = "2.0"
        
    def calculate_hashes(self, filepath):
        """Calculate multiple hash types for file identification"""
        hashes = {}
        try:
            with open(filepath, 'rb') as f:
                data = f.read()
                hashes['md5'] = hashlib.md5(data).hexdigest()
                hashes['sha1'] = hashlib.sha1(data).hexdigest()
                hashes['sha256'] = hashlib.sha256(data).hexdigest()
                hashes['filesize'] = len(data)
            return hashes
        except Exception as e:
            print(f"[-] Error calculating hashes: {e}")
            return None
    
    def print_file_info(self, filepath, description=""):
        """Display comprehensive file information"""
        if not os.path.exists(filepath):
            print(f"[-] File not found: {filepath}")
            return False
            
        file_size = os.path.getsize(filepath)
        hashes = self.calculate_hashes(filepath)
        
        print(f"\n{'='*60}")
        print(f"FILE INFORMATION: {description}")
        print(f"{'='*60}")
        print(f"Filename: {filepath}")
        print(f"Size: {file_size:,} bytes ({file_size/1024/1024:.2f} MB)")
        if hashes:
            print(f"MD5:    {hashes['md5']}")
            print(f"SHA1:   {hashes['sha1']}")
            print(f"SHA256: {hashes['sha256']}")
        print(f"{'='*60}")
        return True
    
    def binary_padding(self, input_file, output_file=None, inflate_size_mb=100, padding_type='null'):
        """
        Apply binary padding to inflate executable size
        
        Args:
            input_file: Path to input executable
            output_file: Path for output file (optional, modifies original if None)
            inflate_size_mb: Size to inflate in MB
            padding_type: Type of padding ('null', 'ff', 'random', 'pattern')
        """
        if not os.path.exists(input_file):
            print(f"[-] Input file not found: {input_file}")
            return False
        
        if output_file is None:
            output_file = input_file
            print(f"[!] Modifying original file: {input_file}")
        
        # Define padding bytes based on type
        padding_bytes = {
            'null': b'\x00',
            'ff': b'\xFF',
            'random': os.urandom(1),
            'pattern': b'\x90'  # NOP pattern
        }
        
        if padding_type not in padding_bytes:
            print(f"[-] Invalid padding type: {padding_type}")
            print(f"[!] Available types: {list(padding_bytes.keys())}")
            return False
        
        padding_byte = padding_bytes[padding_type]
        original_size = os.path.getsize(input_file)
        padding_size = inflate_size_mb * 1024 * 1024
        
        print(f"[*] Starting binary padding operation")
        print(f"    Input file: {input_file}")
        print(f"    Output file: {output_file}")
        print(f"    Original size: {original_size:,} bytes")
        print(f"    Padding size: {padding_size:,} bytes ({inflate_size_mb} MB)")
        print(f"    Padding type: {padding_type} (0x{padding_byte.hex()})")
        print(f"    Target size: {original_size + padding_size:,} bytes")
        
        try:
            # Read original file
            with open(input_file, 'rb') as infile:
                original_data = infile.read()
            
            # Create padded file
            with open(output_file, 'wb') as outfile:
                outfile.write(original_data)
                # Write padding in chunks to handle large sizes
                chunk_size = 1024 * 1024  # 1MB chunks
                chunks_needed = padding_size // chunk_size
                remainder = padding_size % chunk_size
                
                print(f"[*] Applying padding...")
                for i in range(chunks_needed):
                    outfile.write(padding_byte * chunk_size)
                    if i % 10 == 0:  # Progress indicator every 10MB
                        progress_mb = (i * chunk_size) / 1024 / 1024
                        print(f"    Progress: {progress_mb:.1f}/{inflate_size_mb} MB")
                
                if remainder > 0:
                    outfile.write(padding_byte * remainder)
            
            final_size = os.path.getsize(output_file)
            print(f"[+] Padding completed successfully!")
            print(f"    Final size: {final_size:,} bytes ({final_size/1024/1024:.2f} MB)")
            print(f"    Size increase: {final_size - original_size:,} bytes")
            
            return True
            
        except Exception as e:
            print(f"[-] Error during padding operation: {e}")
            return False
    
    def create_compressed_archive(self, input_files, output_zip, compression_level=9):
        """
        Create a highly compressed ZIP archive
        
        Args:
            input_files: List of files to include in ZIP
            output_zip: Output ZIP filename
            compression_level: ZIP compression level (0-9)
        """
        print(f"\n[*] Creating compressed archive: {output_zip}")
        
        # Filter existing files
        existing_files = [f for f in input_files if os.path.exists(f)]
        if not existing_files:
            print("[-] No valid input files found")
            return False
        
        total_original_size = sum(os.path.getsize(f) for f in existing_files)
        
        try:
            with zipfile.ZipFile(output_zip, 'w', compression=zipfile.ZIP_DEFLATED, 
                               compresslevel=compression_level) as zipf:
                for file_path in existing_files:
                    arcname = os.path.basename(file_path)
                    zipf.write(file_path, arcname)
                    file_size = os.path.getsize(file_path)
                    print(f"    Added: {arcname} ({file_size:,} bytes)")
            
            compressed_size = os.path.getsize(output_zip)
            compression_ratio = total_original_size / compressed_size if compressed_size > 0 else 0
            
            print(f"[+] Archive created successfully!")
            print(f"    Total original size: {total_original_size:,} bytes")
            print(f"    Compressed size: {compressed_size:,} bytes")
            print(f"    Compression ratio: {compression_ratio:.2f}:1")
            print(f"    Space savings: {((1 - (compressed_size / total_original_size)) * 100):.1f}%")
            
            return True
            
        except Exception as e:
            print(f"[-] Error creating archive: {e}")
            return False
    
    def advanced_padding_techniques(self, input_file, output_file, techniques):
        """
        Apply advanced padding techniques for evasion
        
        Args:
            input_file: Input executable
            output_file: Output file
            techniques: Dictionary of techniques to apply
        """
        print(f"\n[*] Applying advanced padding techniques")
        
        if 'append_padding' in techniques:
            self.binary_padding(input_file, output_file, 
                              techniques['append_padding']['size_mb'],
                              techniques['append_padding']['type'])
        
        if 'prepend_padding' in techniques:
            print(f"[*] Prepend padding not implemented in this version")
        
        if 'section_padding' in techniques:
            print(f"[*] PE section padding not implemented in this version")
    
    def demonstrate_evasion_technique(self, input_exe, output_dir):
        """
        Complete demonstration of oversize evasion technique
        """
        print(f"\n{'='*60}")
        print("COMPLETE EVASION TECHNIQUE DEMONSTRATION")
        print(f"{'='*60}")
        
        if not os.path.exists(input_exe):
            print(f"[-] Input executable not found: {input_exe}")
            return False
        
        # Step 1: Show original file info
        self.print_file_info(input_exe, "ORIGINAL EXECUTABLE")
        
        # Step 2: Create padded version
        padded_exe = os.path.join(output_dir, "padded_executable.exe")
        if self.binary_padding(input_exe, padded_exe, inflate_size_mb=150, padding_type='null'):
            self.print_file_info(padded_exe, "AFTER BINARY PADDING")
        
        # Step 3: Create compressed archive
        output_zip = os.path.join(output_dir, "compressed_delivery.zip")
        if self.create_compressed_archive([padded_exe], output_zip, compression_level=9):
            self.print_file_info(output_zip, "FINAL COMPRESSED DELIVERY")
        
        print(f"\n[+] Demonstration completed!")
        print(f"    Original EXE -> Padded EXE -> Small ZIP")
        print(f"    Ready for testing in controlled environment")

def main():
    parser = argparse.ArgumentParser(
        description="Enhanced Binary Padding & ZIP Compression Tool",
        epilog="""
EXAMPLES:
  # Basic binary padding
  python binary_padding.py -f mimikatz.exe -s 100
  
  # Padding with custom output and type
  python binary_padding.py -f tool.exe -s 200 -o padded_tool.exe -t ff
  
  # Create compressed archive only
  python binary_padding.py -f file.exe --zip-only -z delivery.zip
  
  # Complete demonstration
  python binary_padding.py -f sample.exe --demo
  
  # Multiple files in archive
  python binary_padding.py -f file1.exe file2.dll --zip-only -z bundle.zip

SECURITY NOTE:
  This tool is for legitimate security research, authorized penetration testing,
  and educational purposes only. Always ensure proper authorization before use.
        """,
        formatter_class=argparse.RawDescriptionHelpFormatter
    )
    
    # Main arguments
    parser.add_argument('-f', '--file', dest='input_files', nargs='+',
                       required=True, help='Input executable file(s) to process')
    parser.add_argument('-s', '--size', dest='inflate_size', type=int, default=100,
                       help='Size in MB to inflate binary by (default: 100)')
    parser.add_argument('-o', '--output', dest='output_file',
                       help='Output filename for padded executable')
    parser.add_argument('-t', '--type', dest='padding_type', default='null',
                       choices=['null', 'ff', 'random', 'pattern'],
                       help='Padding byte type (default: null)')
    
    # ZIP options
    parser.add_argument('--zip-only', dest='zip_only', action='store_true',
                       help='Create ZIP archive without padding')
    parser.add_argument('-z', '--zip', dest='zip_file',
                       help='Output ZIP filename')
    parser.add_argument('-l', '--compression-level', dest='compression_level',
                       type=int, default=9, choices=range(0, 10),
                       help='ZIP compression level 0-9 (default: 9)')
    
    # Advanced options
    parser.add_argument('--demo', dest='demo_mode', action='store_true',
                       help='Run complete demonstration')
    parser.add_argument('--info', dest='info_only', action='store_true',
                       help='Show file information only')
    
    args = parser.parse_args()
    
    tool = BinaryPaddingTool()
    
    # Input validation
    for input_file in args.input_files:
        if not os.path.exists(input_file):
            print(f"[-] File not found: {input_file}")
            return
    
    # Operation modes
    if args.info_only:
        for input_file in args.input_files:
            tool.print_file_info(input_file, "FILE ANALYSIS")
        return
    
    if args.demo_mode:
        output_dir = os.path.dirname(args.input_files[0]) or "."
        tool.demonstrate_evasion_technique(args.input_files[0], output_dir)
        return
    
    if args.zip_only:
        # ZIP creation only
        output_zip = args.zip_file or "compressed_files.zip"
        tool.create_compressed_archive(args.input_files, output_zip, args.compression_level)
        if os.path.exists(output_zip):
            tool.print_file_info(output_zip, "CREATED ARCHIVE")
    else:
        # Binary padding with optional ZIP
        for input_file in args.input_files:
            print(f"\n{'#'*60}")
            print(f"PROCESSING: {input_file}")
            print(f"{'#'*60}")
            
            # Show original info
            tool.print_file_info(input_file, "ORIGINAL FILE")
            
            # Apply padding
            output_exe = args.output_file or input_file
            if tool.binary_padding(input_file, output_exe, args.inflate_size, args.padding_type):
                # Show modified info
                tool.print_file_info(output_exe, "PADDED FILE")
                
                # Create ZIP if requested
                if args.zip_file:
                    tool.create_compressed_archive([output_exe], args.zip_file, args.compression_level)
                    if os.path.exists(args.zip_file):
                        tool.print_file_info(args.zip_file, "FINAL ARCHIVE")
    
    print(f"\n[+] Operations completed successfully!")
    print(f"[!] REMINDER: For authorized testing and research only!")

if __name__ == "__main__":
    main()
