# Dataset Description
*Source : https://etaia.github.io/Welding-Quality-Detection-Challenge/dataset*

---

In this section, a **sample** refers to "a single image" of welding.

A dataset available in this challenge is described using a **Parquet file** containing metadata for all samples within the dataset. A Parquet file represents a dataframe. For each sample, the following fields are available:

| Field | Description |
|-------|-------------|
| `sample_id` | Unique identifier for the sample, following the template `"data_X"`. |
| `class` | Real state of the welding present in the image; this is the ground truth. Two values are possible: `OK` or `KO`. |
| `timestamp` | Datetime when the photo was taken; this field is not expected to be useful. |
| `welding-seams` | Name of the welding seam to which the welding belongs. Welding seams are named `"c_X"`. |
| `labelling_type` | Type of person who annotated the data. Two possible values: `"expert"` or `"operator"`. |
| `resolution` | List containing the resolution of the image `[width, height]`. |
| `path` | Internal path of the image in the challenge storage. |
| `sha256` | A unique hexadecimal key representing the image data, used to detect alteration or corruption in the storage. |
| `storage_type` | Type of sample storage: `"s3"` or `"filesystem"`. |
| `data-origin` | Type of data. Two possible values: `"real"` or `"synthetic"`. The provided datasets contain only real samples. |
| `blur_level` | Level of blur in the image, measured numerically using OpenCV. The lower this value, the blurrier the image. |
| `blur_class` | Class of blur deduced from the `blur_level` field. Two classes: `"blur"` and `"clean"`. Set to `"blur"` when the blur level is below **950**. |
| `luminosity_level` | Percentage of luminosity in the image, measured numerically. |
| `external_path` | URL of the image. This URL can be used by challengers to directly download the sample from storage. |

> **Remark :** There is no relationship between the integer X in `"data_X"` (field `sample_id`) and the integer Y in the image name `"sample_Y.jpeg"` (fields `path` and `external_path`).

---

## Dataset Examples

### Example Mini Dataset

A reduced sample of the dataset `"example_mini_dataset"` is provided to give an overview of the final dataset for this challenge. It contains **2,857 images** of welding, split into three different welding seams: **c102, c20, and c33**.

The metadata file for this dataset can be found here: [Example Mini Dataset Metadata(opens new window)](https://minio-storage.apps.confianceai-public.irtsysx.fr/challenge-welding/datasets/example_mini_dataset/metadata/ds_meta.parquet)

Below is an example of the first nine rows from the metadata file:

| sample_id | class | timestamp | welding-seams | labelling_type | resolution | path | sha256 | storage_type | data_origin | blur_level | blur_class | luminosity_level | external_path |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| data_92409 | OK | 22/01/20 12:49 | c33 | expert | ["1920","1080"] | challenge-weldin... | 71,78,215... | s3 | real | 701.93834076 | blur | 50.53336529442024 | http://minio-storage... |
| data_67943 | OK | 20/02/20 23:53 | c102 | expert | ["1920","1080"] | challenge-weldin... | 115,246,5... | s3 | real | 715.6707015899999 | blur | 47.050603667392885 | http://minio-storage... |
| data_4843 | OK | 20/01/20 20:34 | c20 | expert | ["1920","1080"] | challenge-weldin... | 219,90,17... | s3 | real | 715.85737975 | blur | 46.20424534011135 | http://minio-storage... |
| data_25309 | OK | 18/07/2022 20:18 | c102 | operator | ["960","540"] | challenge-weldin... | 47,99,227... | s3 | real | 869.5130059100001 | blur | 34.3592804405713 | http://minio-storage... |
| data_76144 | OK | 03/10/19 21:14 | c20 | expert | ["1920","1080"] | challenge-weldin... | 202,37,12... | s3 | real | 2676.24690396 | clean | 46.25624413731542 | http://minio-storage... |
| data_40839 | OK | 21/07/2022 22:44 | c33 | operator | ["960","540"] | challenge-weldin... | 97,163,14... | s3 | real | 1938.7930127099999 | clean | 49.50956184943113 | http://minio-storage... |
| data_79549 | OK | 11/07/20 19:08 | c20 | expert | ["1920","1080"] | challenge-weldin... | 71,57,12... | s3 | real | 2831.67676284 | clean | 47.10117518458 | http://minio-storage... |
| data_80892 | OK | 04/11/2020 20:09 | c20 | expert | ["1920","1080"] | challenge-weldin... | 124,189,1... | s3 | real | 4644.53888631 | clean | 44.77387909253207 | http://minio-storage... |
| data_68392 | OK | 11/03/20 17:59 | c102 | expert | ["1920","1080"] | challenge-weldin... | 35,80,129... | s3 | real | 1411.3995897500001 | clean | 45.08214169541273 | http://minio-storage... |

The dataset can be downloaded directly as a ZIP file: https://minio-storage.apps.confianceai-public.irtsysx.fr/challenge-welding/datasets/example_mini_dataset.zip


### Welding Detection Challenge Dataset

The complete dataset provided for this challenge is named `"welding-detection-challenge-dataset"`. It contains **22,753 images** of welding, covering three different welding seams: **c20, c102, and c33**.

The metadata file for this dataset can be found here: https://minio-storage.apps.confianceai-public.irtsysx.fr/challenge-welding/datasets/welding-detection-challenge-dataset/metadata/ds_meta.parquet

The full dataset can be downloaded as a ZIP file: https://minio-storage.apps.confianceai-public.irtsysx.fr/challenge-welding/datasets/welding-detection-challenge-dataset.zip


DebiAI is an open-source bias detection and contextual evaluation tool for AI projects.
We used it to explore the Welding Detection Challenge Dataset Metadata parquet file

Analyze the challenge dataset on our public DebiAI instance

DebiAI was designed to assist data scientists in exploring datasets like the one described in this challenge.
How to create your own Challenge Dataset DebiAI project

DebiAI is developed by Tom Mansion and is integrated in Confiance.ia