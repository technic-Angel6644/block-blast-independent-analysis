// Decompile function pointers held by the candidate C++ lambda vtables.
// @category BlockBlast

import ghidra.app.decompiler.DecompInterface;
import ghidra.app.decompiler.DecompileResults;
import ghidra.app.script.GhidraScript;
import ghidra.program.model.address.Address;
import ghidra.program.model.listing.Function;
import ghidra.program.model.mem.Memory;
import java.util.HashSet;
import java.util.Set;

public class InspectHekVtables extends GhidraScript {
    private static final String[] STARTS = {
        "103fa2fe0", "103fe0730", "103fe07c0", "103fe0840"
    };

    @Override
    protected void run() throws Exception {
        Memory memory = currentProgram.getMemory();
        DecompInterface decompiler = new DecompInterface();
        decompiler.openProgram(currentProgram);
        Set<Address> done = new HashSet<Address>();
        for (String startText : STARTS) {
            Address start = toAddr(startText);
            println("\n=== TABLE REGION " + start + " ===");
            for (int offset = 0; offset < 0xb0; offset += 8) {
                Address slot = start.add(offset);
                long raw;
                try { raw = memory.getLong(slot); } catch (Exception e) { continue; }
                Address value = toAddr(raw);
                Function function = currentProgram.getFunctionManager().getFunctionAt(value);
                if (function == null) function = currentProgram.getFunctionManager().getFunctionContaining(value);
                println(slot + " = " + value + (function == null ? "" : "  " + function.getName(true)));
                if (function != null && done.add(function.getEntryPoint())) {
                    DecompileResults result = decompiler.decompileFunction(function, 180, monitor);
                    println("\n--- " + function.getName(true) + " @ " + function.getEntryPoint() + " ---");
                    if (result.decompileCompleted()) println(result.getDecompiledFunction().getC());
                    else println("FAILED: " + result.getErrorMessage());
                }
            }
        }
        decompiler.dispose();
    }
}