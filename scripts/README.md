# Optional menu import

The original menu was imported into PostgreSQL during setup. Normal API startup
does not use these files.

To populate an empty database again, run this command from the project root:

```powershell
python -m scripts.seed
```

`seed_menu.json` is the import source. The script skips nonempty tables and never
overwrites existing records.
