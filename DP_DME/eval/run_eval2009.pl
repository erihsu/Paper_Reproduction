#!/usr/bin/perl

$resSuffix = ".res";
#@designs = qw(ispd09f11 ispd09f12 ispd09f21 ispd09f22 ispd09f31 ispd09f32 ispd09fnb1);
@designs = qw(ispd09f12_opt );

$HOMEDIR="../";

@teamDirs = qw( 04/ );

foreach $d ( @designs ) {
  print "==== $d\n";
  foreach $t ( @teamDirs ) {
    $file = $HOMEDIR.$t.$d.$resSuffix;
    # print "$file\n";
    print "-- $t\n";
    system("cp $file ./");
    $cmd = "./eval2009v10.pl -s -b $d $d$resSuffix tuned_45nm_HP.pm";
    system($cmd);
    system("rm *.spice *.wave $d$resSuffix");
  }
}
