import subprocess

from hypothesis import given
from hypothesis.strategies import text


with open("run.pl", "w") as outfile:
    outfile.write("""
my $file = "in.txt";
my $input = do {
    local $/ = undef;
    open my $fh, "<", $file
        or die "could not open $file: $!";
    <$fh>;
};

$x = uc $input;
$x = reverse $x;

$y = reverse $input;
$y = uc $y;

print $x == $y;
""")


@given(text())
def test_uppercase_and_reverse_are_commutable_in_perl(s):
    with open("in.txt", "w") as outfile:
        outfile.write(s)
    assert subprocess.check_output(["perl", "s.pl"]).strip() == b"1"
