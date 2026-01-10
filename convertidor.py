import os
import argparse
from pathlib import Path
from typing import Optional, Tuple
import tempfile

def setup_environment():
    """Configura el entorno y verifica dependencias"""
    try:
        import vtracer
        import cairosvg
        import svglib
        from svglib.svglib import svg2rlg
        from reportlab.graphics import renderPM
        from PIL import Image
        return True
    except ImportError as e:
        print(f"Error: Falta instalar dependencias. Ejecuta:")
        print("pip install vtracer cairosvg svglib reportlab pillow")
        return False

def png_to_svg_high_quality(
    input_path: str,
    output_path: str,
    mode: str = 'spline',
    colormode: str = 'color',
    hierarchical: str = 'stacked',
    cores: int = 4,
    filter_speckle: int = 4,
    color_precision: int = 6,
    layer_difference: float = 16,
    corner_threshold: float = 60,
    length_threshold: float = 4.0,
    max_iterations: int = 10,
    splice_threshold: float = 45,
    path_precision: int = 3
) -> bool:
    """
    Convierte PNG a SVG con máxima calidad usando vtracer
    
    Args:
        input_path: Ruta del archivo PNG de entrada
        output_path: Ruta del archivo SVG de salida
        mode: 'spline' para curvas suaves, 'polygon' para líneas rectas
        colormode: 'color', 'binary', 'binary-fast', o 'curve'
        hierarchical: 'stacked' o 'cutout'
        cores: Número de núcleos a usar
        filter_speckle: Tamaño mínimo de detalle a conservar
        color_precision: Precisión de color (1-8)
        layer_difference: Diferencia mínima entre capas
        corner_threshold: Umbral para esquinas (grados)
        length_threshold: Longitud mínima de segmento
        max_iterations: Iteraciones para optimización
        splice_threshold: Umbral para unir segmentos
        path_precision: Precisión decimal de las rutas
        
    Returns:
        True si la conversión fue exitosa
    """
    try:
        import vtracer
        
        # Verificar que el archivo existe
        if not os.path.exists(input_path):
            print(f"Error: No se encontró el archivo {input_path}")
            return False
        
        print(f"Convirtiendo PNG a SVG: {input_path}")
        print("Configuración de alta calidad activada...")
        
        # Configuración para máxima calidad
        vtracer.convert_image_to_svg_py(
            input_path,
            output_path,
            mode=mode,
            colormode=colormode,
            hierarchical=hierarchical,
            cores=cores,
            filter_speckle=filter_speckle,
            color_precision=color_precision,
            layer_difference=layer_difference,
            corner_threshold=corner_threshold,
            length_threshold=length_threshold,
            max_iterations=max_iterations,
            splice_threshold=splice_threshold,
            path_precision=path_precision
        )
        
        print(f"✓ SVG guardado en: {output_path}")
        print(f"Tamaño del archivo: {os.path.getsize(output_path)} bytes")
        return True
        
    except Exception as e:
        print(f"Error en PNG a SVG: {str(e)}")
        return False

