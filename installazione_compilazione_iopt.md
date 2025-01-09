Di seguito un **esempio** (semplificato) di come potresti eseguire lo **script `./configure`** per compilare Ipopt in maniera tradizionale (senza CMake). Tieni presente che i **parametri esatti** dipendono dalle librerie che vuoi usare (BLAS, LAPACK, MUMPS, HSL, ecc.) e da dove queste librerie sono installate sul tuo sistema.

---

## 1. Scarica i sorgenti e posizionati nella cartella

Supponiamo che tu abbia già scaricato o clonato i sorgenti di Ipopt:

```bash
git clone https://github.com/coin-or/Ipopt.git
cd Ipopt
```

Troverai un file `configure` nella root o in una sottocartella come `Ipopt/`.  
In alcuni casi, potresti dover eseguire `./configure` dalla cartella `Ipopt` o da una sottodirectory `Ipopt/Ipopt`. Verifica le istruzioni nel file `INSTALL.md` di Ipopt.

---

## 2. Esempio di comandi `configure`

Un tipico comando `configure` può essere simile a questo (diviso in più righe per chiarezza):

```bash
./configure \
  --prefix=/usr/local \
  --enable-shared \
  --with-blas-lib="-lblas" \
  --with-lapack-lib="-llapack" \
  --disable-static
```

### Significato delle opzioni principali:

- **`--prefix=/usr/local`**: indica la directory d’installazione (binari finiscono in `/usr/local/bin`, librerie in `/usr/local/lib`, ecc.). Se preferisci non usare i privilegi di root, puoi mettere un percorso in `$HOME`, ad esempio `--prefix=$HOME/.local`.
  
- **`--enable-shared`** / **`--disable-static`**:  abilita la creazione di **librerie condivise** (`.so`) e disabilita quelle statiche. Se vuoi anche le statiche (`.a`), non usare `--disable-static`.

- **`--with-blas-lib="-lblas"`** e **`--with-lapack-lib="-llapack"`**: indica quali librerie linkare per BLAS e LAPACK. Se hai installato `libblas-dev` e `liblapack-dev` in un percorso standard (es. Ubuntu), spesso basta `-lblas` e `-llapack`. Se invece sono installate in percorsi custom, potresti dover specificare qualcosa come:

  ```bash
  --with-blas-lib="/percorso/blas/libblas.a -lgfortran -lm"
  --with-lapack-lib="/percorso/lapack/liblapack.a -lgfortran -lm"
  ```
  
- **Eventualmente**: `--with-mumps` e relativi parametri se vuoi compilare con MUMPS. Ad esempio (molto semplificato):
  ```bash
  ./configure \
    --prefix=/usr/local \
    --enable-shared \
    --with-blas-lib="-lblas" \
    --with-lapack-lib="-llapack" \
    --with-mumps \
    --with-mumps-cflags="-I/usr/include" \
    --with-mumps-lflags="-L/usr/lib -ldmumps -lzmumps -lsmumps -lcmumps -lmumps_common"
  ```
  (Ovviamente i nomi dei pacchetti e i path dipendono dalla tua installazione.)

---

## 3. Compilazione ed installazione

Una volta terminata la configurazione (senza errori), lancia:

```bash
make -j$(nproc)
```
*(dove `-j$(nproc)` utilizza tutti i core del processore).*

Dopo la compilazione, installa (spesso come root, se `prefix` è `/usr/local`):
```bash
sudo make install
```
*(oppure senza `sudo` se installi in `$HOME/.local` o in un path in cui hai i permessi di scrittura).*

---

## 4. Verifica

Assicurati che l’eseguibile `ipopt` risulti accessibile nel tuo `PATH`, ad esempio controlla con:

```bash
ipopt -v
```
Se il comando non viene riconosciuto, aggiungi `/usr/local/bin` (o la cartella di installazione scelta) al tuo `PATH`, ad esempio:

```bash
export PATH="/usr/local/bin:$PATH"
```

---

## 5. Riferimenti utili

