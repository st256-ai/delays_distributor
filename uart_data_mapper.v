module uart_data_mapper(
	input wire i_clk,
	input wire [7:0] i_rx_data,
	input wire i_rx_ready,
	output wire [2:0] o_current_byte_num,
	output reg [7:0] o_periods_to_process,
	output reg [2:0] o_phasecounterselect_1,
	output reg [2:0] o_phasecounterselect_2,
	output reg o_pll_to_update,
	output reg o_shift_ready
);

localparam [7:0] INIT = 8'b00000000;
localparam [7:0] BASE = 8'b00110000;
localparam [7:0] STOP = 8'b01010011;

localparam [2:0] INIT_COUNTER = 3'b110;

wire [7:0] mapped_rx_data;
wire [2:0] reduced_rx_data;
reg [2:0] current_byte_num;
reg prev_i_rx_ready;

initial begin
	current_byte_num <= 3'b000;
	prev_i_rx_ready <= 1'b0;
	
	o_phasecounterselect_1 <= INIT_COUNTER;
	o_phasecounterselect_2 <= INIT_COUNTER;
end

assign o_current_byte_num = current_byte_num;
assign mapped_rx_data = i_rx_data - BASE;
assign reduced_rx_data = mapped_rx_data[2:0];

always @(posedge i_clk) begin

	if (i_rx_ready == 1'b1 && prev_i_rx_ready == 1'b0) begin
		if (reduced_rx_data < 3'b100)
			o_phasecounterselect_1 <= reduced_rx_data + 3'b010;
		else
			o_phasecounterselect_2 <= reduced_rx_data - 3'b010;
		
		if (current_byte_num > 3'b000) begin
			if (i_rx_data != STOP)
				o_periods_to_process <= 8'b00001010 * o_periods_to_process + mapped_rx_data;
			else
				o_periods_to_process <= INIT;
		end
		
		if (i_rx_data != STOP)
			current_byte_num <= current_byte_num + 3'b001;	
	end
	
	prev_i_rx_ready <= i_rx_ready;
end

endmodule