# FETsegmenter

**Author**: Caterina Brighi

Algorithms for glioma lesions segmentation on FET PET images.

**Setup/Build/Install** 
To be able to use the above scipts you need to have simpleitk and dicom2nifti installed as python packages and have the ImageAnalysisFunctions.py file in the same folders as the other .py file of this repo. 

**Usage** 
The 2 main project files of this repo are FETsegmentation_CS.py and FETsegmentation_MI.py. They containing a pipeline to semiautomatically perform tumour lesions segmentations on FET PET images of glioma patients. FETsegmentation_CS.py utilised as input coordinates of a point inside a tumour lesion and a crescent shape segmentation delimeated by a reader. FETsegmentation_MI.py utilises as input only coordinates of a point inside a tumour lesion. All the other files perform other statistical analysis tasks associated with this project.

**Directory Structure** 
NA
