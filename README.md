# Bravar Sports Bar – sitio web

Sitio estático (HTML + CSS + JavaScript, sin instalación ni servidor especial).

## Cómo verlo
- Abre `index.html` con doble clic. Funciona sin internet.
- Para publicarlo, sube **toda la carpeta** a tu hosting (Netlify, Vercel, GitHub Pages,
  cPanel…). `index.html` debe quedar en la raíz.

## Estructura
```
index.html            Página (estructura y textos en español)
css/styles.css        Estilos, colores (variables --o naranja, negro, blanco) y animaciones
js/main.js            Navegación, carruseles, libro del menú, transiciones, descarga de PDF
js/i18n.js            Selector de idioma, banderas y traducciones de la interfaz
js/menu-pages.js      Lista de hojas del menú por idioma
assets/
  img/brand/          Logo
  img/hero/           Hamburguesa recortada del inicio
  img/dishes/         Fotos de "Lo más bravo"
  img/ambiente/       Fotos del ambiente y del área de juegos
  img/stories/        Portadas de historias
  fonts/              Anton y Barlow (el sitio no depende de Google Fonts)
  menu/<idioma>/      Hojas del menú (es, en, fr, de, ja, ko, zh)
  menu/photos/        Fotos de las contraportadas del libro
  pdf/                PDF del menú por idioma (respaldo)
tools/menu-generator/ Para regenerar las hojas traducidas del menú
```

## Cambios frecuentes
- **Instagram / Facebook / teléfono / dirección:** busca el enlace o el texto en `index.html`.
- **Textos de la página en otros idiomas:** `js/i18n.js` (la clave es el texto en español).
- **Cambiar fotos de los platillos:** reemplaza el archivo en `assets/img/dishes/` con el mismo nombre.
- **Precios del menú:** ver `tools/menu-generator/README.md`.

## Nota sobre el PDF del menú
El botón "Descargar menú en PDF" arma el PDF en el navegador con las hojas del idioma
elegido. Si abres `index.html` con doble clic y el navegador lo bloquea, se descarga el
PDF de `assets/pdf/`.
