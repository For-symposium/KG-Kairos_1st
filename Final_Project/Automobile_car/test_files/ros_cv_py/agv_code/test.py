import subprocess

def convert_heic_to_jpeg_imagemagick(heic_path, output_path):
    subprocess.run(["convert", heic_path, output_path])

# Example usage
convert_heic_to_jpeg_imagemagick("./IMG_2382.HEIC", "./IMG123.jpg")
