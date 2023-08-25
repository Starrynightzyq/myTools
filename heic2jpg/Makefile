all: pack_heic2jpg_gui_2

pack_heic2jpg_gui:
	python3 -m PyInstaller --collect-all pyheif -D -w --icon="./icon.ico" heic2jpg_gui.py

pack_heic2jpg_gui_2:
	python3 -m PyInstaller --collect-all pillow_heif --collect-all PIL -D -w --icon="./icon.ico" heic2jpg_gui_2.py

clean:
	-rm -rf build *.spec

distclean: clean
	-rm -rf dist
