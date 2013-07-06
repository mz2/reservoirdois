# coding=utf-8
import nltk         # http://nltk.org/
import collections
import string
import re
import os.path
import glob
import cPickle as pickle

# NB you must have run the nltk.download() before first use, to get a language model for english

from HTMLParser import HTMLParser

class MLStripper(HTMLParser):
	def __init__(self):
		self.reset()
		self.fed = []
	def handle_data(self, d):
		self.fed.append(d)
	def get_data(self):
		return ''.join(self.fed)
def strip_tags(html):
	s = MLStripper()
	s.feed(html)
	return s.get_data()

# 94
text = """<title>Materials and Methods</title><sec><title>Data</title><p>We aimed to identify markets selling locally grown, unprocessed FVs. In New Zealand, membership in Farmers’ Markets NZ Inc indicates that: (1) the market must be a food market; (2) the food production is within a defined local area; and (3) the vendor must be directly involved in the growing/production. We compiled member markets’ addresses and also searched online yellow pages and found 13 additional possible markets. Of these, we verified via telephone interview or online materials that 10 met our inclusion criteria. Thus, we identified a total of 48 qualifying, operating farmers’ markets. We obtained coordinates for their addresses using Google Earth, and imported them into a geographic information system (GIS) for analyses.</p><p>Population and area-level deprivation data (NZDep) were compiled at the "meshblock” (MB) level. NZDep consists of nine variables from the 2006 census (<xref ref-type="bibr" rid="ref-10">Crampton, Salmond & Kirkpatrick, 2004</xref>; <xref ref-type="bibr" rid="ref-30">Salmond, Crampton & Atkinson, 2007</xref>). MBs are the finest unit of aggregation in New Zealand (∼41,000 MBs nationally, mean population in 2006 = 195). Population-weighted centroids for census area units (CAUs, the next smallest unit, mean population in 2006 = 2494) were also compiled. Geographic road data were obtained from the Land Information New Zealand 1:50,000 NZTopo database. National FV intake data were derived from the Ministry of Health 2006/7 Health Survey report (<xref ref-type="bibr" rid="ref-23">Ministry of Health, 2008</xref>). These data were used to generate weights for improving FV consumption.</p></sec><sec><title>Location-allocation analyses</title><p>Location-allocation models have been for decision-making for health service delivery (<xref ref-type="bibr" rid="ref-3">Bailey et al., 2011</xref>) and facility location. To run these analyses, we first compiled input map data layers: (1) population-weighted centroids of MBs with population and NZDep, used to weight demand of the origin of travel; (2) road junctions; (3) population-weighted centroids of CAUs which represented candidate facility sites; (4) road network arcs; and (5) shortest paths. Data were entered in ArcMap.10 (ESRI, Redlands, CA, USA) to create a network database and we used the location-allocation tool of the Network Analyst extension.</p><p>Analysis of this network database generates the shortest path between the demand and candidates using specified weights and connectivity restrictions. We set the maximum travel distance at 12.5 km (about 15 min driving time) and set the objective to maximise attendance. To weight demand points, we used the MB NZDep values and the percentage increase required to attain 100% adequate FV consumption. For example, in the most deprived areas, only 55% of the population consumes the recommended FVs (<xref ref-type="bibr" rid="ref-23">Ministry of Health, 2008</xref>). So, we assigned the most deprived MBs a value of 0.45 and multiplied values by the MB’s population to yield a weight.</p><p>We then calculated the proportion of the total population, Māori population and deprivation groups served by existing 48 farmers’ markets, at varying network distances (varying shapes, based on the road network and plausible walking and driving times). To determine whether optimal locations could improve access, we built scenario models to answer: (i) What if this country had no existing farmers’ markets and a total of 48 markets were optimally distributed to meet the dietary needs of deprived populations?; (ii) What if we altered only the existing 18 markets which have the lowest cumulative weighting for the populations served within the 12.5 km buffer (15 min driving time)?; and (iii) What if there were 10 new markets, in addition to the existing 48? Suitable candidate locations (48 sites optimised in Scenario 1, 18 relocated in Scenario 2 and 10 in Scenario 3) were identified and paths were saved for each scenario.</p></sec><sec><title>Calculating geographic access measures to compare results</title><p>To compare scenarios, we generated measures of population access at varying distances from existing/selected candidate locations, using network buffers. Data on transportation type or distances willing to travel to farmers’ markets in New Zealand do not exist, but US data suggest that 70% of low-income shoppers at farmers’ markets lived within 4 miles (6.5 km), 60% drove and 25% walked to markets (<xref ref-type="bibr" rid="ref-28">Ruelas et al., 2012</xref>). Estimated walking speeds are 4.5–5.5 km/h (kmph) depending on the walker’s age (<xref ref-type="bibr" rid="ref-6">Carey, 2005</xref>) and we used 5 kmph. Speed limits in cities/towns in New Zealand are generally 50 kmph and we used this speed (while recognising congestion, traffic lights and motorway travel may change this). We set buffer distances to approximate the following walking and driving times: (a) 2 km  = 24 min walking; (b) 5 km  = 1 h walking/6 min driving; and (c) 12.5 km  = 15 min driving. Road network buffers were created for each distance from existing/proposed farmers’ markets (<xref ref-type="fig" rid="fig-1">Fig. 1</xref>). Population, ethnicity and deprivation data for MB population-weighted centroids within buffers were calculated for comparison.</p><fig id="fig-1"><object-id pub-id-type="doi">10.7717/peerj.94/fig-1</object-id><label>Figure 1</label><caption><title>Example of buffering technique showing Auckland City (largest city in New Zealand).</title></caption><graphic mimetype="image" mime-subtype="png" xlink:href="https://peerj.com/articles/94/fig-1.png"/></fig></sec>"""

