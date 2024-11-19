SynthDef.new(\vibrato,
{|vib, vibdepth|
var osc;
osc = In.kr(0, 1);
osc = Vibrato.ar(osc, vib, depth: vibdepth);
Out.kr(0, osc)}).add;
