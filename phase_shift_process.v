module phase_shift_processor #(parameter PLL_NUM =0) (
	input wire i_clk,
	input wire [7:0] i_periods_to_process,
	input wire i_phasedone,
	input wire i_ready,
	input wire i_pll_to_update,
	output reg o_phasestep
);

localparam [2:0] LISTEN = 3'b000;
localparam [2:0] SHIFT = 3'b001;
localparam [2:0] VALIDATE = 3'b010;
localparam [2:0] RESET = 3'b100;

reg [7:0] _procced_periods;
reg [2:0] _cnt;
reg _th_passed;

reg [2:0] state;
reg [2:0] next_state;

initial begin
	_procced_periods <= 8'b00000000;
	_cnt <= 3'b000;
	_th_passed <= 1'b0;
	
	state <= RESET;
	next_state <= RESET;
end

always @(negedge i_clk)
	state <= next_state;
  
always @(negedge i_clk) begin
	case(state)
		LISTEN: 
			next_state <= i_ready && PLL_NUM == i_pll_to_update ? SHIFT : LISTEN;
		SHIFT:
			next_state <= _th_passed && i_phasedone ? VALIDATE : SHIFT;
		VALIDATE: 
			next_state <= _procced_periods >= i_periods_to_process ? RESET : SHIFT;
		RESET: 
			next_state <= LISTEN;
   endcase
end

always @(*) begin
	case(state)
		LISTEN: begin
			_cnt <= 3'b000;
			_th_passed <= 1'b0;
			o_phasestep <= 1'b0;
		end
		SHIFT: begin
			o_phasestep <= 1'b1;
			if (_cnt == 2)
				_th_passed = 1'b1;
		end
		VALIDATE: begin
			_procced_periods <= _procced_periods + 1'b1;
		
			_cnt <= 3'b000;
			_th_passed <= 1'b0;
			o_phasestep <= 1'b0;
		end
		RESET: begin
			_procced_periods <= 8'b00000000;
		end
   endcase
end

endmodule

//testbench

//testscale 1ns/1ns

module phase_shift_testbench();
	reg i_clk;
	reg [7:0] i_periods_to_process,;
	reg i_phasedone;
	reg i_ready;
	reg i_pll_to_update;
	wire o_phasestep;
	
	initial begin
		

end