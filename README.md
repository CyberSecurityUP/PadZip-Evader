# PadZip-Evader

**Binary Padding & ZIP Oversize Evasion Tool**  
*Educational tool for demonstrating AV/EDR evasion techniques*

## Overview

PadZip-Evader is an educational security tool that demonstrates real-world anti-analysis techniques used to bypass AV/EDR detection systems. It implements **Binary Padding** (MITRE ATT&CK T1027.001) combined with **ZIP Oversize Compression** to create evasion payloads for authorized security testing.

## Evasion Techniques

### 🔍 Binary Padding
- Inflates executable size with meaningless bytes (nulls, 0xFF, random, NOP patterns)
- Changes file hashes to evade hash-based detection
- Exceeds AV/EDR file size scanning limits (typically 100-300MB)
- Preserves original functionality while altering disk representation

### 📦 ZIP Oversize Compression
- Leverages extreme DEFLATE compression ratios (>1000:1) on padded data
- Creates small delivery packages (1-10MB) that expand to huge files
- Bypasses recursive extraction depth limits in security scanners
- Combined approach creates layered evasion

## Installation

```bash
# Clone or download the script
git clone https://github.com/CyberSecurityUP/PadZip-Evader
cd padzip-evader

# No dependencies required - uses pure Python 3
python padzip-evader.py --help
```

## Quick Start

### Basic Evasion Padding
```bash
# Inflate executable by 150MB with null padding
python padzip-evader.py -f payload.exe -s 150

# Use 0xFF padding and save as new file
python padzip-evader.py -f tool.exe -s 200 -o evaded_tool.exe -t ff
```

### Evasion Archive Creation
```bash
# Create highly compressed evasion ZIP
python padzip-evader.py -f payload.exe --zip-only -z delivery.zip

# Multiple files in evasion bundle
python padzip-evader.py -f file1.exe file2.dll --zip-only -z evasion_bundle.zip
```

### Complete Demonstration
```bash
# Run full evasion technique demo
python padzip-evader.py -f sample.exe --demo
```

## Usage Examples

### Scenario 1: Basic Evasion Payload
```bash
# Create 200MB padded version of mimikatz
python padzip-evader.py -f mimikatz.exe -s 200 -t null

# Compress for delivery
python padzip-evader.py -f mimikatz_padded.exe --zip-only -z mimikatz_delivery.zip
```

### Scenario 2: Stealth Evasion
```bash
# Use random padding for better evasion
python padzip-evader.py -f beacon.exe -s 150 -t random -o evaded_beacon.exe

# Create high-compression delivery package
python padzip-evader.py -f evaded_beacon.exe -z beacon_package.zip -l 9
```

### Scenario 3: Quick Analysis
```bash
# Analyze file without modification
python padzip-evader.py -f suspicious.exe --info
```

## Command Reference

### Main Parameters
| Parameter | Description | Default |
|-----------|-------------|---------|
| `-f FILES` | Input executable file(s) | **Required** |
| `-s SIZE` | Inflation size in MB | `100` |
| `-o OUTPUT` | Output filename | (modifies original) |
| `-t TYPE` | Padding type: `null`, `ff`, `random`, `pattern` | `null` |

### Archive Options
| Parameter | Description |
|-----------|-------------|
| `--zip-only` | Create ZIP without padding |
| `-z ZIP_FILE` | Output ZIP filename |
| `-l 0-9` | Compression level (0-9) |

### Advanced Options
| Parameter | Description |
|-----------|-------------|
| `--demo` | Run complete evasion demonstration |
| `--info` | Show file information only |

## Evasion Chain

```
Original EXE 
    ↓ (Binary Padding)
Padded EXE (100-500MB) 
    ↓ (ZIP Compression)  
Small ZIP (1-10MB)
    ↓ (Extraction)
Oversize EXE (bypasses scanner limits)
```

## Detection & Mitigation

### Blue Team Awareness
- **Monitor for**: Extreme compression ratios (>100:1)
- **Alert on**: Files with large padding sections
- **Implement**: Size-based scanning policies
- **Use**: Behavioral analysis alongside static scanning

### Recommended Defenses
- Set appropriate file size scanning limits
- Deploy memory analysis capabilities
- Monitor extraction depth and recursion
- Implement entropy analysis for padding detection

## Educational Value

This tool demonstrates:
- MITRE ATT&CK Technique T1027.001 (Binary Padding)
- AV/EDR scanning limitations and bypasses
- File format manipulation for evasion
- Defense strategy development


## Advanced Training

For comprehensive AV/EDR evasion training:
**Red Team Leaders - Advanced Evasion Course**  
https://redteamleaders.coursestack.com/

## Technical Details

- **Python 3.6+** - No external dependencies
- **Pure Python implementation** - Cross-platform compatibility
- **Chunked processing** - Handles large files efficiently
- **Multiple hash algorithms** - MD5, SHA1, SHA256
- **Compression assessment** - Rates evasion potential

## Support

For educational discussions and authorized use cases only.  
*This tool is provided as-is for security research purposes.*

---

**Remember**: With great power comes great responsibility. Use this knowledge to strengthen defenses, not to circumvent them unlawfully.

*PadZip-Evader - Because sometimes, size does matter in evasion.*
