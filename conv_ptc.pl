#!/usr/bin/env perl

# PubTator Centralから取得したgene2pubtatorcentralなどのtab区切りファイルを入力とし、注釈付を行なったツール名について、
# PubMed IDと注釈対象のID（NCBI Gene IDなど）のペアが重複しないように、処理すると共に、ID単位で行分割するスクリプト。
# さらに、IDに対応する、文献中から抽出された実際の表記文字列を削除して、全てハイフンで置き換える。
#
# 例えば、以下のようなデータが含まれている（た）。
# 17846745        Gene    3630    proinsulin|insulin      GNormPlus|gene2pubmed|generifs_basic
# 17846745        Gene    2641;3630       glucagon and proinsulin GNormPlus
# 以上のデータでは、PubMedID:17846745、Gene ID:3630 が重複している。このため、行単位で独立して処理すると以下のようになる。
# 17846745        Gene    3630    -       GNormPlus
# 17846745        Gene    3630    -       GNormPlus|gene2pubmed|generifs_basic
# 17846745        Gene    2641    -       GNormPlus
# これを以下の一行になるよう処理する。
# 17846745        Gene    3630    -       GNormPlus|gene2pubmed|generifs_basic
# 17846745        Gene    2641    -       GNormPlus

use warnings;
use strict;
use Fatal qw/open/;
use open ':utf8';
use utf8;

my $last_pmid;
my $type;
my %source_data;

while(<>){
  chomp;
  my ($pmid, $_type, $geneids, undef, $sources) = split /\t/;
  $type = $_type;
  if (defined( $last_pmid ) && $pmid != $last_pmid){
    for ( keys %source_data ){
      print join("\t", ($last_pmid, $type, $_, "-", join("|", keys %{ $source_data{$_} }) )), "\n";
    }
    %source_data = ();
  }
  my @_geneids = split /;/, $geneids;
  for my $geneid ( @_geneids ) {
    for my $source ( split /\|/, $sources ){
      $source_data{$geneid}{$source}++;
    }
  }
  $last_pmid = $pmid;
}

for ( keys %source_data ){
  print join("\t", ($last_pmid, $type, $_, "-", join("|", keys %{ $source_data{$_} }) )), "\n";
}

__END__