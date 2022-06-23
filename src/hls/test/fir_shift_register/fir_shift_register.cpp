// Number of coefficient components
#define N_COEFF 11
// FIR using shift register
extern "C" {
void fir_shift_register(int *output_r, int *signal_r, int *coeff, int signal_length) {
#pragma HLS INTERFACE m_axi port=output_r offset=slave bundle=gmem
#pragma HLS INTERFACE m_axi port=signal_r offset=slave bundle=gmem
#pragma HLS INTERFACE m_axi port=coeff offset=slave bundle=gmem
#pragma HLS INTERFACE s_axilite port=output_r bundle=control
#pragma HLS INTERFACE s_axilite port=signal_r bundle=control
#pragma HLS INTERFACE s_axilite port=coeff bundle=control
#pragma HLS INTERFACE s_axilite port=signal_length bundle=control
#pragma HLS INTERFACE s_axilite port=return bundle=control

  int coeff_reg[N_COEFF];

  // Partitioning of this array is required because the shift register
  // operation will need access to each of the values of the array in
  // the same clock. Without partitioning the operation will need to
  // be performed over multiple cycles because of the limited memory
  // ports available to the array.
  int shift_reg[N_COEFF];
#pragma HLS ARRAY_PARTITION variable = shift_reg complete dim = 0

init_loop:
  for (int i = 0; i < N_COEFF; i++) {
#pragma HLS PIPELINE II = 1
    shift_reg[i] = 0;
    coeff_reg[i] = coeff[i];
  }

outer_loop:
  for (int j = 0; j < signal_length; j++) {
#pragma HLS PIPELINE II = 1
    int acc = 0;
    int x = signal_r[j];

  // This is the shift register operation. The N_COEFF variable is defined
  // at compile time so the compiler knows the number of operations
  // performed by the loop. This loop does not require the unroll
  // attribute because the outer loop will be automatically pipelined so
  // the compiler will unroll this loop in the process.
  shift_loop:
    for (int i = N_COEFF - 1; i >= 0; i--) {
      if (i == 0) {
        acc += x * coeff_reg[0];
        shift_reg[0] = x;
      } else {
        shift_reg[i] = shift_reg[i - 1];
        acc += shift_reg[i] * coeff_reg[i];
      }
    }
    output_r[j] = acc;
  }
}
}