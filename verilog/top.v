module top(
	input wire i_clk,							 // input plot
	input wire i_uart_rx,					 // input port for UART reciever
	output wire [7:0] o_modulating, 		 // modulating signals for chaotic generators
	output wire o_uart_tx,					 // output port for UART transmitter 
	output wire [2:0] o_current_state_1,
	output wire [2:0] o_current_state_2,
	output wire o_pll_to_update,
	output wire o_phasestep_2
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
wire phasestep_1;          // signal to enable phase shift
wire phasedone_1;          // shows when current shift is finished (if it's value == 0 => current phase shift have been done)
wire locked_1;					// PLL locked output
////////////////////////////////////////////////////////////////////////////////////////////////////

////////////////////////////////////////////2-nd PLL////////////////////////////////////////////////
wire wc4,wc5,wc6,wc7; 	 	// PLL output
reg areset_2;				 	// async reset (not used here) 
wire [2:0] phasecounter_2;	// counters assosiated with PLL outputs
wire phasestep_2;          // signal to enable phase shift
wire phasedone_2;          // shows when current shift is finished (if it's value == 0 => current phase shift have been done)
wire locked_2;					// PLL locked output
////////////////////////////////////////////////////////////////////////////////////////////////////
wire phaseupdown; 			// direction of phase shifting

wire [7:0] periods_to_process;
wire pll_to_update;
wire shift_ready;

initial begin
	areset_1 <= 1'b0;
	areset_2 <= 1'b0;
end

//always @(posedge rxReady or negedge txReady) begin
//	if(~txReady)
//		txLoad <= 1'b0;
//	else if(rxReady) begin
//		txLoad <= 1'b1;
//		txData <= rxData;
//	end
//end

UART uart
(
	.clockIN(i_clk),
	
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
	.phaseupdown(phaseupdown),
	.phasestep(phasestep_1),
	.scanclk(i_clk),
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
	.phaseupdown(phaseupdown),
	.phasestep(phasestep_2),
	.scanclk(i_clk),
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
	.o_periods_to_process(periods_to_process),
	.o_phasecounterselect_1(phasecounter_1),
	.o_phasecounterselect_2(phasecounter_2),
	//.o_current_byte_num(o_current_byte_num),
	.o_pll_to_update(pll_to_update),
	.o_phaseupdown(phaseupdown),
	.o_shift_ready(shift_ready)
);

phase_shift_processor #(0) phase_shift_processor_1 (
	.i_clk(i_clk),
	.i_periods_to_process(periods_to_process),
	.i_phasedone(phasedone_1),
	.i_ready(shift_ready),
	.i_pll_to_update(pll_to_update),
	.o_phasestep(phasestep_1),
	.o_current_state(o_current_state_1)
);

phase_shift_processor #(1) phase_shift_processor_2 (
	.i_clk(i_clk),
	.i_periods_to_process(periods_to_process),
	.i_phasedone(phasedone_2),
	.i_ready(shift_ready),
	.i_pll_to_update(pll_to_update),
	.o_phasestep(phasestep_2),
	.o_current_state(o_current_state_2)
);

assign o_modulating[0] = !wc0;
assign o_modulating[1] = !wc1;
assign o_modulating[2] = !wc2;
assign o_modulating[3] = !wc3;
assign o_modulating[4] = !wc4;
assign o_modulating[5] = !wc5;
assign o_modulating[6] = !wc6;
assign o_modulating[7] = !wc7;

/////////////////////////////////////////////DEBUG section//////////////////////////////////////////////////
assign o_pll_to_update = pll_to_update;

assign o_shift_ready = shift_ready;
assign o_phasestep_2 = phasestep_2;

//assign o_phaseupdown = phaseupdown; 

//assign o_phasedone_1 = phasedone_1;
//assign o_phasedone_2 = phasedone_2;

//assign o_phasecounter_1 = phasecounter_1;
//assign o_phasecounter_2 = phasecounter_2;

//assign o_periods_to_process[0] = periods_to_process[0];
//assign o_periods_to_process[1] = periods_to_process[1];
//assign o_periods_to_process[2] = periods_to_process[2];
//assign o_periods_to_process[3] = periods_to_process[3];
//assign o_periods_to_process[4] = periods_to_process[4];
//assign o_periods_to_process[5] = periods_to_process[5];
//assign o_periods_to_process[6] = periods_to_process[6];
//assign o_periods_to_process[7] = periods_to_process[7];
////////////////////////////////////////////////////////////////////////////////////////////////////////////

endmodule


//testbench 1ns/1ns
module uart_shift_processor_integration_tb();

	localparam [7:0] INITIAL_PERIODS_NUM = 8'b00110101;
	localparam [7:0] BASE = 8'b00110000;
	localparam [7:0] STOP_SIGNAL = 8'b01110011;

	reg clk;
	reg [7:0] i_rx_data;
	reg i_rx_ready;
	wire o_current_byte_num;
	wire [7:0] periods_to_process;
	wire [2:0] phasecounterselect_1;
	wire [2:0] phasecounterselect_2;
	wire pll_to_update;
	wire o_phaseupdown;
	wire shift_ready;
	
	reg [7:0] _counter;
	reg [7:0] _gener_num_counter;
	reg i_phasedone;
	wire o_phasestep;
	
	integer i;
	                        
	uart_data_mapper uart_data_mapper(
       .i_clk(clk),
		 .i_rx_data(i_rx_data),
	    .i_rx_ready(i_rx_ready),
	    .o_current_byte_num(o_current_byte_num),
	    .o_periods_to_process(periods_to_process),
	    .o_phasecounterselect_1(phasecounterselect_1),
	    .o_phasecounterselect_2(phasecounterselect_2),
		 .o_phaseupdown(o_phaseupdown),
	    .o_pll_to_update(pll_to_update),
	    .o_shift_ready(shift_ready)
	);
	
	phase_shift_processor phase_shift_processor (
       .i_clk(clk),
		 .i_periods_to_process(periods_to_process),
		 .i_phasedone(i_phasedone),
		 .i_ready(shift_ready),
		 .i_pll_to_update(pll_to_update),
		 .o_phasestep(o_phasestep)
	);

	initial begin                                                   
		clk <= 1'b0;
		_counter <= BASE;
		_gener_num_counter <= BASE;
		i_phasedone <= 1'b1;
		i_rx_data <= INITIAL_PERIODS_NUM;
		i_rx_ready <= 1'b0;
		i <= 0;
	end

	always 
		#20  clk = !clk;  

	always begin
		//Sending generator's number
		#120;
		i_rx_ready <= 1'b1;
		_gener_num_counter <= _counter & 7;
		i_rx_data <= BASE + _gener_num_counter;
		#40;
		i_rx_ready <= 1'b0;
		
		//Sending flag for shift direction determining
		#120;
		i_rx_data <= BASE;
		i_rx_ready <= 1'b1;
		#40;
		i_rx_ready <= 1'b0;
		
		//Sending number of shifts to be performed
		#320;
		i_rx_ready <= 1'b1;
		i_rx_data <= _counter;
		#40;
		i_rx_ready <= 1'b0;
		
		//Sending STOP_SIGNAL
		#320;
		i_rx_ready <= 1'b1;
		i_rx_data <= STOP_SIGNAL;
		#40;
		i_rx_ready <= 1'b0;
		
		for(i=0; i < periods_to_process; i=i+1) begin
			#140;
			i_phasedone <= 1'b0; #60;
			i_phasedone <= 1'b1;
		end
		
		_counter <= _counter + 1'b1;
		#320;
	end  
 
endmodule