- **File INSTALL.md** nella root del repository [Ipopt su GitHub](https://github.com/coin-or/Ipopt).  
- **Documentazione** su librerie opzionali (MUMPS, HSL, Metis, Pardiso, ecc.) sul sito [coin-or.org](https://coin-or.github.io/Ipopt/).  
- **Variabili d’ambiente**: in caso di percorsi non standard per BLAS/LAPACK/MUMPS, puoi passare `CPPFLAGS` e `LDFLAGS` a `configure`. Ad esempio:

  ```bash
  CPPFLAGS="-I/percorso/include" LDFLAGS="-L/percorso/lib" ./configure ...
  ```

---

### In sintesi

1. **Installa** le dipendenze (gfortran, blas/lapack, ecc.).  
2. **Scarica** i sorgenti di Ipopt, entra nella directory con `configure`.  
3. **Esegui** `./configure` con le opzioni desiderate (es. `--prefix=/usr/local`, `--with-blas-lib=-lblas`, `--with-lapack-lib=-llapack`).  
4. **make** e **make install**.  
5. **Verifica** che `ipopt -v` funzioni e che l’eseguibile `ipopt` sia nel `PATH`.

L'errore che stai riscontrando:

```
ipopt: error while loading shared libraries: libipoptamplinterface.so.3: cannot open shared object file: No such file or directory
```

indica che l'eseguibile **Ipopt** non riesce a trovare la libreria condivisa **libipoptamplinterface.so.3** necessaria per il suo funzionamento. Questo problema è solitamente legato al fatto che la libreria non si trova nei percorsi di ricerca delle librerie del sistema. Ecco come puoi risolvere:

## Passaggi per Risolvere l'Errore

### 1. Verifica l'Installazione della Libreria

Prima di tutto, assicurati che la libreria **libipoptamplinterface.so.3** sia effettivamente presente nel tuo sistema.

Apri un terminale e utilizza il comando `find` per cercare la libreria:

```bash
sudo find / -name "libipoptamplinterface.so.3" 2>/dev/null
```

**Nota:** Il comando potrebbe richiedere alcuni minuti per completarsi, a seconda delle dimensioni del tuo filesystem.

Se la libreria viene trovata, annota il percorso in cui si trova. Ad esempio, potrebbe trovarsi in `/usr/local/lib/` o in un'altra directory simile.

### 2. Aggiungi il Percorso della Libreria al Sistema

Una volta individuato il percorso della libreria, devi informare il sistema dove trovarla. Ci sono due metodi principali per farlo:

#### a) Utilizzare `LD_LIBRARY_PATH`

Puoi temporaneamente aggiungere il percorso della libreria alla variabile d'ambiente `LD_LIBRARY_PATH`. Questo metodo è utile per testare rapidamente la configurazione.

Supponiamo che la libreria si trovi in `/usr/local/lib/`.

Esegui il seguente comando nel terminale:

```bash
export LD_LIBRARY_PATH=/usr/local/lib:$LD_LIBRARY_PATH
```

Per rendere questa modifica permanente (cioè, valida anche dopo il riavvio del sistema), aggiungi la linea precedente al tuo file `~/.bashrc` o `~/.bash_profile`:

```bash
echo 'export LD_LIBRARY_PATH=/usr/local/lib:$LD_LIBRARY_PATH' >> ~/.bashrc
```

Poi, ricarica il file di configurazione:

```bash
source ~/.bashrc
```

#### b) Configurare il Linker Dinamico

Un metodo più permanente e pulito consiste nell'aggiungere il percorso della libreria al file di configurazione del linker dinamico.

1. **Crea un file di configurazione per Ipopt:**

   ```bash
   sudo bash -c 'echo "/usr/local/lib" > /etc/ld.so.conf.d/ipopt.conf'
   ```

   **Nota:** Sostituisci `/usr/local/lib` con il percorso corretto dove si trova la libreria **libipoptamplinterface.so.3**.

2. **Aggiorna la cache del linker dinamico:**

   ```bash
   sudo ldconfig
   ```

   Questo comando aggiorna la cache delle librerie condivise e include il nuovo percorso.

### 3. Verifica che il Sistema Riconosca la Libreria

Dopo aver aggiunto il percorso della libreria, verifica che il sistema riesca a trovarla.

Esegui:

```bash
ldconfig -p | grep libipoptamplinterface.so.3
```

Dovresti vedere un output simile a questo:

```
libipoptamplinterface.so.3 (libc6,x86-64) => /usr/local/lib/libipoptamplinterface.so.3
```

Se vedi l'output corretto, significa che la libreria è stata riconosciuta correttamente.

### 4. Esegui nuovamente Ipopt

Ora prova a eseguire nuovamente **Ipopt**:

```bash
ipopt
```

Dovrebbe avviarsi senza l'errore precedente.

## Passaggi Aggiuntivi (se necessario)

### a) Verifica Permessi e Installazione Completa

Assicurati di aver completato correttamente l'installazione di Ipopt. Se hai usato `make install`, potrebbe essere necessario eseguire il comando con privilegi di amministratore:

```bash
sudo make install
```

### b) Recompilazione con Opzioni Corrette

Se il problema persiste, potrebbe essere dovuto a una compilazione incompleta o errata. Potresti dover ricompilare Ipopt assicurandoti che tutte le dipendenze siano correttamente linkate.

1. **Ritorna nella directory di build:**

   ```bash
   cd /percorso/della/cartella/Ipopt/build
   ```

2. **Rilancia `make install`:**

   ```bash
   sudo make install
   ```

### c) Controlla le Dipendenze

Assicurati di avere tutte le dipendenze necessarie installate. Per esempio, se hai configurato Ipopt per usare MUMPS, verifica che le librerie MUMPS siano installate e correttamente linkate.

### d) Aggiornare le Variabili d'Ambiente

Se hai installato Ipopt in una directory non standard, potrebbe essere necessario aggiungere anche altri percorsi alle variabili d'ambiente, come `LIBRARY_PATH` o `CPATH`.

Esempio:

```bash
export LIBRARY_PATH=/usr/local/lib:$LIBRARY_PATH
export CPATH=/usr/local/include:$CPATH
```

Aggiungi queste linee al tuo `~/.bashrc` o `~/.bash_profile` se necessario.

## Riepilogo

1. **Verifica** che la libreria **libipoptamplinterface.so.3** sia installata.
2. **Aggiungi** il percorso della libreria alla variabile d'ambiente `LD_LIBRARY_PATH` o al linker dinamico (`ld.so`).
3. **Aggiorna** la cache del linker con `ldconfig`.
4. **Verifica** che il sistema riconosca la libreria usando `ldconfig -p`.
5. **Esegui** nuovamente Ipopt.

Seguendo questi passaggi, dovresti risolvere l'errore relativo alla libreria mancante e poter utilizzare Ipopt correttamente sul tuo sistema Linux.

Se continui a riscontrare problemi, fornisci ulteriori dettagli sull'installazione e i passaggi eseguiti, in modo che possa offrirti un supporto più mirato.
