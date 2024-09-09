module UART_TX #
(
	parameter CLOCK_FREQUENCY = 50_000_000,
	parameter BAUD_RATE       = 9600
)
(
	input  clockIN,
	input  nTxResetIN,
	input  [7:0] txDataIN,
	input  txLoadIN,
	output wire txIdleOUT,
	output wire txReadyOUT,
	output wire txOUT
);

localparam HALF_BAUD_CLK_COMPARE_REG_VALUE = (CLOCK_FREQUENCY / BAUD_RATE / 2 - 1);
localparam HALF_BAUD_CLK_COMPARE_REG_SIZE  = $clog2(HALF_BAUD_CLK_COMPARE_REG_VALUE);

reg [HALF_BAUD_CLK_COMPARE_REG_SIZE-1:0] txClkCounter = 0;
reg txBaudClk = 1'b0;

reg [7:0] txReg   = 8'h00;
reg [3:0] txIndex = 4'hA;
reg       txPin   = 1'b1;

wire [8:0] txData = {1'b1, txReg[7:0]};

assign txReadyOUT = (txIndex[3] & (txIndex[1] | txIndex[0])); //4'b1xx1 (4'h9) || 4'b1x1x (4'hA)
assign txIdleOUT  = (txIndex[3] & txIndex[1]); //4'b1x1x (4'hA)
assign txOUT      = txPin;

always @(posedge clockIN) begin : tx_clock_generate
	if(txIdleOUT & (~txLoadIN)) begin
		txClkCounter <= HALF_BAUD_CLK_COMPARE_REG_VALUE;
		txBaudClk    <= 1'b0;
	end
	else if(txClkCounter == HALF_BAUD_CLK_COMPARE_REG_VALUE) begin
		txClkCounter <= 0;
		txBaudClk    <= ~txBaudClk;
	end
	else begin
		txClkCounter <= txClkCounter + 1'b1;
	end
end

always @(posedge txBaudClk or negedge nTxResetIN) begin : tx_transmit
	if(~nTxResetIN) begin
		txIndex <= 4'hA;
	end
	else if(~txReadyOUT) begin
		txPin = txData[txIndex];
		txIndex = txIndex + 1'b1;
	end
	else if(txLoadIN) begin
		txReg[7:0] <= txDataIN[7:0];
		txIndex <= 4'h0;
		txPin <= 1'b0;
	end
	else begin
		txIndex <= 4'hA;
	end
end

endmodule