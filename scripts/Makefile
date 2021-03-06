all: requirements samples filter metrics patterns rs build_halsted hl merge

# Fetch thousands of Java samples in GitHub and store them
# all in target/01 directory. We don't filter anything at
# this stage. Just clone visible GitHub repos.

requirements:
	pip3 install -r ../requirements.txt

samples:
ifdef nrepos
	python3 ./01-fetch-github.py --nrepos=${nrepos}
else
	python3 ./01-fetch-github.py
endif

# We find all suitable Java classes in target/01 and copy
# them into target/02. The full list of all copies files will
# be stored in target/02-java-files.csv
filter:
ifdef max_classes
	python3 ./02-filter-and-move.py --dir target/01 --max_classes=${max_classes}
else
	python3 ./02-filter-and-move.py --dir target/01
endif

# Here we go through the list of all Java classes in target/02,
# and calculate a few metrics per each of them. The result of
# calculation we store into target/03-metrics.csv

./_tmp/pmd-bin-6.22.0-SNAPSHOT/bin/run.sh:
	mkdir -p _tmp
	wget -c -O ./_tmp/pmd-bin.zip https://github.com/pmd/pmd/releases/download/6.21.0-with-designer/pmd-bin-6.21.0-full.zip
	unzip ./_tmp/pmd-bin.zip -d ./_tmp/
	chmod +x ./_tmp/pmd-bin-6.22.0-SNAPSHOT/bin/run.sh
	touch $@



metrics: ./_tmp/pmd-bin-6.22.0-SNAPSHOT/bin/run.sh
	python3 ./03-calculate-metrics.py

# Here we go through the list of all Java classes in target/02
# and attempt to find patterns there. We produce a summary
# CSV file in target/04-patterns.csv
patterns:
	python3 ./04-find-patterns.py --filename target/02/found-java-files.txt


./_tmp/rsm.jar:
	mkdir -p _tmp
	wget -c -O ./_tmp/readability.zip https://dibt.unimol.it/report/readability/files/readability.zip
	unzip ./_tmp/readability.zip -d ./_tmp/

# Here we go through all Java classes in target/02 and calculate
# readability score per each of them. Then, we save the summary
# into CSV at target/05-rs.csv
rs: ./_tmp/rsm.jar
	python3 ./05-calculate-rs.py --filename target/02/found-java-files.txt

hl:
	python3 ./06-calculate-halstead.py --filename target/02/found-java-files.txt

build_halsted:
	cd ../aibolit/metrics/halsteadvolume && mvn clean package && cp ./target/java-project-1.0-SNAPSHOT.jar ../../../scripts/halstead.jar

merge:
	python3 07-merge.py
	
clean:
	rm -rf target _tmp