def svg_to_png_high_quality(
    input_path: str,
    output_path: str,
    dpi: int = 600,
    scale: float = 1.0,
    background_color: str = None,
    width: int = None,
    height: int = None
) -> bool:
    """
    Convierte SVG a PNG con máxima calidad usando múltiples métodos
    
    Args:
        input_path: Ruta del archivo SVG de entrada
        output_path: Ruta del archivo PNG de salida
        dpi: Resolución en puntos por pulgada
        scale: Factor de escala
        background_color: Color de fondo (ej: 'white', '#FFFFFF')
        width: Ancho específico en píxeles
        height: Alto específico en píxeles
        
    Returns:
        True si la conversión fue exitosa
    """
    try:
        # Método 1: Usando cairosvg (mejor para SVG complejos)
        try:
            import cairosvg
            
            print(f"Convirtiendo SVG a PNG usando cairosvg (método 1)...")
            
            # Configurar opciones de exportación
            kwargs = {
                'dpi': dpi,
                'scale': scale,
                'output_width': width,
                'output_height': height,
            }
            
            # Eliminar None values
            kwargs = {k: v for k, v in kwargs.items() if v is not None}
            
            cairosvg.svg2png(
                url=input_path,
                write_to=output_path,
                background_color=background_color,
                **kwargs
            )
            
        except Exception as e1:
            print(f"Método cairosvg falló: {str(e1)}")
            
            # Método 2: Usando svglib + reportlab (alternativa)
            try:
                from svglib.svglib import svg2rlg
                from reportlab.graphics import renderPM
                
                print("Usando svglib + reportlab (método 2)...")
                
                # Convertir SVG a ReportLab Drawing
                drawing = svg2rlg(input_path)
                
                # Escalar si es necesario
                if scale != 1.0:
                    drawing.width = drawing.width * scale
                    drawing.height = drawing.height * scale
                    drawing.scale(scale, scale)
                
                # Configurar DPI
                renderPM.drawToFile(
                    drawing,
                    output_path,
                    fmt='PNG',
                    dpi=dpi
                )
                
            except Exception as e2:
                print(f"Método svglib falló: {str(e2)}")
                
                # Método 3: Usando PIL como último recurso
                try:
                    from PIL import Image
                    import io
                    
                    print("Usando PIL (método 3)...")
                    
                    # Convertir con cairosvg a bytes y luego a PIL
                    png_bytes = cairosvg.svg2png(
                        url=input_path,
                        dpi=dpi,
                        scale=scale
                    )
                    
                    # Abrir con PIL para posible post-procesamiento
                    img = Image.open(io.BytesIO(png_bytes))
                    
                    # Aplicar configuración de tamaño si se especificó
                    if width and height:
                        img = img.resize((width, height), Image.Resampling.LANCZOS)
                    elif width:
                        ratio = width / img.width
                        new_height = int(img.height * ratio)
                        img = img.resize((width, new_height), Image.Resampling.LANCZOS)
                    elif height:
                        ratio = height / img.height
                        new_width = int(img.width * ratio)
                        img = img.resize((new_width, height), Image.Resampling.LANCZOS)
                    
                    # Guardar con máxima compresión sin pérdida
                    img.save(
                        output_path,
                        'PNG',
                        optimize=True,
                        dpi=(dpi, dpi)
                    )
                    
                except Exception as e3:
                    print(f"Todos los métodos fallaron: {str(e3)}")
                    return False
        
        print(f"✓ PNG guardado en: {output_path}")
        print(f"Tamaño del archivo: {os.path.getsize(output_path)} bytes")
        print(f"Resolución: {dpi} DPI")
        return True
        
    except Exception as e:
        print(f"Error en SVG a PNG: {str(e)}")
        return False

def batch_convert(
    input_pattern: str,
    output_dir: str,
    conversion_type: str,
    **kwargs
) -> Tuple[int, int]:
    """
    Convierte múltiples archivos en lote
    
    Args:
        input_pattern: Patrón de archivos (ej: '*.png', '*.svg')
        output_dir: Directorio de salida
        conversion_type: 'png_to_svg' o 'svg_to_png'
        **kwargs: Parámetros adicionales para las funciones de conversión
        
    Returns:
        Tupla (éxitos, fallos)
    """
    from glob import glob
    
    # Crear directorio de salida si no existe
    os.makedirs(output_dir, exist_ok=True)
    
    # Encontrar archivos
    files = glob(input_pattern)
    
    if not files:
        print(f"No se encontraron archivos con el patrón: {input_pattern}")
        return 0, 0
    
    print(f"Encontrados {len(files)} archivos para convertir...")
    
    successes = 0
    failures = 0
    
    for input_file in files:
        # Generar nombre de archivo de salida
        input_path = Path(input_file)
        
        if conversion_type == 'png_to_svg':
            output_file = input_path.with_suffix('.svg').name
            output_path = os.path.join(output_dir, output_file)
            
            if png_to_svg_high_quality(str(input_path), output_path, **kwargs):
                successes += 1
            else:
                failures += 1
                
        elif conversion_type == 'svg_to_png':
            output_file = input_path.with_suffix('.png').name
            output_path = os.path.join(output_dir, output_file)
            
            if svg_to_png_high_quality(str(input_path), output_path, **kwargs):
                successes += 1
            else:
                failures += 1
    
    return successes, failures

