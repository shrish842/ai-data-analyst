import textwrap
import re


def prompt_to_code(prompt: str):
    """
    Convert known prompts into trusted Python code.
    Returns code string or None if prompt is not recognized.
    """
    p = prompt.lower().strip()

    # Dataset summary
    if p.startswith("summarize"):
        return textwrap.dedent("""
            info = []
            info.append(f"Rows: {len(df)}")
            info.append(f"Columns: {len(df.columns)}")
            info.append(f"Numeric columns: {len(df.select_dtypes(include='number').columns)}")
            result = "\\n".join("- " + i for i in info)
        """)

    # Summary statistics
    if "summary statistics" in p or "describe" in p:
        return "result = df.describe().T"

    # Histogram
    if "histogram" in p:
        cols = re.findall(r"'([^']+)'", prompt)
        if cols:
            col = cols[0]
            return textwrap.dedent(f"""
                plt.figure(figsize=(6,4))
                df['{col}'].dropna().hist(bins=30)
                plt.title('Histogram of {col}')
            """)

    # Scatter plot
    if "scatter plot" in p and "vs" in p:
        cols = re.findall(r"'([^']+)'", prompt)
        if len(cols) >= 2:
            return textwrap.dedent(f"""
                plt.figure(figsize=(6,4))
                df.plot.scatter(x='{cols[0]}', y='{cols[1]}')
            """)
    
    if "correlation matrix" in p or "correlation heatmap" in p:
        return textwrap.dedent("""
            corr = df.select_dtypes(include='number').corr()

            plt.figure(figsize=(6, 5))
            plt.imshow(corr, cmap='viridis', aspect='auto')
            plt.colorbar()

            plt.xticks(range(len(corr.columns)), corr.columns, rotation=90)
            plt.yticks(range(len(corr.columns)), corr.columns)

            plt.title("Correlation Matrix Heatmap")
            plt.tight_layout()
        """)

    
    # Anomaly detection
    if "anomal" in p and "z-score" in p:
        return textwrap.dedent("""
            from scipy import stats
            num = df.select_dtypes(include='number').dropna()
            z = abs(stats.zscore(num))
            mask = (z > 3).any(axis=1)
            result = df.loc[num.index[mask]].head(20)
        """)

    return None
