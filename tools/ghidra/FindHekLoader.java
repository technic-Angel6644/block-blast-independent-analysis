// Locate and decompile the Cocos file-operation delegates relevant to HEK loading.
// @category BlockBlast

import ghidra.app.decompiler.DecompInterface;
import ghidra.app.decompiler.DecompileResults;
import ghidra.app.script.GhidraScript;
import ghidra.program.model.address.Address;
import ghidra.program.model.data.DataType;
import ghidra.program.model.listing.Data;
import ghidra.program.model.listing.DataIterator;
import ghidra.program.model.listing.Function;
import ghidra.program.model.listing.FunctionIterator;
import ghidra.program.model.mem.Memory;
import ghidra.program.model.symbol.Reference;
import ghidra.program.model.symbol.ReferenceIterator;
import ghidra.program.model.symbol.Symbol;
import ghidra.program.model.symbol.SymbolIterator;
import java.nio.charset.StandardCharsets;
import java.util.HashSet;
import java.util.Set;

public class FindHekLoader extends GhidraScript {
    private static final String[] NEEDLES = {
        "jsb_init_file_operation_delegate",
        "applicationDidFinishLaunching",
        "ScriptEngine::runScript",
        "Can't decrypt code",
        "HEK:",
        "AppDelegate29applicationDidFinishLaunchingEvE3$_7",
        "NSt3__110__function6__funcIZN11AppDelegate29applicationDidFinishLaunchingEvE3$_7",
        "NSt3__110__function6__funcIZ32jsb_init_file_operation_delegatevE3$_0",
        "NSt3__110__function6__funcIZ32jsb_init_file_operation_delegatevE3$_1",
        "NSt3__110__function6__funcIZ32jsb_init_file_operation_delegatevE3$_2"
    };

    private boolean interesting(String value) {
        for (String needle : NEEDLES) {
            if (value.contains(needle)) return true;
        }
        return false;
    }

    private void decompile(DecompInterface decompiler, Function function) {
        if (function == null) return;
        println("\n=== FUNCTION " + function.getName(true) + " @ " + function.getEntryPoint() + " ===");
        DecompileResults result = decompiler.decompileFunction(function, 120, monitor);
        if (result.decompileCompleted()) {
            println(result.getDecompiledFunction().getC());
        } else {
            println("DECOMPILE FAILED: " + result.getErrorMessage());
        }
    }

    private void chaseReferences(DecompInterface decompiler, Address target, int depth,
                                 Set<Address> seen) {
        if (depth > 4 || !seen.add(target)) return;
        ReferenceIterator refs = currentProgram.getReferenceManager().getReferencesTo(target);
        while (refs.hasNext() && !monitor.isCancelled()) {
            Reference ref = refs.next();
            Address from = ref.getFromAddress();
            Function function = currentProgram.getFunctionManager().getFunctionContaining(from);
            println("  DEPTH " + depth + " REF " + from + " -> " + target + " [" +
                ref.getReferenceType() + "] in " + (function == null ? "<data>" : function.getName(true)));
            if (function != null) decompile(decompiler, function);
            else chaseReferences(decompiler, from, depth + 1, seen);
        }
    }

    private byte[] littleEndianPointer(Address address) {
        long value = address.getOffset();
        byte[] result = new byte[8];
        for (int i = 0; i < 8; i++) result[i] = (byte)(value >>> (8 * i));
        return result;
    }

    private void findRawPointers(DecompInterface decompiler, Memory memory, Address target) {
        byte[] pattern = littleEndianPointer(target);
        Address cursor = memory.getMinAddress();
        int count = 0;
        while (cursor != null && !monitor.isCancelled()) {
            Address hit = memory.findBytes(cursor, pattern, null, true, monitor);
            if (hit == null) break;
            println("  RAW PTR " + hit + " -> " + target);
            Function function = currentProgram.getFunctionManager().getFunctionContaining(hit);
            decompile(decompiler, function);
            chaseReferences(decompiler, hit, 1, new HashSet<Address>());
            if (++count >= 100) { println("  (pointer matches capped)"); break; }
            try { cursor = hit.add(1); } catch (Exception e) { break; }
        }
    }

    private void inspectRttiObject(DecompInterface decompiler, Memory memory, String hex) throws Exception {
        Address namePointerSlot = toAddr(hex);
        Address objectStart = namePointerSlot.subtract(8);
        println("\nRTTI OBJECT near " + objectStart + " (name slot " + namePointerSlot + ")");
        for (int delta = -32; delta <= 64; delta += 8) {
            Address at = objectStart.add(delta);
            try { println("  QWORD " + at + " = 0x" + Long.toUnsignedString(memory.getLong(at), 16)); }
            catch (Exception ignored) { }
        }
        findRawPointers(decompiler, memory, objectStart);
        findRawPointers(decompiler, memory, namePointerSlot);
    }

    @Override
    protected void run() throws Exception {
        DecompInterface decompiler = new DecompInterface();
        decompiler.openProgram(currentProgram);

        println("=== MATCHING FUNCTIONS BY NAME ===");
        FunctionIterator functions = currentProgram.getFunctionManager().getFunctions(true);
        while (functions.hasNext() && !monitor.isCancelled()) {
            Function function = functions.next();
            if (interesting(function.getName(true))) decompile(decompiler, function);
        }

        println("\n=== MATCHING ALL SYMBOLS BY NAME ===");
        SymbolIterator symbols = currentProgram.getSymbolTable().getAllSymbols(true);
        while (symbols.hasNext() && !monitor.isCancelled()) {
            Symbol symbol = symbols.next();
            if (!interesting(symbol.getName(true))) continue;
            println("SYMBOL " + symbol.getName(true) + " @ " + symbol.getAddress() +
                " type=" + symbol.getSymbolType());
            Function function = currentProgram.getFunctionManager().getFunctionContaining(symbol.getAddress());
            decompile(decompiler, function);
        }

        println("\n=== RAW BYTE MATCHES AND REFERENCE CHAINS ===");
        Memory memory = currentProgram.getMemory();
        inspectRttiObject(decompiler, memory, "103fa3088");
        inspectRttiObject(decompiler, memory, "103fe07d8");
        inspectRttiObject(decompiler, memory, "103fe0858");
        inspectRttiObject(decompiler, memory, "103fe08e8");
        for (String needle : NEEDLES) {
            byte[] pattern = needle.getBytes(StandardCharsets.UTF_8);
            Address cursor = memory.getMinAddress();
            while (cursor != null && !monitor.isCancelled()) {
                Address hit = memory.findBytes(cursor, pattern, null, true, monitor);
                if (hit == null) break;
                println("\nRAW STRING '" + needle + "' @ " + hit);
                chaseReferences(decompiler, hit, 0, new HashSet<Address>());
                findRawPointers(decompiler, memory, hit);
                try { cursor = hit.add(1); } catch (Exception e) { break; }
            }
        }

        println("\n=== MATCHING DEFINED STRINGS AND REFERENCES ===");
        DataIterator dataItems = currentProgram.getListing().getDefinedData(true);
        while (dataItems.hasNext() && !monitor.isCancelled()) {
            Data item = dataItems.next();
            Object value = item.getValue();
            if (value == null) continue;
            String text = value.toString();
            if (!interesting(text)) continue;
            Address address = item.getAddress();
            println("\nSTRING @ " + address + ": " + text);
            chaseReferences(decompiler, address, 0, new HashSet<Address>());
        }
        decompiler.dispose();
    }
}