def ie_preprocess(document):
	document = document.lower()
	document = re.sub(r'[^\w\s]','',document)
	sentences = strip_tags(document)
	sentences = nltk.sent_tokenize(document)
	sentences = [nltk.word_tokenize(sent) for sent in sentences]
	sentences = [[w for w in sent if w not in nltk.stem.stopwords.words('english')] for sent in sentences]
	sentences = [nltk.pos_tag(sent) for sent in sentences]
	return sentences




def text_to_counts(document):
	print "NLTK preprocessing..."
	sentences = ie_preprocess(strip_tags(document))

	print "Counting..."
	countlist = []
	ngramlen = 1  #2
	for sent in sentences:
		#print sent
		#print ""
		for position in range(len(sent) + 1 - ngramlen):
			#print sent[position:position+ngramlen]
			#print [x[0] for x in sent[position:position+ngramlen]]
			countlist.append(" ".join([x[0] for x in sent[position:position+ngramlen]]))

	counted = collections.Counter(countlist)
	print "==================="
	print "Most common %i-grams:" % ngramlen
	for item in counted.most_common(20):
		print item
	print counted
	return counted

def analyse_folderfull_of_methods(folder):
	filepaths = glob.glob("%s/*.methods" % folder)
	analyses = {}
	grandwordlist = collections.Counter()
	for fp in filepaths:

		try:
			f = open("%s.pickle" % fp, 'rb')
			analyses[basename] = pickle.load(f)
			f.close()
		except:
			basename = os.path.basename(fp)
			f = open(fp, 'r')
			thetext = f.read()
			f.close()
			analyses[basename] = text_to_counts(thetext)
			pickle.dump(analyses[basename], open("%s.pickle" % fp, 'wb'), -1)
		grandwordlist.update(analyses[basename])

	print "GRAND MOST COMMON:"
	print grandwordlist.most_common(20)
	return (analyses, grandwordlist)

################################################
if __name__=='__main__':
	#analyse_some_text(text)
	analyse_folderfull_of_methods('Resources/peerj')

