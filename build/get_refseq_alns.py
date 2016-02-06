#!/usr/bin/env python
# Copyright (C) 2016 Sascha Steinbiss <sascha@steinbiss.name>

# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

from Bio import Entrez
import os

Entrez.email = 'sascha@steinbiss.name'

def get_seqs(qry, targetfile):
	resh = Entrez.esearch(db='nuccore', term=qry, retmax=20000)
	res = Entrez.read(resh)
	resh.close()
	result_ids = ','.join(res['IdList'])
	print(len(res['IdList']))
	entryData = Entrez.efetch(db='nuccore', id=result_ids, rettype='fasta')
	outfile = open(targetfile, 'w+')
	outfile.write(entryData.read())
	outfile.close()

# Find 28s eukaryotic genes
entrez_28s_query = "28s[All Fields] AND srcdb_refseq[PROP] AND ((animals[filter] OR plants[filter] OR fungi[filter] OR protists[filter]) AND biomol_rrna[PROP])"
get_seqs(entrez_28s_query, "28s.euk.fasta")
if not os.path.isfile("28s.euk.aln"):
	os.system("mafft --auto 28s.euk.fasta > 28s.euk.aln")
#os.system("hmmbuild --rna -n 28s_rRNA 28s.euk.hmm 28s.euk.aln")
#os.system("cmbuild -F --noss 28s.euk.cm 28s.euk.aln")

# Find 23s archaeal genes
entrez_23s_arc_query = "23s[All Fields] AND srcdb_refseq[PROP] AND (archaea[filter] AND biomol_rrna[PROP])"
get_seqs(entrez_23s_arc_query, "23s.arc.fasta")
if not os.path.isfile("23s.arc.aln"):
	os.system("mafft --auto 23s.arc.fasta > 23s.arc.aln")
#os.system("hmmbuild --rna -n 23s_rRNA 23s.arc.hmm 23s.arc.aln")
#os.system("cmbuild -F --noss 23s.arc.cm 23s.arc.aln")

# Find 23s bacterial genes
entrez_23s_bac_query = "23s[All Fields] AND srcdb_refseq[PROP] AND (bacteria[filter] AND biomol_rrna[PROP])"
get_seqs(entrez_23s_bac_query, "23s.bac.fasta")
if not os.path.isfile("23s.bac.aln"):
	os.system("mafft --auto 23s.bac.fasta > 23s.bac.aln")
#os.system("hmmbuild --rna -n 23s_rRNA 23s.bac.hmm 23s.bac.aln")
#os.system("cmbuild -F --noss 23s.bac.cm 23s.bac.aln")
