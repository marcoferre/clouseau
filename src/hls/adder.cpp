

void adder(int a, int b, int* c){
// AXI Lite interfaces for the top function arguments
#pragma HLS INTERFACE s_axilite port=a
#pragma HLS INTERFACE s_axilite port=b
#pragma HLS INTERFACE s_axilite port=c

// AXI Lite interface to control the IP
// In the way, we can monitor the IP status
#pragma HLS INTERFACE s_axilite port=return

// Sum operation
// We write to the result variable pointed by c
	*c = a + b;

}

