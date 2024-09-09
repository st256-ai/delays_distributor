module UART_RX #
(
	parameter CLOCK_FREQUENCY = 50_000_000,
	parameter BAUD_RATE       = 9600
)
(
	input  clockIN,
	input  nRxResetIN,
	input  rxIN, 
	output wire rxIdleOUT,
	output wire rxReadyOUT,
	output wire [7:0] rxDataOUT
);

localparam HALF_BAUD_CLK_COMPARE_REG_VALUE = (CLOCK_FREQUENCY / BAUD_RATE / 2 - 1);
localparam HALF_BAUD_CLK_COMPARE_REG_SIZE  = $clog2(HALF_BAUD_CLK_COMPARE_REG_VALUE);

reg [HALF_BAUD_CLK_COMPARE_REG_SIZE-1:0] rxClkCounter = 0;
reg rxBaudClk = 1'b0;

reg [8:0] rxReg      = 9'h000;
reg [3:0] rxIndex    = 4'h9;

assign rxIdleOUT = (rxIndex[3] & rxIndex[0]); //4'b1xx1 || 4'h9
assign rxReadyOUT = (rxIdleOUT & rxReg[8]);
assign rxDataOUT[7:0] = rxReg[7:0];

always @(posedge clockIN) begin : rx_clock_generate
	if(rxIN & rxIdleOUT) begin
		rxClkCounter <= 0;
		rxBaudClk    <= 0;
	end
	else if(rxClkCounter == HALF_BAUD_CLK_COMPARE_REG_VALUE) begin
		rxClkCounter <= 0;
		rxBaudClk <= ~rxBaudClk;
	end
	else begin
		rxClkCounter <= rxClkCounter + 1'b1;
	end
end

always @(posedge rxBaudClk or negedge nRxResetIN) begin : rx_receive
	if(~nRxResetIN) begin
		rxReg[8] <= 1'b0;
		rxIndex  <= 4'h9;
	end
	else if(~rxIdleOUT) begin
		rxReg[rxIndex] = rxIN;
		rxIndex = rxIndex + 1'b1;
	end
	else if(~rxIN) begin
		rxIndex <= 4'h0;
	end
end

endmodule