

void vector_addition(float *a, float *b, float *c, float d, unsigned int size){
// AXI Master interfaces for the top function pointer arguments
// A correct depth is necessary to properly cosimulate the design
#pragma HLS INTERFACE m_axi depth=10000 port=a bundle=gmem0
#pragma HLS INTERFACE m_axi depth=10000 port=b bundle=gmem1
#pragma HLS INTERFACE m_axi depth=10000 port=c bundle=gmem2

// AXI Lite interfaces for the top function arguments
#pragma HLS INTERFACE s_axilite port=a
#pragma HLS INTERFACE s_axilite port=b
#pragma HLS INTERFACE s_axilite port=c
#pragma HLS INTERFACE s_axilite port=d
#pragma HLS INTERFACE s_axilite port=size

// AXI Lite interface to control the IP
// In the way, we can monitor the IP status
#pragma HLS INTERFACE s_axilite port=return

// Local copy of the scalar arguments
	unsigned int size_local = size;
	float d_local = d;

	loop1:for(unsigned int i = 0; i < size_local; i++){
#pragma HLS PIPELINE
// Pipelined read from off-chip memory -> burst
		float b_val = b[i];
		float c_val = c[i];
// Vector addition operation
		float a_val = b_val + c_val*d_local;
// Pipelined write to off-chip memory -> burst
		a[i] = a_val;
	}

}

