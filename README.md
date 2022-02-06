# FETsegmenter

**Author**: Caterina Brighi

Algorithms for glioma lesions segmentation on FET PET images.

**Setup/Build/Install** 
To be able to use the above scipts you need to have simpleitk and dicom2nifti installed as python packages and have the ImageAnalysisFunctions.py file in the same folders as the other .py file of this repo. 

**Usage** 
The two main project files of this repo are FETsegmentation_CS.py and FETsegmentation_MI.py. They contain a pipeline to semiautomatically perform tumour lesions segmentations on FET PET images of glioma patients. FETsegmentation_CS.py utilises as input the coordinates of a point in a tumour lesion and a crescent shape segmentation delineated by a reader according to a set of guidelines. FETsegmentation_MI.py utilises as input only the coordinates of a point in a tumour lesion. All the other files perform other statistical analysis tasks associated with this project.

The original peer-reviewed article published on this work is the following, and is availale for Open Access at this link: https://rdcu.be/cGpSI

Brighi, C., Puttick, S., Li, S. et al. A novel semiautomated method for background activity and biological tumour volume definition to improve standardisation of 18F-FET PET imaging in glioblastoma. EJNMMI Phys 9, 9 (2022). https://doi.org/10.1186/s40658-022-00438-2

**Directory Structure** 
NA

**Citation**

If you use this repository in your work, please cite this work by downloading the citation from the right hand tab.
http://doi.org/10.5281/zenodo.5988382
