# jcsdks - JavaCard SDK Manager

A simple tool to help JavaCard developers configure and manage their JavaCard SDKs. This project does NOT distribute any Oracle JavaCard SDK files - users must obtain SDKs directly from Oracle.

## Features

- 📦 **SDK Installation Guidance**: Step-by-step guide to obtain and configure JavaCard SDKs
- 🔍 **SDK Validation**: Verify that SDKs are properly configured
- ⚙️ **Path Management**: Help users set up SDK paths correctly
- 📋 **Configuration Check**: Validate user's SDK configuration
- 📚 **Documentation**: Clear instructions for SDK installation

## Installation

```bash
pip install jcsdks
```

## Getting Started

### 1. Obtain JavaCard SDKs

JavaCard SDKs can be obtained from the following sources:
- [Oracle JavaCard SDK Downloads](https://www.oracle.com/java/technologies/javacard-downloads.html) (Official Oracle releases)
- [GitHub - martinpaljak/oracle_javacard_sdks](https://github.com/martinpaljak/oracle_javacard_sdks) (Convenient repository for multiple SDK versions)

### 2. Extract SDKs

Extract the downloaded SDKs to a directory of your choice. For example:

```
E:/JavaCardSDKs/
├── jc20_kit/
├── jc21_kit/
├── jc211_kit/
├── jc212_kit/
├── jc220_kit/
├── jc221_kit/
├── jc222_kit/
├── jc301classic_kit/
├── jc302classic_kit/
├── jc303_kit/
├── jc304_kit/
├── jc305u1_kit/
├── jc305u2_kit/
├── jc305u3_kit/
├── jc305u4_kit/
├── jc310b43_kit/
├── jc310r20210706_kit/
├── jc320v24.0_kit/
├── jc320v24.1_kit/
├── jc320v25.0_kit/
└── jc320v25.1_kit/
```

### 3. Configure SDK Path

Set the `JAVACARD_SDK_ROOT` environment variable to point to your SDK directory:

#### Windows
```cmd
set JAVACARD_SDK_ROOT=E:/JavaCardSDKs
```

#### Linux/macOS
```bash
export JAVACARD_SDK_ROOT=/path/to/your/sdks
```

### 4. Verify Configuration

```bash
python -m jcsdks validate
```

## Project Structure

```
jcsdks/
├── jcsdks/
│   ├── __init__.py          # Package initialization
│   ├── config.py            # Configuration management
│   ├── validator.py         # SDK validation
│   └── cli.py               # Command-line interface
├── tests/                   # Test files
├── README.md                # This file
└── setup.py                 # Installation script
```

## Commands

### Validate SDK Configuration

```bash
python -m jcsdks validate
```

Validates that:
- `JAVACARD_SDK_ROOT` environment variable is set
- SDK directory exists
- SDKs have the expected structure

### Show SDK Information

```bash
python -m jcsdks info
```

Displays information about detected SDKs.

### Installation Wizard

```bash
python -m jcsdks wizard
```

Interactive wizard to guide SDK installation and configuration.

## Expected SDK Structure

Each SDK should follow this structure:

```
jcXXX_kit/
├── lib/                    # Contains JAR files
│   ├── api.jar
│   ├── apdutool.jar
│   └── jcwde.jar
├── bin/                    # Contains executable files
│   ├── apdutool.bat
│   └── converter.bat
└── LICENSE                 # Oracle license file
```

## Requirements

- Python 3.8+
- Oracle JavaCard SDKs (obtained directly from Oracle)

## License

This project is licensed under the MIT License. See [LICENSE](LICENSE) for details.

**Important**: This project does NOT distribute any Oracle JavaCard SDKs. Users must obtain SDKs directly from Oracle and comply with Oracle's licensing terms.

## Contributing

Contributions are welcome! Please submit issues and pull requests on [GitHub](https://github.com/ibaibing/jcsdks).