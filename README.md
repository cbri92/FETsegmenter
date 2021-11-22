# FETsegmenter

**Author**: Caterina Brighi

Algorithms for glioma lesions segmentation on FET PET images.

**Setup/Build/Install** 
To be able to use the above scipts you need to have simpleitk and dicom2nifti installed as python packages and have the ImageAnalysisFunctions.py file in the same folders as the other .py file of this repo. 

**Usage** 
The two main project files of this repo are FETsegmentation_CS.py and FETsegmentation_MI.py. They contain a pipeline to semiautomatically perform tumour lesions segmentations on FET PET images of glioma patients. FETsegmentation_CS.py utilises as input the coordinates of a point in a tumour lesion and a crescent shape segmentation delineated by a reader according to the guidelines published in this paper "Unterrainer, M., Vettermann, F., Brendel, M. et al. Towards standardization of 18F-FET PET imaging: do we need a consistent method of background activity assessment?. EJNMMI Res 7, 48 (2017). https://doi.org/10.1186/s13550-017-0295-y". FETsegmentation_MI.py utilises as input only the coordinates of a point in a tumour lesion. All the other files perform other statistical analysis tasks associated with this project.

**Directory Structure** 
NA
