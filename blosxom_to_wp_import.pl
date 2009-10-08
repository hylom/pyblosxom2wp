#!/usr/bin/perl -w

use XML::Writer;
#use Date::Manip;
use XML::Parser;

use 

my $DIR = $ARGV[0] or
  die( "Usage blosxom_to_wp_import directory\n\n" );

my $author = $ENV{ 'USER' } or
  die( "Couldn't get USER from env" );

-d $DIR or
  die( "Unrecognized directory $DIR\n" );

my @files = `find $DIR -name '*.txt' -perm 644`;

my $writer = get_xml_writer( );

$writer->xmlDecl( "UTF-8" );
$writer->startTag( 'rss', 'version' => '2.0' );
$writer->startTag( 'channel' );

foreach my $file ( @files )
{
  chomp( $file );

  my ( $name, $category ) = get_meta( $file );
  my $pubdate = get_pubdate( $file );
  my ( $title, $description ) = read_story( $file );
  $writer->startTag( 'item' );
  $writer->dataElement( 'category', $category );
  $writer->dataElement( 'name', $name );
  $writer->dataElement( 'title', $title );
  $writer->dataElement( 'pubdate', $pubdate );
  $writer->dataElement( 'description', $description );
  $writer->endTag( 'item' );
}

$writer->endTag( 'channel' );
$writer->endTag( 'rss' );


sub get_meta
{
    my ( $file ) = @_;

    $file =~ s/^\/?$DIR\/?//;

    my @parts = split( /\//, $file );
    
    my $category = shift( @parts );

    $name = join( '_', @parts );

    $name =~ s/\.txt$//;

    return ( $name, $category );
}

sub get_pubdate
{
  my ( $file ) = @_;

  my ( $dev,$ino,$mode,$nlink,$uid,$gid,$rdev,$size,
       $atime,$mtime,$ctime,$blksize,$blocks ) = stat( $file ) or
         die( "Couldn't stat $file: $!" );

  my $date = UnixDate( "epoch $mtime", "%a, %d %b %Y %H:%M:%S PDT" );
  
  return $date;
}

sub get_xml_writer
{
    return new XML::Writer( NAMESPACES => 1 );
}


sub read_story
{
  my ( $file ) = @_;

  open ( STORY, $file ) or
    die( "Couldn't open $file: $!" );

  my $title = <STORY>;

  chomp( $title );

  $title or die( "Couldn't get title from $file" );

  $title or
    die( "Couldn't get title" );

  my $description = "";

  while ( <STORY> )
  {
    $description .= $_;
  }

  $description or die( "Couldn't read story" );

  $description = tidy( $description );
    
  close( STORY );

  return ( $title, $description );
}

sub tidy
{
  my ( $xml ) = @_;

  my $validate_xml = $xml;

  $validate_xml =~ s/\&/\&amp;/g;

  my $parser = new XML::Parser( );

  $parser->parse( "<xml>$validate_xml</xml>" );

  $xml =~ s/(<pre>.*?<\/pre>)/escape($1)/gise;
  $xml =~ s/\s+/ /g;
  $xml = unescape( $xml );
  

  return $xml;
}


sub escape
{
    my ( $xml ) = @_;

    die( "Invalid characters in $xml" ) if $xml =~ m/\001/;
    die( "Invalid characters in $xml" ) if $xml =~ m/\002/;
    die( "Invalid characters in $xml" ) if $xml =~ m/\003/;
    die( "Invalid characters in $xml" ) if $xml =~ m/\r/;
    
    $xml =~ s/ /\001/g;
    $xml =~ s/\t/\002/g;
    $xml =~ s/\n/\003/g;

    return $xml;
}


sub unescape
{
    my ( $xml ) = @_;

    $xml =~ s/\001/ /g;
    $xml =~ s/\002/\t/g;
    $xml =~ s/\003/\n/g;

    return $xml;
}
