/* * ALETHEIA QUANTUM - FPGA CORE V3
 * Target: Xilinx Kintex-7
 * Logic: Sigma-X Sequencer with Safety Interlock
 */

module fpga_core_v3 (
    input wire clk,              // System Clock
    input wire rst_n,            // Reset
    input wire start_trigger,    // Trigger
    input wire [7:0] pulse_width_ticks,
    output reg safety_scram      // SCRAM Signal
);

    // SAFETY INTERLOCK:
    // InAs-Al braids require > 5ns pulses (Adiabatic Limit).
    // If pulse_width_ticks < 10 (assuming 2GHz clock), trigger SCRAM.
    always @(posedge clk or negedge rst_n) begin
        if (!rst_n) begin
            safety_scram <= 0;
        end else begin
            if (start_trigger && pulse_width_ticks < 10) begin
                safety_scram <= 1; 
            end
        end
    end

endmodule