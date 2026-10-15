// Ghidra headless post-script: export function list + basic stats.
// @category OoT3D
import ghidra.app.script.GhidraScript;
import ghidra.program.model.listing.*;
import ghidra.program.model.address.*;
import java.io.*;

public class ExportFuncs extends GhidraScript {
    @Override
    public void run() throws Exception {
        String out = getScriptArgs().length > 0 ? getScriptArgs()[0] : "functions_ghidra.tsv";
        PrintWriter w = new PrintWriter(new FileWriter(out));
        FunctionIterator it = currentProgram.getFunctionManager().getFunctions(true);
        int n = 0, thumb = 0;
        ghidra.program.model.lang.Register tmode = currentProgram.getRegister("TMode");
        while (it.hasNext()) {
            Function f = it.next();
            boolean t = false;
            if (tmode != null) {
                java.math.BigInteger v = currentProgram.getProgramContext().getValue(tmode, f.getEntryPoint(), false);
                t = v != null && v.intValue() == 1;
            }
            if (t) thumb++;
            w.printf("0x%08x\t%d\t%s\t%s%n", f.getEntryPoint().getOffset(), f.getBody().getNumAddresses(), t ? "thumb" : "arm", f.getName());
            n++;
        }
        w.close();
        println("EXPORTED functions=" + n + " thumb=" + thumb);
    }
}
