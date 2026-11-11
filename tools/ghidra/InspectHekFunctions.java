// Create/decompile stripped candidate functions reached from HEK-adjacent callbacks.
// @category BlockBlast

import ghidra.app.decompiler.DecompInterface;
import ghidra.app.decompiler.DecompileResults;
import ghidra.app.script.GhidraScript;
import ghidra.program.model.address.Address;
import ghidra.program.model.listing.Function;
import ghidra.program.model.listing.Data;

public class InspectHekFunctions extends GhidraScript {
    private static final String[] FUNCTIONS = {
        "100468cc4", "1012d8cb4", "1012d942c", "1012d9698",
        "1033c88c0", "1033a9800", "1032e3e00", "103278be0"
    };
    private static final String[] DATA = {
        "103888c0b", "1040ca940", "10421a8e0"
    };

    @Override
    protected void run() throws Exception {
        DecompInterface decompiler = new DecompInterface();
        decompiler.openProgram(currentProgram);
        for (String text : DATA) {
            Address address = toAddr(text);
            Data data = getDataAt(address);
            println("DATA " + address + " = " + (data == null ? "<undefined>" : data.toString()));
        }
        for (String text : FUNCTIONS) {
            Address address = toAddr(text);
            Function function = getFunctionAt(address);
            if (function == null) {
                disassemble(address);
                function = createFunction(address, null);
            }
            println("\n=== " + address + " " + (function == null ? "<no function>" : function.getName(true)) + " ===");
            if (function == null) continue;
            DecompileResults result = decompiler.decompileFunction(function, 300, monitor);
            if (result.decompileCompleted()) println(result.getDecompiledFunction().getC());
            else println("FAILED: " + result.getErrorMessage());
        }
        decompiler.dispose();
    }
}