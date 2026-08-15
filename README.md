# InfoWorks ICM Python Results Integration

This repository contains a small Python wrapper and Ruby helper script to export results from a finished InfoWorks ICM run into pandas.

## Files

- `export_results.rb` — Ruby script executed through `ICMExchange.exe` / `IExchange.exe`.
- `icm_results.py` — Python wrapper to invoke the Ruby script and load the exported `results.csv` into a pandas DataFrame.

## Usage

1. Confirm the installed ICM Exchange executable path.
   - Typical names: `ICMExchange.exe`, `IExchange.exe`

2. Run exported results from Python:

```python
from icm_results import ICMResultsExporter

exporter = ICMResultsExporter(r"C:\Program Files\Autodesk\InfoWorks ICM\ICMExchange.exe")
df = exporter.export_results(
    db_path=r"C:\path\to\network.icm",
    run_id="12345",
    object_ids="all",
    fields="all",
    user="myuser",
    password="mypassword",
)
print(df.head())
```

## Notes

- The Ruby script assumes `ARGV[0] == 'ADSK'` and starts real parameters at `ARGV[1]`.
- `object_ids` and `fields` can be a comma-separated string or an iterable of strings.
- The temporary CSV is deleted automatically after being loaded into pandas.
- If the installed ICM version uses `IExchange.exe` instead, update the `exchange_exe` path accordingly.

## Validation

The Ruby API method names used by `export_results.rb` are best-effort guesses. Confirm them against your installed version of ICM Exchange or sample Autodesk Ruby scripts, and adjust the script if any methods differ.
