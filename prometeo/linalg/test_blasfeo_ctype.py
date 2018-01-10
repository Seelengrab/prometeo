from ctypes import *
from os import *

class blasfeo_dmat(Structure):
    _fields_ = [    ("m", c_int),
	            ("n", c_int),
	            ("pm", c_int),
	            ("cn", c_int),
	            ("pA", POINTER(c_double)),
	            ("dA", POINTER(c_double)),
	            ("use_dA", c_int),
	            ("memsize", c_int)]

cwd = getcwd()
bw = CDLL('%s/../../external/blasfeo/lib/libblasfeo.so' %cwd)

#ctypes seems to be struggling with arg types of the dgemm routine:
bw.blasfeo_dgemm_nt.argtypes = [c_int, c_int, c_int, c_double, 
    POINTER(blasfeo_dmat), c_int, c_int, POINTER(blasfeo_dmat), c_int, c_int, 
    c_double, POINTER(blasfeo_dmat), c_int, c_int, POINTER(blasfeo_dmat), c_int, c_int]

n = 5 

size_strmat = 100*bw.blasfeo_memsize_dmat(n, n)
memory_strmat = c_void_p() 
import pdb; pdb.set_trace()
bw.v_zeros_align(byref(memory_strmat), size_strmat)

ptr_memory_strmat = cast(memory_strmat, c_char_p)

sA = blasfeo_dmat()

bw.blasfeo_allocate_dmat(n, n, byref(sA))
bw.blasfeo_create_dmat(n, n, byref(sA), ptr_memory_strmat)
bw.blasfeo_print_dmat(n, n, byref(sA), 0, 0)

ptr_memory_strmat = cast(ptr_memory_strmat, c_void_p)
ptr_memory_strmat.value = ptr_memory_strmat.value + sA.memsize
ptr_memory_strmat = cast(ptr_memory_strmat, c_char_p)

sD = blasfeo_dmat()

bw.blasfeo_allocate_dmat(n, n, byref(sD))
bw.blasfeo_create_dmat(n, n, byref(sD), ptr_memory_strmat)
ptr_memory_strmat = cast(ptr_memory_strmat, c_void_p)
ptr_memory_strmat.value = ptr_memory_strmat.value + sD.memsize
ptr_memory_strmat = cast(ptr_memory_strmat, c_char_p)

sB = blasfeo_dmat()

bw.blasfeo_allocate_dmat(n, n, byref(sB))
bw.blasfeo_create_dmat(n, n, byref(sB), ptr_memory_strmat)
ptr_memory_strmat = cast(ptr_memory_strmat, c_void_p)
ptr_memory_strmat.value = ptr_memory_strmat.value + sB.memsize
ptr_memory_strmat = cast(ptr_memory_strmat, c_char_p)

#for i in range(N):
#    B[0][i] = i
#    A[0][i] = i

#import pdb; pdb.set_trace()
bw.blasfeo_dgemm_nt(n, n, n, 1.0, byref(sA), 0, 0, byref(sA), 0, 0, 1, byref(sB), 0, 0, byref(sD), 0, 0);

