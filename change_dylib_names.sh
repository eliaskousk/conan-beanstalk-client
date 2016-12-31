set -e
for LIBRARY in $(find . -name "*.dylib"); do
	echo "Fixing rpath for lib: $LIBRARY"
	install_name_tool -id "$(basename $LIBRARY)" $LIBRARY
done
