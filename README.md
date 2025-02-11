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


## Usage Examples

### 1. Direct Format Conversion
Convert your dataset directly using the scripts in the `direct_trans` directory:
```bash
python direct_trans/voc2yolo.py
```

### 2. CSV Intermediate Conversion
Convert your data to CSV first, then transform it to the desired format:
```bash
python with_csv/yolo2csv.py
python with_csv/csv2coco.py 
```

### 3. Dataset Splitting
Automatically split your dataset into training, validation, and testing sets:
```bash
python split/data_distrubu_withjson.py
```

### 4. Data Cleaning
Clean your dataset by removing invalid or noisy entries:
```bash
python clear/cleardata.py
```

### 5. Special Dataset Conversions

- **VisDrone Dataset:**
  Considering VisDrone dataset has its own format, we use the method below to get the coco format dataset.
  Convert the VisDrone dataset into your desired format:
  ```bash
  python VisDrone/vis2coco.py
  ```

- **UVADT Dataset:**
  UVADT dataset is mainly used for tracking, so if you want to train it for detection, we recommnd to do the following.
  Process and convert the UVADT dataset:
  ```bash
  # put all images into 1 directory
  python UVADT/imagescopy2onedir.py
  # converet to the coco
  python UVADT/txt2json.py
  ```

## Contributing

We love contributions! If you have ideas, improvements, or bug fixes, feel free to open an issue or submit a pull request. Let’s make data prepping enjoyable and efficient together! ✌️

## License

This project is licensed under the [MIT License](LICENSE).
