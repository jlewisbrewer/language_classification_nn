class Converter():
    """Class to convert strings into machine readable features vector
    
    Example Usage:
        ########################
        s = 'This is just an example'
        c = Converter(s)
        print(c.orig)
        print(c.result)
        ########################

    Args:
        s (str) : A sentence string

    Attributes:
        orig (list(str)) : a formatted list of sentence string
        result (list(float)) : a features vector

    """
    def __init__(self, s):
        self.no_features = 22
        self.orig = self._format_sentence(s)
        self.result = self._convert_sentence()


    def _format_sentence(self, s):
        """Changes certain characters in a string

        Args:
            s (str) : A sentence string

        Returns:
            list (str) : A list of formatted words in s
        """

        digraph = ['s', 'c', 'z', 't', 'n', 'g']
        replace = ['š', 'č', 'ž', 'þ', 'ŋ', 'ǧ']

        formatted = ''.join(word for word in s if not word.isdigit() 
                and word.isalpha() or word == ' ') 
        formatted = formatted.lower().split()
        for i in range(len(formatted)):
            word = list(formatted[i])
            for j in range(len(word)):
                if word[j] == 'h' or word[j] == 'g':
                    #need to check preceding char
                    if j > 0:
                        if word[j-1] in digraph:
                            index = digraph.index(word[j-1])
                            word[j-1] = replace[index]
                            #remove h, replace prev char
                            word[j] = ''
            formatted[i] = ''.join(char for char in word)

        return formatted

    def _convert_sentence(self):
        """Converts a list of strings into a feature vector

        Returns:
            list (float) : a feature vector
        """

        total = list(0 for _ in range(self.no_features))
        n = len(self.orig)

        for word in self.orig:
            cword = list(self._convert_word(word))
            for i in range(len(cword)):
                total[i] += cword[i]
        for i in range(len(total)):
            total[i] /= n

        return total
               
    def _convert_word(self, word):
        """Converts a string into a feature vector

        Args:
            word (str) : a string

        Returns:
            tuple (float) : a feature vector
        """

        l = len(word)

        last = l-1
        base_vowels = ['a', 'e', 'i', 'o', 'u']
        creak_vowels = ['ǒ', 'ǎ', 'ǔ', 'ě', 'ǐ']
        falling_vowels = ['à', 'ì', 'è', 'ò', 'ù' ]
        accented_vowels = ['ó', 'é', 'í', 'ú', 'á']
        long_vowels = ['ī', 'ā', 'ū', 'ē', 'ō']
        umlauted_vowels = ['ö', 'ü']
        dotless_i = ['ı']
        vowels = base_vowels + creak_vowels + falling_vowels + accented_vowels \
                + long_vowels + umlauted_vowels + dotless_i
        tones = creak_vowels + falling_vowels + accented_vowels + long_vowels
        nasals = ['n', 'ŋ']
        laterals = ['l']
        uvulars = ['q', 'ʾ', 'ʿ']
        thorn = ['þ']
        enye = ['ñ']
        cedillas = ['ş', 'ç', 'ğ']
            
        v_cnt = 0
        cluster = 0
        cluster_cnt = 0
        ends_consonant = 0
        ends_nasal = 0
        ends_vowel = 0
        ends_a_or_o = 0
        ends_e = 0
        ends_k = 0
        ends_ng = 0

        contains_uvulars = 0
        contains_laterals = 0
        contains_thorns = 0
        contains_tones = 0
        contains_umlauts = 0
        contains_dotless_i = 0
        contains_accented_vowels = 0
        contains_long_vowels = 0
        contains_clusters_two = 0
        contains_clusters_three = 0
        contains_enye = 0
        contains_cedillas = 0
        contains_c = 0
    

        cluster_letters = []
        for i in range(l):
            if word[i] in vowels:
                v_cnt += 1
                if i == 1:
                    if len(cluster_letters) > 0:
                        cluster_letters.pop()
                        cluster = 0
                if i > 1:
                    if word[i -2] in vowels:
                        if len(cluster_letters) > 0:
                            cluster_letters.pop()
                            cluster = 0
                if cluster == 2:
                    contains_clusters_two = 1
                    cluster_cnt += 1
                if cluster > 2 :
                    contains_clusters_three = 1
                    cluster_cnt += 1
                cluster = 0
            if word[i] not in vowels:
                cluster += 1
                cluster_letters.append(word[i])
                if i is last and word[i -1] in vowels:
                    cluster_letters.pop()
            if word[i] in tones:
                contains_tones = 1
            if word[last] not in vowels and word[last] not in nasals:
                ends_consonant = 1
                if cluster > 1:
                    cluster_cnt += 1
            if word[last] in vowels:
                ends_vowel = 1
            if word[last] in nasals:
                ends_nasal = 1
            if word[last] == 'a' or word[last] == 'o':
                ends_a_or_o = 1
            if word[last] == 'e':
                ends_e = 1
            if word[last] == 'k':
                ends_k = 1
            if word[last] == 'ŋ':
                ends_ng = 1
            if word[i] in uvulars:
                contains_uvulars = 1
            if word[i] in laterals:
                contains_laterals = 1
            if word[i] in thorn:
                contains_thorns = 1
            if word[i] in umlauted_vowels:
                contains_umlauts = 1
            if word[i] in dotless_i:
                contains_dotless_i = 1
            if word[i] in accented_vowels:
                contains_accented_vowels = 1
            if word[i] in long_vowels:
                contains_long_vowels = 1
            if word[i] in enye:
                contains_enye = 1
            if word[i] in cedillas:
                contains_cedillas = 1
            if word[i] is 'c':
                contains_c = 1

        vc_ratio = v_cnt/l
        no_consonants = l - v_cnt
        if no_consonants == 0:
            clc_ratio = 0
        else:
            clc_ratio = len(cluster_letters)/no_consonants


        return (vc_ratio, clc_ratio, ends_consonant, ends_nasal, ends_vowel, 
        ends_a_or_o, ends_e, ends_k, ends_ng, contains_uvulars, contains_thorns, 
        contains_laterals, contains_tones, contains_umlauts, contains_dotless_i, 
        contains_accented_vowels, contains_long_vowels, contains_clusters_two, 
        contains_clusters_three, contains_enye, contains_cedillas, contains_c)