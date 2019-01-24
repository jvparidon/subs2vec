Deep Semantic Analogies Dataset
--------------------------------------------

This collection contains six newly created semantic datasets.

It contains 5 files:
 * de_re-rated_Schm280.txt
 * de_sem-para_SemRel.txt
 * en_sem-para_BLESS.txt
 * en_sem-para_SemRel.txt
 * de_toefl_subset.txt
 * de_trans_Google_analogies.txt

For a detailed description of the data, please refer to the paper (see reference below).
For questions, please contact
  Maximilian Koeper (koepermn@ims.uni-stuttgart.de),
  Christian Scheible (scheibcn@ims.uni-stuttgart.de), or
  Sabine Schulte im Walde (schulte@ims.uni-stuttgart.de)

File descriptions:
------------------
* de_re-rated_Schm280.txt contains the re-rated version of the Schm280 set (Schmidt et al. 2001). Schm280 consists of 280 translated word pairs from WordSim350. We re-rated these pairs, asking 10 Judges under the same conditions as in WordSim353. We call the resulting dataset WordSim280. Each line contains a word pair and the mean similarity score in [0,10]
	
* en_sem-para_SemRel.txt and de_sem-para_SemRel.txt contain analogy questions based on the word pairs from (Scheible and Schulte im Walde, 2014). Each question is of the form A:B::C:D. The questions cover the relations adj-antonym, noun-hyperonym, noun-synonym, noun-antonym, and verb-antonym. For more details, please refer to the paper. This file consists of several sections (delimited by header lines), each for a different relation. Within a section, each line lists the four related words A, B, C, and D of an analogy "A is to B as C is to D".
	
* en_sem-para_BLESS.txt was constructed the same way as the SemRel datasets, but based on hyperonymy and meronymy relations from the BLESS dataset (Baroni & Lenci. 2011). The format is the same as for the SemRel files.
	
* de_toefl_subset.txt is a subset of the German word choice questions from the University of Darmstadt (Mohammad et al., 2007). We removed all questions that contain phrases in order to obtain a challenge of a difficulty comparable to the English TOEFL data. Each line contains a question of the form "stem correct_answer distractor1 distractor2 distractor3".
	
* de_trans_Google_analogies.txt is the German translation of the Google (Mikolov et al., 2013a) analogy set. We omit the  adjective-adverb relation as this distinction does not exist in German. The format is again the same as for the SemRel files.

Reference:
----------

@inproceedings{KoeperScheibleSchulte2015IWCS,
   title     = {Multilingual Reliability and ``Semantic''  Structure of Continuous Word Spaces},
   author    = {Maximilian K\"oper, Christian Scheible, Sabine {Schulte im Walde}},
   booktitle = {Proceedings of the 11th International Conference on Computational Semantics (IWCS 2015) -- Short Papers},
   address   = {London, UK},
   year      = {2015}
}
