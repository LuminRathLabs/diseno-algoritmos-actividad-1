# Actividad 1 · Subsecuencia común más larga

Implementaciones en Python de recursión directa (A), Hirschberg (B) y
programación dinámica tabular (C). Las tres reconstruyen una LCS.

## Ejecución

Con Python 3.13, desde la raíz del proyecto:

~~~powershell
python -m pip install -r requirements.txt
python run.py
~~~

La segunda orden ejecuta las pruebas, vuelve a medir y actualiza los resultados.
Para regenerar solo las gráficas a partir de las mediciones guardadas, ejecuta
`python run.py --report-only`.

## Experimento

Se usan diez parejas de cadenas ACGT de 8 a 1.000 símbolos. Las cadenas y sus
semillas están en `datasets/cases.json`. Se hacen cinco repeticiones por métrica
y combinación factible, con un proceso por repetición. El tiempo se mide con
`process_time_ns` y se divide por el número de llamadas tras acumular al menos
125 ms de CPU. La memoria se mide por separado con `tracemalloc`, en KiB de
asignaciones Python. Los límites de ejecución son de 5 s para A y 180 s
para B y C. Tras el primer `TIMEOUT` de A, sus mediciones restantes se marcan
`SKIPPED_BY_DESIGN`.

Las observaciones y el entorno están en `results/raw/`. Las medianas, el rango
de CPU y los estados están en `results/summary.csv`. Las gráficas se guardan
en `results/figures/`.
