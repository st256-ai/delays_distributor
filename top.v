module top(
	input wire i_clk,							 // input plot
	input wire i_uart_rx,					 // input port for UART reciever
	output wire [7:0] o_modulating, 		 // modulating signals for chaotic generators
	output wire o_uart_tx,					 // output port for UART transmitter 
	output wire [2:0] o_current_byte_num
);


defparam uart.CLOCK_FREQUENCY = 50_000_000;
defparam uart.BAUD_RATE       = 921600;

//////////////////////////////////////////////UART//////////////////////////////////////////////////
reg [7:0] txData;
reg txLoad  = 1'b0;

wire txReset = 1'b1;
wire rxReset = 1'b1;
wire [7:0] rxData;
wire txIdle;
wire txReady;
wire rxIdle;
wire rxReady;
////////////////////////////////////////////1-st PLL////////////////////////////////////////////////
wire wc0,wc1,wc2,wc3;  	 	// PLL output
reg areset_1;					// async reset (not used here) 
wire [2:0] phasecounter_1;	// counters assosiated with PLL outputs
reg phaseupdown_1;			// direction of phase shifting
wire phasestep_1;           // signal to enable phase shift
wire phasedone_1;          // shows when current shift is finished (if it's value == 0 => current pahse shift have been done)
wire locked_1;					// PLL locked output
////////////////////////////////////////////////////////////////////////////////////////////////////

////////////////////////////////////////////2-nd PLL////////////////////////////////////////////////
wire wc4,wc5,wc6,wc7; 	 	// PLL output
reg areset_2;				 	// async reset (not used here) 
wire [2:0] phasecounter_2;	// counters assosiated with PLL outputs
reg phaseupdown_2;         // direction of phase shifting
wire phasestep_2;           // signal to enable phase shift
wire phasedone_2;          // shows when current shift is finished (if it's value == 0 => current pahse shift have been done)
wire locked_2;					// PLL locked output
////////////////////////////////////////////////////////////////////////////////////////////////////
wire [7:0] periods_to_process;
wire pll_to_update;
wire shift_ready;

initial begin
	areset_1 <= 1'b0;
	areset_2 <= 1'b0;
	
	phaseupdown_1 <= 1'b1;
	phaseupdown_2 <= 1'b1;
end

UART uart
(
	.clockIN(clockIN),
	
	.nTxResetIN(txReset),
	.txDataIN(txData),
	.txLoadIN(txLoad),
	.txIdleOUT(txIdle),
	.txReadyOUT(txReady),
	.txOUT(o_uart_tx),
	
	.nRxResetIN(rxReset),
	.rxIN(i_uart_rx), 
	.rxIdleOUT(rxIdle),
	.rxReadyOUT(rxReady),
	.rxDataOUT(rxData)
);

pll_0_3 pll_0_3(
	.inclk0(i_clk),
	.areset(areset_1),
	.phasecounterselect(phasecounter_1),
	.phaseupdown(phaseupdown_1),
	.phasestep(phasestep_1),
	.scanclk(wc0),
	.c0(wc0),
	.c1(wc1),
	.c2(wc2),
	.c3(wc3),
	.phasedone(phasedone_1),
	.locked(locked_1)
);

pll_4_7 pll_4_7(
	.inclk0(i_clk),
	.areset(areset_2),
	.phasecounterselect(phasecounter_2),
	.phaseupdown(phaseupdown_2),
	.phasestep(phasestep_2),
	.scanclk(wc4),
	.c0(wc4),
	.c1(wc5),
	.c2(wc6),
	.c3(wc7),
	.phasedone(phasedone_2),
	.locked(locked_2)
);

uart_data_mapper uart_data_mapper(
	.i_clk(i_clk),
	.i_rx_data(rxData),
	.i_rx_ready(rxReady),
	.o_current_byte_num(),
	.o_periods_to_process(periods_to_process),
	.o_phasecounterselect_1(phasecounter_1),
	.o_phasecounterselect_2(phasecounter_2),
	.o_pll_to_update(pll_to_update),
	.o_shift_ready(shift_ready)
);

phase_shift_processor #(0) phase_shift_processor_1 (
	.i_clk(i_clk),
	.i_periods_to_process(periods_to_process),
	.i_phasedone(phasedone_1),
	.i_ready(shift_ready),
	.i_pll_to_update(phasecounter_1),
	.o_phasestep(phasestep_1)
);

phase_shift_processor #(1) phase_shift_processor_2 (
	.i_clk(i_clk),
	.i_periods_to_process(periods_to_process),
	.i_phasedone(phasedone_2),
	.i_ready(shift_ready),
	.i_pll_to_update(phasecounter_2),
	.o_phasestep(phasestep_2)
);

assign o_modulating[0] = !wc0;
assign o_modulating[1] = !wc1;
assign o_modulating[2] = !wc2;
assign o_modulating[3] = !wc3;
assign o_modulating[4] = !wc4;
assign o_modulating[5] = !wc5;
assign o_modulating[6] = !wc6;
assign o_modulating[7] = !wc7;

endmodule