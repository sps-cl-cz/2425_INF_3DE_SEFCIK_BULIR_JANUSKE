# File Tracker Script 🚀  
**File Tracker Script** je jednoduchý nástroj pro sledování změn souborů pomocí SHA-1 hashů. Tento program umožňuje inicializovat sledování, přidávat nové soubory, odstraňovat sledované soubory a kontrolovat aktuální stav sledovaných souborů.  

## 🚀 Funkce  
- **`init`**: Inicializuje sledování vytvořením souboru `hash.check`.  
- **`add`**: Přidává (nebo aktualizuje) soubory ke sledování.  
- **`remove`**: Odstraňuje soubory ze sledování.  
- **`status`**: Zobrazuje aktuální stav sledovaných souborů.  

---

## 🛠️ Použití  
Program se spouští přes příkazovou řádku. Níže naleznete dostupné příkazy a jejich popis.  

### Inicializace  
Vytvoří nový soubor `hash.check` pro sledování souborů. Pokud již soubor existuje, můžete jej přepsat.  
```bash
python tracker.py init
```  

### Přidání souboru  
Přidá nový soubor k sledování nebo aktualizuje jeho hash, pokud se změnil obsah.  
```bash
python tracker.py add <cesta_k_souboru>
```  
Příklad:  
```bash
python tracker.py add test.txt
```  

### Odstranění souboru  
Odstraní soubor ze seznamu sledovaných souborů.  
```bash
python tracker.py remove <cesta_k_souboru>
```  
Příklad:  
```bash
python tracker.py remove test.txt
```  

### Stav sledování  
Zobrazí aktuální stav sledovaných souborů, včetně počtu:  
- `[OK]`: Soubory bez změn.  
- `[CHANGED]`: Soubory, u kterých se změnil hash.  
- `[ERROR]`: Soubory, které nelze najít.  
```bash
python tracker.py status
```  

---

## 📂 Struktura projektu  
```
📂 Projekt
 ┣ 📜 tracker.py         # Hlavní soubor se skriptem
 ┣ 📜 hash.check         # Vytvořený soubor pro sledování (po spuštění init)
 ┗ 📜 README.md          # Tento popis projektu
```

---

## 🧰 Požadavky  
- **Python 3.6+**  
- Moduly: `argparse`, `hashlib`, `os`

---

## 📝 Příklad použití  
1. Inicializujte sledování:  
   ```bash
   python tracker.py init
   ```
2. Přidejte soubor ke sledování:  
   ```bash
   python tracker.py add example.txt
   ```
3. Zkontrolujte stav:  
   ```bash
   python tracker.py status
   ```
4. Odeberte soubor:  
   ```bash
   python tracker.py remove example.txt
   ```

---

## 📜 Licence  
Tento projekt je licencován pod licencí MIT.  

---

## 🧑‍💻 Autor  
Šefčík
Bulíř
Januške
