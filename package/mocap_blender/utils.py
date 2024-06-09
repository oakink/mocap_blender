import os
import numpy as np

class ndarray_pydata(np.ndarray):
    def __bool__(self) -> bool:
        return len(self) > 0

    @staticmethod
    def parse(array:np.ndarray):
        return array.view(ndarray_pydata)
    
def getAffineMat(matrix:np.ndarray) -> np.ndarray:
    affine_mat = matrix.copy()
    affine_mat = np.insert(affine_mat,3,values=[0,0,0],axis=1)
    affine_mat = np.insert(affine_mat,3,values=[0,0,0,1],axis=0)
    return affine_mat

def getAffineMatFromTransl(x,y,z) -> np.ndarray:
    return np.array([[1,0,0,x],
                     [0,1,0,y],
                     [0,0,1,z],
                     [0,0,0,1]])

def getAffineMatFromTranslArray(v:np.ndarray) -> np.ndarray:
    return getAffineMatFromTransl(v[0],v[1],v[2])