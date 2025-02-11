# datapre - Dataset Preparation Tool 😎🚀

## Overview

**datapre** is your go-to toolkit for getting your datasets in shape! Whether you need direct format conversion, an intermediate CSV step, or splitting datasets into train/validation/test sets, this tool makes it simple and fun. Plus, we’ve got custom conversion scripts for the VisDrone and UVADT datasets to handle your specialized needs. Let’s get your data prepped and ready to roll! 🎉

## Features

- **Direct Format Conversion:** Quickly transform your data from one format to another.
- **CSV Intermediate Conversion:** Convert data to CSV first, then to your target format.
- **Dataset Splitting:** Automatically divide datasets that lack predefined partitions.
- **Data Cleaning:** Remove invalid or messy data entries with ease.
- **Specialized Conversions:** Dedicated scripts for handling VisDrone and UVADT datasets.

## Directory Structure

```
├── UVADT/            # Conversion scripts for UVADT dataset
├── VisDrone/         # Conversion scripts for VisDrone dataset
├── clear/            # Data cleaning scripts
├── direct_trans/     # Direct format conversion scripts
├── split/            # Dataset splitting scripts
├── with_csv/         # CSV intermediate conversion scripts
├── get_file_name.py   # Utility for retrieving file names
└── jsontrans.py       # JSON format conversion tool
```

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/Flulike/datapre.git
   cd datapre
   ```

2. Install any dependencies (if available):
   ```bash
   pip install -r requirements.txt
   ```

## Usage Examples

### 1. Direct Format Conversion
Convert your dataset directly using the scripts in the `direct_trans` directory:
```bash
python direct_trans/convert.py --input path/to/source --output path/to/target
```

### 2. CSV Intermediate Conversion
Convert your data to CSV first, then transform it to the desired format:
```bash
python with_csv/convert_to_csv.py --input path/to/source --output path/to/intermediate.csv
python with_csv/convert_from_csv.py --input path/to/intermediate.csv --output path/to/target
```

### 3. Dataset Splitting
Automatically split your dataset into training, validation, and testing sets:
```bash
python split/split_data.py --input path/to/dataset --train_ratio 0.7 --val_ratio 0.2 --test_ratio 0.1
```

### 4. Data Cleaning
Clean your dataset by removing invalid or noisy entries:
```bash
python clear/clean_data.py --input path/to/raw --output path/to/cleaned
```

### 5. Special Dataset Conversions

- **VisDrone Dataset:**  
  Convert the VisDrone dataset into your desired format:
  ```bash
  python VisDrone/convert_visdrone.py --input path/to/VisDrone --output path/to/converted
  ```

- **UVADT Dataset:**  
  Process and convert the UVADT dataset:
  ```bash
  python UVADT/convert_uvadt.py --input path/to/UVADT --output path/to/converted
  ```

## Contributing

We love contributions! If you have ideas, improvements, or bug fixes, feel free to open an issue or submit a pull request. Let’s make data prepping enjoyable and efficient together! ✌️

## License

This project is licensed under the [MIT License](LICENSE).
