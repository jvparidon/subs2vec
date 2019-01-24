import os
import frequencies
import deduplicate

if __name__ == '__main__':
    for filename in sorted(os.listdir()):
        if filename.endswith('.txt'):
            print(filename)
            freq_counter, word_count, _ = frequencies.count_freqs(filename)
            frequencies.write_freqs(filename.replace('.txt', '.freqs'), freq_counter, word_count)

            dedup_filename = filename.replace('.txt', '.dedup.txt')
            deduplicate.dedup_file(filename, dedup_filename)
            freq_counter, word_count, _ = frequencies.count_freqs(dedup_filename)
            frequencies.write_freqs(dedup_filename.replace('.txt', '.freqs'), freq_counter, word_count)
