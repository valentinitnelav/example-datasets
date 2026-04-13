# InsectAI Example Datasets: Camtrap DP and Derived Metadata Standards

<img src="logos/insectAI.svg" alt="InsectAI Logo" width="300"/>

---

## 🧪 Contents

- `datasets/` - example datasets
- `logos/` – organization logos for use in notebooks and presentations
- `README.md` – this file
- `requirements.txt` – Python dependencies for running the conversion scripts
- `*_template.csv` – reference files used to initialize the Camtrap DP CSVs. These contain all necessary headers to ensure the final output meets the data package specifications

---

## 📂 Dataset Organization

The `datasets/` directory is structured to facilitate the conversion from raw data formats to the [Camtrap DP](https://tdwg.github.io/camtrap-dp/) standard.

### 📦 Dataset Subfolders
Each individual dataset is located in a folder named `<DATASET_NAME>` with the following internal structure:

| Component | Description |
| :--- | :--- |
| `media/` | Folder containing all images, potentially organized into subdirectories. |
| `raw_labels/` | The original annotations in their source format (JSON, CSV, TXT, etc.). |
| `main.ipynb` | The conversion script (Jupyter, R, etc.) used to convert the dataset in raw format to the Camtrap DP standard. |
| `deployments.csv` | **Generated:** Records of camera/sensor deployments. |
| `media.csv` | **Generated:** Metadata for all media files. |
| `observations.csv`| **Generated:** Taxonomic or individual observations. |
| `datapackage.json`| **Generated:** The metadata descriptor for the data package. |

---

## 📝 Technical Requirements

To run the conversion scripts and work with these datasets, please set up a Python environment and install the dependencies:

1. **Create a Python environment** (using `venv` or `conda`)
   Example using `venv`:
   ```bash
   python -m venv venv
   ```
2. **Activate the environment**
   Example for `venv`:
   - On Windows:
     ```bash
     venv\Scripts\activate
     ```
   - On macOS/Linux:
     ```bash
     source venv/bin/activate
     ```
3. **Install requirements**:
   ```bash
   pip install -r requirements.txt
   ```

---

## About the datathon

During the "datathon" we work together to standardize disparate insect “minidatasets”, creating reproducible examples for the InsectAI community. 

Along the way, we reflect on and develop Camtrap DP and InsectAI data standards, produce scripts for data mapping, and journalize the experience of standardizing data and metadata.

We will prove to ourselves (and the world!) that we can store our data in a common format, laying foundations for future collaborations and insect image megadatasets 💾

# Outcomes of the datathon, found here in the repo:

- Several example standardized datasets to browse and learn from under `datasets/`
- Refined InsectAI/Camtrap DP standards (including github issues to petition the Camtrap DP team), feeding into the InsectAI WG3 report
- A presentation and online materials (especially READMEs under `datasets/<DATASET_NAME>`) to disseminate and demystify working with standards
- Scripts and tools to map data to, and read data from, Camtrap DP/InsectAI (also under `datasets/<DATASET_NAME>`)

## Link to 2025 InsectAI demo of CamtrapDP

[https://github.com/cpadubidri/insectAI-demo.git]
