SynthDef.new(\angel,
{|amp=1, sus=1, pan=0, freq=440, fmod=0, rq=0.5|
var osc, env;
freq = [freq, freq+fmod];
amp=(amp * 2);
freq = freq * [1, 1.01];
osc = Ringz.ar(ClipNoise.ar(0.001).dup / 2, freq * 3);
osc = RHPF.ar(osc, freq * 2.5, rq);
env = EnvGen.ar(Env([1, 0.8, 0.5, 0],[0.2 * sus, 0.5 * sus, 0.7 * sus]), doneAction: 14);
osc = Mix(osc) * env * amp;
osc = Pan2.ar(osc, pan);
Out.ar(0, osc)}).add;
