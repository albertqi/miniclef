SynthDef.new(\saw,
{|amp=1, sus=1, pan=0, freq=440, fmod=0, blur=1|
var osc, env;
sus = sus * blur;
freq = [freq, freq+fmod];
amp=(amp / 8);
osc=Saw.ar(freq);
osc=(osc * amp);
env=EnvGen.ar(Env(times: [0.01, (sus - 0.01), 0.01],levels: [0, 1, 1, 0],curve: 'lin'), doneAction: 14);
osc=(osc * env);
osc = Mix(osc) * 0.5;
osc = Pan2.ar(osc, pan);
Out.ar(0, osc)}).add;
