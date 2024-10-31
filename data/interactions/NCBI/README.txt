Used NCBI Virus Database
Filtered Virus/taxonomy for virus, taxid=10239
Filtered host for Aves(birds), taxid=8782

Downloaded by using downloaded button while on nucleotide page, selected results tables = CSV format, download all records (347, 583), selected columns:
	Accession	Organism_Name	GenBank_RefSeq	Assembly	Submitters 	Organization	Org_location	Isolate	Species		Nuc_Completeness	Host

The cleaned csv files (interactions-assembly.csv, interactions-organism_name.csv, interactions-species.csv) contain only the follwowing columns:
	Pathogen Organism Name - Organism_Name in the orginal data, this column is only in interactions-assembly.csv and interactions-organism_name.csv
	Assembly - the assembly number associated with the pathogen,  this column is only in interactions-assembly.csv
	Pathogen Species - Species in the original data
	Host - scientific name of the avaian host that the pathogen infected
	Total Count - total number of entries in the original data for this pathogen, host pair
	GenBank - number of entries in the orginal data that are from GenBank for this pathogen, host pair
	RefSeq - number of entries in the orginal data that are from RefSeq for this pathogen, host pair
	Completed Count - number of entries in the orginal data with Nuc_Completeness = complete for this pathogen, host pair

Number of interactions found:
	interactions-assembly.csv 92791
	interactions-organism_name.csv 34207
	interactions-species.csv 4744