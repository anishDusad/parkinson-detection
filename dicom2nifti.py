import os
import sys
import warnings
import dicom2nifti
from datetime import datetime

# Suppress warnings about invalid VR UI values from pydicom
warnings.filterwarnings("ignore", message="Invalid value for VR UI")

def convert_dicom_to_nifti(dicom_dir, output_dir, subject_id):
    
    try:
        # Create subject-specific output directory
        subject_output_dir = os.path.join(output_dir, subject_id)
        if not os.path.exists(subject_output_dir):
            os.makedirs(subject_output_dir)

        # Get current timestamp for unique filenames
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

        # Perform the conversion - dicom2nifti will handle multiple series
        dicom2nifti.convert_directory(dicom_dir, subject_output_dir, compression=True)

        # Rename files to include subject ID and scan type
        for fname in os.listdir(subject_output_dir):
            if fname.endswith('.nii.gz'):
                # Determine scan type based on filename
                if 't1' in fname.lower():
                    scan_type = 'T1w'
                elif 't2' in fname.lower():
                    scan_type = 'T2w'
                else:
                    scan_type = 'other'

                old_path = os.path.join(subject_output_dir, fname)
                new_path = os.path.join(subject_output_dir, f"{subject_id}_{scan_type}_{timestamp}.nii.gz")
                os.rename(old_path, new_path)

        print(f"Successfully converted DICOM files from {dicom_dir} to {subject_output_dir}")

    except dicom2nifti.exceptions.ConversionError as e:
        print(f"Error converting DICOM files from {dicom_dir}: {e}")
        sys.exit(1)
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        sys.exit(1)

def process_subjects(base_dicom_dir, output_dir):
    
    if not os.path.exists(base_dicom_dir):
        print(f"Error: Base DICOM directory '{base_dicom_dir}' does not exist.")
        sys.exit(1)

    subject_dirs = [d for d in os.listdir(base_dicom_dir)
                    if os.path.isdir(os.path.join(base_dicom_dir, d))]

    if not subject_dirs:
        print(f"Error: No subject directories found in '{base_dicom_dir}'.")
        sys.exit(1)

    for subject_dir_name in subject_dirs:
        subject_dir_path = os.path.join(base_dicom_dir, subject_dir_name)
        convert_dicom_to_nifti(subject_dir_path, output_dir, subject_dir_name)

# Configuration with updated directory paths
base_dicom_dir = r"/content/drive/MyDrive/BTP/CONTROL"
output_dir = r"/content/drive/MyDrive/BTP/NIFTI_21"

# Process the subjects
process_subjects(base_dicom_dir, output_dir)
print("Conversion complete.")
