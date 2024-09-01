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

reg [7:0] _processed_periods;
reg [2:0] _cnt;
reg _phase_done;

reg [2:0] state;
reg [2:0] next_state;

initial begin
	_processed_periods <= 8'b00000000;
	_cnt <= 3'b000;
	_phase_done <= 1'b1;
	o_phasestep <= 1'b0;
	
	state <= RESET;
	next_state <= RESET;
end

always @(negedge i_clk)
	state <= next_state;
  
always @(*) begin
	case(state)
		LISTEN: 
			next_state <= i_ready && PLL_NUM == i_pll_to_update ? SHIFT : LISTEN;
		SHIFT:
			next_state <= _cnt >= 3'b001 && !_phase_done ? VALIDATE : SHIFT;
		VALIDATE: 
			next_state <= _processed_periods >= i_periods_to_process ? RESET : SHIFT;
		RESET: 
			next_state <= LISTEN;
   endcase
end

always @(negedge i_clk) begin
	case(state)
		LISTEN: begin
			_cnt = 3'b000;
			o_phasestep = 1'b0;
		end
		SHIFT: begin
			_cnt = _cnt + 1'b1;
			if (_cnt == 1) begin
				o_phasestep = 1'b1;
				_processed_periods = _processed_periods + 1'b1;
			end
			
			if (_cnt > 2) begin
				o_phasestep = 1'b0;
			end
			
			if (!i_phasedone) begin
				_phase_done = 1'b0;
				//if(_cnt >= 1) begin
				//	o_phasestep <= 1'b0;
				//end
			end
		end
		VALIDATE: begin
			_cnt = 3'b000;
			_phase_done = 1'b1;
			o_phasestep = 1'b0;
		end
		RESET: begin
			_processed_periods = 8'b00000000;
		end
   endcase
end

endmodule

//testbench 1ns/1ns
module phase_shift_testbench();

	localparam [7:0] INITIAL_PERIODS_NUM = 8'b00000101;

	reg i_clk;
	reg [7:0] i_periods_to_process;
	reg i_phasedone;
	reg i_ready;
	reg i_pll_to_update;
	wire o_phasestep;
	
	integer i;
	                        
	phase_shift_processor phase_shift_processor (
       .i_clk(i_clk),
		 .i_periods_to_process(i_periods_to_process),
		 .i_phasedone(i_phasedone),
		 .i_ready(i_ready),
		 .i_pll_to_update(i_pll_to_update),
		 .o_phasestep(o_phasestep)
	);

	initial begin                                                   
		i_clk <= 1'b0;
		i_periods_to_process <= INITIAL_PERIODS_NUM;
		i_phasedone <= 1'b1; 
		i_ready <= 1'b0;
 		i_pll_to_update <= 1'b0;                       
	end

	always
		#20  i_clk = !i_clk;

	always begin
		#75; 
		i_ready <= 1'b1;
		#40;
		i_ready <= 1'b0;
		
		if(i_pll_to_update == 1'b0) begin
			for(i=0; i < i_periods_to_process; i=i+1) begin
				#200;
				i_phasedone <= 1'b0; #60;
				i_phasedone <= 1'b1;
			end
		end
		
		//i_pll_to_update <= i_periods_to_process % 2;
		#600;
		i_periods_to_process <= i_periods_to_process + 1;
	end
 
endmodule