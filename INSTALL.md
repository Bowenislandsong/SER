# Installation Guide

This guide provides detailed instructions for installing the SER library using various methods.

## Table of Contents
1. [PyPI Installation](#pypi-installation)
2. [Conda Installation](#conda-installation)
3. [Docker Installation](#docker-installation)
4. [Source Installation](#source-installation)
5. [Verifying Installation](#verifying-installation)
6. [Troubleshooting](#troubleshooting)

## PyPI Installation

PyPI (Python Package Index) is the recommended installation method for most users.

### Prerequisites
- Python 3.8 or higher
- pip (usually comes with Python)

### Installation Steps

```bash
pip install ser-algorithms
```

### Upgrading

```bash
pip install --upgrade ser-algorithms
```

### Installing a Specific Version

```bash
pip install ser-algorithms==0.1.0
```

## Conda Installation

Conda is recommended for users who prefer conda environments or need better dependency management.

### Prerequisites
- Anaconda or Miniconda installed

### Installation Steps

```bash
conda install -c conda-forge ser-algorithms
```

### Creating a New Environment

```bash
# Create a new environment with SER
conda create -n ser-env python=3.11 ser-algorithms

# Activate the environment
conda activate ser-env
```

### Upgrading

```bash
conda update -c conda-forge ser-algorithms
```

## Docker Installation

Docker provides an isolated, reproducible environment with all dependencies pre-installed.

### Prerequisites
- Docker installed on your system

### Basic Usage

**Pull the latest image:**
```bash
docker pull ghcr.io/bowenislandsong/ser:latest
```

**Run Python interactively:**
```bash
docker run -it ghcr.io/bowenislandsong/ser:latest python
```

**Run Jupyter Notebook:**
```bash
docker run -p 8888:8888 ghcr.io/bowenislandsong/ser:latest
```
Then open your browser to the URL shown in the terminal output.

### Advanced Usage

**Mount a local directory:**
```bash
docker run -it -v $(pwd):/workspace ghcr.io/bowenislandsong/ser:latest python
```

**Run a specific script:**
```bash
docker run -v $(pwd):/workspace ghcr.io/bowenislandsong/ser:latest python /workspace/my_script.py
```

**Use a specific version:**
```bash
docker pull ghcr.io/bowenislandsong/ser:v0.1.0
docker run -it ghcr.io/bowenislandsong/ser:v0.1.0 python
```

## Source Installation

Installing from source is recommended for developers or users who want the latest unreleased features.

### Prerequisites
- Python 3.8 or higher
- git

### Installation Steps

**Clone the repository:**
```bash
git clone https://github.com/Bowenislandsong/SER.git
cd SER
```

**Install in development mode:**
```bash
pip install -e .
```

This creates a link to the source code, so any changes you make will be immediately available.

**Install with development dependencies:**
```bash
pip install -e ".[dev]"
```

### Running Tests

```bash
pytest tests/
```

### Building from Source

```bash
pip install build
python -m build
```

This creates distribution packages in the `dist/` directory.

## Verifying Installation

After installation, verify that SER is properly installed:

```python
import ser
print(ser.__version__)

# Test basic functionality
from ser import SVDEmbeddingRegression, DistributedSVD, FederatedSVD
print("All imports successful!")
```

Expected output:
```
0.1.0
All imports successful!
```

## Troubleshooting

### ImportError: No module named 'ser'

**Solution:** Ensure the package is installed in the active Python environment:
```bash
pip list | grep ser-algorithms
```

### Version Conflicts

**Solution:** Create a fresh virtual environment:
```bash
python -m venv ser-env
source ser-env/bin/activate  # On Windows: ser-env\Scripts\activate
pip install ser-algorithms
```

### NumPy/SciPy Installation Issues

**Solution:** Install NumPy and SciPy separately first:
```bash
pip install numpy scipy
pip install ser-algorithms
```

### Docker Permission Denied

**Solution:** Run Docker with sudo or add your user to the docker group:
```bash
sudo usermod -aG docker $USER
```
Log out and back in for changes to take effect.

### Conda Channel Not Found

**Solution:** Make sure you've specified the conda-forge channel:
```bash
conda config --add channels conda-forge
conda install ser-algorithms
```

## Getting Help

If you encounter issues not covered here:

1. Check the [GitHub Issues](https://github.com/Bowenislandsong/SER/issues)
2. Read the [documentation](https://bowenislandsong.github.io/SER/)
3. Open a new issue with details about your problem

## Next Steps

After installation, check out:
- [Quick Start Guide](https://bowenislandsong.github.io/SER/#quickstart)
- [API Reference](https://bowenislandsong.github.io/SER/#api)
- [Examples](https://github.com/Bowenislandsong/SER/tree/main/examples)
