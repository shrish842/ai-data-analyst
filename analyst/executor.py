import io
import sys
import tempfile
import signal
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

def run_code(df: pd.DataFrame, code: str):
    """
    Execute code string in a restricted local namespace.
    Returns a dict:
      - {"type":"text","output":...}
      - {"type":"dataframe","df": pandas.DataFrame}
      - {"type":"image","path": path_to_png}
    Execution conventions:
      - If code sets a variable `result` to a DataFrame or string, we return it.
      - If code uses matplotlib to plot, we save the current figure to a temp PNG and return image.
      - If code raises, return error text.
    """
    # prepare namespace
    local_ns = {"pd": pd, "np": np, "df": df, "plt": plt}
    # capture prints
    old_stdout = sys.stdout
    stdout_buf = io.StringIO()
    sys.stdout = stdout_buf
    try:
        # run
        exec(code, {}, local_ns)
        # first, if plotting occurred (plt has a current figure), save it
        # If code created result_img_path variable, prefer it
        if "result_img_path" in local_ns and local_ns["result_img_path"]:
            path = local_ns["result_img_path"]
            return {"type": "image", "path": path}
        # check for figure in plt
        figs = plt.get_fignums()
        if figs:
            with tempfile.NamedTemporaryFile(delete=False, suffix=".png") as f:
                plt.savefig(f.name, bbox_inches="tight", dpi=150)
                plt.close("all")
                return {"type": "image", "path": f.name}
        # check for result variable
        if "result" in local_ns:
            res = local_ns["result"]
            if isinstance(res, pd.DataFrame):
                return {"type": "dataframe", "df": res}
            else:
                return {"type": "text", "output": str(res)}
        # otherwise, return captured stdout
        out = stdout_buf.getvalue().strip()
        if out:
            return {"type": "text", "output": out}
        return {"type": "text", "output": "Execution finished. No result produced."}
    except Exception as e:
        return {"type": "text", "output": f"Execution error: {e}"}
    finally:
        sys.stdout = old_stdout