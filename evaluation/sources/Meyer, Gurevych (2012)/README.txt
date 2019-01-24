Supplementary Material to our COLING 2012 submission:

	To Exhibit is not to Loiter: A Multilingual, Sense-Disambiguated
	Wiktionary for Measuring Verb Similarity
	Christian M. Meyer and Iryna Gurevych

Available from http://www.ukp.tu-darmstadt.de/data/lexical-resources/wiktionary/


1. Relation Disambiguation
--------------------------

* disambiguation_monoling_enen.xls
* disambiguation_monoling_dede.xls
* disambiguation_crossling_ende.xls
* disambiguation_crossling_deen.xls
    Our four gold standard datasets for evaluating Wiktionary relation disambiguation.
	File format: Spreadsheet to be opened in MS Excel or OpenOffice Calc.

* disambiguation_monoling_enen.txt
* disambiguation_monoling_dede.txt
* disambiguation_crossling_ende.txt
* disambiguation_crossling_deen.txt
    The same datasets as above, but in plain text format.
	File format: <source-sense-ID> TAB <source-sense-definition> TAB 
	    <source-word> TAB <annotation = {0,1}> TAB <target-word> TAB
        <target-sense-definition> TAB <target-sense-ID> TAB 
		<relation-type> TAB <sample-group> LINE_BREAK

* disambiguation_monoling_enen_sampling.txt
* disambiguation_monoling_dede_sampling.txt
* disambiguation_crossling_ende_sampling.txt
* disambiguation_crossling_deen_sampling.txt
    Details on our sampling procedure, i.e., how many relations have been
	taken from which sampling category.
	File format: human readable plain text.
 
* disambiguation_annotation_guidebook.pdf
    The guidebook given to the human raters explaining their annotation task.
	File format: Adobe PDF

 
 2. Verb Similarity Datasets
 ---------------------------
 
* verbsim_dede_YP130.txt 
    Translation of the 130 verb pairs introduced by Yang&Powers (2006) into German.
	File format: <verb1> TAB <verb2> TAB <numerical-score> LINE_BREAK

* verbsim_ende_YP130.txt
    Mixed pairs of our (de:de) dataset and the dataset by Yang&Powers (2006).
	The first verb of each pair is taken from the English dataset, the second one from the German.
	File format: <verb1> TAB <verb2> TAB <numerical-score> LINE_BREAK

* verbsim_deen_YP130.txt
    Mixed pairs of our (de:de) dataset and the dataset by Yang&Powers (2006).
	The first verb of each pair is taken from the English dataset, the second one from the German.
	File format: <verb1> TAB <verb2> TAB <numerical-score> LINE_BREAK

	
3. Our Final Wiktionary-based Resource
--------------------------------------

* coling2012-meyer-resource_word_senses_en.tsv
* coling2012-meyer-resource_word_senses_de.tsv
    Word senses extracted from the English (en) and German (de) Wiktionaries.
	File format: <sense-ID> TAB <lexical-item> TAB <part-of-speech> TAB 
	    <sense-definition> TAB <example-sentences> LINE_BREAK

* coling2012-meyer-resource_semantic_relations_en.tsv
* coling2012-meyer-resource_semantic_relations_de.tsv
    Sense disambiguated semantic relations in English (en) and German (de).
	File format: <source-sense-ID> TAB <source-word> TAB <relation-type> TAB
	    <target-sense-ID> TAB <target-word> LINE_BREAK

* coling2012-meyer-resource_translations_en.tsv
* coling2012-meyer-resource_translations_de.tsv
    Sense disambiguated translations from English to German (en) and vice-versa (de).
	File format: <source-sense-ID> TAB <source-word> TAB <target-language> TAB
	    <target-sense-ID> TAB <target-word> LINE_BREAK

Since this resource is based on data from Wiktionary, it will be made available under the Creative Commons Attribution/Share-Alike License (CC-BY-SA). See http://creativecommons.org/licenses/by-sa/3.0/ and http://www.wiktionary.org/ for details.
