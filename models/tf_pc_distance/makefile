cuda_inc = /usr/local/cuda/include/
cuda_lib = /usr/local/cuda/lib64/
nvcc = /usr/local/cuda/bin/nvcc
tf_inc = /home/yangli95/miniconda3/lib/python3.7/site-packages/tensorflow_core/include
tf_lib = /home/yangli95/miniconda3/lib/python3.7/site-packages/tensorflow_core

all: tf_nndistance_so.so tf_approxmatch_so.so

tf_nndistance.cu.o: tf_nndistance.cu
	$(nvcc) tf_nndistance.cu -o tf_nndistance.cu.o -c -O2 -D_GLIBCXX_USE_CXX11_ABI=1 \
	-std=c++11  -I $(tf_inc) -DGOOGLE_CUDA=1 -x cu -Xcompiler -fPIC

tf_nndistance_so.so: tf_nndistance.cpp tf_nndistance.cu.o
	g++ tf_nndistance.cpp tf_nndistance.cu.o -o tf_nndistance_so.so \
	-I $(cuda_inc) -I $(tf_inc) -I $(tf_inc)/external/nsync/public \
	-L $(cuda_lib) -lcudart -L $(tf_lib) -ltensorflow_framework \
    -shared -D_GLIBCXX_USE_CXX11_ABI=1 -std=c++11 -fPIC -O2

tf_approxmatch.cu.o: tf_approxmatch.cu
	$(nvcc) tf_approxmatch.cu -o tf_approxmatch.cu.o -c -O2 -D_GLIBCXX_USE_CXX11_ABI=1 \
	-std=c++11  -I $(tf_inc) -DGOOGLE_CUDA=1 -x cu -Xcompiler -fPIC

tf_approxmatch_so.so: tf_approxmatch.cpp tf_approxmatch.cu.o
	g++ -shared $(CPPFLAGS) tf_approxmatch.cpp tf_approxmatch.cu.o -o tf_approxmatch_so.so \
	-I $(cuda_inc) -I $(tf_inc) -I $(tf_inc)/external/nsync/public \
	-L $(cuda_lib) -lcudart -L $(tf_lib) -ltensorflow_framework \
    -shared -D_GLIBCXX_USE_CXX11_ABI=1 -std=c++11 -fPIC -O2

clean:
	rm -rf *.o *.so
