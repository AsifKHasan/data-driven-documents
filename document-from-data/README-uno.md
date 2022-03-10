"C:\Program Files\LibreOffice\program\soffice.exe" --headless --convert-to pdf --outdir "../out/salary-enhancement/tmp" "../out/salary-enhancement/tmp/celloscope__salary-enhancement__2022__001__kamruzzaman-tanim.odt"

"C:\Program Files\LibreOffice\program\soffice.exe" --nologo --headless --nofirststartwizard --accept='socket,host=127.0.0.1,port=2220,tcpNoDelay=1;urp'
"C:\Program Files\LibreOffice\program\unoconv.exe" --connection 'socket,host=127.0.0.1,port=2220,tcpNoDelay=1;urp;StarOffice.ComponentContext' -f pdf ../out/salary-enhancement/tmp/celloscope__salary-enhancement__2022__001__kamruzzaman-tanim.odt


# Unoserver

## Usage
unoserver [-h] [--interface INTERFACE] [--port PORT] [--daemon] [--executable EXECUTABLE]

  --interface: The interface used by the server, defaults to "localhost"
  --port: The port used by the server, defaults to "2002"
  --daemon: Deamonize the server
  --executable: The path to the LibreOffice executable

unoserver --interface 127.0.0.1 --port 2002 --daemon --executable "C:/Program Files/LibreOffice/program/soffice.exe"


# Unoconvert

## Usage
unoconvert [-h] [--convert-to CONVERT_TO] [--interface INTERFACE] [--port PORT] infile outfile

  infile: The path to the file to be converted (use - for stdin)
  outfile: The path to the converted file (use - for stdout)
  --convert-to: The file type/extension of the output file (ex pdf). Required when using stdout
  --interface: The interface used by the server, defaults to "localhost"
  --port: The port used by the server, defaults to "2002"

unoconvert --convert-to pdf ../out/salary-enhancement/tmp/celloscope__salary-enhancement__2022__001__kamruzzaman-tanim.odt ../out/salary-enhancement/tmp/celloscope__salary-enhancement__2022__001__kamruzzaman-tanim.pdf