def main():
    """Función principal para uso desde línea de comandos"""
    
    # Verificar dependencias
    if not setup_environment():
        return
    
    parser = argparse.ArgumentParser(
        description='Convertidor de imágenes PNG ↔ SVG de alta calidad'
    )
    
    subparsers = parser.add_subparsers(dest='command', help='Comandos disponibles')
    
    # Parser para PNG a SVG
    png2svg = subparsers.add_parser('png2svg', help='Convertir PNG a SVG')
    png2svg.add_argument('input', help='Archivo PNG de entrada o patrón (ej: *.png)')
    png2svg.add_argument('-o', '--output', help='Archivo SVG de salida o directorio')
    png2svg.add_argument('--mode', choices=['spline', 'polygon'], default='spline',
                        help='Modo de vectorización')
    png2svg.add_argument('--colormode', 
                        choices=['color', 'binary', 'binary-fast', 'curve'],
                        default='color', help='Modo de color')
    png2svg.add_argument('--dpi', type=int, default=600,
                        help='DPI para procesamiento (sugerido: 300-1200)')
    
    # Parser para SVG a PNG
    svg2png = subparsers.add_parser('svg2png', help='Convertir SVG a PNG')
    svg2png.add_argument('input', help='Archivo SVG de entrada o patrón (ej: *.svg)')
    svg2png.add_argument('-o', '--output', help='Archivo PNG de salida o directorio')
    svg2png.add_argument('--dpi', type=int, default=600,
                        help='Resolución en DPI (sugerido: 300-1200)')
    svg2png.add_argument('--scale', type=float, default=1.0,
                        help='Factor de escala')
    svg2png.add_argument('--width', type=int, help='Ancho específico en píxeles')
    svg2png.add_argument('--height', type=int, help='Alto específico en píxeles')
    svg2png.add_argument('--background', help='Color de fondo (ej: white, #FFFFFF)')
    
    # Parser para conversión por lotes
    batch = subparsers.add_parser('batch', help='Conversión por lotes')
    batch.add_argument('pattern', help='Patrón de archivos (ej: *.png, *.svg)')
    batch.add_argument('output_dir', help='Directorio de salida')
    batch.add_argument('--type', choices=['png2svg', 'svg2png'], required=True,
                      help='Tipo de conversión')
    batch.add_argument('--dpi', type=int, default=600,
                      help='Resolución para conversiones')
    
    args = parser.parse_args()
    
    if not args.command:
        parser.print_help()
        return
    
    if args.command == 'png2svg':
        # Verificar si es un patrón o archivo único
        if '*' in args.input:
            # Conversión por lotes
            output_dir = args.output if args.output else 'svg_output'
            successes, failures = batch_convert(
                args.input,
                output_dir,
                'png_to_svg',
                mode=args.mode,
                colormode=args.colormode
            )
            print(f"\nConversión completa: {successes} éxitos, {failures} fallos")
        else:
            # Archivo único
            if args.output:
                output_path = args.output
            else:
                input_path = Path(args.input)
                output_path = input_path.with_suffix('.svg')
            
            success = png_to_svg_high_quality(
                args.input,
                output_path,
                mode=args.mode,
                colormode=args.colormode
            )
            
            if not success:
                print("La conversión falló")
    
    elif args.command == 'svg2png':
        if '*' in args.input:
            # Conversión por lotes
            output_dir = args.output if args.output else 'png_output'
            successes, failures = batch_convert(
                args.input,
                output_dir,
                'svg_to_png',
                dpi=args.dpi,
                scale=args.scale,
                width=args.width,
                height=args.height,
                background_color=args.background
            )
            print(f"\nConversión completa: {successes} éxitos, {failures} fallos")
        else:
            # Archivo único
            if args.output:
                output_path = args.output
            else:
                input_path = Path(args.input)
                output_path = input_path.with_suffix('.png')
            
            success = svg_to_png_high_quality(
                args.input,
                output_path,
                dpi=args.dpi,
                scale=args.scale,
                width=args.width,
                height=args.height,
                background_color=args.background
            )
            
            if not success:
                print("La conversión falló")
    
    elif args.command == 'batch':
        successes, failures = batch_convert(
            args.pattern,
            args.output_dir,
            'png_to_svg' if args.type == 'png2svg' else 'svg_to_png',
            dpi=args.dpi
        )
        print(f"\nConversión por lotes completa: {successes} éxitos, {failures} fallos")

def convertir_png_a_svg_simple(ruta_png: str, ruta_svg: str = None) -> bool:
    """Función simple para convertir PNG a SVG"""
    if not ruta_svg:
        ruta_svg = Path(ruta_png).with_suffix('.svg')
    
    return png_to_svg_high_quality(
        ruta_png,
        ruta_svg,
        mode='spline',
        colormode='color',
        color_precision=8,
        max_iterations=20
    )

def convertir_svg_a_png_simple(ruta_svg: str, ruta_png: str = None, dpi: int = 600) -> bool:
    """Función simple para convertir SVG a PNG"""
    if not ruta_png:
        ruta_png = Path(ruta_svg).with_suffix('.png')
    
    return svg_to_png_high_quality(
        ruta_svg,
        ruta_png,
        dpi=dpi,
        scale=1.0
    )

if __name__ == "__main__":
    # Si se ejecuta directamente, usar línea de comandos
    main()