#!/bin/bash
for f in `ls *.xml`; do xmllint --xpath '//sec[@sec-type="methods"]//p/text()' ${f} > ${f}.methods; done
