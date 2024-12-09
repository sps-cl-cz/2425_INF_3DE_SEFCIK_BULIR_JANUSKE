# 2425_INF_3DE_SEFCIK_BULIR_JANUSKE
K použití skriptu je potřeba mít nainstalovaný interpret Python (kód byl napsán ve verzi Python 3.13.0)

=======>https://www.python.org/downloads/<=======

Dále je možné pro jednodušší manipulaci použít jakýkoliv editor jako je Visual Studio Code
Základní Python interpret a jeho konzole postačí

Je nutné, aby uživatel byl v jakémkoliv prostředí, ať je to VS CODE, cmd nebo Python interpret, a aby dodržel následující:
    1. Prompt musí být vždy ve složce se skriptem.
        Př: C:\ja\zbytek\cesty> Pokud prompt bude zde, tak je nutné, aby ve složce \cesty byl skript
    2. dale pak se ridit samotnym scriptem ktery se spousti:
        cesta k interpretu python, stačí jen zástupce ==> Python check.py command cesta <================== cesta k souboru se kterým se bude něco provádět
                                                                    ||        ||
                                                                    ||        ||
                                                                    ||        ||
                                                                    ||         ========> prikazy init                               
                                                                    ||                           add
                                                                    ||                           remove                                         
                                                                    ||                           status
                                                                    ||                           -h
                                                                    \/
                                                                vždy zadat název skriptu


KNOWN ISSUES

### Function `init`
1. **PermissionError**: Insufficient permissions to access or modify the file.###SOLVED###
2. **FileNotFoundError**: The directory or file may not exist. ###SOLVED###

### Function `sha1_calculation(pathspec)`
- ###SOLVED###

### Function `add`
1. **PermissionError**: Insufficient permissions to access or modify the file. ###SOLVED###
2. **FileNotFoundError**: The directory or file may not exist. ###SOLVED###
3. **Check the return value** from `sha1_calculation(pathspec)`. ###SOLVED###
4. **Logic misstake**: If there is a 2nd new hash to a changed file it would not delete the previus new one ###SOLVED###

### Function `remove`
1. **PermissionError**: Insufficient permissions to access or modify the file.
2. **FileNotFoundError**: The directory or file may not exist.
3. **Logic misstake**: If there is more than 2 NEW HASHES this function woun't remove them

### Function `status`
1. **PermissionError**: Insufficient permissions to access or modify the file.
2. **FileNotFoundError**: The directory or file may not exist.

### Function `main`
1. **ValueError**: Invalid input.

### Errors that apply to the entire code:
1. **ImportError**: Applies to `os`, `hashlib`, `argparse`.
2. **OSError**: General operating system errors.
