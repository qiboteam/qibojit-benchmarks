def to_markdown(data, columns=None, indexcol=None):
    """Prints DataFrame to markdown table format."""
    if columns is None:
        columns = data.columns

    if indexcol is None:
        entrystr = ""
    else:
        entrystr = "{} | ".format(indexcol)
    entrystr += " | ".join(columns)
    print(entrystr)

    if indexcol is None:
        entrystr = ""
    else:
        entrystr = " -- | "
    entrystr += " | ".join("--" for k in columns)
    print(entrystr)

    for idx, entry in data.iterrows():
        if indexcol is not None:
            entrystr = "{} | ".format(idx)
        else:
            entrystr = ""
        entrystr += " | ".join(str(entry[k]) for k in columns)
        print(entrystr)

