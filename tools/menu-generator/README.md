# Generador de hojas del menú traducidas

Las hojas del menú en inglés, francés, alemán, japonés, coreano y chino se generan
a partir de los textos de este folder. El español usa las hojas originales
(`assets/menu/es/`), que no se tocan.

- `data.py` → estructura del menú (platillos, precios, iconos) y textos en español.
- `tr1.py` → traducciones: inglés, francés, alemán.
- `tr2.py` → traducciones: japonés, coreano, chino.
- `page.css` → diseño de las hojas.

## Cambiar un precio o un texto
1. Edita el precio en `data.py` (por ejemplo `'$230.00'`) y, si cambia el texto, la
   descripción en cada idioma de `tr1.py` / `tr2.py`.
2. Instala lo necesario (una sola vez):
   `pip install playwright pillow` y luego `playwright install chromium`.
   Para japonés, coreano y chino hace falta la fuente "Noto Sans CJK" en el sistema.
3. Ejecuta `python render.py` (o `python render.py en ja` para solo algunos idiomas).
   Las imágenes nuevas se guardan en `assets/menu/<idioma>/page-N.jpg`.
4. Para el español, reemplaza `assets/menu/es/page-N.jpg` por tus hojas actualizadas.
5. Genera de nuevo los PDF de respaldo en `assets/pdf/` (ver README principal).

`render.py` también avisa si una cifra de la traducción no coincide con la del español.
