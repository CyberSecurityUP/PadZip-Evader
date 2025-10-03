# PadZip Evader - Binary Padding & ZIP Oversize Tool

## Overview

This educational tool demonstrates anti-analysis techniques used in security research, specifically **Binary Padding** and **ZIP Oversize compression** methods that can bypass AV/EDR detection mechanisms.

## Technique Explanation

### Binary Padding (MITRE ATT&CK T1027.001)
- Inflates executable file size by adding meaningless bytes (nulls, 0xFF, etc.)
- Changes file hashes to evade hash-based blocklists
- Can exceed AV/EDR file size scanning limits
- Preserves original functionality while altering disk representation

### ZIP Oversize Compression
- Leverages high compression ratios of repetitive data
- Small ZIP files (1-10MB) can expand to hundreds of MB when extracted
- May bypass recursive extraction depth limits in security scanners
- Combined with padding for layered evasion

## Prerequisites

- Python 3.6+
- No additional dependencies required

## Usage Examples

### Basic Binary Padding
```bash
# Inflate executable by 100MB with null bytes
python binary_padding.py -f mimikatz.exe -s 100

# Inflate with 0xFF padding and save as new file
python binary_padding.py -f tool.exe -s 200 -o padded_tool.exe -t ff
```

### Compression Only
```bash
# Create highly compressed ZIP without padding
python binary_padding.py -f file1.exe file2.dll --zip-only -z delivery.zip
```

### Complete Demonstration
```bash
# Run full technique demonstration
python binary_padding.py -f sample.exe --demo
```

### File Analysis
```bash
# Show file information and hashes
python binary_padding.py -f executable.exe --info
```

## Full Parameter Reference

```bash
Required:
  -f FILES [FILES ...]    Input executable file(s) to process

Padding Options:
  -s SIZE                 Size in MB to inflate binary (default: 100)
  -o OUTPUT               Output filename for padded executable
  -t {null,ff,random,pattern}  Padding type (default: null)

ZIP Options:
  --zip-only              Create ZIP archive without padding
  -z ZIP_FILE             Output ZIP filename
  -l {0-9}                Compression level 0-9 (default: 9)

Advanced:
  --demo                  Run complete technique demonstration
  --info                  Show file information only
```

## Educational Purpose

This tool is designed for:
- Security researchers studying evasion techniques
- Red team professionals in authorized engagements
- Blue team members developing detection strategies
- Educational demonstrations in controlled environments

## Security Notice

⚠️ **FOR AUTHORIZED USE ONLY**
- Only use on systems you own or have explicit permission to test
- Never deploy against systems without written authorization
- Intended for legitimate security research and education
- Maintain ethical boundaries and legal compliance

## Detection & Mitigation

For blue team awareness:
- Monitor for extreme compression ratios
- Implement file size scanning limits appropriately
- Use behavioral analysis in addition to static scanning
- Deploy memory scanning capabilities
- Flag files with large padding sections

## Advanced Training

For comprehensive AV/EDR evasion training, check out:
**Red Team Leaders - AV/EDR Evasion Course**
https://redteamleaders.coursestack.com/

## Legal & Ethical Use

By using this tool, you agree:
1. To only use for legitimate security research
2. To obtain proper authorization before testing
3. To comply with all applicable laws
4. To use responsibly and ethically

## Technical Details

- Implements binary padding per MITRE ATT&CK T1027.001
- Uses DEFLATE compression for high ratios on repetitive data
- Preserves PE file functionality while altering hashes
- Demonstrates real-world evasion techniques documented by security researchers

---

*Use responsibly. Knowledge is power - wield it wisely.*
```

7. **Legal compliance emphasis**

The tone is professional yet accessible, making it suitable for both security beginners and experienced professionals looking to understand these evasion techniques.
