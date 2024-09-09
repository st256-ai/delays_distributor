module uart_data_mapper(
	input wire i_clk,
	input wire [7:0] i_rx_data,
	input wire i_rx_ready,
	output wire [2:0] o_current_byte_num,
	output reg [7:0] o_periods_to_process,
	output reg [2:0] o_phasecounterselect_1,
	output reg [2:0] o_phasecounterselect_2,
	output reg o_pll_to_update,
	output reg o_phaseupdown,
	output reg o_shift_ready
);

localparam [7:0] INIT = 8'b00000000;
localparam [7:0] BASE = 8'b00110000;
localparam [7:0] STOP_SIGNAL = 8'b01010011;

localparam [2:0] INIT_COUNTER = 3'b110;

wire [7:0] mapped_rx_data;
wire [2:0] reduced_rx_data;
reg [2:0] current_byte_num;
reg prev_i_rx_ready;
reg prev_o_shift_ready;

initial begin
	current_byte_num <= 3'b000;
	prev_i_rx_ready <= 1'b0;
	prev_o_shift_ready <= 1'b0;
	
	o_phasecounterselect_1 <= INIT_COUNTER;
	o_phasecounterselect_2 <= INIT_COUNTER;
	
	o_periods_to_process <= INIT;
	o_pll_to_update <= 1'b0;
	o_shift_ready <= 1'b0;
	o_phaseupdown <= 1'b0;
end

assign o_current_byte_num = current_byte_num;
assign mapped_rx_data = i_rx_data - BASE;
assign reduced_rx_data = mapped_rx_data[2:0];

always @(negedge i_clk) begin
	if (o_shift_ready == 1'b1 && prev_o_shift_ready == 1'b0) begin
		o_shift_ready <= 1'b0;
	end

	if (i_rx_ready == 1'b1 && prev_i_rx_ready == 1'b0) begin
		if (current_byte_num == 3'b000) begin
			o_periods_to_process <= INIT;
			
			if (reduced_rx_data < 3'b100) begin
				o_phasecounterselect_1 <= reduced_rx_data + 3'b010;
				o_pll_to_update <= 1'b0;
			end else begin
				o_phasecounterselect_2 <= reduced_rx_data - 3'b010;
				o_pll_to_update <= 1'b1;
			end
		end
		
		if (current_byte_num == 3'b001) begin
			o_phaseupdown <= reduced_rx_data[0];
		end
		
		if (current_byte_num > 3'b001) begin
			if (i_rx_data == STOP_SIGNAL && o_periods_to_process != INIT)
				o_shift_ready <= 1'b1;
			else
				o_periods_to_process <= 8'b00001010 * o_periods_to_process + mapped_rx_data;
		end
		
		if (i_rx_data == STOP_SIGNAL)
			current_byte_num <= 3'b000;
		else
			current_byte_num <= current_byte_num + 3'b001;
	end
	
	prev_i_rx_ready <= i_rx_ready;
	prev_o_shift_ready <= o_shift_ready;
end 

endmodule

//testbench 1ns/1ns
module uart_data_mapper_testbench();

	localparam [7:0] INITIAL_PERIODS_NUM = 8'b00110101;
	localparam [7:0] BASE = 8'b00110000;
	localparam [7:0] STOP_SIGNAL = 8'b01010011;
	localparam [2:0] INITIAL_COUNTER = 3'b110;

	reg i_clk;
	reg [7:0] i_rx_data;
	reg i_rx_ready;
	wire [2:0] o_current_byte_num;
	wire [7:0] o_periods_to_process;
	wire [2:0] o_phasecounterselect_1;
	wire [2:0] o_phasecounterselect_2;
	wire o_phaseupdown;
	wire o_pll_to_update;
	wire o_shift_ready;
	
	reg [7:0] _counter;
	reg [7:0] _gener_num_counter;

	uart_data_mapper uart_data_mapper(
       .i_clk(i_clk),
		 .i_rx_data(i_rx_data),
	    .i_rx_ready(i_rx_ready),
	    .o_current_byte_num(o_current_byte_num),
	    .o_periods_to_process(o_periods_to_process),
	    .o_phasecounterselect_1(o_phasecounterselect_1),
	    .o_phasecounterselect_2(o_phasecounterselect_2),
	    .o_pll_to_update(o_pll_to_update),
		 .o_phaseupdown(o_phaseupdown),
	    .o_shift_ready(o_shift_ready)
	);

	initial begin                                                  
		i_clk <= 1'b0;
		i_rx_data <= BASE;
		i_rx_ready <= 1'b0;
		//i <= 0;

		_counter <= BASE;
		_gener_num_counter <= BASE;
	end

	always
		#20  i_clk = !i_clk;  

	always begin
		//Sending generator's number
		#200;
		_gener_num_counter <= _counter & 7;
		i_rx_data <= BASE + _gener_num_counter;
		i_rx_ready <= 1'b1;
		#40;
		i_rx_ready <= 1'b0;
		
		//Sending flag for shift direction determining
		#200;
		i_rx_data <= BASE;
		i_rx_ready <= 1'b1;
		#40;
		i_rx_ready <= 1'b0;
		
		//Sending number of shifts to be performed
		#320;
		i_rx_data <= _counter;
		_counter <= _counter + 1'b1;
		i_rx_ready <= 1'b1;
		#40;
		i_rx_ready <= 1'b0;
		
		//Sending STOP_SIGNAL
		#320;
		i_rx_data <= STOP_SIGNAL;
		i_rx_ready <= 1'b1;
		#40;
		i_rx_ready <= 1'b0;
	end

endmodule