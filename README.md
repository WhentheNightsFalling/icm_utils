# icm_utils

A Python wrapper around [InfoWorks ICM](https://www.autodesk.com/products/infoworks-icm)'s
`ICMExchange.exe` command-line tool, for scripting hydraulic modeling workflows --
listing simulations and extracting time-varying results as `pandas` DataFrames --
without writing Ruby by hand.

> **Status: early / work in progress.** The core mechanics (session management,
> script execution, argument passing) are solid and tested against a real model,
> but there is still active work being done. Not yet published to
> PyPI. Expect breaking changes.

## Why this exists

InfoWorks ICM Exchange only runs scripts written in Ruby, invoked from the
command line, with no return value beyond whatever gets printed to stdout or
written to a file. `icm_exchange` handles the plumbing -- running the
executable, passing arguments reliably, reading results back -- so you can
call plain Python methods and get `pandas` DataFrames instead of writing Ruby
and parsing text output by hand.

## Requirements

- A licensed installation of InfoWorks ICM Ultimate (this has been developed
  and tested against the **Autodesk-licensed build** of `ICMExchange.exe`
  specifically -- see [Notes on the Autodesk build](#notes-on-the-autodesk-build) below)
- Python 3.10+
- `pandas`

## Quick start

```python
from pathlib import Path
from icm_exchange import ICMConfig, ICMSession

config = ICMConfig(
    exchange_path=Path(r"C:\Program Files\Autodesk\InfoWorks ICM Ultimate 2026\ICMExchange.exe"),
)

session = ICMSession(config, database_path=r"C:\models\my_network.icmm")

# List every simulation in the database
sims = session.list_simulations()
for sim in sims:
    print(sim.run_name, sim.sim_name, sim.status)

# Extract time-varying results for one simulation
results = session.extract_simulation_results(sims[0], attributes=[["Node", ["depth"]]])
```

## Features

- List all simulations in a database, with run name, path, and status
- Extract time-varying results as a `pandas.DataFrame`, with optional
  `selection` (specific objects) and `attributes` (specific fields) narrowing
- Batch extraction across multiple result tables (e.g. Node + Link at once)
  as a `dict[str, DataFrame]`
- Works with local `.icmm` files or workgroup-hosted databases
  (`server:port/database`), since database paths are treated as opaque
  strings throughout

## Architecture

Four core pieces, each with one job -- see [`docs/package_reference.md`](docs/package_reference.md)
for the full reasoning behind the split:

- **`ICMConfig`** -- installation-level settings (path to the executable, timeout)
- **`ScriptLibrary`** -- locates the bundled Ruby scripts
- **`ExchangeRunner`** -- runs a script + arguments via subprocess; knows nothing about ICM concepts
- **`ICMSession`** -- the public API; owns a database connection, composes the above

Python and Ruby communicate only through subprocess arguments (in) and stdout
or files on disk (out) -- see [`docs/argument_convention.md`](docs/argument_convention.md)
for the conventions used for passing data reliably in both directions,
including why some arguments are JSON+base64-encoded.

## Notes on the Autodesk build

If you're working with the Autodesk-licensed `ICMExchange.exe` (bundled with
InfoWorks ICM Ultimate), a couple of things aren't obvious from the official
documentation and are worth knowing:

- This executable follows a different command-line calling convention than
  the generic `IExchange` documented for standalone Exchange products -- no
  app-code (`ICM`/`IA`/`WS`) argument slot exists.
- It silently prepends its own internal argument (observed as `"ADSK"`)
  ahead of whatever arguments you pass. Scripts in this package read their
  own arguments from the *end* of `ARGV` (`ARGV.last(n)`) rather than the
  start, specifically to be robust to this.
- Passing double-quote characters through as command-line arguments on
  Windows appears to strip them somewhere in transit -- this is why
  structured arguments (like `selection`/`attributes`) are base64-encoded,
  not passed as raw JSON.

## Known limitations

- No automated tests yet
- Silent failure on non-zero return codes -- a failed Ruby script currently
  returns normally rather than raising
- `timeout_s` in `ICMConfig` is not yet enforced
- Only tested against ICM Ultimate on Windows; InfoAsset / WS Pro Exchange
  are not tested and may need adjustments

## License

Not yet chosen -- to be added. If you're considering using or contributing
to this before a license is set, ask first.

## Contributing

This is currently a personal learning/tooling project and moving fast
