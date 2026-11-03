# Auditoria de honorarios

Revisa un listado de boletas de honorarios y genera un reporte en Excel con las boletas que hay que revisar.

## Qué valida

- RUT del emisor y del receptor (dígito verificador).
- Que la retención informada corresponda a la tasa vigente.
- Boletas duplicadas (mismo emisor y mismo número).

## Instalación

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

## Ejecución

Desde la carpeta principal:

```powershell
python src/main.py
```

El reporte queda en `output/reporte_auditoria.xlsx`.
